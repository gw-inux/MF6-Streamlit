"""Small animation panel, rendered after the existing results sections."""
import json
from inspect import signature
import streamlit as st
from .animation import render_animation, MAX_FRAMES, MAX_3D_CELLS


def _show_animation_player(html,title,mode):
    """Embed generated HTML across Streamlit's old and new iframe APIs.

    Native iframe versions before accessibility labels were added reject
    ``alt``. Detect the actual callable rather than assuming a version number.
    Earlier installations without st.iframe use the HTML component (not the
    URL-only legacy iframe), which also runs the player's JavaScript.
    """
    embed=getattr(st,'iframe',None)
    if callable(embed):
        options={'height':'content'}
        if 'alt' in signature(embed).parameters:options['alt']=title
        embed(html,**options)
    else:
        import streamlit.components.v1 as components
        components.html(html,height=840 if mode=='2d' else 750,scrolling=True)


@st.fragment
def animation_panel(run,active,t,view):
    """Rerun only this region when preparing frames; leave the model readable."""
    c=run.config
    st.markdown('### '+t('Plume animation'))
    with st.expander(t('Animation settings')):
        st.caption(t('animation_hint'))
        a,b,d=st.columns(3)
        with a:mode=view('selectbox','Animation view','animation_mode','2d',options=['2d']+(['3d'] if c.nlay>1 else []),
                         format_func=lambda key:t('animation_'+key),help=t('help_animation_mode'))
        if c.nlay==1:st.caption(t('animation_layers_hint'))
        stored=st.session_state.setdefault('_view_values',{})
        maximum=min(MAX_FRAMES,len(run.times))
        stored['animation_frames']=max(2,min(maximum,stored.get('animation_frames',min(31,maximum))))
        with b:frames=view('number_input','Animation frames','animation_frames',min(31,maximum),min_value=2,max_value=maximum,step=1,help=t('help_animation_frames'))
        with d:fps=view('slider','Playback speed (frames/s)','animation_fps',4,min_value=1,max_value=12,help=t('help_animation_fps'))
        a,b=st.columns(2)
        with a:
            colour_mode=view('selectbox','Animation colour scale','animation_colour','enhanced',
                             options=['enhanced','linear','log'],format_func=lambda key:t('animation_colour_'+key),
                             help=t('help_animation_colour'))
        with b:
            focus=view('toggle','Zoom animation to plume','animation_focus',True,help=t('help_animation_focus'))
            threshold=view('number_input','Plume threshold (% of peak)','animation_threshold',.1,
                           min_value=.001,max_value=50.,step=.1,format='%.3f',help=t('help_animation_threshold'))
        exaggeration=5.
        if mode=='3d':
            exaggeration=view('slider','Vertical exaggeration','animation_exaggeration',5.,min_value=1.,max_value=20.,step=1.,help=t('help_animation_exaggeration'))
            st.caption(t('animation_3d_hint',maximum=MAX_3D_CELLS))
        layer=int(stored.get('view_layer_'+active,0));layer=max(0,min(c.nlay-1,layer))
        options={key:stored.get(state,default) for key,state,default in [
            ('y_section','section_y_'+active,c.width/2),('x_section','section_x_'+active,c.src_x),
            ('fill','fill',True),('contours','lines',True),('opacity','opacity',.65),('log','log',False),
            ('show_particles','particle_paths',True),('show_heads','show_heads',True),
            ('relative','relative_xy',False),('show_grid','show_grid',False)]}
        options.update(focus=focus,focus_threshold=threshold)
        settings={'mode':mode,'frames':frames,'fps':fps,'layer':layer,'plot_options':options,
                  'exaggeration':exaggeration,'colour_mode':colour_mode}
    signature=(str(run.workspace),active,t.language,json.dumps(settings,sort_keys=True))
    generate=st.button(t('Generate / refresh animation'),key='generate_animation',help=t('help_generate_animation'))
    progress_slot=st.empty()
    # Keep the output outside the settings expander and clear any stale player
    # before starting slow work. A fragment rerun does not fade the main app.
    output=st.empty()
    if generate:
        output.empty()
        bar=progress_slot.progress(0.,text=t('animation_progress',percent=0))
        try:
            def progress(fraction):
                bar.progress(fraction,text=t('animation_progress',percent=round(100*fraction)))
            html=render_animation(run,t=t,progress=progress,**settings)
            st.session_state['animation_bytes']=(active,signature,html)
        except Exception as exc:
            st.error(t('animation_failed'));st.code(str(exc),language=None)
        finally:progress_slot.empty()
    cached=st.session_state.get('animation_bytes')
    with output.container():
        if cached and cached[1]==signature:
            _show_animation_player(cached[2],t('Plume animation'),mode)
            st.download_button(t('Download animation (HTML)'),cached[2].encode('utf-8'),
                               'plume_animation.html','text/html',key='download_animation')
        elif cached:st.caption(t('animation_refresh_hint'))
