"""Auditable MODFLOW models for 1-D / horizontal 2-D, layered groundwater flow.

All engine inputs use metres and seconds. No numerical head is substituted by the
analytical solution. Streamlit is deliberately absent from this module.
"""

# BEGIN CODE CONTENTS
# Manual edits: jump to these release line numbers (refresh with tools/update_code_map.py).
#   ROOT: line 82
#   ENGINE_NAMES: line 83
#   EXE_NAMES: line 84
#   SECONDS_PER_DAY: line 89
#   SECONDS_PER_YEAR: line 90
#   MAX_CELLS: line 91
#   DEFAULT_HEAD_CLOSE: line 92
#   DEFAULT_FLOW_CLOSE: line 94
#   Scenario: line 98
#   Scenario.validate: line 123
#   Scenario.nrow: line 156
#   Scenario.shape: line 160
#   Scenario.total_cells: line 164
#   Scenario.grid_label: line 168
#   Scenario.dy: line 172
#   Scenario.botm: line 176
#   Scenario.z_centres: line 180
#   Scenario.analytical_available: line 185
#   Scenario.comparison_group: line 191
#   Scenario.active_mask: line 196
#   Scenario.chd_mask: line 205
#   Scenario.k_field: line 210
#   Scenario.top: line 223
#   Scenario.bottom: line 227
#   Scenario.aquifer_label: line 231
#   Scenario.dx: line 235
#   Scenario.x: line 239
#   Scenario.recharge_ms: line 243
#   Scenario.transmissivity: line 247
#   Scenario.discharge_potential: line 251
#   Scenario.analytic: line 260
#   Scenario.starting_heads: line 274
#   Scenario.head_array: line 285
#   Scenario.heads_table: line 292
#   NWT_PRESETS: line 306
#   IMS_PRESETS: line 323
#   Solver: line 346
#   Solver.label: line 354
#   Solver.parameters: line 357
#   usable_executable: line 392
#   find_executable: line 413
#   find_library: line 445
#   build_model: line 457
#   fingerprint: line 541
#   head_metrics: line 545
#   read_native_budget: line 599
#   read_face_flows: line 625
#   NUMBER: line 632
#   parse_diagnostics: line 635
#   run_once: line 728
#   run_repeated: line 777
#   comparison_row: line 792
#   record_mf6: line 810
# END CODE CONTENTS

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from pathlib import Path
import hashlib
import json
import os
import re
import shutil
import stat
import subprocess
import sys
import time

import flopy
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent
ENGINE_NAMES = {"mf2005": "MODFLOW-2005", "mfnwt": "MODFLOW-NWT", "mf6": "MODFLOW 6"}
EXE_NAMES = {
    "mf2005": ["mf2005dbl", "mf2005", "MODFLOW-2005_64"],
    "mfnwt": ["mfnwtdbl", "MODFLOW-NWT_64", "mfnwt"],
    "mf6": ["mf6"],
}
SECONDS_PER_DAY = 86400.0
SECONDS_PER_YEAR = 365.25 * SECONDS_PER_DAY
MAX_CELLS = 255_000
DEFAULT_HEAD_CLOSE = 1e-4
# App starting values in m³/s; closure tests are not equivalent across solvers.
DEFAULT_FLOW_CLOSE = {"mf2005": 1e-4, "mfnwt": 5e-3, "mf6": 1e-4}


@dataclass(frozen=True)
class Scenario:
    n: int = 11
    length: float = 5000.0
    thickness: float = 20.0
    k_ms: float = 1e-4
    recharge_mmy: float = 150.0
    left: float = 18.0
    right: float = 16.0
    width: float = 1.0
    initial: str = "Mean boundary head"
    initial_head: float = 17.0
    confined: bool = True
    aquifer_top: float = 20.0
    complexity: bool = False
    horizontal_2d: bool = False
    nlay: int = 1
    random_k: bool = False
    k_min: float = 1e-5
    k_max: float = 1e-3
    k_seed: int = 42
    k_zones: int = 11
    initial_min: float = 10.0
    initial_max: float = 25.0
    initial_seed: int = 24

    def validate(self):
        vals = [self.length, self.thickness, self.aquifer_top, self.k_ms, self.width,
                self.recharge_mmy, self.left, self.right, self.initial_head,
                self.k_min, self.k_max, self.initial_min, self.initial_max]
        if not all(np.isfinite(vals)):
            raise ValueError("All physical inputs must be finite.")
        if not isinstance(self.n, int) or not 3 <= self.n <= 10001:
            raise ValueError("Use between 3 and 10,001 cells, including the two CHD cells.")
        if min(self.length, self.thickness, self.aquifer_top, self.k_ms, self.width) <= 0:
            raise ValueError("Length, aquifer thickness/top, conductivity and width must be positive.")
        if min(self.left, self.right) <= 0 or self.recharge_mmy < 0:
            raise ValueError("Heads must exceed 0 m (confined roof or unconfined bottom); recharge must be nonnegative.")
        if self.initial not in ["Mean boundary head", "Linear between boundaries", "Specified uniform head", "Random distribution"]:
            raise ValueError("Unknown initial-head option.")
        if self.initial == "Specified uniform head" and self.initial_head <= 0:
            raise ValueError("The initial head must exceed 0 m (confined roof or unconfined bottom).")
        if not isinstance(self.nlay, int) or not 1 <= self.nlay <= 50:
            raise ValueError("Use between 1 and 50 layers.")
        if not self.complexity and (self.horizontal_2d or self.nlay != 1 or self.random_k):
            raise ValueError("Enable Add Complexity before using a 2-D grid, layers or a random K field.")
        if self.total_cells > MAX_CELLS:
            raise ValueError(f"This grid has {self.total_cells:,} cells. Use at most {MAX_CELLS:,} cells per model; reduce the horizontal count or layers.")
        if not 1 <= self.k_zones <= 100:
            raise ValueError("Use 1–100 K zones per horizontal direction.")
        if self.random_k and not 0 < self.k_min <= self.k_max:
            raise ValueError("The K limits must satisfy 0 < minimum ≤ maximum.")
        if self.initial == "Random distribution" and not 0 < self.initial_min <= self.initial_max:
            raise ValueError("Initial-head limits must satisfy 0 < minimum ≤ maximum.")
        for seed in (self.k_seed, self.initial_seed):
            if not isinstance(seed, int) or not 0 <= seed <= 2**32-1:
                raise ValueError("Random seeds must be integers between 0 and 4,294,967,295.")

    @property
    def nrow(self):
        return self.n if self.horizontal_2d else 1

    @property
    def shape(self):
        return (self.nlay, self.nrow, self.n)

    @property
    def total_cells(self):
        return self.nlay * self.nrow * self.n

    @property
    def grid_label(self):
        return f"{self.n} × {self.nrow} × {self.nlay} (x × y × layers)"

    @property
    def dy(self):
        return self.dx if self.horizontal_2d else self.width

    @property
    def botm(self):
        return np.linspace(self.top, self.bottom, self.nlay+1)[1:]

    @property
    def z_centres(self):
        edges = np.linspace(self.top, self.bottom, self.nlay+1)
        return (edges[:-1]+edges[1:])/2

    @property
    def analytical_available(self):
        # A multi-layer recharge model can have vertical gradients. Do not use
        # the vertically integrated benchmark as an exact layer-head reference.
        return self.nlay == 1 and not self.random_k

    @property
    def comparison_group(self):
        # Retain runs across confinement, layer-count and parameter changes.
        # Only horizontal dimensionality/extent define this comparison group.
        return (self.horizontal_2d, self.length, self.width if not self.horizontal_2d else None)

    def active_mask(self):
        active = np.ones(self.shape, dtype=bool)
        if not self.confined:
            # A reservoir head cannot prescribe a saturated head in a layer
            # entirely above that reservoir. Its wet boundary layers stay CHD.
            active[:, :, 0] = (self.left > self.botm)[:, None]
            active[:, :, -1] = (self.right > self.botm)[:, None]
        return active

    def chd_mask(self):
        mask = self.active_mask()
        mask[:, :, 1:-1] = False
        return mask

    def k_field(self):
        if not self.random_k:
            return np.full(self.shape, self.k_ms)
        # Fixed physical zones, independent of computational grid resolution.
        # A refinement samples this same seeded realization at cell centres.
        rng = np.random.default_rng(self.k_seed)
        zones = rng.uniform(np.log(self.k_min), np.log(self.k_max),
                            (self.nlay, self.k_zones if self.horizontal_2d else 1, self.k_zones))
        index = np.minimum((self.x/self.length*self.k_zones).astype(int), self.k_zones-1)
        rows = index if self.horizontal_2d else np.array([0])
        return np.exp(zones[:, rows[:, None], index[None, :]])

    @property
    def top(self):
        return 0.0 if self.confined else self.aquifer_top

    @property
    def bottom(self):
        return -self.thickness if self.confined else 0.0

    @property
    def aquifer_label(self):
        return "Confined" if self.confined else "Unconfined / convertible"

    @property
    def dx(self):
        return self.length / (self.n - 1)

    @property
    def x(self):
        return np.linspace(0.0, self.length, self.n)

    @property
    def recharge_ms(self):
        return self.recharge_mmy / 1000.0 / SECONDS_PER_YEAR

    @property
    def transmissivity(self):
        """Constant confined T, or fully saturated T limit in convertible mode."""
        return self.k_ms * (self.top - self.bottom)

    def discharge_potential(self, heads):
        """Integral of saturated thickness dh, without K; bottom is zero.

        The linear branch above TOP handles locally fully saturated cells.
        Differentiation gives min(h, TOP), so K*d(potential)/dx is -q/W.
        """
        h = np.asarray(heads, dtype=float)
        return np.where(h <= self.top, .5*h*h, self.top*(h-.5*self.top))

    def analytic(self, x=None):
        if not self.analytical_available:
            raise ValueError("No analytical head reference is defined for heterogeneous or layered models.")
        x = self.x if x is None else np.asarray(x)
        if not self.confined:
            left, right = self.discharge_potential([self.left, self.right])
            potential = (left + (right-left)*x/self.length
                         + self.recharge_ms*x*(self.length-x)/(2*self.k_ms))
            return np.where(potential <= .5*self.top**2,
                            np.sqrt(np.maximum(2*potential, 0.)),
                            potential/self.top + .5*self.top)
        return (self.left + (self.right - self.left) * x / self.length
                + self.recharge_ms * x * (self.length - x) / (2 * self.transmissivity))

    def starting_heads(self):
        if self.initial == "Linear between boundaries":
            h = np.broadcast_to(np.linspace(self.left, self.right, self.n), self.shape).copy()
        elif self.initial == "Random distribution":
            h = np.random.default_rng(self.initial_seed).uniform(self.initial_min, self.initial_max, self.shape)
        else:
            v = self.initial_head if self.initial == "Specified uniform head" else (self.left + self.right) / 2
            h = np.full(self.shape, v, dtype=float)
        h[:, :, 0], h[:, :, -1] = self.left, self.right
        return h.ravel()

    def head_array(self, heads):
        h = np.asarray(heads, dtype=float).reshape(self.shape).copy()
        h[~self.active_mask() | ~np.isfinite(h) | (np.abs(h) >= 1e20)] = np.nan
        if not self.confined:
            h[h <= self.botm[:, None, None]] = np.nan
        return h

    def heads_table(self, heads):
        layer, row, col = np.indices(self.shape)
        data = dict(layer=(layer+1).ravel(), cell_y=(row+1).ravel(), cell_x=(col+1).ravel(),
                    x_m=self.x[col].ravel(), y_m=(row*self.dy).ravel(),
                    z_centre_m=self.z_centres[layer].ravel(), k_ms=self.k_field().ravel(),
                    initial_head_m=self.starting_heads(), modflow_head_m=self.head_array(heads).ravel(),
                    active=self.active_mask().ravel(), specified_head=self.chd_mask().ravel())
        if self.analytical_available:
            data["analytical_head_m"] = self.analytic()[col].ravel()
        return pd.DataFrame(data)


# NWT 1.3.0 native preset values. The installed program's listing remains the
# authority for built-in mode. SPECIFIED writes every value explicitly.
NWT_PRESETS = {
    "SIMPLE": dict(dbdtheta=.97, dbdkappa=.0001, dbdgamma=0., momfact=0.,
                   backflag=0, maxbackiter=20, backtol=1.5, backreduce=.97,
                   maxitinner=50, ilumethod=2, levfill=1, stoptol=1e-10, msdr=5,
                   iacl=1, norder=0, level=1, north=5, iredsys=1,
                   rrctols=0., idroptol=1, epsrn=.005, hclosexmd=.001, mxiterxmd=50),
    "MODERATE": dict(dbdtheta=.90, dbdkappa=.00001, dbdgamma=0., momfact=.1,
                     backflag=0, maxbackiter=20, backtol=1.1, backreduce=.9,
                     maxitinner=50, ilumethod=2, levfill=1, stoptol=1e-10, msdr=10,
                     iacl=1, norder=0, level=1, north=10, iredsys=1,
                     rrctols=0., idroptol=1, epsrn=.005, hclosexmd=.001, mxiterxmd=100),
    "COMPLEX": dict(dbdtheta=.85, dbdkappa=.00001, dbdgamma=0., momfact=.1,
                    backflag=1, maxbackiter=50, backtol=1.1, backreduce=.7,
                    maxitinner=50, ilumethod=2, levfill=1, stoptol=1e-10, msdr=15,
                    iacl=2, norder=0, level=15, north=1, iredsys=1,
                    rrctols=0., idroptol=1, epsrn=.001, hclosexmd=.0001, mxiterxmd=200),
}
IMS_PRESETS = {
    "SIMPLE": dict(outer_dvclose=.001, outer_maximum=25, inner_dvclose=.001,
                   inner_maximum=50, rcloserecord=.1/SECONDS_PER_DAY, linear_acceleration="CG",
                   under_relaxation="NONE", relaxation_factor=0., preconditioner_levels=0,
                   preconditioner_drop_tolerance=0., number_orthogonalizations=0),
    "MODERATE": dict(outer_dvclose=.01, outer_maximum=50, inner_dvclose=.01,
                     inner_maximum=100, rcloserecord=.1/SECONDS_PER_DAY, linear_acceleration="BICGSTAB",
                     under_relaxation="DBD", under_relaxation_theta=.9,
                     under_relaxation_kappa=.0001, relaxation_factor=.97,
                     preconditioner_levels=0, preconditioner_drop_tolerance=0.,
                     number_orthogonalizations=0),
    "COMPLEX": dict(outer_dvclose=.1, outer_maximum=100, inner_dvclose=.1,
                    inner_maximum=500, rcloserecord=.1/SECONDS_PER_DAY, linear_acceleration="BICGSTAB",
                    under_relaxation="DBD", under_relaxation_theta=.8,
                    under_relaxation_kappa=.0001, backtracking_number=20,
                    backtracking_tolerance=1.05, backtracking_reduction_factor=.1,
                    backtracking_residual_limit=.002/SECONDS_PER_DAY, relaxation_factor=0.,
                    preconditioner_levels=5, preconditioner_drop_tolerance=.0001,
                    number_orthogonalizations=2),
}


@dataclass
class Solver:
    engine: str
    method: str = "PCG"
    preset: str = "SIMPLE"
    overrides: dict = field(default_factory=dict)
    nwt_specified: bool = False

    @property
    def label(self):
        return f"{ENGINE_NAMES[self.engine]} / {self.method}"

    def parameters(self):
        if self.engine == "mf2005":
            if self.method == "PCG":
                p = dict(mxiter=100, iter1=100, npcond=1, hclose=DEFAULT_HEAD_CLOSE,
                         rclose=DEFAULT_FLOW_CLOSE["mf2005"], relax=1., nbpol=0, iprpcg=1, mutpcg=0, damp=1.)
            elif self.method == "SIP":
                p = dict(mxiter=500, nparm=5, accl=1., hclose=DEFAULT_HEAD_CLOSE,
                         ipcalc=1, wseed=0., iprsip=1)
            else:
                raise ValueError("MODFLOW-2005 supports PCG and SIP in this app.")
        elif self.engine == "mfnwt":
            if self.method not in ("GMRES", "XMD"):
                raise ValueError("NWT method must be GMRES or XMD.")
            p = dict(headtol=DEFAULT_HEAD_CLOSE, fluxtol=DEFAULT_FLOW_CLOSE["mfnwt"], maxiterout=100, thickfact=1e-5,
                     linmeth=1 if self.method == "GMRES" else 2, iprnwt=2, ibotav=0,
                     options="SPECIFIED" if self.nwt_specified else self.preset)
            if self.nwt_specified:
                p.update(NWT_PRESETS[self.preset])
        elif self.engine == "mf6":
            if self.method not in ("CG", "BICGSTAB"):
                raise ValueError("IMS method must be CG or BICGSTAB.")
            p = dict(complexity=self.preset, print_option="ALL",
                     csv_outer_output_filerecord="outer.csv",
                     csv_inner_output_filerecord="inner.csv",
                     linear_acceleration=self.method,
                     scaling_method="DIAGONAL",
                     outer_dvclose=DEFAULT_HEAD_CLOSE, inner_dvclose=DEFAULT_HEAD_CLOSE,
                     rcloserecord=DEFAULT_FLOW_CLOSE["mf6"],
                     backtracking_residual_limit=.002/SECONDS_PER_DAY)
        else:
            raise ValueError("Unknown engine.")
        p.update(self.overrides)
        return p


def usable_executable(path: Path) -> str | None:
    """Validate a local/native program and restore an owner execute bit on POSIX.

    Matches the boundary app's repository-bin deployment. No download, shell,
    solver substitution or model-parameter change occurs here.
    """
    try:
        path = path.resolve()
        if not path.is_file():
            return None
        if os.name != "nt":
            with path.open("rb") as binary:
                if binary.read(2) == b"MZ":
                    return None  # A Windows binary cannot run on Linux/macOS.
            if not os.access(path, os.X_OK):
                path.chmod(path.stat().st_mode | stat.S_IXUSR)
        return str(path) if os.access(path, os.X_OK) else None
    except OSError:
        return None


def find_executable(engine: str, custom: str = "") -> str | None:
    """Explicit override, script/parent/cwd bin folders, then PATH.

    The parent bin supports an app subfolder in the existing Streamlit repo.
    An invalid explicit override never silently selects a different program.
    """
    explicit = (custom.strip() or os.environ.get(engine.upper() + "_EXE", "").strip()
                or os.environ.get(engine.upper() + "_EXECUTABLE", "").strip())
    if explicit:
        path = Path(explicit).expanduser()
        candidates = [path] if path.is_absolute() else [ROOT/path, Path.cwd()/path]
        for candidate in candidates:
            if candidate.is_file():
                return usable_executable(candidate)
        found = shutil.which(explicit)
        return usable_executable(Path(found)) if found else None
    names = [name + ext for name in EXE_NAMES[engine]
             for ext in ([".exe", ""] if os.name == "nt" else ["", ".exe"])]
    for folder in dict.fromkeys([ROOT/"bin", ROOT.parent/"bin", Path.cwd()/"bin", ROOT]):
        for name in names:
            candidate = usable_executable(folder/name)
            if candidate:
                return candidate
    for name in names:
        found = shutil.which(name)
        if found:
            candidate = usable_executable(Path(found))
            if candidate:
                return candidate
    return None


def find_library(custom=""):
    value = custom.strip() or os.environ.get("LIBMF6_PATH", "").strip()
    if value:
        p = Path(value).expanduser()
        return str(p.resolve()) if p.is_file() else None
    for name in ("libmf6.dll", "libmf6.so", "libmf6.dylib"):
        p = ROOT / "bin" / name
        if p.is_file():
            return str(p)
    return None


def build_model(s: Scenario, solver: Solver, directory: Path, executable: str):
    """Same physical problem; end nodes are CHD reservoirs.

    Convertible conductance retains each engine's native averaging: LPF/NPF
    harmonic means and UPW upstream weighting. MF6 retains Picard iteration,
    allowing both CG and BICGSTAB; NWT uses its Newton formulation.
    """
    s.validate()
    directory = Path(directory).resolve()
    directory.mkdir(parents=True, exist_ok=True)
    rch = np.full((s.nrow, s.n), s.recharge_ms)
    rch[:, [0, -1]] = 0.0
    initial = s.starting_heads().reshape(s.shape)
    active = s.active_mask().astype(int)
    conductivity = s.k_field()
    chd = [(tuple(int(v) for v in cell), s.left if cell[2] == 0 else s.right)
           for cell in np.argwhere(s.chd_mask())]
    wetting = not s.confined and s.nlay > 1
    p = solver.parameters()
    if solver.engine == "mf6":
        sim = flopy.mf6.MFSimulation(sim_name="lab", sim_ws=str(directory), exe_name=executable)
        sim.simulation_data.float_precision = 16
        sim.simulation_data.float_characters = 25
        flopy.mf6.ModflowTdis(sim, time_units="SECONDS", nper=1, perioddata=[(1., 1, 1.)])
        flopy.mf6.ModflowIms(sim, **p)
        gwf = flopy.mf6.ModflowGwf(sim, modelname="flow", save_flows=True)
        flopy.mf6.ModflowGwfdis(gwf, nlay=s.nlay, nrow=s.nrow, ncol=s.n, delr=s.dx,
                              delc=s.dy, top=s.top, botm=s.botm, idomain=active, length_units="METERS")
        flopy.mf6.ModflowGwfic(gwf, strt=initial)
        npf_options = dict(rewet_record=[("WETFCT", .5, "IWETIT", 1, "IHDWET", 0)],
                           wetdry=-.01, cvoptions=[("VARIABLECV", "DEWATERED")]) if wetting else {}
        flopy.mf6.ModflowGwfnpf(gwf, icelltype=int(not s.confined), k=conductivity,
                               k33=conductivity, save_flows=True, **npf_options)
        flopy.mf6.ModflowGwfchd(gwf, stress_period_data=chd, save_flows=True)
        flopy.mf6.ModflowGwfrcha(gwf, recharge=rch, save_flows=True)
        # Absence of STO means steady flow. The 1-second TDIS step is bookkeeping,
        # not a simulated transient or a solver iteration.
        flopy.mf6.ModflowGwfoc(gwf, head_filerecord="flow.hds", budget_filerecord="flow.cbc",
                             saverecord=[("HEAD", "ALL"), ("BUDGET", "ALL")],
                             printrecord=[("BUDGET", "ALL")])
        sim.write_simulation(silent=True)
        return [executable], directory / "flow.hds"
    model = flopy.modflow.Modflow("flow", version=solver.engine, exe_name=executable, model_ws=str(directory))
    flopy.modflow.ModflowDis(model, nlay=s.nlay, nrow=s.nrow, ncol=s.n, delr=s.dx, delc=s.dy,
                           top=s.top, botm=s.botm, nper=1, perlen=1., nstp=1,
                           steady=True, itmuni=1, lenuni=2)
    flopy.modflow.ModflowBas(model, ibound=active, strt=initial)
    if solver.engine == "mf2005":
        flopy.modflow.ModflowLpf(model, laytyp=int(not s.confined), hk=conductivity, vka=conductivity,
                                ipakcb=53, laywet=int(wetting), wetdry=-.01, wetfct=.5, iwetit=1, ihdwet=0)
        if solver.method == "PCG":
            flopy.modflow.ModflowPcg(model, **p)
        else:
            flopy.modflow.ModflowSip(model, **p)
    else:
        flopy.modflow.ModflowUpw(model, laytyp=int(not s.confined), hk=conductivity, vka=conductivity, ipakcb=53)
        flopy.modflow.ModflowNwt(model, **p)
    flopy.modflow.ModflowChd(model, stress_period_data={0: [[*cell, head, head] for cell, head in chd]})
    flopy.modflow.ModflowRch(model, nrchop=3, rech=rch, ipakcb=53)
    flopy.modflow.ModflowOc(model, stress_period_data={(0, 0): ["save head", "save budget", "print budget"]},
                          compact=True)
    # FloPy's legacy arrays are float32 internally; avoid additional loss from
    # its default seven-significant-digit text serialization.
    for package in model.packagelist:
        for value in vars(package).values():
            arrays = []
            if isinstance(value, flopy.utils.Util2d):
                arrays = [value]
            elif isinstance(value, flopy.utils.Util3d):
                arrays = value.util_2ds
            elif isinstance(value, flopy.utils.Transient2d):
                arrays = list(value.transient_2ds.values())
            for array in arrays:
                if np.issubdtype(array.dtype, np.floating):
                    # Legacy MODFLOW reads one grid row at a time. FloPy's
                    # formatter streams continuously, so each row must end on
                    # a record boundary (critical when NCOL is not a multiple
                    # of five). One complete row per record is unambiguous.
                    count = array.shape[-1] if len(array.shape) == 2 and array.shape[0] > 1 else 5
                    array.format.fortran = f"({count}E25.16)"
    model.write_input()
    return [executable, "flow.nam"], directory / "flow.hds"


def fingerprint(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, default=str).encode()).hexdigest()[:16]


def head_metrics(s: Scenario, heads, face_flows=None):
    raw = np.asarray(heads, dtype=float)
    if raw.size != s.total_cells:
        raise ValueError("Missing or invalid head array size.")
    h = s.head_array(raw)
    if not np.isfinite(h[:, :, 1:-1]).any(axis=0).all():
        raise ValueError("Missing, invalid or entirely dry groundwater columns.")
    boundary = s.chd_mask()
    prescribed = np.broadcast_to(np.where(np.arange(s.n) == 0, s.left, s.right), s.shape)
    if not np.isfinite(h[boundary]).all():
        raise ValueError("Missing, invalid or dry specified-head values.")
    if s.confined and not np.isfinite(h[s.active_mask()]).all():
        raise ValueError("Missing or invalid confined head values.")
    error = (h[:, :, 1:-1] - s.analytic()[None, None, 1:-1]) if s.analytical_available else None
    if s.confined and s.nlay == 1 and not s.horizontal_2d and not s.random_k:
        # Independent check of the original homogeneous 1-D benchmark.
        h1 = h.ravel()
        conductance = s.transmissivity * s.width / s.dx
        residual = conductance * (h1[:-2] - 2*h1[1:-1] + h1[2:]) + s.recharge_ms*s.width*s.dx
        qleft = conductance*(h1[0]-h1[1])
        qright = conductance*(h1[-1]-h1[-2])
        recharge = s.recharge_ms*s.width*(s.n-2)*s.dx
    elif isinstance(face_flows, dict):
        # Positive right/front/lower native face flows leave the current cell.
        right, front, lower, rch = (np.asarray(face_flows[k], dtype=float).reshape(s.shape)
                                    for k in ("right", "front", "lower", "recharge"))
        if not all(np.isfinite(v).all() for v in (right, front, lower, rch)):
            raise ValueError("Invalid native budget flows.")
        residual = rch-right-front-lower
        residual[:, :, 1:] += right[:, :, :-1]
        residual[:, 1:, :] += front[:, :-1, :]
        residual[1:, :, :] += lower[:-1, :, :]
        residual = residual[s.active_mask() & ~boundary]
        qleft, qright = right[:, :, 0].sum(), -right[:, :, -2].sum()
        recharge = rch[:, :, 1:-1].sum()
    else:
        # Compatibility for direct single-layer, single-row budget checks.
        if s.nlay != 1 or s.nrow != 1 or face_flows is None:
            raise ValueError("These diagnostics require native cell-face flows and recharge.")
        face = np.asarray(face_flows, dtype=float).ravel()
        if face.size != s.n-1 or not np.isfinite(face).all():
            raise ValueError("Missing or invalid native cell-face flows.")
        residual = face[:-1]-face[1:]+s.recharge_ms*s.width*s.dx
        qleft, qright = face[0], -face[-1]
        recharge = s.recharge_ms*s.width*(s.n-2)*s.dx
    return dict(rmse_m=float(np.sqrt(np.mean(error**2))) if error is not None else None,
                max_error_m=float(np.max(np.abs(error))) if error is not None else None,
                max_residual_m3s=float(np.max(np.abs(residual))),
                boundary_error_m=float(np.max(np.abs(h[boundary]-prescribed[boundary]))),
                qleft_m3s=float(qleft), qright_m3s=float(qright), recharge_m3s=float(recharge),
                balance_m3s=float(qleft+qright+recharge),
                dry_cells=int(np.count_nonzero(s.active_mask() & ~np.isfinite(h))))


def read_native_budget(directory: Path, engine: str, shape, precision=None):
    """Native intercell flows and actual recharge placement in m³/s."""
    if precision is None:
        with flopy.utils.HeadFile(Path(directory)/"flow.hds", precision="auto") as head:
            precision = head.precision
    with flopy.utils.CellBudgetFile(Path(directory)/"flow.cbc", precision=precision) as budget:
        if engine == "mf6":
            from flopy.mf6.utils.postprocessing import get_structured_faceflows
            flowja = budget.get_data(text="FLOW-JA-FACE")[-1]
            right, front, lower = get_structured_faceflows(flowja, grb_file=str(Path(directory)/"flow.dis.grb"))
            recharge = np.zeros(shape)
            values = budget.get_data(text="RCH")[-1]
            np.add.at(recharge.ravel(), values["node"]-1, values["q"])
        else:
            names = [v.decode().strip() for v in budget.get_unique_record_names()]
            def read_flow(name):
                if name not in names:
                    return np.zeros(shape)
                return np.asarray(np.ma.filled(budget.get_data(text=name, full3D=True)[-1], 0.))
            right = read_flow("FLOW RIGHT FACE")
            front = read_flow("FLOW FRONT FACE")
            lower = read_flow("FLOW LOWER FACE")
            recharge = read_flow("RECHARGE")
    return dict(right=right, front=front, lower=lower, recharge=recharge)


def read_face_flows(directory: Path, engine: str, precision=None):
    """Single-row compatibility helper, with flows now expressed in m³/s."""
    with flopy.utils.HeadFile(Path(directory)/"flow.hds", precision="auto") as head:
        shape = head.get_data().shape
    return read_native_budget(directory, engine, shape, precision)["right"].ravel()[:-1]


NUMBER = r"[-+]?(?:\d+\.?\d*|\.\d+)(?:[EeDd][-+]?\d+)?"


def parse_diagnostics(directory: Path, solver: Solver):
    """Native counts only. Unavailable diagnostics stay None, never guessed."""
    directory = Path(directory)
    listing = "\n".join(p.read_text(errors="replace") for p in sorted(directory.iterdir())
                        if p.suffix.lower() in (".lst", ".list"))
    result = dict(outer_iterations=None, inner_iterations=None, sip_iterations=None,
                  budget_percent=None, history=[], listing=listing)
    budget = re.findall(r"PERCENT DISCREPANCY\s*=\s*(" + NUMBER + ")", listing, re.I)
    if budget:
        result["budget_percent"] = float(budget[-1].replace("D", "E"))
    if solver.engine == "mf6":
        outer_file, inner_file = directory / "outer.csv", directory / "inner.csv"
        if outer_file.is_file():
            outer = pd.read_csv(outer_file)
            outer.columns = outer.columns.str.strip().str.lower()
            result["outer_iterations"] = len(outer)
            if len(outer) and "total_inner_iterations" in outer:
                result["inner_iterations"] = int(outer.total_inner_iterations.max())
            for _, row in outer.iterrows():
                result["history"].append(dict(iteration=int(row.get("nouter", len(result["history"]) + 1)),
                                               head_change=abs(float(row.get("solution_outer_dvmax", np.nan))),
                                               residual=np.nan, kind="outer"))
        if inner_file.is_file():
            inner = pd.read_csv(inner_file)
            inner.columns = inner.columns.str.strip().str.lower()
            # total_inner_iterations counts actual linear iterations, not CSV rows.
            if len(inner) and "total_inner_iterations" in inner:
                result["inner_iterations"] = int(inner.total_inner_iterations.max())
            # Very long failed solves can produce hundreds of thousands of
            # rows. Preserve the native total, but bound the UI history size.
            if len(inner) > 20000:
                result["history_sampled"] = True
                inner = inner.iloc[np.linspace(0, len(inner)-1, 20000).astype(int)]
            values = inner[["total_inner_iterations", "solution_inner_dvmax", "solution_inner_rmax"]].to_numpy()
            result["history"].extend(dict(iteration=int(i), head_change=abs(float(h)),
                                          residual=abs(float(r)), kind="inner") for i, h, r in values)
    elif solver.engine == "mfnwt":
        outer = re.search(r"NWT REQUIRED\s+(\d+) OUTER ITERATIONS", listing)
        inner = re.search(r"AND A TOTAL OF\s+(\d+) INNER ITERATIONS", listing)
        result["outer_iterations"] = int(outer[1]) if outer else None
        result["inner_iterations"] = int(inner[1]) if inner else None
        in_table = False
        for line in listing.splitlines():
            if "Residual-Control" in line and "Outer-Iter." in line:
                in_table = True
                continue
            if not in_table:
                continue
            values = line.split()
            if len(values) == 12:
                try:
                    result["history"].append(dict(iteration=int(values[1]),
                        head_change=abs(float(values[6].replace("D", "E"))),
                        residual=abs(float(values[10].replace("D", "E"))), kind="outer"))
                except ValueError:
                    pass
            elif not line.strip() and result["history"]:
                in_table = False
    elif solver.method == "PCG":
        outer = re.search(r"(\d+) CALLS TO PCG ROUTINE", listing)
        inner = re.search(r"(\d+) TOTAL ITERATIONS", listing)
        result["outer_iterations"] = int(outer[1]) if outer else None
        result["inner_iterations"] = int(inner[1]) if inner else None
    else:
        iterations = re.search(r"(\d+) ITERATIONS FOR TIME STEP", listing)
        result["sip_iterations"] = int(iterations[1]) if iterations else None
    if solver.engine == "mf2005":
        def table_values(title):
            part = listing.split(title, 1)
            if len(part) != 2:
                return []
            block = part[1].split("---", 1)
            if len(block) != 2:
                return []
            values = []
            for line in block[1].splitlines()[1:]:
                if not line.strip():
                    break
                if "(" in line or not line.strip("- "):
                    continue
                nums = re.findall(NUMBER, line)
                if solver.method == "PCG":
                    nums = nums[1::2]  # skip first-inner-iteration flags
                values.extend(abs(float(v.replace("D", "E"))) for v in nums)
            return values
        changes = table_values("MAXIMUM HEAD CHANGE FOR EACH ITERATION")
        residuals = table_values("MAXIMUM RESIDUAL FOR EACH ITERATION")
        result["history"] = [dict(iteration=i+1, head_change=v,
            residual=residuals[i] if i < len(residuals) else np.nan,
            kind="inner" if solver.method == "PCG" else "SIP") for i, v in enumerate(changes)]
    return result


def run_once(s: Scenario, solver: Solver, directory: Path, executable: str, timeout=60.):
    directory = Path(directory).resolve()
    start = time.perf_counter()
    command, headfile = build_model(s, solver, directory, executable)
    build_s = time.perf_counter() - start
    stdoutfile = directory / "stdout.txt"
    start = time.perf_counter()
    timed_out = False
    try:
        proc = subprocess.run(command, cwd=directory, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                              timeout=timeout, check=False, shell=False, text=True, errors="replace")
        returncode, stdout = proc.returncode, proc.stdout
    except subprocess.TimeoutExpired as e:
        timed_out, returncode = True, None
        stdout = (e.stdout or b"").decode(errors="replace") if isinstance(e.stdout, bytes) else (e.stdout or "")
    except OSError as e:
        stdout, returncode = str(e), -1
    wall_s = time.perf_counter() - start
    stdoutfile.write_text(stdout)
    diagnostics = parse_diagnostics(directory, solver)
    combined = stdout + "\n" + diagnostics["listing"]
    normal = "normal termination" in stdout.lower()
    failure = bool(re.search(r"FAILED TO (?:CONVERGE|MEET)|CONVERGENCE FAILURE|FAILURE TO CONVERGE", combined, re.I))
    success = normal and returncode == 0 and not failure and not timed_out
    result = dict(engine=solver.engine, method=solver.method, label=solver.label,
                  scenario=asdict(s), solver=asdict(solver), directory=str(directory),
                  executable=str(executable), build_s=build_s, wall_s=wall_s,
                  returncode=returncode, timed_out=timed_out, success=success,
                  stdout=stdout, heads=None, metrics={}, **diagnostics)
    if headfile.is_file():
        try:
            with flopy.utils.HeadFile(headfile, precision="auto") as reader:
                heads = reader.get_data().ravel()
            faces = read_native_budget(directory, solver.engine, s.shape, reader.precision)
            result["metrics"] = head_metrics(s, heads, faces)
            result["heads"] = s.head_array(heads).ravel().tolist()
        except (ValueError, EOFError, OSError, KeyError, IndexError) as e:
            result["read_error"] = str(e)
            result["success"] = False
    else:
        result["success"] = False
    native_fpe = bool(re.search(r"floating divide by zero|floating invalid|floating overflow|floating.point exception", combined, re.I))
    result["native_fpe"] = native_fpe
    result["status"] = "Converged" if result["success"] else (
        "Timed out" if timed_out else "Native floating-point failure" if native_fpe else "Failed / not converged")
    (directory / "scenario.json").write_text(json.dumps(dict(scenario=asdict(s), solver=asdict(solver)), indent=2))
    return result


def run_repeated(s, solver, directory, executable, repeats=1, timeout=60.):
    runs = [run_once(s, solver, Path(directory) / f"repeat_{i+1}", executable, timeout) for i in range(repeats)]
    result = runs[-1]
    samples = [r["wall_s"] for r in runs]
    result.update(wall_s=float(np.median(samples)), wall_min_s=min(samples), wall_max_s=max(samples),
                  time_samples_s=samples, repeats=repeats,
                  all_repeats_converged=all(r["success"] for r in runs),
                  repeat_status=[{k: r[k] for k in ("success", "outer_iterations", "inner_iterations", "sip_iterations")}
                                 for r in runs])
    if not result["all_repeats_converged"]:
        result["success"] = False
        result["status"] = "At least one repeat failed"
    return result


def comparison_row(r):
    scenario = Scenario(**r["scenario"])
    # Describe the sampled model field, including uniform one-zone/equal-limit cases.
    heterogeneous = scenario.random_k and np.ptp(scenario.k_field()) > 0
    label = r["label"] + (" · het." if heterogeneous else "")
    return {"Model / solver": label, "Aquifer": scenario.aquifer_label,
            "Cells": scenario.total_cells,
            "Grid (x × y × layers)": scenario.grid_label,
            "Δx (m)": scenario.dx, "Δy (m)": scenario.dy,
            "Layers": scenario.nlay, "Status": r["status"],
            "Outer iterations": r["outer_iterations"], "Inner iterations": r["inner_iterations"],
            "SIP iterations": r["sip_iterations"], "Process time (s)": r["wall_s"],
            "Min time (s)": r.get("wall_min_s", r["wall_s"]), "Max time (s)": r.get("wall_max_s", r["wall_s"]),
            "RMSE (m)": r["metrics"].get("rmse_m"), "Max error (m)": r["metrics"].get("max_error_m"),
            "Max cell residual (m³/s)": r["metrics"].get("max_residual_m3s"),
            "Budget discrepancy (%)": r["budget_percent"]}


def record_mf6(s, solver, directory, executable, library, timeout=60.):
    """Separate process: native libraries have global state and may terminate."""
    directory = Path(directory).resolve()
    build_model(s, solver, directory, executable)
    with (directory / "api_stdout.txt").open("w") as output:
        proc = subprocess.run([sys.executable, str(ROOT / "api_worker.py"), library, str(directory)],
                              stdout=output, stderr=subprocess.STDOUT, timeout=timeout, check=False)
    datafile = directory / "snapshots.npz"
    if proc.returncode or not datafile.is_file():
        raise RuntimeError((directory / "api_stdout.txt").read_text(errors="replace")[-4000:])
    with np.load(datafile) as data:
        return {key: data[key].copy() for key in data.files}
