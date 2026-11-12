"""Equivalent native MF2005/LPF, NWT/UPW and MF6/NPF-STO models.

Keep engine-specific behavior explicit. In particular, MF2005 wetting/drying
and NWT/MF6 flow reductions are not interchangeable solver algorithms.
"""

import os
import shutil
import stat
from pathlib import Path

import flopy
import numpy as np

from .config import Scenario, Solver

ROOT = Path(__file__).resolve().parent.parent
EXE_NAMES = {
    "mf2005": ("mf2005dbl", "mf2005", "MODFLOW-2005_64"),
    "mfnwt": ("mfnwtdbl", "mfnwt", "MODFLOW-NWT_64"),
    "mf6": ("mf6",),
}


def find_executable(engine):
    """App bin, parent bin or PATH; environment override has precedence."""
    override = os.environ.get(engine.upper() + "_EXE", "").strip()
    candidates = []
    if override:
        candidates = [Path(shutil.which(override) or override)]
    else:
        suffix = ".exe" if os.name == "nt" else ""
        names = [name + suffix for name in EXE_NAMES[engine]]
        for folder in (ROOT / "bin", ROOT.parent / "bin", Path.cwd() / "bin"):
            candidates.extend(folder / name for name in names)
        candidates.extend(Path(p) for name in names if (p := shutil.which(name)))
    for path in candidates:
        if not path.is_file():
            continue
        if os.name != "nt":
            with path.open("rb") as handle:
                if handle.read(2) == b"MZ":
                    continue
            try:
                path.chmod(path.stat().st_mode | stat.S_IXUSR)
            except OSError:
                continue
        if os.access(path, os.X_OK):
            return str(path.resolve())
    return None


def build_model(s: Scenario, cfg: Solver, directory: Path, executable: str):
    """Write one native simulation; return its command, never invoke a shell."""
    s.validate()
    cfg.validate()
    directory = Path(directory).resolve()
    directory.mkdir(parents=True, exist_ok=True)
    periods = s.periods()
    active = s.active_mask().astype(int)
    conductivity = s.k_field()
    recharge = np.full((s.nrow, s.ncol), s.recharge_ms)
    recharge[:, [0, -1]] = 0.0  # CHD columns are reservoirs, not recharge area
    recharge[~active.any(axis=0).astype(bool)] = 0.0
    chd = [
        (tuple(map(int, cell)), s.left if cell[2] == 0 else s.right)
        for cell in np.argwhere(s.chd_mask())
    ]
    well = {
        p: [
            (k, i, j, s.well_rate(w, period) * weight)
            for w in s.wells
            for k, i, j, weight in s.well_cells(w)
        ]
        for p, period in enumerate(periods)
    }
    convertible = int(not s.confined)

    if cfg.engine == "mf6":
        sim = flopy.mf6.MFSimulation(
            sim_name="lab", sim_ws=str(directory), exe_name=executable
        )
        sim.simulation_data.float_precision = 16
        flopy.mf6.ModflowTdis(
            sim,
            time_units="SECONDS",
            nper=len(periods),
            perioddata=[(p.seconds, p.steps, p.multiplier) for p in periods],
        )
        flopy.mf6.ModflowIms(
            sim,
            complexity="COMPLEX",
            print_option="ALL",
            outer_dvclose=cfg.head_close,
            inner_dvclose=cfg.head_close,
            outer_maximum=cfg.outer,
            inner_maximum=cfg.inner,
            rcloserecord=[cfg.flow_close, "STRICT"],
            linear_acceleration="BICGSTAB",
            scaling_method="DIAGONAL",
            relaxation_factor=0.97,
            csv_outer_output_filerecord="outer.csv",
            csv_inner_output_filerecord="inner.csv",
        )
        newton = "NEWTON UNDER_RELAXATION" if convertible and cfg.newton else None
        gwf = flopy.mf6.ModflowGwf(
            sim, modelname="flow", save_flows=True, newtonoptions=newton
        )
        flopy.mf6.ModflowGwfdis(
            gwf,
            nlay=s.nlay,
            nrow=s.nrow,
            ncol=s.ncol,
            delr=s.cell_size,
            delc=s.cell_size,
            top=s.top,
            botm=s.botm,
            idomain=active,
            length_units="METERS",
        )
        flopy.mf6.ModflowGwfic(gwf, strt=s.starting_heads())
        npf_options = {}
        if convertible and not cfg.newton and cfg.rewet:
            npf_options.update(
                rewet_record=[("WETFCT", 0.5, "IWETIT", 1, "IHDWET", 0)],
                wetdry=cfg.wetdry,
            )
        flopy.mf6.ModflowGwfnpf(
            gwf,
            icelltype=convertible,
            k=conductivity,
            k33=conductivity * s.vertical_ratio,
            **npf_options,
        )
        # SS_CONFINED_ONLY matches LPF/UPW elastic storage below/above layer top.
        flopy.mf6.ModflowGwfsto(
            gwf,
            iconvert=convertible,
            ss=s.ss,
            sy=s.sy,
            ss_confined_only=True,
            save_flows=True,
            steady_state={0: True},
            transient={1: True} if s.transient else None,
        )
        flopy.mf6.ModflowGwfchd(gwf, stress_period_data={0: chd}, save_flows=True)
        flopy.mf6.ModflowGwfrcha(gwf, recharge=recharge, save_flows=True)
        well6 = {
            p: [(tuple(v[:3]), v[3]) for v in values] for p, values in well.items()
        }
        flopy.mf6.ModflowGwfwel(
            gwf,
            stress_period_data=well6,
            save_flows=True,
            auto_flow_reduce=cfg.flow_reduction if convertible else None,
            afrcsv_filerecord="well_reduction.csv" if convertible else None,
        )
        flopy.mf6.ModflowGwfoc(
            gwf,
            head_filerecord="flow.hds",
            budget_filerecord="flow.cbc",
            saverecord=[("HEAD", "ALL"), ("BUDGET", "ALL")],
            printrecord=[("BUDGET", "ALL")],
        )
        sim.write_simulation(silent=True)
        return [executable]

    model = flopy.modflow.Modflow(
        "flow", version=cfg.engine, exe_name=executable, model_ws=str(directory)
    )
    flopy.modflow.ModflowDis(
        model,
        nlay=s.nlay,
        nrow=s.nrow,
        ncol=s.ncol,
        delr=s.cell_size,
        delc=s.cell_size,
        top=s.top,
        botm=s.botm,
        nper=len(periods),
        perlen=[p.seconds for p in periods],
        nstp=[p.steps for p in periods],
        tsmult=[p.multiplier for p in periods],
        steady=[p.steady for p in periods],
        itmuni=1,
        lenuni=2,
    )
    flopy.modflow.ModflowBas(model, ibound=active, strt=s.starting_heads())
    properties = dict(
        laytyp=convertible,
        hk=conductivity,
        vka=conductivity * s.vertical_ratio,
        ss=s.ss,
        sy=s.sy,
        ipakcb=53,
        hdry=-1e30,
    )
    if cfg.engine == "mf2005":
        flopy.modflow.ModflowLpf(
            model,
            **properties,
            laywet=int(convertible and cfg.rewet),
            wetdry=cfg.wetdry,
            wetfct=0.5,
            iwetit=1,
            ihdwet=0,
        )
        flopy.modflow.ModflowPcg(
            model,
            mxiter=cfg.outer,
            iter1=cfg.inner,
            hclose=cfg.head_close,
            rclose=cfg.flow_close,
            damp=cfg.damping,
            dampt=cfg.damping,
            iprpcg=1,
            mutpcg=0,
        )
    else:
        flopy.modflow.ModflowUpw(model, **properties, iphdry=0)
        flopy.modflow.ModflowNwt(
            model,
            options="SPECIFIED",
            headtol=cfg.head_close,
            fluxtol=cfg.flow_close,
            maxiterout=cfg.outer,
            linmeth=cfg.nwt_method,
            ibotav=cfg.ibotav,
            iprnwt=2,
            thickfact=1e-5,
            maxitinner=cfg.inner,
            mxiterxmd=cfg.inner,
            hclosexmd=cfg.head_close,
            dbdtheta=0.85,
            dbdkappa=1e-5,
            dbdgamma=0.0,
            momfact=0.1,
            backflag=1,
            maxbackiter=50,
            backtol=1.1,
            backreduce=0.7,
            ilumethod=2,
            levfill=1,
            msdr=15,
            iacl=2,
            norder=0,
            level=15,
            north=1,
            iredsys=1,
            epsrn=0.001,
        )
    flopy.modflow.ModflowChd(
        model, stress_period_data={0: [[*c, h, h] for c, h in chd]}
    )
    flopy.modflow.ModflowRch(model, nrchop=3, rech=recharge, ipakcb=53)
    # Explicitly set the native NWT reduction fraction; report actual CBC flows.
    options = [f"SPECIFY {cfg.flow_reduction:.12g}"] if cfg.engine == "mfnwt" else None
    flopy.modflow.ModflowWel(model, stress_period_data=well, ipakcb=53, options=options)
    output = {
        (p, step): ["save head", "save budget", "print budget"]
        for p, period in enumerate(periods)
        for step in range(period.steps)
    }
    flopy.modflow.ModflowOc(model, stress_period_data=output, compact=True)
    # Preserve one row per array record, including odd column counts.
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
                    count = array.shape[-1] if len(array.shape) == 2 else 5
                    array.format.fortran = f"({count}E25.16)"
    model.write_input()
    return [executable, "flow.nam"]
