"""MT3D 2D/3D lab v0.5.0.

Contents: language/introduction; model inputs; preview/run; comparison results.
Native solvers are retained; random material arrays use the existing package inputs.
"""
from pathlib import Path
import io
import json
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
from .transport_lab.content import Catalog, available_languages
from .transport_lab.controls import model_inputs, navigation, panel, page_width_control, page_width_css, run_label_css
from .transport_lab.engine import find_engines, run_case
from .transport_lab.results import enrich,analytical_reference,summary_table,observation_table,breakthrough_table,export_run,reference_curve_table
from .transport_lab.history import add_run,retain_runs,sync_series,SHORT_METHOD
from .transport_lab import plots
from .transport_lab.figure_io import show_figure, svg_figure, SCRIPT_FONTS

ROOT=Path(__file__).resolve().parent
cached_reference_curves=st.cache_data(max_entries=12,show_spinner=False)(reference_curve_table)
st.set_page_config(page_title='MT3D – 2D/3D Transport Lab',layout='wide')
st.markdown('<style>'+(ROOT/'assets/style.css').read_text(encoding='utf-8')+'</style>',unsafe_allow_html=True)
st.session_state.setdefault('history',[]);st.session_state.setdefault('next_run',1)
languages=available_languages()
with st.container(key='language_header'):
    language_column,width_column=st.columns(2,vertical_alignment='center')
    with language_column:
        language=st.selectbox('Language / Sprache',list(languages),format_func=languages.get,key='language')
    t=Catalog(language)
    with width_column:page_width=page_width_control(t)
st.markdown('<style>'+page_width_css(page_width)+'</style>',unsafe_allow_html=True)
if language=='ar':
    st.markdown('''<style>
    .stMain [data-testid="stMarkdownContainer"], .stMain [data-testid="stWidgetLabel"] {direction:rtl;text-align:right;}
    .stMain .katex, .stMain [data-testid="stDataFrame"] {direction:ltr;text-align:initial;}
    .st-key-language_header [data-testid="stWidgetLabel"] p {text-align:center;}
    </style>''',unsafe_allow_html=True)
if not (ROOT/'assets/md'/f'interface_{language}.md').exists():
    st.caption(t('language_fallback'))


def show(fig):
    t.figure(fig);show_figure(fig,language);plt.close(fig)


def _remember_view(key):st.session_state.setdefault('_view_values',{})[key]=st.session_state[key]


def view(kind,label,key,default,**kwargs):
    stored=st.session_state.setdefault('_view_values',{})
    if key not in st.session_state:st.session_state[key]=stored.get(key,default)
    if 'options' in kwargs:
        options=kwargs['options']
        if kind=='multiselect':st.session_state[key]=[x for x in st.session_state[key] if x in options]
        elif st.session_state[key] not in options:st.session_state[key]=default
    return getattr(st,kind)(t(label),key=key,on_change=_remember_view,args=(key,),**kwargs)


def discard_run_tags():
    retain_runs(st.session_state,st.session_state.get('retained_runs',[]))


def local_frame(frame):
    return frame.rename(columns={key:t(key) for key in frame.columns})


def full_comparison(entries):
    frame=summary_table(entries)
    frame['Method']=frame.Method.map(SHORT_METHOD)
    frame['Signal']=frame.Signal.map(lambda x:t('signal_short_'+x))
    frame['Flow']=frame.Flow.map(t)
    return frame.rename(columns={
        'Grid (x × y × z)':'Grid','MT3D MB discrepancy (%)':'MB disc. (%)','Flow WB discrepancy (%)':'Flow disc. (%)',
        'MT3D runtime (s)':'MT3D (s)','MODPATH runtime (s)':'MP7 (s)','Flow runtime (s)':'Flow (s)',
        'Total runtime (s)':'Total (s)','Reference L1 error (%)':'Ref. L1 (%)','Final dissolved mass (g)':'Mass (g)',
        'Released mass (g)':'Input (g)','Minimum C (g/m³)':'Min. C (g/m³)','Negative mass (g)':'Neg. mass (g)',
        'Centroid x (m)':'Centroid x (m)','Transport steps':'Steps','End time (d)':'End (d)'})


st.title(t('title'))
st.markdown(t.document('intro'))
with st.container(key='teaching_notice'):st.markdown(t.document('status'))
intro=ROOT/'assets'/f'intro_{language}.svg'
if not intro.exists():intro=ROOT/'assets'/f'intro_{language}.png'
if not intro.exists():intro=ROOT/'assets/intro_en.png'
if intro.exists():
    _,centre,_=st.columns([1.2,7.6,1.2])
    with centre,st.container(key='intro_illustration'):
        st.image(str(intro),caption=t('intro_caption'),width='stretch')
with st.expander('**'+t('Concept, assumptions and equations')+'**'):st.markdown(t.document('theory'))
with st.expander('**'+t('Guided experiments')+'**'):st.markdown(t.document('experiments'))
st.subheader(t('Model & run'),divider='orange')
try:c=model_inputs(t)
except (ValueError,TypeError,KeyError,OverflowError) as exc:
    st.error(t('input_error'));st.code(str(exc),language=None);st.stop()
if sync_series(st.session_state,c):st.info(t('series_reset'))
errors=None
try:c.validate()
except (ValueError,IndexError) as exc:errors=str(exc)
if errors:
    st.error(t('input_error'));st.caption(t.translate_literal(errors))
else:
    heads=None
    for _,saved in reversed(st.session_state.history):
        if saved.config.fingerprint()==c.fingerprint():heads=saved.heads;break
    _,preview_column,_=st.columns([.6,8.8,.6])
    with preview_column,st.container(key='model_preview_frame'):show(plots.preview(c,heads=heads))
    st.caption(t('grid_summary',nx=c.ncol,ny=c.nrow,nz=c.nlay,dx=c.dx,dy=c.dy,dz=c.dz))
    if not(c.heterogeneous or c.transient):st.caption(t('velocity_summary',velocity=c.velocity))
    with st.expander(t('Actual source footprint')):
        b=c.source_bounds()
        st.write(t('source_bounds',x0=b[0][0],x1=b[0][1],y0=b[1][0],y1=b[1][1],z0=b[2][0],z1=b[2][1]))
        st.caption(t('source_snap_hint'))
engines=find_engines();required=['mf2005','mt3dms']+(['mp7'] if c.track_particles else [])
missing=[n for n in required if not engines.get(n)]
if missing:st.warning(t('missing_executables',names=', '.join(missing)))
with st.container(key='run_label_panel'):
    label=st.text_input(t('Optional run label'),max_chars=60,key='run_label',placeholder=t('label_placeholder'))
st.markdown('<style>'+run_label_css(label)+'</style>',unsafe_allow_html=True)
full=len(st.session_state.history)>=10
if full:st.info(t('history_full'))
_,button,_=st.columns([1,1.4,1])
with button,st.container(key='main_run'):
    clicked=st.button(t('Run model'),type='primary',width='stretch',disabled=bool(errors or missing or full),key='run_model')
if clicked:
    try:
        with st.spinner(t('running')):result=enrich(run_case(c,engines=engines))
        add_run(st.session_state,result,label);st.session_state['result_section']='plume'
        st.success(t('run_success'))
    except Exception as exc:
        st.error(t('run_failed'))
        with st.expander(t('Run diagnostic'),expanded=True):st.code(str(exc),language=None)

entries=st.session_state.history
if entries:
    st.subheader(t('Results & method comparison'),divider='orange')
    table=full_comparison(entries)
    basic=['Run','Grid','Active cells','MB disc. (%)','Flow disc. (%)','MT3D (s)','MP7 (s)','Ref. L1 (%)','Mass (g)']
    configs={t(key):st.column_config.NumberColumn(format='%.4f',help=t('table_help_'+key)) for key in basic if key not in ('Run','Grid')}
    configs[t('Active cells')]=st.column_config.NumberColumn(format='%d',help=t('table_help_Active cells'))
    st.dataframe(local_frame(table[basic]),hide_index=True,width='stretch',column_config=configs)
    with st.expander(t('More comparison metrics')):
        st.dataframe(local_frame(table),hide_index=True,width='stretch')
        st.markdown(t.document('comparison'))
    if len({r.config.source_bounds() for _,r in entries})>1:st.caption(t('changed_source_footprint'))
    if st.session_state.get('displayed_run') not in dict(entries):st.session_state['displayed_run']=entries[-1][0]
    a,b=st.columns([1.2,2.8],vertical_alignment='bottom')
    active=a.selectbox(t('Displayed run'),[n for n,_ in entries],key='displayed_run')
    st.session_state.setdefault('retained_runs',[n for n,_ in entries])
    b.multiselect(t('Comparison runs'),[n for n,_ in entries],key='retained_runs',on_change=discard_run_tags,help=t('discard_tags_hint'))
    run=dict(entries)[active];rc=run.config
    # Keep routine explanatory text in the theory. Numerical warnings remain visible.
    for warning in run.warnings:
        if warning.startswith(('Advective release is approximated','Storage is active','Specific storage is assigned','Analytical reference requires')):continue
        st.warning(t.translate_literal(warning))
    section=navigation([('plume','Plume & sections'),('observations','Observation curves'),('mass','Mass & diagnostics'),('export','Export')],'result_section',t)
    if section=='plume':
        left,right=st.columns([4,1.4],vertical_alignment='center')
        with left:
            a,b=st.columns(2)
            with a:ti=view('select_slider','Time (days)','view_time_'+active,len(run.times)-1,options=list(range(len(run.times))),format_func=lambda i:f'{run.times[i]:.3f}')
            with b:layer=view('selectbox','Top-view layer','view_layer_'+active,0,options=list(range(rc.nlay)),format_func=lambda i:t('Layer {number}',number=i+1))
        with right,st.container(key='analytic_panel'):
            overlay=view('toggle','Analytical reference','analytic_on',False)
        with panel('result_settings_panel','Plot settings and section positions',t,True):
            a,b=st.columns(2)
            with a:ys=view('slider','x-direction section · y (m)','section_y_'+active,rc.width/2,min_value=0.,max_value=rc.width)
            with b:xs=view('slider','y-direction section · x (m)','section_x_'+active,float(np.clip(rc.src_x+rc.velocity*run.times[ti],0,rc.length)),min_value=0.,max_value=rc.length)
            cols=st.columns(3)
            with cols[0]:fill=view('checkbox','Colour fill','fill',True)
            with cols[1]:lines=view('checkbox','Contour lines','lines',True)
            with cols[2]:show_heads=view('checkbox','Head contours','show_heads',True)
            cols=st.columns(3)
            with cols[0]:log=view('checkbox','Log colours','log',False)
            with cols[1]:particles=view('checkbox','Particle paths','particle_paths',True)
            with cols[2]:opacity=view('slider','Opacity','opacity',.65,min_value=.1,max_value=1.,step=.05)
            a,b,d=st.columns(3)
            with a:focus=view('toggle','Focus on plume','focus_plume',False)
            with b:relative=view('toggle','Plume-centered x/y','relative_xy',False,help=t('relative_hint'))
            with d:show_grid=view('toggle','Show model grid','show_grid',False,help=t('grid_hint'))
            a,b=st.columns([1,2],vertical_alignment='center')
            with a:focus_threshold=view('number_input','Focus threshold (% of peak)','focus_threshold',.1,min_value=.001,max_value=50.,step=.1,format='%.3f',disabled=not focus)
            if focus:
                with b:st.caption(t('focus_hint'))
            if relative:
                ox,oy,fallback=plots.plume_origin(run,ti,layer)
                st.caption(t('relative_source_origin' if fallback else 'relative_mass_origin',x=ox,y=oy))
        comparisons=[];compare_top=False
        with panel('comparison_panel','Compare runs in x / y sections',t,True):
            compare=view('toggle','Compare section profiles','compare_sections',False,disabled=len(entries)<2)
            if compare:
                options=[n for n,_ in entries if n!=active]
                selected=view('multiselect','Runs for section comparison','overlay_runs',options,options=options)
                compare_top=view('checkbox','Also overlay top-view contours','compare_top',False)
                for name,r in entries:
                    if name not in selected:continue
                    target=float(run.times[ti])
                    if target>r.times[-1]+1e-5:st.caption(t('no_comparison_time',name=name,time=target));continue
                    idx=int(np.argmin(np.abs(r.times-target)));comparisons.append((r,idx))
                    if abs(float(r.times[idx])-target)>1e-3:st.caption(t('nearest_time',name=name,time=r.times[idx],target=target))
        ref=None
        if overlay:
            with st.spinner(t('evaluating_reference')):ref,info=analytical_reference(rc,run.times[ti])
            if not info['accuracy_eligible']:st.info(t.translate_literal(info['message']));ref=None
        obs=[p for p in c.observations if 0<=p[0]<=rc.length and 0<=p[1]<=rc.width and 0<=p[2]<=rc.thickness]
        fig=plots.plume_figure(run,ti,layer=layer,y_section=ys,x_section=xs,fill=fill,contours=lines,opacity=opacity,log=log,reference=ref,show_particles=particles,comparison=comparisons,observations=obs,compare_top=compare_top,show_heads=show_heads,focus=focus,focus_threshold=focus_threshold,show_grid=show_grid,relative=relative)
        t.figure(fig);show_figure(fig,language)
        if language in SCRIPT_FONTS:
            image=svg_figure(fig,language,bbox_inches='tight').encode('utf-8')
            st.download_button(t('Download plume figure (SVG)'),image,'plume_sections.svg','image/svg+xml')
        else:
            image=io.BytesIO();fig.savefig(image,format='png',dpi=180,bbox_inches='tight')
            st.download_button(t('Download plume figure (PNG)'),image.getvalue(),'plume_sections.png','image/png')
        plt.close(fig)
    elif section=='observations':
        left,right=st.columns([4,1.4],vertical_alignment='center')
        with left:selected=view('multiselect','Runs in breakthrough comparison','btc_runs',[n for n,_ in entries],options=[n for n,_ in entries])
        with right,st.container(key='analytic_btc_panel'):analytic=view('toggle','Analytical reference','btc_analytical',False)
        picked=[(n,r) for n,r in entries if n in selected];reference_curves=None
        if analytic:
            if rc.heterogeneous or rc.transient:st.info(t('Analytical reference requires homogeneous steady flow.'))
            else:
                with st.spinner(t('evaluating_reference')):reference_curves=cached_reference_curves(rc.to_dict(),tuple(float(x) for x in run.times),tuple(tuple(p) for p in c.observations))
        if picked:
            show(plots.profiles_figure(picked,c.observations,reference_curves=reference_curves))
            with st.expander(t('Observation cells used by each run')):st.dataframe(local_frame(observation_table(picked,c.observations)),hide_index=True)
            st.download_button(t('Download breakthrough curves (CSV)'),breakthrough_table(picked,c.observations).to_csv(index=False),'breakthrough_curves.csv','text/csv')
    elif section=='mass':
        show(plots.budget_figure(entries))
        with panel('diagnostics_panel','Detailed mass-budget data',t):
            st.markdown(t.document('budget'))
            columns={'time':'Time (days)','total_in':'Cumulative in (g)','total_out':'Cumulative out (g)','sources':'Sources (g)','sinks':'Sinks (g)','fluid_storage':'Fluid storage (g)','total_mass':'Native resident mass (g)','error_in-out':'MB disc. (%)','error_alt':'Alternative disc. (%)'}
            st.dataframe(local_frame(run.mass.rename(columns=columns)),hide_index=True,width='stretch')
        with st.expander(t('Stored run configuration')):st.json(rc.to_dict())
    else:
        st.download_button(t('Download comparison table (CSV)'),local_frame(table).to_csv(index=False),'method_comparison.csv','text/csv')
        st.download_button(t('Download run configuration (JSON)'),json.dumps(rc.to_dict(),indent=2),'configuration.json','application/json')
        st.caption(t('export_hint'))
        if st.button(t('Prepare complete displayed-run archive'),key='prepare_export'):
            with st.spinner(t('Preparing archive…')):st.session_state.export_bytes=(active,export_run(run))
        cached=st.session_state.get('export_bytes')
        if cached and cached[0]==active:st.download_button(t('Download run archive (ZIP)'),cached[1],'transport_run.zip','application/zip')
else:st.info(t('no_runs'))
st.caption(t('footer'))
