"""Comparison metrics and reproducible result exports."""
from __future__ import annotations
import io
import json
from pathlib import Path
import zipfile
import numpy as np
import pandas as pd
from .analytical import reference_concentration, boundary_diagnostics


def analytical_reference(c, t):
    if c.heterogeneous or c.transient:
        return None, {'accuracy_eligible':False,'message':'Analytical reference requires homogeneous steady flow.'}
    v=c.velocity
    disp=(v*c.al+c.dmcoef,v*c.al*c.trpt+c.dmcoef,v*c.al*c.trpv+c.dmcoef) if c.dispersion else (0.,0.,0.)
    kw=dict(time=float(t),source_kind=c.source_kind,source_mass=c.source_mass,mass_rate=c.mass_rate,pulse_duration=c.pulse_duration)
    ref=reference_concentration(c.x_edges,c.y_edges,c.z_edges,velocity=v,dispersion=disp,porosity=c.porosity,source_bounds=c.source_bounds(),**kw)
    info=boundary_diagnostics(ref,c.x_edges,c.y_edges,c.z_edges,porosity=c.porosity,velocity=v,dispersion=disp,source_bounds=c.source_bounds(),boundary_positions=(c.dx/2,c.length-c.dx/2),**kw)
    return ref,info


def enrich(run):
    c=run.config
    ref,info=analytical_reference(c,run.times[-1])
    run.reference_info=info
    run.final_reference=ref
    pv=c.arrays()[2]*c.dx*c.dy*c.dz
    conc=run.concentration[-1]
    mass=float(np.sum(conc*pv))
    run.metrics['mass_grid_g']=mass
    run.metrics['negative_mass_g']=float(-np.sum(np.minimum(conc,0)*pv))
    run.metrics['l1_reference_pct']=float(100*np.sum(np.abs(conc-ref)*pv)/np.sum(ref*pv)) if ref is not None and info['accuracy_eligible'] and np.sum(ref*pv)>0 else np.nan
    pos=np.maximum(conc,0)*pv
    xc=(c.x_edges[:-1]+c.x_edges[1:])/2
    run.metrics['centroid_x_m']=float(np.sum(pos*xc[None,None,:])/np.sum(pos)) if np.sum(pos)>0 else np.nan
    if not info['accuracy_eligible'] and info['message'] not in run.warnings:run.warnings.append(info['message'])
    return run


def summary_table(entries):
    rows=[]
    for label,r in entries:
        c=r.config;m=r.metrics
        bounds=c.source_bounds();size=' × '.join(f'{b-a:.2f}' for a,b in bounds)
        rows.append({'Run':label,'Method':c.method,'Signal':c.source_kind,'Grid (x × y × z)':f'{c.ncol} × {c.nrow} × {c.nlay}',
                     'Active cells':int(np.prod(c.shape)),'K zones':len(c.zones),'Random field':c.random_field is not None,'Flow':'transient' if c.transient else 'steady',
                     'MT3D MB discrepancy (%)':m.get('mass_discrepancy_pct'),
                     'Flow WB discrepancy (%)':m.get('flow_discrepancy_pct'),
                     'MT3D runtime (s)':m.get('transport_runtime_s'),'MODPATH runtime (s)':m.get('particle_runtime_s',m.get('modpath_runtime_s')),
                     'Flow runtime (s)':m.get('flow_runtime_s'),'Total runtime (s)':m.get('total_runtime_s'),
                     'Reference L1 error (%)':m.get('l1_reference_pct'),'Final dissolved mass (g)':m.get('mass_grid_g'),'Released mass (g)':m.get('mass_input_g'),
                     'Minimum C (g/m³)':m.get('concentration_min'),'Negative mass (g)':m.get('negative_mass_g'),
                     'Centroid x (m)':m.get('centroid_x_m'),'Transport steps':m.get('transport_steps'),
                     'Source box (m)':size,'PERCEL':c.solver.percel,'CCLOSE':c.solver.cclose,'End time (d)':float(r.times[-1]),
                     'Scenario':c.fingerprint()})
    return pd.DataFrame(rows)


def observation_table(entries,observations):
    rows=[]
    for label,r in entries:
        c=r.config
        for p,(x,y,z) in enumerate(observations,1):
            if not(0<=x<=c.length and 0<=y<=c.width and 0<=z<=c.thickness):continue
            k,i,j=c.cell(x,y,z)
            rows.append({'Run':label,'Point':f'P{p}','Requested x':x,'Requested y':y,'Requested z':z,
                         'Cell centre x':(j+.5)*c.dx,'Cell centre y':c.width-(i+.5)*c.dy,'Cell centre z':c.thickness-(k+.5)*c.dz,
                         'Layer':k+1,'Row':i+1,'Column':j+1})
    return pd.DataFrame(rows)


def breakthrough_table(entries,observations):
    rows=[]
    for label,r in entries:
        c=r.config
        for p,(x,y,z) in enumerate(observations,1):
            if not(0<=x<=c.length and 0<=y<=c.width and 0<=z<=c.thickness):continue
            k,i,j=c.cell(x,y,z)
            rows.extend({'Run':label,'Point':f'P{p}','Time (days)':float(t),'C (g/m3)':float(val)} for t,val in zip(r.times,r.concentration[:,k,i,j]))
    return pd.DataFrame(rows)


def export_run(run):
    """In-memory export generated only when explicitly requested in the app."""
    buf=io.BytesIO()
    with zipfile.ZipFile(buf,'w',zipfile.ZIP_DEFLATED) as z:
        z.writestr('configuration.json',json.dumps(run.config.to_dict(),indent=2))
        z.writestr('metrics.json',json.dumps(run.metrics,indent=2,default=lambda x:float(x)))
        z.writestr('warnings.txt','\n'.join(run.warnings))
        z.writestr('mass_balance.csv',run.mass.to_csv(index=False))
        b=io.BytesIO();np.savez_compressed(b,time_days=run.times,concentration_g_m3=run.concentration,heads_m=run.heads,x_edges=run.config.x_edges,y_edges=run.config.y_edges,z_edges=run.config.z_edges)
        z.writestr('arrays.npz',b.getvalue())
        folder=Path(run.workspace)
        if folder.exists():
            for p in folder.rglob('*'):
                if p.is_file() and p.suffix.lower() not in ('.hds','.cbc','.ftl','.ucn','.mpbin','.mppth','.mpts','.mpend') and p.stat().st_size<5_000_000:
                    z.write(p,'model_files/'+str(p.relative_to(folder)))
        p=run.particles
        if p is not None:
            for attr in ('paths','timepoints','endpoints','releases','arrivals'):
                value=getattr(p,attr,None)
                if isinstance(value,pd.DataFrame):z.writestr(f'modpath_{attr}.csv',value.to_csv(index=False))
            z.writestr('modpath_metrics.json',json.dumps(p.metrics,indent=2))
            z.writestr('modpath_warnings.txt','\n'.join(p.warnings))
    return buf.getvalue()


def reference_curve_table(config_dict,times,observations):
    """Analytical cell means at observations; omit boundary-affected times."""
    from .config import Config
    c=Config.from_dict(config_dict);rows=[]
    if c.heterogeneous or c.transient:return pd.DataFrame(columns=['Point','Time (days)','C (g/m3)'])
    for t in times:
        ref,info=analytical_reference(c,t)
        if ref is None or not info['accuracy_eligible']:continue
        for p,(x,y,z) in enumerate(observations,1):
            if 0<=x<=c.length and 0<=y<=c.width and 0<=z<=c.thickness:
                rows.append({'Point':f'P{p}','Time (days)':float(t),'C (g/m3)':float(ref[c.cell(x,y,z)])})
    return pd.DataFrame(rows,columns=['Point','Time (days)','C (g/m3)'])
