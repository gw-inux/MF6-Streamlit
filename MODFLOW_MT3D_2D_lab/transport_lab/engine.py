"""Native MODFLOW-2005/MT3DMS engine with independently checked outputs.

All hydraulic/transport inputs use metres, days and grams. Each calculation owns
its directory; process output goes to disk to avoid pipe back-pressure stalls.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from pathlib import Path
import copy
import os
import platform
import re
import shutil
import stat
import subprocess
import tempfile
from time import perf_counter

import flopy
import numpy as np
import pandas as pd

from .config import Config, METHODS

ROOT = Path(__file__).resolve().parents[1]
ALIASES = {
    'mf2005': ('mf2005', 'mf2005_MT3D', 'MODFLOW-2005_64', 'MODFLOW2005', 'MODFLOW-2005'),
    'mt3dms': ('mt3dms', 'mt3dms5b', 'MT3DMS_64', 'MT3DMS5', 'MT3DMS'),
    'mp7': ('mp7', 'mpath7', 'MODPATH7', 'modpath7'),
}

class RunError(RuntimeError):
    """A native calculation did not yield a complete, usable result."""


def _available(path: Path) -> bool:
    try:
        if not path.is_file():
            return False
        if os.name != 'nt':
            with path.open('rb') as binary:
                if binary.read(2) == b'MZ':
                    return False
            if not os.access(path, os.X_OK):
                path.chmod(path.stat().st_mode | stat.S_IXUSR)
        return os.access(path, os.X_OK)
    except OSError:
        return False


def find_engines(root=None):
    """Find the three native programs, without network calls or installations."""
    root = Path(root) if root else ROOT
    ostag = 'win64' if os.name == 'nt' else ('macarm' if platform.system() == 'Darwin' and platform.machine() == 'arm64' else 'mac' if platform.system() == 'Darwin' else 'linux')
    configured = os.getenv('TRANSPORT_LAB_BIN')
    dirs = ([Path(configured).expanduser()] if configured else []) + [
        root / 'bin' / ostag, root / 'bin', root, root.parent / 'bin' / ostag,
        root.parent / 'bin', root / 'common', root.parent / 'common',
        root / 'common' / 'bin', root.parent / 'common' / 'bin']
    result = {}
    for kind, aliases in ALIASES.items():
        explicit = os.getenv('TRANSPORT_LAB_' + kind.upper())
        if explicit and _available(Path(explicit).expanduser()):
            result[kind] = str(Path(explicit).expanduser().resolve())
            continue
        names = [name + ext for name in aliases for ext in (('.exe', '') if os.name == 'nt' else ('',))]
        match = next((d / n for d in dirs for n in names if _available(d / n)), None)
        result[kind] = str(match.resolve()) if match else next((p for n in names if (p := shutil.which(n))), None)
    return result


def periods(config: Config, equilibrium=False):
    if equilibrium:
        return [1.0], [1]
    lengths = ([config.pulse_duration, config.duration-config.pulse_duration]
               if config.source_kind == 'pulse' else [config.duration])
    steps = [max(1, int(np.ceil(config.flow_steps * p/config.duration))) if config.transient else 1 for p in lengths]
    return lengths, steps


def initial_concentration(config: Config):
    initial = np.zeros(config.shape, dtype=float)
    if config.source_kind == 'dirac':
        por = config.arrays()[2]
        cells = config.source_cells()
        porevolume = sum(por[k, i, j] * config.dx * config.dy * config.dz for k, i, j in cells)
        for cell in cells:
            initial[cell] = config.source_mass / porevolume
    return initial


def build_flow(config: Config, workspace, engines, initial_heads=None, equilibrium=False):
    """Build and write a fully confined flow model; heads act at end-cell centres."""
    folder = Path(workspace); folder.mkdir(parents=True, exist_ok=True)
    lengths, steps = periods(config, equilibrium)
    steady = equilibrium or not config.transient
    hk, ss, _ = config.arrays()
    right = config.head_right if equilibrium or not config.transient else config.head_right_final
    if initial_heads is None:
        initial_heads = np.broadcast_to(np.linspace(config.head_left, config.head_right, config.ncol), config.shape).copy()
    flow = flopy.modflow.Modflow('flow', version='mf2005', exe_name=engines.get('mf2005'), model_ws=str(folder))
    flopy.modflow.ModflowDis(flow, nlay=config.nlay, nrow=config.nrow, ncol=config.ncol,
        delr=config.dx, delc=config.dy, top=config.thickness,
        botm=np.linspace(config.thickness-config.dz, 0., config.nlay),
        nper=len(lengths), perlen=lengths, nstp=steps, tsmult=1.0,
        steady=steady, itmuni=4, lenuni=2)
    flopy.modflow.ModflowBas(flow, ibound=np.ones(config.shape, dtype=np.int32), strt=initial_heads)
    flopy.modflow.ModflowLpf(flow, laytyp=0, hk=hk, vka=hk*config.kv_ratio, ss=ss, ipakcb=53)
    boundaries = [(k,i,j,h,h) for k in range(config.nlay) for i in range(config.nrow)
                  for j,h in ((0, config.head_left), (config.ncol-1,right))]
    flopy.modflow.ModflowChd(flow, stress_period_data={p:boundaries for p in range(len(lengths))})
    s=config.solver
    flopy.modflow.ModflowPcg(flow, mxiter=s.flow_mxiter, iter1=s.flow_iter1, hclose=s.hclose, rclose=s.rclose)
    flopy.modflow.ModflowOc(flow, stress_period_data={
        (p, step): ['save head', 'save budget', 'print budget']
        for p,n in enumerate(steps) for step in range(n)}, compact=True)
    if not equilibrium:
        flopy.modflow.ModflowLmt(flow, output_file_name='transport.ftl', output_file_header='extended', output_file_format='unformatted')
    flow.write_input()
    return flow


def build_transport(config: Config, flow, engines):
    """Mass loading adds solute without water; discharge uses resident C."""
    s=config.solver
    mt=flopy.mt3d.Mt3dms('transport', modflowmodel=flow, model_ws=flow.model_ws,
        ftlfilename='transport.ftl', exe_name=engines.get('mt3dms'))
    _, _, por=config.arrays()
    timprs=np.linspace(0, config.duration, config.outputs)[1:]
    flopy.mt3d.Mt3dBtn(mt, prsity=por, icbund=1, sconc=initial_concentration(config),
        tunit='D', lunit='M', munit='G', nprs=len(timprs), timprs=timprs,
        savucn=True, chkmas=True, nprmas=1, dt0=s.dt0, mxstrn=s.mxstrn,
        ttsmult=s.ttsmult, ttsmax=s.ttsmax)
    mixelm,nadvfd=METHODS[config.method]
    advkeys=('percel','mxpart','itrack','wd','dceps','nplane','npl','nph','npmin','npmax','nlsink','npsink','dchmoc')
    adv=flopy.mt3d.Mt3dAdv(mt,mixelm=mixelm,nadvfd=nadvfd,**{key:getattr(s,key) for key in advkeys})
    # FloPy constructor fixes this to 1; assign the validated supported control explicitly.
    adv.interp=s.interp
    flopy.mt3d.Mt3dDsp(mt, al=config.al if config.dispersion else 0., trpt=config.trpt,
        trpv=config.trpv, dmcoef=config.dmcoef if config.dispersion else 0.)
    cells=config.source_cells()
    poreweights=np.array([por[cell] for cell in cells]);poreweights/=poreweights.sum()
    clean=[(k,i,j,0.,1) for k in range(config.nlay) for i in range(config.nrow) for j in (0,config.ncol-1)]
    ssm={}
    for p in range(flow.dis.nper):
        active=config.source_kind=='continuous' or (config.source_kind=='pulse' and p==0)
        # Explicit zero loading prevents MT3D stress-period reuse after switch-off.
        loading=[(*cell,float(config.mass_rate*w if active else 0.),15) for cell,w in zip(cells,poreweights)]
        ssm[p]=clean+loading
    flopy.mt3d.Mt3dSsm(mt,stress_period_data=ssm,mxss=len(clean)+len(cells))
    gcgkeys=('mxiter','iter1','isolve','ncrs','accl','cclose','iprgcg')
    flopy.mt3d.Mt3dGcg(mt,**{key:getattr(s,key) for key in gcgkeys})
    mt.write_input()
    return mt


def _tail(path, limit=6000):
    path=Path(path)
    if not path.exists():return ''
    with path.open('rb') as f:
        f.seek(0,2); f.seek(max(0,f.tell()-limit));return f.read().decode(errors='replace')


def execute(exe, input_file, folder, timeout, kind):
    """Run one native executable with bounded wall time and disk-backed logs."""
    folder=Path(folder); log=folder/(kind+'.log')
    start=perf_counter()
    try:
        with log.open('wb') as output:
            process=subprocess.run([str(exe),str(input_file)],cwd=folder,stdin=subprocess.DEVNULL,
                stdout=output,stderr=subprocess.STDOUT,timeout=timeout,check=False)
    except (OSError,subprocess.TimeoutExpired) as exc:
        raise RunError(f'{kind} failed: {exc}\n{_tail(log)}') from exc
    elapsed=perf_counter()-start
    marker=r'\bnormal termination\b' if kind=='flow' else r'\b(program completed|normal termination)\b'
    if process.returncode or not re.search(marker,_tail(log),re.I):
        raise RunError(f'{kind} did not finish successfully (exit {process.returncode}).\n{_tail(log)}\n{_tail(folder/(kind+".list"))}')
    return elapsed


def _read_flow(folder):
    folder=Path(folder)
    with flopy.utils.HeadFile(folder/'flow.hds', precision='auto') as h:
        heads=h.get_data().copy()
    if not np.isfinite(heads).all() or np.any(np.abs(heads)>1e20):
        raise RunError('MODFLOW returned invalid heads.')
    text=(folder/'flow.list').read_text(errors='replace')
    values=re.findall(r'PERCENT DISCREPANCY\s*=\s*([-+0-9.EeDd]+)',text,re.I)
    if not values:raise RunError('MODFLOW water-budget discrepancy was not written.')
    discrepancies=[float(v.replace('D','E').replace('d','e')) for v in values]
    # Last printed value is final time-step budget discrepancy; also expose maximum.
    return heads,discrepancies[-1],max(abs(v) for v in discrepancies)


def _read_transport(folder, config):
    folder=Path(folder)
    try:
        with flopy.utils.UcnFile(folder/'MT3D001.UCN',precision='auto') as f:
            times=np.asarray(f.get_times(),float)
            concentration=f.get_alldata().copy()
        mas=np.atleast_1d(flopy.mt3d.Mt3dms.load_mas(str(folder/'MT3D001.MAS')))
    except Exception as exc:
        raise RunError(f'Unable to read MT3DMS results: {exc}\n{_tail(folder/"transport.list")}') from exc
    tol=max(1e-4,config.duration*2e-6)
    if (not len(times) or not np.isclose(times[-1],config.duration,rtol=0,atol=tol)
        or np.any(np.diff(times)<=0) or not np.isfinite(times).all()
        or concentration.shape!=(len(times),*config.shape) or not np.isfinite(concentration).all()
        or np.any(np.abs(concentration)>1e20)):
        raise RunError('MT3DMS returned incomplete or invalid concentration output.')
    if not len(mas) or not np.isclose(mas['time'][-1],config.duration,rtol=0,atol=max(.1,tol)):
        raise RunError('MT3DMS mass output did not reach the requested end time.')
    if not np.isfinite(mas['error_in-out'][-1]):raise RunError('MT3DMS final mass discrepancy is invalid.')
    if times[0]>0:
        times=np.r_[0.,times]
        concentration=np.concatenate([initial_concentration(config)[None,...],concentration])
    times[-1]=config.duration
    return times,concentration,pd.DataFrame(mas)


@dataclass
class Run:
    config: Config
    times: np.ndarray
    concentration: np.ndarray
    heads: np.ndarray
    mass: pd.DataFrame
    metrics: dict
    warnings: list
    workspace: Path
    flowmodel: object = field(default=None,repr=False)
    particles: object = None

    def snapshot(self,time):
        """Return a field linearly interpolated between saved times (no clipping)."""
        time=float(np.clip(time,self.times[0],self.times[-1]))
        i=int(np.searchsorted(self.times,time))
        if i==0:return self.concentration[0]
        if i==len(self.times):return self.concentration[-1]
        if self.times[i]==time:return self.concentration[i]
        w=(time-self.times[i-1])/(self.times[i]-self.times[i-1])
        return self.concentration[i-1]*(1-w)+self.concentration[i]*w

    def breakthrough(self,x,y,z):
        """Return concentration in the containing model cell, explicitly no interpolation."""
        return self.concentration[(slice(None),*self.config.cell(x,y,z))]


def run_case(config: Config, engines=None, workdir=None):
    """Run flow, transport and optional MODPATH; retain all inputs/logs for export."""
    config=copy.deepcopy(config);config.validate()
    engines=find_engines() if engines is None else dict(engines)
    if not all(engines.get(k) for k in ('mf2005','mt3dms')):
        raise RunError('MODFLOW-2005 and MT3DMS executables are required; use setup_executables.py or place them in bin/.')
    folder=Path(workdir) if workdir else Path(tempfile.mkdtemp(prefix='mt3d_2d_lab_'))
    folder.mkdir(parents=True,exist_ok=True)
    if any(folder.glob('flow.*')):
        raise RunError('Use a fresh run folder to avoid mixing new and previous engine output.')
    start=perf_counter();flowtime=0.;heads0=None
    if config.transient:
        eq=build_flow(config,folder/'equilibrium',engines,equilibrium=True)
        flowtime+=execute(engines['mf2005'],eq.namefile,Path(eq.model_ws),config.solver.timeout,'flow')
        heads0,_,_=_read_flow(eq.model_ws)
    flow=build_flow(config,folder,engines,initial_heads=heads0)
    build_transport(config,flow,engines)
    flowtime+=execute(engines['mf2005'],flow.namefile,folder,config.solver.timeout,'flow')
    heads,flowerror,flowmax=_read_flow(folder)
    if not (folder/'transport.ftl').exists():raise RunError('MODFLOW did not create the LMT transport link.')
    transporttime=execute(engines['mt3dms'],'transport.nam',folder,config.solver.timeout,'transport')
    times,concentration,mass=_read_transport(folder,config)
    por=config.arrays()[2];volume=config.dx*config.dy*config.dz
    final=concentration[-1];peak=float(np.max(final));cmin=float(np.min(concentration));cmax=float(np.max(concentration))
    expected=(config.source_mass if config.source_kind=='dirac' else config.mass_rate*(config.pulse_duration if config.source_kind=='pulse' else config.duration))
    metrics={
        'flow_runtime_s':flowtime,'transport_runtime_s':transporttime,
        'total_runtime_s':perf_counter()-start,'flow_discrepancy_pct':flowerror,
        'flow_max_discrepancy_pct':flowmax,
        'mass_discrepancy_pct':float(mass['error_in-out'].iloc[-1]),
        'mass_alt_discrepancy_pct':float(mass['error_alt'].iloc[-1]),
        'mass_input_g':expected,'mass_aqueous_g':float(np.sum(final*por)*volume),
        'mass_reported_g':float(mass['total_mass'].iloc[-1]),
        'mass_sources_g':float(mass['sources'].iloc[-1]),
        'mass_sinks_g':float(mass['sinks'].iloc[-1]),
        'mass_fluid_storage_g':float(mass['fluid_storage'].iloc[-1]),
        'concentration_min':cmin,'concentration_max':cmax,'transport_steps':len(mass),
        'negative_cells':int(np.sum(final< -max(1e-12,cmax*1e-7))),
        'cells':int(np.prod(config.shape)),
    }
    warnings=[]
    if abs(metrics['mass_discrepancy_pct'])>1:warnings.append('MT3DMS final mass discrepancy exceeds 1%; inspect method and transport time step settings.')
    if flowmax>.1:warnings.append('At least one MODFLOW water-budget discrepancy exceeds 0.1%.')
    if cmin< -max(1e-10,cmax*1e-6):warnings.append('Negative concentrations occurred. They are retained in diagnostics and exports; central FD and particle methods can oscillate.')
    edge=float(np.max(np.abs(final[:,:,[0,-1]])))
    if peak>0 and edge/peak>.005:warnings.append('The plume reaches an x specified-head boundary; enlarge the domain before treating the infinite-x analytical solution as a benchmark.')
    if config.transient:warnings.append('Storage is active in the transient flow calculation; no uniform steady-flow analytical benchmark is claimed.')
    elif config.zones and any(z.ss!=config.ss for z in config.zones):warnings.append('Specific storage is assigned to zones but has no effect during steady flow.')
    run=Run(config,times,concentration,heads,mass,metrics,warnings,folder,flow)
    if config.track_particles:
        if not engines.get('mp7'):
            warnings.append('MODPATH 7 executable is unavailable; transport results are complete but particle tracking was not run.')
        else:
            try:
                from .particles import run_particles
                run.particles=run_particles(config,flow,engines['mp7'],workspace=folder/'particles')
                run.warnings.extend(run.particles.warnings)
                metrics['particle_runtime_s']=run.particles.metrics['runtime_s']
            except Exception as exc:
                warnings.append(f'MODPATH failed; the completed MT3DMS result is retained. Details: {exc}')
    metrics['total_runtime_s']=perf_counter()-start
    return run
