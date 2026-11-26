"""Validated model configuration. Internal units: metre, day, gram."""
from dataclasses import dataclass, field, asdict
import hashlib
import json
import numpy as np
from .heterogeneity import RandomField, sample_field

METHODS = {'FD upstream': (0, 0), 'FD central': (0, 2), 'TVD': (-1, 0),
           'MOC': (1, 0), 'MMOC': (2, 0), 'HMOC': (3, 0)}

@dataclass
class Zone:
    name: str = 'Low K lens'
    x0: float = 400.
    x1: float = 650.
    y0: float = 140.
    y1: float = 260.
    first_layer: int = 0
    last_layer: int = 0
    k: float = 0.0864
    ss: float = 1e-4
    porosity: float = 0.3

@dataclass
class Solver:
    percel: float = 0.75
    mxpart: int = 800000
    itrack: int = 3
    wd: float = 0.5
    dceps: float = 1e-5
    nplane: int = 1
    npl: int = 4
    nph: int = 16
    npmin: int = 2
    npmax: int = 32
    interp: int = 1
    nlsink: int = 0
    npsink: int = 16
    dchmoc: float = 1e-4
    mxiter: int = 1
    iter1: int = 100
    isolve: int = 3
    ncrs: int = 0
    accl: float = 1.0
    cclose: float = 1e-6
    iprgcg: int = 0
    dt0: float = 0.
    mxstrn: int = 50000
    ttsmult: float = 1.
    ttsmax: float = 0.
    hclose: float = 1e-7
    rclose: float = 1e-5
    flow_mxiter: int = 100
    flow_iter1: int = 100
    timeout: int = 180

@dataclass
class Config:
    length: float = 1200.
    width: float = 400.
    thickness: float = 20.
    ncol: int = 81
    nrow: int = 41
    nlay: int = 1
    k: float = 8.64
    kv_ratio: float = 1.
    ss: float = 1e-4
    porosity: float = 0.3
    head_left: float = 42.
    head_right: float = 30.
    transient: bool = False
    head_right_final: float = 32.
    flow_steps: int = 60
    duration: float = 600.
    outputs: int = 31
    source_kind: str = 'pulse'
    source_mass: float = 5000.
    mass_rate: float = 100.
    pulse_duration: float = 60.
    src_x: float = 250.
    src_y: float = 200.
    src_layer: int = 0
    source_all_layers: bool = True
    src_ncol: int = 1
    src_nrow: int = 1
    dispersion: bool = True
    al: float = 10.
    trpt: float = 0.1
    trpv: float = 0.01
    dmcoef: float = 0.
    method: str = 'TVD'
    zones: list[Zone] = field(default_factory=list)
    random_field: RandomField | None = None
    solver: Solver = field(default_factory=Solver)
    track_particles: bool = True
    particles_per_cell: int = 16
    release_groups: int = 12
    observations: list = field(default_factory=lambda: [(400., 200., 10.)])

    @property
    def dx(self): return self.length / self.ncol
    @property
    def dy(self): return self.width / self.nrow
    @property
    def dz(self): return self.thickness / self.nlay
    @property
    def x_edges(self): return np.linspace(0, self.length, self.ncol + 1)
    @property
    def y_edges(self): return np.linspace(self.width, 0, self.nrow + 1)
    @property
    def z_edges(self): return np.linspace(self.thickness, 0, self.nlay + 1)
    @property
    def velocity(self): return self.k*(self.head_left-self.head_right)/((self.ncol-1)*self.dx)/self.porosity
    @property
    def shape(self): return (self.nlay, self.nrow, self.ncol)

    def cell(self, x, y, z):
        return (min(self.nlay-1,max(0,int((self.thickness-z)/self.dz))),
                min(self.nrow-1,max(0,int((self.width-y)/self.dy))),
                min(self.ncol-1,max(0,int(x/self.dx))))

    def source_cells(self):
        _,i,j=self.cell(self.src_x,self.src_y,self.thickness/2)
        j0=j-self.src_ncol//2; i0=i-self.src_nrow//2
        layers=range(self.nlay) if self.source_all_layers else [self.src_layer]
        return [(k,ii,jj) for k in layers for ii in range(i0,i0+self.src_nrow) for jj in range(j0,j0+self.src_ncol)]

    def source_bounds(self):
        cells=np.asarray(self.source_cells()); lo=cells.min(axis=0); hi=cells.max(axis=0)
        return ((lo[2]*self.dx,(hi[2]+1)*self.dx),
                (self.width-(hi[1]+1)*self.dy,self.width-lo[1]*self.dy),
                (self.thickness-(hi[0]+1)*self.dz,self.thickness-lo[0]*self.dz))

    @property
    def heterogeneous(self):return bool(self.zones) or self.random_field is not None

    def arrays(self):
        hk=np.full(self.shape,self.k,dtype=float); ss=np.full(self.shape,self.ss,dtype=float); por=np.full(self.shape,self.porosity,dtype=float)
        xc=(self.x_edges[:-1]+self.x_edges[1:])/2; yc=(self.y_edges[:-1]+self.y_edges[1:])/2
        if self.random_field is not None:
            a,b,c=sample_field(self.random_field,xc,yc)
            hk[:]=a;ss[:]=b;por[:]=c
        for z in self.zones:
            mask=((xc[None,:]>=z.x0)&(xc[None,:]<=z.x1)&(yc[:,None]>=z.y0)&(yc[:,None]<=z.y1))
            for k in range(z.first_layer,z.last_layer+1):
                hk[k][mask]=z.k;ss[k][mask]=z.ss;por[k][mask]=z.porosity
        return hk,ss,por

    def validate(self):
        errors=[]
        if self.random_field is not None:
            if not isinstance(self.random_field,RandomField):raise ValueError('Invalid random-field configuration.')
            self.random_field.validate()
        def finite(value):
            try:
                return isinstance(value, (int, float, np.integer, np.floating)) and not isinstance(value, (bool, np.bool_)) and bool(np.isfinite(value))
            except (TypeError, ValueError):
                return False
        def integer(value):
            return isinstance(value, (int, np.integer)) and not isinstance(value, (bool, np.bool_))
        # Reject malformed imported settings before using them for array dimensions.
        counts={'ncol':5,'nrow':3,'nlay':1,'flow_steps':1,'outputs':2,
                'src_ncol':1,'src_nrow':1,'src_layer':0,
                'particles_per_cell':1,'release_groups':1}
        for name, minimum in counts.items():
            value=getattr(self,name)
            if not integer(value) or value<minimum:
                errors.append(f'{name} must be an integer of at least {minimum}.')
        numeric=('length','width','thickness','k','kv_ratio','ss','porosity',
                 'head_left','head_right','head_right_final','duration','source_mass',
                 'mass_rate','pulse_duration','src_x','src_y','al','trpt','trpv','dmcoef')
        for name in numeric:
            if not finite(getattr(self,name)):errors.append(f'{name} must be finite.')
        s=self.solver
        for name,value in vars(s).items():
            if not finite(value):errors.append(f'Solver {name} must be finite.')
        int_solver=('mxpart','itrack','nplane','npl','nph','npmin','npmax','interp',
                    'nlsink','npsink','mxiter','iter1','isolve','ncrs','iprgcg',
                    'mxstrn','flow_mxiter','flow_iter1','timeout')
        for name in int_solver:
            if not integer(getattr(s,name)):errors.append(f'Solver {name} must be an integer.')
        if errors:raise ValueError('\n'.join(dict.fromkeys(errors)))
        for name in ('length','width','thickness','k','kv_ratio','ss','duration','source_mass','mass_rate'):
            if getattr(self,name)<=0:errors.append(f'{name} must be positive.')
        if errors:raise ValueError('\n'.join(dict.fromkeys(errors)))
        if self.ncol*self.nrow*self.nlay*(self.outputs+1)>20_000_000:
            raise ValueError('Reduce cells or saved times (20 million concentration values maximum).')
        if self.src_ncol>self.ncol or self.src_nrow>self.nrow:
            raise ValueError('Source cell counts must not exceed the grid dimensions.')
        if not 0<self.porosity<1:errors.append('Porosity must be between 0 and 1.')
        if self.head_left<=self.head_right:errors.append('Left specified head must exceed the original right head.')
        if min(self.head_left,self.head_right,self.head_right_final if self.transient else self.head_right)<self.thickness:errors.append('This confined lab requires heads at or above aquifer top.')
        if self.source_kind not in ('dirac','pulse','continuous'):errors.append('Unknown input signal.')
        if self.source_kind=='pulse' and not 0<self.pulse_duration<self.duration:errors.append('Pulse duration must be between zero and model duration.')
        if not 0<=self.src_layer<self.nlay:errors.append('Source layer is outside the grid.')
        if not(0<=self.src_x<=self.length and 0<=self.src_y<=self.width):errors.append('Source coordinates must lie inside the domain.')
        if any(k<0 or k>=self.nlay or i<0 or i>=self.nrow or j<1 or j>=self.ncol-1 for k,i,j in self.source_cells()):errors.append('Source must lie inside the grid, excluding specified-head columns.')
        if self.method not in METHODS:errors.append('Unknown advection method.')
        if min(self.al,self.trpt,self.trpv,self.dmcoef)<0:errors.append('Dispersion parameters must be nonnegative.')
        if not 1<=len(self.observations)<=5:errors.append('Choose one to five observation points.')
        for obs in self.observations:
            if not isinstance(obs,(tuple,list,np.ndarray)) or len(obs)!=3 or not all(finite(v) for v in obs):
                errors.append('Each observation requires three finite x, y, z coordinates.');continue
            x,y,z=obs
            if not(0<=x<=self.length and 0<=y<=self.width and 0<=z<=self.thickness):errors.append('Observation point is outside the model.')
        xc=(self.x_edges[:-1]+self.x_edges[1:])/2
        yc=(self.y_edges[:-1]+self.y_edges[1:])/2
        for z in self.zones:
            if not isinstance(z,Zone):errors.append('Each material zone must use the Zone configuration.');continue
            if not all(finite(v) for v in (z.x0,z.x1,z.y0,z.y1,z.k,z.ss,z.porosity)):
                errors.append(f'Zone {z.name}: every material parameter and extent must be finite.');continue
            if not(integer(z.first_layer) and integer(z.last_layer)):
                errors.append(f'Zone {z.name}: layer indices must be integers.');continue
            if not(0<=z.x0<z.x1<=self.length and 0<=z.y0<z.y1<=self.width and 0<=z.first_layer<=z.last_layer<self.nlay):errors.append(f'Zone {z.name}: invalid extent.')
            if z.k<=0 or z.ss<=0 or not 0<z.porosity<1:errors.append(f'Zone {z.name}: invalid material parameters.')
            if not np.any((xc>=z.x0)&(xc<=z.x1)) or not np.any((yc>=z.y0)&(yc<=z.y1)):
                errors.append(f'Zone {z.name}: extent contains no cell centres; enlarge it or refine the grid.')
        if s.percel<=0 or s.cclose<=0 or s.hclose<=0 or s.rclose<=0 or s.dt0<0 or s.ttsmax<0 or s.ttsmult<1:errors.append('Invalid solver tolerance/time stepping setting.')
        if self.method=='TVD' and s.percel>1:errors.append('TVD requires PERCEL no greater than 1.')
        if s.itrack not in (1,2,3) or s.isolve not in (1,2,3) or s.ncrs not in (0,1) or s.interp!=1:errors.append('Invalid solver option.')
        if not .5<=s.wd<=1:errors.append('WD concentration weighting must be between 0.5 and 1.')
        if s.npmin>s.npmax or s.npl>s.nph:errors.append('Minimum particle counts must not exceed maximum counts.')
        for name in ('mxpart','nph','npmax','npsink','mxiter','iter1','mxstrn','flow_mxiter','flow_iter1','timeout'):
            if getattr(s,name)<1:errors.append(f'Solver {name} must be positive.')
        for name in ('nplane','npl','npmin','nlsink','iprgcg'):
            if getattr(s,name)<0:errors.append(f'Solver {name} must be nonnegative.')
        if s.accl<=0 or s.dceps<0 or s.dchmoc<0:errors.append('Invalid relaxation or characteristic gradient threshold.')
        if np.prod(self.shape)*(self.outputs+1)>20_000_000:errors.append('Reduce cells or saved times (20 million concentration values maximum).')
        groups=1 if self.source_kind=='dirac' else self.release_groups
        if self.track_particles and len(self.source_cells())*self.particles_per_cell*groups>100000:errors.append('Reduce source size, particles per cell or release batches (100,000 MODPATH particles maximum).')
        if errors:raise ValueError('\n'.join(dict.fromkeys(errors)))

    def fingerprint(self):
        d=asdict(self)
        for key in ('method','solver','observations','track_particles','particles_per_cell','release_groups'):d.pop(key,None)
        return hashlib.sha256(json.dumps(d,sort_keys=True).encode()).hexdigest()[:12]

    def to_dict(self):return asdict(self)

    @classmethod
    def from_dict(cls,d):
        d=dict(d);d['solver']=Solver(**d.get('solver',{}));d['zones']=[Zone(**x) for x in d.get('zones',[])]
        if d.get('random_field') is not None:d['random_field']=RandomField(**d['random_field'])
        return cls(**d)
