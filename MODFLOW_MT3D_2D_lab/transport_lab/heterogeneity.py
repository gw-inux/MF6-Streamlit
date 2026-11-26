"""Reproducible material samples on a physical lattice, independent of the grid.

Each physical unit has independent K, Ss and porosity samples. Cell centres
sample this fixed field; numerical refinement never draws a new realisation.
This is a teaching random pattern, not a covariance-calibrated random field.
"""
from dataclasses import dataclass
import numpy as np


@dataclass
class RandomField:
    seed: int = 42
    unit_x: float = 1200. / 81
    unit_y: float = 400. / 41
    k_min: float = .864
    k_max: float = 86.4
    ss_min: float = 1e-5
    ss_max: float = 1e-3
    por_min: float = .3
    por_max: float = .3

    def validate(self):
        if isinstance(self.seed,(bool,np.bool_)) or not isinstance(self.seed,(int,np.integer)) or not 0<=self.seed<2**31:
            raise ValueError('Random seed must be an integer between 0 and 2147483647.')
        names=('unit_x','unit_y','k_min','k_max','ss_min','ss_max','por_min','por_max')
        if any(isinstance(getattr(self,n),(bool,np.bool_)) or not isinstance(getattr(self,n),(int,float,np.integer,np.floating)) or not np.isfinite(getattr(self,n)) or getattr(self,n)<=0 for n in names):
            raise ValueError('Random-field sizes and bounds must be finite and positive.')
        if self.unit_x<.01 or self.unit_y<.01:raise ValueError('Random units must be at least 0.01 m wide.')
        if any(lo>hi for lo,hi in ((self.k_min,self.k_max),(self.ss_min,self.ss_max),(self.por_min,self.por_max))):
            raise ValueError('Random-field minima must not exceed maxima.')
        if self.por_max>=1:raise ValueError('Random-field porosity must be below one.')


def _uniform(ix,iy,seed,stream):
    # SplitMix64 permutation of physical lattice addresses. All integer overflow
    # is deliberate modulo 2**64. No enormous auxiliary lattice is allocated.
    with np.errstate(over='ignore'):
        z=(ix*np.uint64(0x9E3779B97F4A7C15)) ^ (iy*np.uint64(0xD1B54A32D192ED03))
        z=z+np.uint64(seed)+np.uint64(stream)*np.uint64(0x94D049BB133111EB)
        z=(z^(z>>np.uint64(30)))*np.uint64(0xBF58476D1CE4E5B9)
        z=(z^(z>>np.uint64(27)))*np.uint64(0x94D049BB133111EB)
        z=z^(z>>np.uint64(31))
    return (z>>np.uint64(11)).astype(np.float64)*(1./2**53)


def sample_field(field,x,y):
    field.validate()
    ix=np.floor(np.asarray(x,dtype=float)[None,:]/field.unit_x).astype(np.uint64)
    iy=np.floor(np.asarray(y,dtype=float)[:,None]/field.unit_y).astype(np.uint64)
    def draw(lo,hi,stream,log):
        u=_uniform(ix,iy,field.seed,stream)
        a=np.exp(np.log(lo)+u*(np.log(hi)-np.log(lo))) if log else lo+u*(hi-lo)
        return np.clip(a,lo,hi)
    return (draw(field.k_min,field.k_max,1,True),draw(field.ss_min,field.ss_max,2,True),draw(field.por_min,field.por_max,3,False))
