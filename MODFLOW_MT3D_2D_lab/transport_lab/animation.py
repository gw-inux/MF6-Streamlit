"""On-demand, self-contained plume animations; no video encoder or CDN.

Frames use saved numerical output, one fixed colour scale and a fixed camera.
The 3D view shows concentration at cell centres, not an inferred isosurface.
Only one generated player is retained per Streamlit session.
"""
from base64 import b64encode
from html import escape
from io import BytesIO
import json
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
from matplotlib.ticker import FuncFormatter, MaxNLocator
from . import plots
from .figure_io import SCRIPT_FONTS, svg_figure

MAX_FRAMES = 80
MAX_3D_CELLS = 12000
MAX_HTML_BYTES = 45 * 1024 * 1024
LOW_CONCENTRATION_GAMMA = .35


class _SignedPowerNorm(colors.TwoSlopeNorm):
    """Enhance both sides of zero without hiding numerical undershoots.

    Retain TwoSlopeNorm's zero-centred colour map and physical colourbar values.
    Only the colour mapping changes; concentrations and profile values do not.
    """
    def __call__(self, value, clip=None):
        centred=2*super().__call__(value,clip)-1
        return .5+.5*np.sign(centred)*np.abs(centred)**LOW_CONCENTRATION_GAMMA

    def inverse(self, value):
        centred=2*np.asarray(value)-1
        linear=.5+.5*np.sign(centred)*np.abs(centred)**(1/LOW_CONCENTRATION_GAMMA)
        return super().inverse(linear)


def frame_indices(times, count):
    """Subsample saved times, including both endpoints; never invent output."""
    if not isinstance(count, (int, np.integer)) or not 2 <= count <= MAX_FRAMES:
        raise ValueError('Choose between 2 and 80 animation frames.')
    return np.unique(np.rint(np.linspace(0, len(times)-1, min(count,len(times)))).astype(int))


def colour_scale(run, indices, log=False, enhanced=False):
    # Extremes suffice for linear colours; include the smallest positive value
    # for the same log convention as static plots without stacking the 4D data.
    low,high,positive=0.,0.,np.inf
    for index in indices:
        a=run.concentration[index];finite=a[np.isfinite(a)]
        if finite.size:
            low=min(low,float(finite.min()));high=max(high,float(finite.max()))
            p=finite[finite>0]
            if p.size:positive=min(positive,float(p.min()))
    norm,levels=plots._levels([np.array([low,high,positive if np.isfinite(positive) else 0.])],log)
    if enhanced and not log:
        if low<0:
            norm=_SignedPowerNorm(vcenter=0,vmin=low,vmax=max(high,abs(low),1.) if high<=0 else high)
        else:
            norm=colors.PowerNorm(LOW_CONCENTRATION_GAMMA,vmin=0,vmax=norm.vmax)
        # Include physically labelled low-concentration isolines in late frames.
        levels=high*np.array([.001,.01,.05,.2,.5,.8]) if high>0 else np.array([])
    return norm,levels


def cloud_sample(shape):
    """Even Cartesian cell-centre sample with a documented display-only bound."""
    counts=np.array(shape,dtype=int)
    while np.prod(counts)>MAX_3D_CELLS:
        axis=int(np.argmax(counts));counts[axis]-=1
    return tuple(np.unique(np.rint(np.linspace(0,n-1,m)).astype(int)) for n,m in zip(shape,counts))


def plume_3d_figure(run,index,scale,layer=0,show_particles=True,relative=False,
                    threshold_percent=.1,exaggeration=5.,limits=None):
    c=run.config
    if c.nlay<2:raise ValueError('Add model layers before using the 3D animation.')
    norm,_=scale
    ik,iy,ix=cloud_sample(c.shape)
    z,y,x=np.meshgrid(plots._centers(c.z_edges)[ik],plots._centers(c.y_edges)[iy],
                       plots._centers(c.x_edges)[ix],indexing='ij')
    values=run.concentration[index][np.ix_(ik,iy,ix)]
    # Keep numerical undershoots visible as well as the positive plume.
    threshold=max(abs(norm.vmin),abs(norm.vmax))*threshold_percent/100
    mask=np.isfinite(values)&(np.abs(values)>=threshold)&(values!=0)
    if isinstance(norm,colors.LogNorm):mask &= values>0
    fig=plt.figure(figsize=(10,6.5),layout='constrained')
    ax=fig.add_subplot(111,projection='3d')
    cmap=plots.SIGNED_CMAP if isinstance(norm,colors.TwoSlopeNorm) else plots.PLUME_CMAP
    ax.scatter(x[mask],y[mask],z[mask],c=values[mask],cmap=cmap,norm=norm,
               s=13,alpha=.72,edgecolors='none',depthshade=False)
    if show_particles:
        for path in plots._path_arrays(run,float(run.times[index])):
            ax.plot(path[:,1],path[:,2],path[:,3],color=plots.PARTICLE,lw=.3,alpha=.35)
            ax.scatter(*path[-1,1:],s=22,color=plots.PARTICLE,edgecolors='none',linewidths=0,depthshade=False)
    xlim,ylim=limits if limits is not None else ((0,c.length),(0,c.width))
    ax.set(xlim=xlim,ylim=ylim,zlim=(0,c.thickness),
           xlabel='x (m)',ylabel='y (m)',zlabel='Elevation z (m)')
    ax.set_box_aspect((np.ptp(xlim),np.ptp(ylim),c.thickness*exaggeration))
    for axis in (ax.xaxis,ax.yaxis,ax.zaxis):
        axis.set_major_locator(MaxNLocator(4));axis.labelpad=12
    ax.tick_params(labelsize=8,pad=2)
    ax.view_init(elev=25,azim=-65)
    if relative:
        # Use all layers for a volume view. Uniform cell volume cancels.
        mass=np.maximum(np.nan_to_num(run.concentration[index],nan=0.),0)*c.arrays()[2]
        total=mass.sum()
        if total>0:
            ox=float((mass*plots._centers(c.x_edges)[None,None,:]).sum()/total)
            oy=float((mass*plots._centers(c.y_edges)[None,:,None]).sum()/total)
        else:
            bounds=c.source_bounds();ox=np.mean(bounds[0]);oy=np.mean(bounds[1])
        ax.xaxis.set_major_formatter(FuncFormatter(lambda v,pos:f'{v-ox:.1f}'))
        ax.yaxis.set_major_formatter(FuncFormatter(lambda v,pos:f'{v-oy:.1f}'))
        ax.set_xlabel('x′ (m)');ax.set_ylabel('y′ (m)')
    ax.set_title(f'{c.method} · t = {run.times[index]:g} d')
    fig.colorbar(plt.cm.ScalarMappable(norm=norm,cmap=cmap),ax=ax,shrink=.55,
                 pad=.08,label='Concentration (g/m³)')
    return fig


def render_animation(run, *, t, mode='2d', frames=31, fps=4, layer=0,
                     plot_options=None, exaggeration=5., progress=None, colour_mode=None):
    """Return an offline HTML player. Rendering never invokes a native solver."""
    if mode not in ('2d','3d'):raise ValueError('Unknown animation view.')
    if not np.isfinite(fps) or not 1<=fps<=12:raise ValueError('Playback speed must be 1–12 frames/s.')
    if not np.isfinite(exaggeration) or not 1<=exaggeration<=20:raise ValueError('Vertical exaggeration must be 1–20.')
    if not 0<=layer<run.config.nlay:raise ValueError('Animation layer is outside the model.')
    options=dict(plot_options or {})
    if colour_mode is not None:
        if colour_mode not in ('enhanced','linear','log'):raise ValueError('Unknown animation colour scale.')
        options['log']=colour_mode=='log'
    indices=frame_indices(run.times,frames)
    scale=colour_scale(run,indices,options.get('log',False),enhanced=colour_mode=='enhanced')
    images=[];byte_count=0
    # With focus enabled retain one window over the whole trajectory. This
    # avoids a moving camera obscuring advection; relative tick labels may move.
    limits=None
    if options.get('focus',False):
        boxes=[]
        for i in indices:
            field=run.concentration[i,layer] if mode=='2d' else np.max(run.concentration[i],axis=0)
            paths=plots._path_arrays(run,float(run.times[i])) if options.get('show_particles',True) else []
            if mode=='3d':
                # Project every layer's paths into the chosen plan slice only
                # for the framing calculation; tracking arrays stay untouched.
                paths=[path.copy() for path in paths]
                for path in paths:path[:,3]=plots._centers(run.config.z_edges)[layer]
            if np.any(field>0) or paths:
                boxes.append(plots.plume_focus_limits(run.config,[(run.config,field)],paths,
                             layer,options.get('focus_threshold',.1)))
        if boxes:limits=((min(b[0][0] for b in boxes),max(b[0][1] for b in boxes)),
                        (min(b[1][0] for b in boxes),max(b[1][1] for b in boxes)))
    for number,index in enumerate(indices):
        fig=None
        try:
            if mode=='2d':
                fig=plots.plume_figure(run,int(index),layer=layer,colour_scale=scale,**options)
                if limits:fig.axes[0].set(xlim=limits[0],ylim=limits[1])
                if run.config.nlay==1 and not options.get('log',False):
                    for ax in fig.axes[1:3]:ax.set_ylim(min(0,scale[0].vmin),scale[0].vmax*1.05)
            else:
                fig=plume_3d_figure(run,int(index),scale,layer=layer,
                    show_particles=options.get('show_particles',True),relative=options.get('relative',False),
                    threshold_percent=options.get('focus_threshold',.1),exaggeration=exaggeration,limits=limits)
            t.figure(fig)
            if t.language in SCRIPT_FONTS:
                data=svg_figure(fig,t.language).encode('utf-8');mime='image/svg+xml'
            else:
                stream=BytesIO();fig.savefig(stream,format='png',dpi=95);data=stream.getvalue();mime='image/png'
            encoded='data:'+mime+';base64,'+b64encode(data).decode('ascii')
            byte_count+=len(encoded)
            if byte_count>MAX_HTML_BYTES:raise ValueError(t('animation_size_limit'))
            images.append(encoded)
        finally:
            if fig is not None:plt.close(fig)
        if progress:progress((number+1)/len(indices))
    return player_html(images,[float(run.times[i]) for i in indices],fps,t,getattr(run,'label',run.config.method))


def player_html(images,times,fps,t,title):
    # All dynamic values use JSON data or escaped text, including custom labels.
    data=json.dumps({'images':images,'times':times,'interval':round(1000/fps)},ensure_ascii=True).replace('<','\\u003c')
    labels={key:escape(t(key),quote=True) for key in ('Play','Pause','Time (days)','Animation frame')}
    return '''<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<style>body{font:15px system-ui;margin:0;color:#22334a;background:white}.controls{display:flex;gap:12px;align-items:center;padding:10px}button{border:1px solid #486482;border-radius:6px;padding:7px 15px;background:#e9f3ff;cursor:pointer}input{flex:1;min-width:60px}img{width:100%;height:auto;display:block}h4{margin:8px 12px}output{white-space:nowrap}</style>
</head><body><h4>'''+escape(title)+'''</h4><div class="controls"><button id="play">'''+labels['Play']+'''</button>
<input id="frame" type="range" min="0" max="'''+str(len(images)-1)+'''" value="0" aria-label="'''+labels['Animation frame']+'''">
<output id="time"></output></div><img id="image" alt="'''+labels['Animation frame']+'''">
<script type="application/json" id="data">'''+data+'''</script><script>
const data=JSON.parse(document.getElementById('data').textContent),slider=document.getElementById('frame'),image=document.getElementById('image'),button=document.getElementById('play'),time=document.getElementById('time');
const playLabel='''+json.dumps(t('Play'))+''',pauseLabel='''+json.dumps(t('Pause'))+''',timeLabel='''+json.dumps(t('Time (days)'))+''';
let timer=null,index=0;
function show(i){index=i;image.src=data.images[index];slider.value=index;time.textContent=timeLabel+': '+Number(data.times[index].toPrecision(6));}
function pause(){clearInterval(timer);timer=null;button.textContent=playLabel;}
button.onclick=()=>{if(timer){pause();return;}button.textContent=pauseLabel;timer=setInterval(()=>show((index+1)%data.images.length),data.interval);};
slider.oninput=()=>{pause();show(Number(slider.value));};window.addEventListener('pagehide',pause);show(0);
</script></body></html>'''
