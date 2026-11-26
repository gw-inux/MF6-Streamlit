"""Comparison-series identity, independent of numerical discretization."""
import hashlib
import json
import shutil

SHORT_METHOD={'FD upstream':'FD up','FD central':'FD cen','TVD':'TVD','MOC':'MOC','MMOC':'MMOC','HMOC':'HMOC'}
SHORT_SIGNAL={'pulse':'Pulse','continuous':'Cont','dirac':'Dirac'}


def _geometry(config):
    # Explicitly requested conceptual changes reset the series. Numerical and
    # material parameter changes remain variants. Realised snapped source
    # geometry can change on refinement and is reported separately in results.
    keys=('length','width','thickness','source_kind','src_x','src_y',
          'source_all_layers','src_ncol','src_nrow')
    d={k:getattr(config,k) for k in keys}
    if not config.source_all_layers:d['src_layer']=config.src_layer
    return d


def series_key(config):
    return hashlib.sha256(json.dumps(_geometry(config),sort_keys=True).encode()).hexdigest()[:16]


def run_label(number,config,custom=''):
    base=custom.strip() or f'{SHORT_METHOD[config.method]} / {SHORT_SIGNAL[config.source_kind]}'
    return f'{number:02d} {base}'+(' / het.' if config.heterogeneous else '')


def clear_history(state,delete_workspaces=True):
    if delete_workspaces:
        for _,run in state.get('history',[]):shutil.rmtree(run.workspace,ignore_errors=True)
    state['history']=[];state['next_run']=1
    views=state.get('_view_values',{})
    for key in list(views):
        if key in ('overlay_runs','btc_runs','retained_runs') or key.startswith(('view_time_','view_layer_','section_x_','section_y_')):views.pop(key,None)
    for key in list(state):
        if key in ('displayed_run','remove_run','export_bytes','overlay_runs','btc_runs','retained_runs') or key.startswith(('view_time_','view_layer_','section_x_','section_y_')):
            state.pop(key,None)


def sync_series(state,config):
    key=series_key(config);old=state.get('series_key');changed=old is not None and old!=key
    geometry=_geometry(config);previous=state.get('series_geometry')
    # Removing layers can clamp a localized source into the remaining grid.
    # That is a discretization variant; an explicit source-layer edit still
    # starts a new series. Report realised source footprints in the table.
    if changed and previous is not None and state.get('series_layers')!=config.nlay:
        without_layer=lambda d:{k:v for k,v in d.items() if k!='src_layer'}
        if without_layer(previous)==without_layer(geometry):changed=False
    had_runs=bool(state.get('history'))
    if changed:clear_history(state)
    state['series_key']=key
    state['series_geometry']=geometry;state['series_layers']=config.nlay
    return changed and had_runs


def add_run(state,run,label=''):
    name=run_label(state.get('next_run',1),run.config,label)
    run.label=name
    state.setdefault('history',[]).append((name,run));state['next_run']=state.get('next_run',1)+1
    # Set before rendering the selectbox: every completed run becomes active.
    state['displayed_run']=name
    state['retained_runs']=[n for n,_ in state['history']]
    state['btc_runs']=[n for n,_ in state['history']]
    state.setdefault('_view_values',{})['btc_runs']=list(state['btc_runs'])
    state['_view_values']['overlay_runs']=[n for n,_ in state['history'] if n!=name]
    state.pop('overlay_runs',None)
    state.pop('export_bytes',None)
    return name


def retain_runs(state,names):
    """Remove discarded tags and their temporary files before rerendering widgets."""
    names=set(names);old=state.get('history',[])
    removed={n for n,r in old if n not in names}
    for n,r in old:
        if n in removed:shutil.rmtree(r.workspace,ignore_errors=True)
    kept=[(n,r) for n,r in old if n in names]
    state['history']=kept
    if not kept:
        clear_history(state);return
    if state.get('displayed_run') not in names:state['displayed_run']=kept[-1][0]
    state['retained_runs']=[n for n,r in kept]
    for bucket in (state,state.get('_view_values',{})):
        for key in ('overlay_runs','btc_runs'):
            if key in bucket:bucket[key]=[n for n in bucket[key] if n in names]
        for key in list(bucket):
            if any(key==prefix+n for n in removed for prefix in ('view_time_','view_layer_','section_x_','section_y_')):bucket.pop(key,None)
    if state.get('export_bytes') and state['export_bytes'][0] in removed:state.pop('export_bytes',None)
