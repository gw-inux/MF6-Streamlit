"""Deterministic teaching presets and grid-independent stochastic rectangles."""
from __future__ import annotations
import numpy as np
from .config import Zone

PRESETS=('homogeneous','random','lens','channel','barrier')


def rectangular_partition(length,width,count,seed=42):
    """Exactly count nonoverlapping rectangles covering the full xy domain.

    Recursively split the largest block near its midpoint along its longer
    relative dimension. Geometry depends on physical extent and seed, never on
    cell counts, so discretization changes preserve the geological realisation.
    """
    if not isinstance(count,(int,np.integer)) or not 1<=count<=100:
        raise ValueError('Use 1–100 stochastic zones.')
    if length<=0 or width<=0:raise ValueError('Domain dimensions must be positive.')
    rng=np.random.default_rng(seed);boxes=[(0.,float(length),0.,float(width))]
    while len(boxes)<count:
        idx=max(range(len(boxes)),key=lambda i:(boxes[i][1]-boxes[i][0])*(boxes[i][3]-boxes[i][2]))
        x0,x1,y0,y1=boxes.pop(idx)
        # Normalisation yields several zones across both domain dimensions.
        along_x=(x1-x0)/length >= (y1-y0)/width
        f=rng.uniform(.4,.6)
        if along_x:
            cut=x0+f*(x1-x0);boxes.extend([(x0,cut,y0,y1),(cut,x1,y0,y1)])
        else:
            cut=y0+f*(y1-y0);boxes.extend([(x0,x1,y0,cut),(x0,x1,cut,y1)])
    return sorted(boxes)


def make_zones(config,preset='homogeneous',*,count=15,seed=42,k_bounds=None,ss_bounds=None,por_bounds=None):
    c=config;L,W=c.length,c.width
    def zone(name,x0,x1,y0,y1,k,ss=None,por=None):
        return Zone(name,x0,x1,y0,y1,0,c.nlay-1,k,c.ss if ss is None else ss,c.porosity if por is None else por)
    if preset=='homogeneous':return []
    if preset=='lens':return [zone('Low K lens',L*.34,L*.56,W*.32,W*.68,c.k*.01)]
    if preset=='channel':return [zone('High K channel',0,L,W*.4,W*.6,c.k*10)]
    if preset=='barrier':return [zone('Low K barrier',L*.45,L*.53,0,W*.8,c.k*.01)]
    if preset!='stochastic':raise ValueError('Unknown zonation preset.')
    kb=k_bounds or (c.k*.1,c.k*10);sb=ss_bounds or (c.ss*.1,c.ss*10);pb=por_bounds or (c.porosity,c.porosity)
    for bounds in (kb,sb,pb):
        if len(bounds)!=2 or not np.isfinite(bounds).all() or not 0<bounds[0]<=bounds[1]:raise ValueError('Zone parameter ranges must be finite, positive and increasing.')
    if pb[1]>=1:raise ValueError('Zone porosity must be below 1.')
    boxes=rectangular_partition(L,W,count,seed)
    # Separate streams keep geometry and material samples independently reproducible.
    rng=np.random.default_rng(np.random.SeedSequence([int(seed),781]))
    kvals=np.exp(rng.uniform(np.log(kb[0]),np.log(kb[1]),count))
    ssvals=np.exp(rng.uniform(np.log(sb[0]),np.log(sb[1]),count))
    pors=rng.uniform(pb[0],pb[1],count)
    return [zone(f'Z{i+1:02d}',*box,float(k),float(ss),float(por)) for i,(box,k,ss,por) in enumerate(zip(boxes,kvals,ssvals,pors))]
