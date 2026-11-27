"""Persistent controls behind three equally sized navigation buttons."""
from contextlib import contextmanager
from dataclasses import asdict
import math
import numpy as np
import streamlit as st
from .config import Config, Solver, METHODS
from .heterogeneity import RandomField
from .zonation import PRESETS, make_zones
from .history import SHORT_METHOD


PAGE_WIDTHS={1:'750px',2:'925px',3:'1100px',4:'1400px',5:'100%'}


def _remember_page_width():
    try:width=st.session_state['page_width']
    except KeyError:return
    st.session_state['_page_width']=width


def page_width_control(t):
    # Preserve the selection even when the translated slider labels change.
    st.session_state['page_width']=st.session_state.get('_page_width',3)
    width=st.select_slider(t('Page width'),options=list(PAGE_WIDTHS),
                           format_func=lambda value:t('width_'+str(value)),
                           key='page_width',on_change=_remember_page_width,
                           help=t('page_width_hint'))
    st.session_state['_page_width']=width
    return width


def page_width_css(choice):
    return '.stApp {--lab-max-width:'+PAGE_WIDTHS.get(choice,PAGE_WIDTHS[3])+';}'


def run_label_css(label):
    background,border=('#EEF9F0','#79B88C') if label.strip() else ('#FFF7DB','#D1A12C')
    return '.st-key-run_label_panel {--label-background:'+background+';--label-border:'+border+';}'


def navigation(items,key,t):
    """items are (stable ID, translation key); all buttons have equal width."""
    valid=[k for k,_ in items]
    if st.session_state.get(key) not in valid:st.session_state[key]=valid[0]
    with st.container(key=key+'_buttons'):
        for col,(value,label) in zip(st.columns(len(items),gap='small'),items):
            col.button(t(label),key=f'{key}_{value}',width='stretch',
                       type='primary' if st.session_state[key]==value else 'secondary',
                       on_click=_select,args=(key,value))
    return st.session_state[key]


def _select(key,value):st.session_state[key]=value


@contextmanager
def panel(key,label,t,expanded=False):
    with st.container(key=key),st.expander('**'+t(label)+'**',expanded=expanded):yield


def _remember(key):
    # Ignore a queued event for a widget that no longer exists. Preserve the
    # canonical model settings instead of inventing a replacement value.
    try:v=st.session_state['_model_values'];new=st.session_state[key]
    except KeyError:return
    if key=='grid_mode' and new!=v[key]:
        if new=='width':
            v['cell_x']=v['length']/v['ncol'];v['cell_y']=v['width']/v['nrow']
            for k in ('cell_x','cell_y'):st.session_state.pop(k,None)
        else:
            v['ncol']=max(5,math.ceil(v['length']/v['cell_x']-1e-10))
            v['nrow']=max(3,math.ceil(v['width']/v['cell_y']-1e-10))
            for k in ('ncol','nrow'):st.session_state.pop(k,None)
    v[key]=new


def values():
    if '_model_values' not in st.session_state:
        c=Config();v=asdict(c);v.pop('zones');v.pop('solver');v.pop('observations')
        v.update(expert=False,sliders=False,k=c.k/86400,src_layer=1,grid_mode='count',cell_x=c.dx,cell_y=c.dy,
                 zones_preset='homogeneous',zone_seed=42,random_unit_x=c.dx,random_unit_y=c.dy,
                 zone_k_min=1e-5,zone_k_max=1e-3,zone_ss_min=1e-5,zone_ss_max=1e-3,
                 zone_por_min=.3,zone_por_max=.3,nobs=1)
        for key,value in vars(c.solver).items():v['s_'+key]=value
        for i in range(5):v.update({f'obs_x{i}':400.+100*i,f'obs_y{i}':200.,f'obs_z{i}':10.})
        st.session_state['_model_values']=v
    v=st.session_state['_model_values']
    v.setdefault('particle_count_mode','cell')
    v.setdefault('source_particle_count',None)
    v.setdefault('total_source_particles',16)
    v.setdefault('random_unit_x',v['length']/v['ncol']);v.setdefault('random_unit_y',v['width']/v['nrow'])
    if v['zones_preset'] not in PRESETS:v['zones_preset']='random' if v['zones_preset']=='stochastic' else 'homogeneous'
    return v


def widget(kind,key,label,t,**kwargs):
    v=values();default=v[key]
    # Rebind on every render: changing widget type (number input / slider)
    # creates a new Streamlit widget identity even when its key is unchanged.
    # Callbacks have already updated the canonical value before this rerun.
    st.session_state[key]=default
    # Keep a canonical copy independent of Streamlit's hidden-widget cleanup.
    fn=getattr(st,kind)
    help_key='help_'+key
    if key.startswith('obs_'):help_key='help_observation'
    if 'help' not in kwargs and help_key in t.entries:kwargs['help']=t(help_key)
    if kind in ('selectbox','radio'):
        options=kwargs['options']
        if st.session_state[key] not in options:st.session_state[key]=options[0]
    result=fn(t(label),key=key,on_change=_remember,args=(key,),**kwargs)
    v[key]=result
    return result


def number(key,label,t,lo,hi=None,step=None,sliders=False,format=None):
    options={'min_value':lo}
    if hi is not None:options['max_value']=hi
    if step is not None:options['step']=step
    if format:options['format']=format
    return widget('slider' if sliders and hi is not None else 'number_input',key,label,t,**options)


def build_config(v):
    c=Config()
    for key in vars(c):
        if key in v and key not in ('k','src_layer','solver','zones','observations'):setattr(c,key,v[key])
    c.k=v['k']*86400;c.src_layer=min(v['src_layer']-1,c.nlay-1)
    c.source_particle_count=v.get('total_source_particles',16) if v.get('particle_count_mode','cell')=='total' else None
    c.solver=Solver(**{key:v['s_'+key] for key in vars(Solver())})
    c.observations=[(v[f'obs_x{i}'],v[f'obs_y{i}'],v[f'obs_z{i}']) for i in range(v['nobs'])]
    if v['grid_mode']=='width':
        # Preserve physical extent. Requested width is a maximum; edge cells
        # are not truncated and the resulting uniform width is shown explicitly.
        c.ncol=max(5,math.ceil(c.length/v['cell_x']-1e-10))
        c.nrow=max(3,math.ceil(c.width/v['cell_y']-1e-10))
    # The teaching interface is steady; legacy JSON/CLI transient cases remain supported.
    c.transient=False
    if v['zones_preset']=='random':
        c.zones=[]
        c.random_field=RandomField(seed=v['zone_seed'],unit_x=v['random_unit_x'],unit_y=v['random_unit_y'],
            k_min=v['zone_k_min']*86400,k_max=v['zone_k_max']*86400,
            ss_min=v['zone_ss_min'],ss_max=v['zone_ss_max'],por_min=v['zone_por_min'],por_max=v['zone_por_max'])
    else:
        c.random_field=None;c.zones=make_zones(c,v['zones_preset'])
    return c


def _flow(t,v):
    cols=st.columns(3,gap='medium')
    with cols[0]:
        with panel('spatial_panel','Model extent and spatial discretization',t,True):
            number('length','Model length in x-direction (m)',t,100.,10000.,50.,sliders=v['sliders'])
            number('width','Model width in y-direction (m)',t,50.,5000.,25.,sliders=v['sliders'])
            number('thickness','Aquifer thickness / top elevation (m)',t,1.,500.,1.,sliders=v['sliders'])
            mode=widget('radio','grid_mode','Define the grid by',t,options=['count','width'],format_func=lambda x:t('Number of cells' if x=='count' else 'Cell width'),horizontal=True)
            a,b=st.columns(2)
            if mode=='count':
                with a:number('ncol','Cells x',t,5,max(501,v['ncol']),2,sliders=v['sliders'])
                with b:number('nrow','Cells y',t,3,max(301,v['nrow']),2,sliders=v['sliders'])
            else:
                with a:number('cell_x','Cell width x (m)',t,.1,2000.,1.)
                with b:number('cell_y','Cell width y (m)',t,.1,2000.,1.)
            if v['expert'] or v['nlay']>1:number('nlay','Number of layers',t,1,31,1)
    with cols[1]:
        with panel('scenario_panel','Hydraulic properties',t,True):
            number('k','Hydraulic conductivity K (m/s)',t,1e-9,1.,format='%.2e')
            number('porosity','Effective porosity (-)',t,.01,.8,.01)
            number('ss','Specific storage Ss (1/m)',t,1e-9,.1,format='%.2e')
            if v['expert']:number('kv_ratio','Vertical / horizontal K',t,.001,100.,.1)
        with panel('complexity_panel','Hydrogeology and zonation',t,True):
            widget('selectbox','zones_preset','Hydrogeology preset',t,options=list(PRESETS),format_func=lambda x:t('preset_'+x))
            if v['zones_preset']=='random':
                number('zone_seed','Random seed',t,0,2**31-1,1)
                a,b=st.columns(2)
                with a:number('random_unit_x','Random unit x (m)',t,.01,10000.,1.,format='%.3f')
                with b:number('random_unit_y','Random unit y (m)',t,.01,5000.,1.,format='%.3f')
                for left,right,label in [('zone_k_min','zone_k_max','K range (m/s)'),('zone_ss_min','zone_ss_max','Ss range (1/m)'),('zone_por_min','zone_por_max','Porosity range (-)')]:
                    st.markdown(t(label));a,b=st.columns(2)
                    with a:number(left,'Minimum',t,1e-9,.99 if left=='zone_por_min' else 1.,format='%.3g')
                    with b:number(right,'Maximum',t,1e-9,.99 if right=='zone_por_max' else 1.,format='%.3g')
                st.caption(t('random_hint'))
            elif v['zones_preset'] in ('lens','channel','barrier'):st.caption(t('preset_hint_'+v['zones_preset']))
    with cols[2]:
        with panel('boundary_panel','Boundary conditions',t,True):
            number('head_left','Specified head left (m)',t,0.,1000.,.5,sliders=v['sliders'])
            number('head_right','Specified head right (m)',t,0.,1000.,.5,sliders=v['sliders'])
        with panel('solver_panel','Numerical solution for flow',t):
            st.caption('MODFLOW-2005 · PCG')
            if v['expert']:
                for key,label in [('hclose','Head tolerance (m)'),('rclose','Flow residual tolerance (m³/day)')]:number('s_'+key,label,t,1e-12,format='%.2e')
                for key,label in [('flow_mxiter','PCG outer iterations'),('flow_iter1','PCG inner iterations')]:number('s_'+key,label,t,1,10000,1)
            else:st.caption(t('expert_flow_hint'))


def _transport(t,v):
    cols=st.columns(3,gap='medium')
    with cols[0]:
        with panel('time_panel','Temporal discretization',t,True):
            number('duration','Transport duration (days)',t,1.,10000.,10.,sliders=v['sliders'])
            if v['expert']:
                number('s_dt0','DT0 · initial step (days; 0 = automatic)',t,0.,10000.,1.)
                number('s_ttsmax','TTSMAX · maximum step (days; 0 = automatic)',t,0.,10000.,1.)
                number('s_ttsmult','TTSMULT · step multiplier',t,1.,10.,.1)
                number('s_mxstrn','MXSTRN · maximum transport steps',t,1,10000000,100)
    with cols[1]:
        with panel('transport_properties_panel','Transport parameters',t,True):
            widget('toggle','dispersion','Dispersion',t)
            if v['dispersion']:
                number('al','Longitudinal dispersivity (m)',t,0.,1000.,1.)
                number('trpt','Horizontal transverse / longitudinal',t,0.,1.,.01)
                if v['nlay']>1:number('trpv','Vertical transverse / longitudinal',t,0.,1.,.01)
    with cols[2]:
        with panel('transport_boundary_panel','Boundary conditions and source',t,True):
            widget('selectbox','source_kind','Input signal',t,options=['pulse','continuous','dirac'],format_func=lambda x:t('signal_'+x))
            if v['source_kind']=='dirac':number('source_mass','Released mass (g)',t,.001,1e9,100.)
            else:number('mass_rate','Mass input rate (g/day)',t,.001,1e9,10.)
            if v['source_kind']=='pulse':number('pulse_duration','Pulse duration (days)',t,.001,10000.,10.)
            number('src_x','Source x (m)',t,0.,10000.,10.)
            number('src_y','Source y (m)',t,0.,5000.,10.)
            if v['expert']:
                a,b=st.columns(2)
                with a:number('src_ncol','Source cells x',t,1,31,1)
                with b:number('src_nrow','Source cells y',t,1,31,1)
            if v['nlay']>1:
                widget('checkbox','source_all_layers','Source spans all layers',t)
                if not v['source_all_layers']:
                    # Clamping a layer index when layers are removed is explicit
                    # in the stored control, preventing an invisible invalid value.
                    if v['src_layer']>v['nlay']:
                        v['src_layer']=v['nlay'];st.session_state['src_layer']=v['nlay']
                    number('src_layer','Source layer (1 = top)',t,1,v['nlay'],1)
        with panel('transport_solver_panel','Numerical solution for transport',t,True):
            widget('selectbox','method','MT3D advection method',t,options=list(METHODS),format_func=lambda x:SHORT_METHOD[x])
            if v['expert']:st.caption(t('expert_transport_location_hint'))
    if v['expert']:
        with panel('expert_solver_panel','Expert transport solver settings',t,True):
            st.caption(t('expert_transport_hint'))
            a,b,d=st.columns(3)
            with a:number('s_percel','PERCEL · Courant number',t,.001,10.,.05)
            with b:number('s_cclose','CCLOSE · concentration tolerance',t,1e-12,1.,format='%.2e')
            with d:number('s_timeout','Timeout per executable (seconds)',t,1,3600,10)
            labels={
                'mxpart':'MXPART · maximum particles','itrack':'ITRACK · tracking algorithm','wd':'WD · concentration weighting',
                'dceps':'DCEPS · gradient threshold','nplane':'NPLANE · particle planes','npl':'NPL · low-gradient particles',
                'nph':'NPH · high-gradient particles','npmin':'NPMIN · minimum particles/cell','npmax':'NPMAX · maximum particles/cell',
                'interp':'INTERP · interpolation','nlsink':'NLSINK · sink planes','npsink':'NPSINK · sink particles',
                'dchmoc':'DCHMOC · HMOC threshold','mxiter':'MXITER · GCG outer iterations','iter1':'ITER1 · GCG inner iterations',
                'isolve':'ISOLVE · preconditioner','ncrs':'NCRS · cross-dispersion','accl':'ACCL · relaxation','iprgcg':'IPRGCG · print interval'}
            positive={'mxpart','nph','npmax','npsink','mxiter','iter1'};selections={'itrack':[1,2,3],'interp':[1],'isolve':[1,2,3],'ncrs':[0,1]}
            cols=st.columns(3)
            for idx,(key,label) in enumerate(labels.items()):
                with cols[idx%3]:
                    if key in selections:widget('selectbox','s_'+key,label,t,options=selections[key])
                    else:
                        val=v['s_'+key]
                        if isinstance(val,int):number('s_'+key,label,t,1 if key in positive else 0,10000000,1)
                        else:number('s_'+key,label,t,.5 if key=='wd' else 0.,1. if key=='wd' else 1e6,format='%.8g')
    # Keep the full-width MT3D expander next in reading order after its method
    # selector. MODPATH is an independent comparison and follows all MT3D controls.
    with panel('particle_settings_panel','MODPATH settings',t,True):
        widget('toggle','track_particles','MODPATH particle comparison',t)
        if v['track_particles']:
            a,b,d=st.columns(3)
            with a:widget('selectbox','particle_count_mode','MODPATH particle count',t,
                          options=['cell','total'],format_func=lambda x:t('particle_count_'+x))
            with b:
                if v['particle_count_mode']=='cell':number('particles_per_cell','Particles per source cell',t,1,100000,1)
                else:number('total_source_particles','Particles in the whole source per release',t,1,100000,1)
            with d:
                if v['source_kind']!='dirac':number('release_groups','Release batches (pulse / continuous)',t,1,100,1)
            cells=v['src_ncol']*v['src_nrow']*(v['nlay'] if v['source_all_layers'] else 1)
            count=cells*v['particles_per_cell'] if v['particle_count_mode']=='cell' else v['total_source_particles']
            groups=1 if v['source_kind']=='dirac' else v['release_groups']
            st.caption(t('particle_count_summary',count=count,cells=cells,groups=groups,total=count*groups))


def _postprocessing(t,v):
    a,b=st.columns([2,1])
    with a:
        with panel('observation_panel','Observation points',t,True):
            number('nobs','Number of observation points',t,1,5,1)
            for i in range(v['nobs']):
                x,y,z=st.columns(3)
                with x:number(f'obs_x{i}',f'P{i+1} · x (m)',t,0.,10000.,10.)
                with y:number(f'obs_y{i}',f'P{i+1} · y (m)',t,0.,5000.,10.)
                with z:number(f'obs_z{i}',f'P{i+1} · elevation z (m)',t,0.,500.,1.)
            st.caption(t('observation_hint'))
    with b:
        with panel('output_panel','Output settings',t,True):
            number('outputs','Saved transport times',t,5,201,2)
            st.caption(t('output_hint'))


def model_inputs(t):
    v=values();a,b=st.columns(2)
    with a:widget('toggle','expert','Expert settings',t)
    with b:widget('toggle','sliders','Use sliders for main parameters',t)
    section=navigation([('flow','Flow & domain'),('transport','Transport & source'),('post','Post-processing & observations')],'input_section',t)
    if section=='flow':_flow(t,v)
    elif section=='transport':_transport(t,v)
    else:_postprocessing(t,v)
    return build_config(v)
