"""Matplotlib figures for the transport lab; all coordinates in m and time in d.

Concentrations are finite-volume cell values. Particle traces are advective
MODPATH results, restricted to the plotted layer or section cell aperture.
"""
from __future__ import annotations

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
from matplotlib.collections import LineCollection
from matplotlib.lines import Line2D
from matplotlib.patches import Rectangle, Patch
from matplotlib.ticker import MaxNLocator, FuncFormatter
from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection

BLUE = '#2563a6'
ORANGE = '#cc6c24'
REFERENCE = '#a12f78'
PARTICLE = '#176b53'
PLUME_CMAP=colors.LinearSegmentedColormap.from_list('plume',['#ffffff','#eef6fc','#abd2e8','#4393c3','#2166ac','#ef8a62','#b2182b'])
SIGNED_CMAP=colors.LinearSegmentedColormap.from_list('signed_plume',[(0.,'#542788'),(.25,'#b2abd2'),(.5,'#ffffff'),(.6,'#eef6fc'),(.72,'#4393c3'),(.86,'#ef8a62'),(1.,'#b2182b')])


def _style(ax, xlabel=None, ylabel=None):
    ax.set_facecolor('white')
    ax.spines[['top', 'right']].set_visible(False)
    ax.tick_params(labelsize=8)
    if xlabel: ax.set_xlabel(xlabel, fontsize=9)
    if ylabel: ax.set_ylabel(ylabel, fontsize=9)
    ax.grid(alpha=.13, linewidth=.5)
    ax.set_axisbelow(True)


def _centers(edges):
    edges = np.asarray(edges)
    return (edges[:-1] + edges[1:]) / 2


def _named_runs(runs):
    result = []
    for i, item in enumerate(runs):
        if isinstance(item, tuple) and len(item) == 2 and isinstance(item[0], str):
            label, run = item
        else:
            run = item
            label = getattr(run, 'label', None) or getattr(run, 'name', None) or f'{i+1}: {run.config.method}'
        result.append((str(label), run))
    return result


def _source_patch(ax, cfg, plane, *, label=True):
    b = cfg.source_bounds()
    a, v = {'xy': (0, 1), 'xz': (0, 2), 'yz': (1, 2)}[plane]
    ax.add_patch(Rectangle((b[a][0], b[v][0]), b[a][1]-b[a][0], b[v][1]-b[v][0],
                           facecolor='none', edgecolor=ORANGE, linewidth=1.5,
                           label='Source cells' if label else None, zorder=6))


def _zones(ax, cfg, plane, layer=0, section=None):
    for iz, zone in enumerate(cfg.zones):
        zlo = cfg.thickness-(zone.last_layer+1)*cfg.dz
        zhi = cfg.thickness-zone.first_layer*cfg.dz
        if plane == 'xy':
            if not zone.first_layer <= layer <= zone.last_layer: continue
            xy, w, h = (zone.x0, zone.y0), zone.x1-zone.x0, zone.y1-zone.y0
        elif plane == 'xz':
            if section is not None and not zone.y0 <= section <= zone.y1: continue
            xy, w, h = (zone.x0, zlo), zone.x1-zone.x0, zhi-zlo
        else:
            if section is not None and not zone.x0 <= section <= zone.x1: continue
            xy, w, h = (zone.y0, zlo), zone.y1-zone.y0, zhi-zlo
        ax.add_patch(Rectangle(xy, w, h, facecolor='.75', edgecolor='.35', alpha=.2,
                               linewidth=.8, zorder=0))
        if len(cfg.zones)<=6:
            ax.text(xy[0]+w/2, xy[1]+h*.92, zone.name, ha='center', va='top',fontsize=7, color='.3', zorder=1)


def _frame3d(ax, cfg):
    x, y, z = cfg.length, cfg.width, cfg.thickness
    corners = np.array([[0,0,0],[x,0,0],[x,y,0],[0,y,0],
                        [0,0,z],[x,0,z],[x,y,z],[0,y,z]])
    pairs = [(0,1),(1,2),(2,3),(3,0),(4,5),(5,6),(6,7),(7,4),(0,4),(1,5),(2,6),(3,7)]
    ax.add_collection3d(Line3DCollection([corners[[a,b]] for a,b in pairs], colors='.35', linewidths=.6))
    for xx in [cfg.dx/2, x-cfg.dx/2]:
        ax.add_collection3d(Poly3DCollection([[(xx,0,0),(xx,y,0),(xx,y,z),(xx,0,z)]],
                                             facecolor=BLUE, alpha=.13, edgecolor=BLUE, linewidth=.6))
    b = cfg.source_bounds()
    s = np.array([[xx,yy,zz] for zz in b[2] for yy in b[1] for xx in b[0]])
    faces = [s[[0,1,3,2]],s[[4,5,7,6]],s[[0,1,5,4]],s[[2,3,7,6]],s[[0,2,6,4]],s[[1,3,7,5]]]
    ax.add_collection3d(Poly3DCollection(faces, facecolor=ORANGE, alpha=.5, edgecolor=ORANGE, linewidth=.4))
    for zz in cfg.z_edges[1:-1]:
        ax.plot([0,x,x,0,0],[0,0,y,y,0],[zz]*5, color='.5', alpha=.45, linewidth=.5)
    ax.set(xlim=(0,x),ylim=(0,y),zlim=(0,z),xlabel='x (m)',ylabel='y (m)',zlabel='z (m)')
    ax.set_xticks([0,x/2,x]);ax.set_yticks([0,y/2,y]);ax.set_zticks([0,z/2,z])
    ax.set_box_aspect((2.5,1.3,.8));ax.view_init(elev=24, azim=-55)
    ax.tick_params(labelsize=7, pad=0)
    for axis in [ax.xaxis,ax.yaxis,ax.zaxis]:
        axis.label.set_size(8);axis.labelpad=1
    ax.set_title(f'{cfg.nlay} layer(s); vertical scale exaggerated',fontsize=9)


def _head_contours(ax,cfg,heads,layer=0):
    if heads is None:return False
    h=np.asarray(heads,dtype=float)[layer]
    if h.shape!=(cfg.nrow,cfg.ncol) or not np.isfinite(h).all() or np.ptp(h)<1e-12:return False
    levels=np.linspace(float(h.min()),float(h.max()),7)[1:-1]
    cs=ax.contour(_centers(cfg.x_edges),_centers(cfg.y_edges),h,levels=levels,
                  colors=['#6a8392'],linewidths=.55,alpha=.6,zorder=3.2)
    ax.clabel(cs,inline=True,fontsize=6,fmt=lambda v:f'h = {v:.1f} m')
    return True


def _conductivity_preview(ax,cfg,layer):
    """White reference material; coloured actual cells and physical K labels."""
    if not cfg.heterogeneous:return
    hk=cfg.arrays()[0][layer]/86400.
    background=cfg.k/86400.
    if cfg.random_field is not None:
        f=cfg.random_field
        low=f.k_min/86400.;high=f.k_max/86400.
        norm=colors.LogNorm(low,high if high>low else low*1.01)
        ax.pcolormesh(cfg.x_edges,cfg.y_edges,hk,cmap='YlGnBu',norm=norm,shading='flat',alpha=.55,zorder=0)
        handles=[Patch(facecolor=plt.get_cmap('YlGnBu')(.1),alpha=.55,edgecolor='.55',label=f'K min = {low:.2e} m/s'),
                 Patch(facecolor=plt.get_cmap('YlGnBu')(.9),alpha=.55,edgecolor='.55',label=f'K max = {high:.2e} m/s')]
    else:
        # Draw only cells that differ from the white background. The same
        # centre-based assignment is used in the native MODFLOW inputs.
        lower=np.ma.masked_where(hk>=background,hk)
        higher=np.ma.masked_where(hk<=background,hk)
        for values,colour in ((lower,'#D59A52'),(higher,'#4B92C4')):
            ax.pcolormesh(cfg.x_edges,cfg.y_edges,values,cmap=colors.ListedColormap([colour]),shading='flat',alpha=.38,zorder=0)
        handles=[Patch(facecolor='white',edgecolor='.5',label=f'Background K = {background:.2e} m/s')]
        for z in cfg.zones:
            if not z.first_layer<=layer<=z.last_layer:continue
            colour='#D59A52' if z.k<cfg.k else '#4B92C4'
            label=f'{z.name}: K = {z.k/86400.:.2e} m/s'
            handles.append(Patch(facecolor=colour,alpha=.38,edgecolor='.5',label=label))
    legend=ax.legend(handles=handles,loc='upper right',fontsize=7,framealpha=.95)
    ax.add_artist(legend)


def preview(cfg,heads=None):
    """Large discretized plan above 3D view and source schedule.

    Only solved heads or the exact homogeneous steady field are contoured.
    Heterogeneous/transient fields are never represented by fictitious contours.
    """
    fig=plt.figure(figsize=(10,7.5),layout='constrained')
    gs=fig.add_gridspec(2,2,height_ratios=(1.35,1))
    ax=fig.add_subplot(gs[0,:]);_style(ax,'x (m)','y (m)')
    layer=min(cfg.src_layer,cfg.nlay-1)
    _conductivity_preview(ax,cfg,layer)
    ax.vlines(cfg.x_edges,0,cfg.width,color='#536a81',lw=.35,alpha=.22,zorder=1)
    ax.hlines(cfg.y_edges,0,cfg.length,color='#536a81',lw=.35,alpha=.22,zorder=1)
    for xx,head in [(cfg.dx/2,cfg.head_left),(cfg.length-cfg.dx/2,cfg.head_right_final if cfg.transient and heads is not None else cfg.head_right)]:
        ax.axvline(xx,color=BLUE,lw=2,zorder=3)
        ax.text(xx,cfg.width*1.02,f'Specified head: {head:g} m',ha='left' if xx<cfg.length/2 else 'right',fontsize=9,color=BLUE)
    headfield=None;headlabel=''
    if heads is not None:
        headfield=np.asarray(heads)[layer];headlabel='Computed head contours'
    elif not cfg.heterogeneous and not cfg.transient:
        headfield=np.broadcast_to(np.linspace(cfg.head_left,cfg.head_right,cfg.ncol),(cfg.nrow,cfg.ncol));headlabel='Homogeneous steady head contours'
    if headfield is not None:
        _head_contours(ax,cfg,np.asarray(headfield)[None,:,:],0)
    elif cfg.heterogeneous:headlabel='Head contours appear after running the model'
    _source_patch(ax,cfg,'xy')
    if not cfg.heterogeneous and not cfg.transient:
        ax.annotate('Background flow',xy=(cfg.length*.73,cfg.width*.76),xytext=(cfg.length*.53,cfg.width*.76),arrowprops={'arrowstyle':'->','color':BLUE},color=BLUE,fontsize=9,va='center')
    for i,(x,y,z) in enumerate(cfg.observations):
        ax.plot(x,y,'x',color='.15',ms=5);ax.annotate(f'P{i+1}',(x,y),xytext=(4,4),textcoords='offset points',fontsize=7)
    ax.set(xlim=(0,cfg.length),ylim=(0,cfg.width),aspect='equal')
    ax.set_title('Model preview: grid, boundaries and source',fontsize=11,pad=28)
    if headlabel:ax.text(.5,1.025,headlabel,transform=ax.transAxes,ha='center',fontsize=7,color='#667b8a')
    ax.legend(loc='upper left',fontsize=8,framealpha=.9)
    ax3=fig.add_subplot(gs[1,0],projection='3d');_frame3d(ax3,cfg)
    sig=fig.add_subplot(gs[1,1]);_style(sig,'Time (d)','Mass rate (g/d)')
    if cfg.source_kind=='dirac':
        sig.annotate('',xy=(0,1),xytext=(0,0),arrowprops={'arrowstyle':'->','color':ORANGE,'lw':2})
        sig.text(cfg.duration*.06,.8,f'{cfg.source_mass:g} g at t = 0',fontsize=9)
        sig.set_ylim(0,1.15);sig.set_yticks([]);sig.set_ylabel('Instantaneous mass (g)');sig.set_xlim(-cfg.duration*.04,cfg.duration)
    else:
        stop=cfg.duration if cfg.source_kind=='continuous' else cfg.pulse_duration
        sig.plot([0,0,stop,stop,cfg.duration],[0,cfg.mass_rate,cfg.mass_rate,0,0],color=ORANGE,lw=2)
        sig.fill_between([0,stop],cfg.mass_rate,alpha=.15,color=ORANGE)
        sig.set(xlim=(-cfg.duration*.02,cfg.duration),ylim=(0,cfg.mass_rate*1.2))
        sig.text(.97,.92,f'Total: {cfg.mass_rate*stop:g} g',ha='right',va='top',transform=sig.transAxes,fontsize=8)
    sig.set_title({'dirac':'Dirac input (initial cell mass)','pulse':'Finite pulse input','continuous':'Continuous input'}[cfg.source_kind],fontsize=10)
    return fig


def intro_figure(run):
    """A compact, computed example for the welcome text; not current controls."""
    c=run.config;fig,(ax,bx)=plt.subplots(1,2,figsize=(10,2.65),layout='constrained',gridspec_kw={'width_ratios':[1.6,1]})
    field=run.concentration[-1,0];norm,levels=_levels([field]);cm=_field(ax,c.x_edges,c.y_edges,field,norm,levels,True,True,1.)
    _style(ax,'x (m)','y (m)');ax.set(xlim=(100,700),ylim=(80,320),aspect='equal')
    ax.set_title('Example: pulse plume after 600 days',fontsize=10)
    handles=[Line2D([],[],color='.2',lw=.8,label='MT3D (TVD)')]
    if run.final_reference is not None:
        _reference_contour(ax,c.x_edges,c.y_edges,run.final_reference[0],levels)
        handles.append(Line2D([],[],color=REFERENCE,ls='--',label='Analytical reference'))
    ax.legend(handles=handles,loc='upper left',fontsize=7,ncol=2)
    x,y,z=c.observations[0];ax.plot(x,y,'x',color='black');ax.annotate('P1',(x,y),xytext=(4,4),textcoords='offset points',fontsize=8)
    bx.plot(run.times,run.breakthrough(x,y,z),color=BLUE,lw=1.7,label='TVD')
    _style(bx,'Time (d)','Concentration (g/m³)');bx.set_title('Example: observation P1',fontsize=10);bx.legend(loc='upper left',fontsize=8)
    return fig


def _levels(arrays, log=False):
    vals=np.concatenate([np.asarray(a,dtype=float).ravel() for a in arrays])
    vals=vals[np.isfinite(vals)]
    vmax=float(vals.max()) if len(vals) else 0.
    vmin=float(vals.min()) if len(vals) else 0.
    if vmax<=0:
        return colors.Normalize(vmin=min(vmin,0),vmax=max(1.,abs(vmin))), np.array([])
    if log:
        positive=vals[vals>0]
        low=max(vmax*1e-4,float(positive.min()))
        if low>=vmax:low=vmax/10
        return colors.LogNorm(vmin=low,vmax=vmax),np.geomspace(low,vmax,7)[1:-1]
    return (colors.TwoSlopeNorm(vcenter=0,vmin=vmin,vmax=vmax) if vmin<0 else colors.Normalize(vmin=0,vmax=vmax)),np.linspace(0,vmax,7)[1:-1]


def _field(ax,xedges,yedges,values,norm,levels,fill,contours,opacity,log=False):
    values=np.asarray(values,dtype=float)
    mappable=None
    if fill:
        shown=np.ma.masked_invalid(values)
        if log:shown=np.ma.masked_less_equal(shown,0)
        else:shown=np.ma.masked_where(values==0,shown)
        mappable=ax.pcolormesh(xedges,yedges,shown,cmap=SIGNED_CMAP if isinstance(norm,colors.TwoSlopeNorm) else PLUME_CMAP,norm=norm,
                               alpha=opacity,shading='flat',rasterized=True,zorder=2)
    if contours and values.shape[0]>=2 and values.shape[1]>=2 and len(levels):
        valid_levels=levels[(levels>np.nanmin(values))&(levels<np.nanmax(values))]
        if len(valid_levels):
            contour=ax.contour(_centers(xedges),_centers(yedges),values,
                               levels=valid_levels,colors='.2',linewidths=.65,zorder=3)
            ax.clabel(contour,inline=True,fontsize=6,fmt='%.2g')
    return mappable


def _reference_contour(ax,xedges,yedges,values,levels,color=REFERENCE):
    a=np.asarray(values)
    if not np.isfinite(a).any():return False
    xx=_centers(xedges);yy=_centers(yedges)
    if a.shape[0]==1:a=np.repeat(a,2,axis=0);yy=np.asarray(yedges)
    if a.shape[1]==1:a=np.repeat(a,2,axis=1);xx=np.asarray(xedges)
    use=levels[(levels>np.nanmin(a))&(levels<np.nanmax(a))]
    if not len(use):return False
    ax.contour(xx,yy,a,levels=use,colors=[colors.to_rgba(color)],
               linestyles='--',linewidths=1.,zorder=5)
    return True


def _path_arrays(run,time):
    particles=getattr(run,'particles',None)
    if particles is None:return []
    paths=getattr(particles,'paths',None)
    if paths is None or len(paths)==0:return []
    result=[]
    # Keep a bounded visual sample without changing calculations or exports.
    identifiers=paths['particleid'].unique()
    stride=max(1,int(np.ceil(len(identifiers)/120)))
    for pid in identifiers[::stride]:
        data=paths[paths['particleid']==pid].sort_values('time')
        a=data[['time','x','y','z']].to_numpy(dtype=float)
        if not len(a) or a[0,0]>time+1e-8:continue
        earlier=a[a[:,0]<=time+1e-8]
        later=a[a[:,0]>time+1e-8]
        if len(earlier) and len(later) and earlier[-1,0]<time:
            p,q=earlier[-1],later[0];frac=(time-p[0])/(q[0]-p[0])
            earlier=np.vstack([earlier,p+frac*(q-p)])
        if len(earlier):result.append(earlier)
    return result


def _particles(ax,paths,plane,lower,upper):
    a,b,f={'xy':(1,2,3),'xz':(1,3,2),'yz':(2,3,1)}[plane]
    for path in paths:
        mask=(path[:,f]>=lower-1e-8)&(path[:,f]<=upper+1e-8)
        xx=np.where(mask,path[:,a],np.nan);yy=np.where(mask,path[:,b],np.nan)
        ax.plot(xx,yy,color=PARTICLE,lw=.55,alpha=.48,zorder=4)
        if mask[-1]:ax.plot(xx[-1],yy[-1],'.',color=PARTICLE,ms=2.2,alpha=.8,zorder=5)


def plume_focus_limits(cfg, fields, paths=(), layer=0, threshold_percent=.1, padding=.2):
    """Bounds of positive plumes and visible, time-truncated particle paths.

    Each (config, 2D concentration) field uses its own positive peak, so a weak
    comparison plume is not cropped by a stronger run. Cell edges include the
    whole qualifying cells. No concentrations, normals or section limits change.
    Empty views retain the full domain. Paths must already be truncated in time.
    """
    if not np.isfinite(threshold_percent) or not 0 < threshold_percent <= 100:
        raise ValueError('Focus threshold must be in (0, 100] percent.')
    if not np.isfinite(padding) or padding < 0:
        raise ValueError('Focus padding must be nonnegative.')
    xs=[];ys=[]
    for material, values in fields:
        values=np.asarray(values,dtype=float)
        positive=np.isfinite(values)&(values>0)
        if not positive.any():continue
        peak=float(values[positive].max())
        rows,cols=np.where(positive&(values>=peak*threshold_percent/100.))
        xs.extend([material.x_edges[cols.min()],material.x_edges[cols.max()+1]])
        ys.extend([material.y_edges[rows.min()],material.y_edges[rows.max()+1]])
    lower,upper=sorted(cfg.z_edges[layer:layer+2])
    for path in paths:
        mask=np.isfinite(path[:,1:4]).all(axis=1)&(path[:,3]>=lower-1e-8)&(path[:,3]<=upper+1e-8)
        if mask.any():
            xs.extend([path[mask,1].min(),path[mask,1].max()])
            ys.extend([path[mask,2].min(),path[mask,2].max()])
    if not xs:return (0.,cfg.length),(0.,cfg.width)
    def limits(values,extent,spacing):
        lo,hi=np.clip([min(values),max(values)],0,extent)
        span=max(hi-lo,min(3*spacing,extent))
        centre=(lo+hi)/2;half=span*(.5+padding)
        return max(0.,centre-half),min(extent,centre+half)
    return limits(xs,cfg.length,cfg.dx),limits(ys,cfg.width,cfg.dy)


def plume_origin(run,time_index,layer=0):
    """Return (x, y, source_fallback) in absolute coordinates.

    The centroid uses positive dissolved mass in the displayed layer, including
    local porosity. Uniform cell volume cancels from this weighted mean. Signed
    concentrations are never modified. Before arrival, use the actual source
    cells (in this layer when available), weighted by their pore volumes.
    """
    cfg=run.config
    layer=int(np.clip(layer,0,cfg.nlay-1))
    time_index=int(np.clip(time_index,0,len(run.times)-1))
    values=np.asarray(run.concentration[time_index,layer],dtype=float)
    porosity=cfg.arrays()[2]
    positive=np.where(np.isfinite(values)&(values>0),values,0.)
    peak=float(positive.max())
    xc,yc=map(_centers,[cfg.x_edges,cfg.y_edges])
    if peak>0:
        weights=(positive/peak)*porosity[layer]
        total=float(weights.sum())
        if total>0:
            return float(np.dot(weights.sum(axis=0),xc)/total),float(np.dot(weights.sum(axis=1),yc)/total),False
    cells=cfg.source_cells()
    selected=[cell for cell in cells if cell[0]==layer] or cells
    weights=np.array([porosity[cell] for cell in selected],dtype=float)
    return (float(np.average([xc[j] for _,i,j in selected],weights=weights)),
            float(np.average([yc[i] for _,i,j in selected],weights=weights)),True)


class _RelativeLocator(MaxNLocator):
    """Place round relative ticks while preserving absolute plot geometry."""
    def __init__(self,origin):
        super().__init__(nbins='auto')
        self.origin=float(origin)

    def tick_values(self,vmin,vmax):
        return super().tick_values(vmin-self.origin,vmax-self.origin)+self.origin


def _relative_axis(axis,origin):
    axis.set_major_locator(_RelativeLocator(origin))
    def label(value,position):
        relative=value-origin
        if abs(relative)<1e-10*max(1.,abs(origin)):return '0.0'
        return f'{relative:g}'
    axis.set_major_formatter(FuncFormatter(label))


def _relative_position(value,origin,cell_size):
    """Suppress sub-millionth-cell roundoff in section-title coordinates only."""
    offset=float(value-origin)
    return 0. if abs(offset)<1e-6*cell_size else offset


def _model_grid(ax,xedges,yedges=None):
    """Subtle actual-cell edges, with no effect on limits or concentration data.

    Without yedges, draw vertical cell-edge guides in a concentration profile.
    Axis-fraction y coordinates work for both linear and logarithmic profiles.
    """
    if yedges is None:
        segments=[[(x,0.),(x,1.)] for x in xedges]
        transform=ax.get_xaxis_transform()
    else:
        segments=([[(x,min(yedges)),(x,max(yedges))] for x in xedges]+
                  [[(min(xedges),y),(max(xedges),y)] for y in yedges])
        transform=ax.transData
    grid=LineCollection(segments,colors='#7A838C',linewidths=.35,alpha=.35,
                        zorder=2.5,transform=transform)
    grid.set_gid(f'model-grid-{ax.figure.axes.index(ax)}')
    ax.add_collection(grid,autolim=False)


def plume_figure(run,time_index,layer=0,y_section=None,x_section=None,fill=True,
                 contours=True,opacity=.65,log=False,reference=None,
                 show_particles=True,comparison=None,observations=None,compare_top=False,show_heads=True,
                 focus=False,focus_threshold=.1,show_grid=False,relative=False):
    """Plan plume and two user-positioned sections/profiles.

    `reference` is a concentration cube on the active run's grid. `comparison`
    accepts Run objects (nearest saved time) or (Run, time_index) pairs; their
    top-view isolines share the active figure's absolute concentration levels.
    Relative x/y axes share the displayed run's positive-mass centroid. All
    plot geometry and model/observation inputs retain absolute coordinates.
    """
    cfg=run.config
    layer=int(np.clip(layer,0,cfg.nlay-1));time_index=int(np.clip(time_index,0,len(run.times)-1))
    time=float(run.times[time_index]);c=np.asarray(run.concentration[time_index])
    y_requested=cfg.src_y if y_section is None else float(y_section)
    x_requested=cfg.src_x if x_section is None else float(x_section)
    _,row,col=cfg.cell(x_requested,y_requested,cfg.thickness/2)
    xc,yc,zc=map(_centers,[cfg.x_edges,cfg.y_edges,cfg.z_edges])
    comparisons=[]
    for other in comparison or []:
        if isinstance(other,tuple):r,idx=other
        else:r=other;idx=int(np.argmin(abs(np.asarray(r.times)-time)))
        ok=int(np.argmin(abs(_centers(r.config.z_edges)-zc[layer])))
        comparisons.append((r,int(idx),ok))
    arrays=[c]
    if reference is not None:arrays.append(reference)
    arrays.extend(r.concentration[i] for r,i,k in comparisons)
    norm,levels=_levels(arrays,log)
    fig=plt.figure(figsize=(10,7.3),layout='constrained')
    gs=fig.add_gridspec(2,2,height_ratios=(1.25,1))
    top=fig.add_subplot(gs[0,:]);xa=fig.add_subplot(gs[1,0]);ya=fig.add_subplot(gs[1,1])
    _style(top,'x (m)','y (m)');_zones(top,cfg,'xy',layer)
    cm=_field(top,cfg.x_edges,cfg.y_edges,c[layer],norm,levels,fill,contours,opacity,log)
    bounds=cfg.source_bounds()
    if bounds[2][0] <= zc[layer] <= bounds[2][1]:
        _source_patch(top,cfg,'xy')
    top.axvline(cfg.dx/2,color=BLUE,lw=1.2,label='Specified head')
    top.axvline(cfg.length-cfg.dx/2,color=BLUE,lw=1.2)
    top.axhline(yc[row],color='.35',ls=':',lw=.8,label='Section locations')
    top.axvline(xc[col],color='.35',ls=':',lw=.8)
    handles,labels=top.get_legend_handles_labels()
    if show_heads and _head_contours(top,cfg,getattr(run,'heads',None),layer):
        handles.append(Line2D([],[],color='#6a8392',lw=.6));labels.append('Computed head contours (m)')
    if reference is not None:
        _reference_contour(top,cfg.x_edges,cfg.y_edges,np.asarray(reference)[layer],levels)
        handles.append(Line2D([],[],color=REFERENCE,ls='--'));labels.append('Analytical reference')
    for nr,(r,idx,k) in enumerate(comparisons):
        color=plt.get_cmap('tab10')((nr+1)%10)
        if compare_top:_reference_contour(top,r.config.x_edges,r.config.y_edges,r.concentration[idx,k],levels,color)
        handles.append(Line2D([],[],color=color,ls='--'));labels.append(f'{getattr(r,"label",r.config.method)}, {r.times[idx]:g} d')
    paths=_path_arrays(run,time) if show_particles else []
    if paths:
        _particles(top,paths,'xy',cfg.z_edges[layer+1],cfg.z_edges[layer])
        handles.append(Line2D([],[],color=PARTICLE,lw=1));labels.append('MODPATH advection (slice)')
    for i,(x,y,z) in enumerate(cfg.observations if observations is None else observations):
        top.plot(x,y,'x',color='black',ms=5,zorder=7)
        top.annotate(f'P{i+1}',(x,y),xytext=(4,4),textcoords='offset points',fontsize=7,zorder=7)
    if focus:
        fields=[(cfg,c[layer])]
        if reference is not None:fields.append((cfg,np.asarray(reference)[layer]))
        if compare_top:fields.extend((r.config,r.concentration[idx,k]) for r,idx,k in comparisons)
        xlim,ylim=plume_focus_limits(cfg,fields,paths,layer,focus_threshold)
        top.set(xlim=xlim,ylim=ylim)
    else:top.set(xlim=(0,cfg.length),ylim=(0,cfg.width))
    top.set_title(f'{cfg.method} · t = {time:g} d · layer {layer+1} (z = {zc[layer]:.3g} m)',fontsize=11)
    top.legend(handles,labels,loc='upper left',fontsize=7,ncol=min(3,max(1,len(labels)//2)),framealpha=.9)
    if cfg.nlay==1:
        for ax,coords,vals,ref,xlab,title in [
            (xa,xc,c[layer,row,:],None if reference is None else reference[layer,row,:],'x (m)',f'x profile at y = {yc[row]:.3g} m'),
            (ya,yc,c[layer,:,col],None if reference is None else reference[layer,:,col],'y (m)',f'y profile at x = {xc[col]:.3g} m')]:
            _style(ax,xlab,'Concentration (g/m³)')
            ax.plot(coords,vals,color=BLUE,lw=1.6,label=getattr(run,'label',cfg.method))
            if ref is not None:ax.plot(coords,ref,color=REFERENCE,ls='--',lw=1.3,label='Analytical')
            ax.set_title(title,fontsize=10)
            if log and np.any(vals>0):ax.set_yscale('log');ax.set_ylim(norm.vmin,norm.vmax*1.2)
            ax.legend(loc='upper left',fontsize=7)
        for nr,(r,idx,k) in enumerate(comparisons):
            rc=r.config;_,ri,rj=rc.cell(x_requested,y_requested,zc[layer]);color=plt.get_cmap('tab10')((nr+1)%10)
            xa.plot(_centers(rc.x_edges),r.concentration[idx,k,ri,:],color=color,ls='--',lw=1,label=getattr(r,'label',rc.method))
            ya.plot(_centers(rc.y_edges),r.concentration[idx,k,:,rj],color=color,ls='--',lw=1,label=getattr(r,'label',rc.method))
        xa.legend(loc='upper left',fontsize=7);ya.legend(loc='upper left',fontsize=7)
    else:
        for ax,plane,edges,vals,ref,section in [
            (xa,'xz',cfg.x_edges,c[:,row,:],None if reference is None else reference[:,row,:],yc[row]),
            (ya,'yz',cfg.y_edges,c[:,:,col],None if reference is None else reference[:,:,col],xc[col])]:
            _style(ax,'x (m)' if plane=='xz' else 'y (m)','Elevation z (m)')
            _zones(ax,cfg,plane,section=section)
            _field(ax,edges,cfg.z_edges,vals,norm,levels,fill,contours,opacity,log)
            if ref is not None:_reference_contour(ax,edges,cfg.z_edges,ref,levels)
            for nr,(other,oi,ok) in enumerate(comparisons):
                oc=other.config;_,ori,orj=oc.cell(x_requested,y_requested,zc[layer])
                oval=other.concentration[oi,:,ori,:] if plane=='xz' else other.concentration[oi,:,:,orj]
                oedges=oc.x_edges if plane=='xz' else oc.y_edges
                _reference_contour(ax,oedges,oc.z_edges,oval,levels,plt.get_cmap('tab10')((nr+1)%10))
            source_axis=1 if plane=='xz' else 0
            if bounds[source_axis][0] <= section <= bounds[source_axis][1]:
                _source_patch(ax,cfg,plane,label=False)
            if paths:
                lower,upper=(cfg.y_edges[row+1],cfg.y_edges[row]) if plane=='xz' else (cfg.x_edges[col],cfg.x_edges[col+1])
                _particles(ax,paths,plane,lower,upper)
            ax.set(xlim=(0,cfg.length if plane=='xz' else cfg.width),ylim=(0,cfg.thickness))
            ax.set_title(f'{plane[0]}–z section at {"y" if plane=="xz" else "x"} = {section:.3g} m',fontsize=10)
    if show_grid:
        _model_grid(top,cfg.x_edges,cfg.y_edges)
        _model_grid(xa,cfg.x_edges,None if cfg.nlay==1 else cfg.z_edges)
        _model_grid(ya,cfg.y_edges,None if cfg.nlay==1 else cfg.z_edges)
    if relative:
        ox,oy,_=plume_origin(run,time_index,layer)
        for axis,origin in ((top.xaxis,ox),(top.yaxis,oy),(xa.xaxis,ox),(ya.xaxis,oy)):
            _relative_axis(axis,origin)
        top.set_xlabel('x′ (m)',fontsize=9);top.set_ylabel('y′ (m)',fontsize=9)
        xa.set_xlabel('x′ (m)',fontsize=9);ya.set_xlabel('y′ (m)',fontsize=9)
        section_x=_relative_position(xc[col],ox,cfg.dx)
        section_y=_relative_position(yc[row],oy,cfg.dy)
        if cfg.nlay==1:
            xa.set_title(f'x profile at y′ = {section_y:.3g} m',fontsize=10)
            ya.set_title(f'y profile at x′ = {section_x:.3g} m',fontsize=10)
        else:
            xa.set_title(f'x–z section at y′ = {section_y:.3g} m',fontsize=10)
            ya.set_title(f'y–z section at x′ = {section_x:.3g} m',fontsize=10)
    if cm is not None:
        cb=fig.colorbar(cm,ax=[top] if cfg.nlay==1 else [top,xa,ya],shrink=.8,pad=.015)
        cb.set_label('Concentration (g/m³)',fontsize=9);cb.ax.tick_params(labelsize=8)
    minimum=float(np.nanmin(c))
    if minimum<0:
        fig.suptitle(f'Numerical minimum: {minimum:.3g} g/m³'+(' (nonpositive values hidden on log scale)' if log else ''),fontsize=9,color='#994322')
    return fig


def profiles_figure(runs,observations,reference_curves=None):
    """Breakthrough curves in containing cells, with no extrapolation of domains.

    `reference_curves` optionally contains the active-run analytical results with
    columns ``Point`` (P1...), ``Time (days)`` and ``C (g/m3)``. Cell locations
    can differ between grids; out-of-domain locations have no numerical trace.
    """
    named=_named_runs(runs);n=len(observations)
    if n<1 or n>5:raise ValueError('One to five observation points are required.')
    if reference_curves is not None and len(reference_curves):
        required={'Point','Time (days)','C (g/m3)'}
        if not required.issubset(reference_curves.columns):
            raise ValueError('Analytical curves require Point, Time (days), and C (g/m3) columns.')
    cols=1 if n==1 else 2;rows=int(np.ceil(n/cols))
    fig,axes=plt.subplots(rows,cols,figsize=(9,2.8*rows),squeeze=False,layout='constrained')
    for i,(x,y,z) in enumerate(observations):
        ax=axes.flat[i];_style(ax,'Time (d)','Concentration (g/m³)')
        absent=[]
        for label,run in named:
            cfg=run.config
            if not (0<=x<=cfg.length and 0<=y<=cfg.width and 0<=z<=cfg.thickness):
                absent.append(label)
                continue
            k,r,c=cfg.cell(x,y,z)
            ax.plot(run.times,run.concentration[:,k,r,c],lw=1.5,label=label)
        if reference_curves is not None and len(reference_curves):
            ref=reference_curves[reference_curves['Point']==f'P{i+1}'].sort_values('Time (days)')
            if len(ref):
                t=np.asarray(ref['Time (days)'],dtype=float)
                c=np.asarray(ref['C (g/m3)'],dtype=float)
                valid=np.isfinite(t)&np.isfinite(c)
                if np.any(valid):
                    ax.plot(t[valid],c[valid],color=REFERENCE,ls='--',lw=1.5,
                            label='Analytical (active run)')
        ax.set_title(f'P{i+1}: x = {x:g}, y = {y:g}, z = {z:g} m',fontsize=10)
        handles,labels=ax.get_legend_handles_labels()
        for label in absent:
            handles.append(Line2D([],[],color='.55',marker='x',ls='none',ms=4))
            labels.append(f'{label}: outside domain — no data')
        if handles:ax.legend(handles,labels,loc='upper left',fontsize=7)
        ax.axhline(0,color='.5',lw=.5)
    for i in range(n,rows*cols):axes.flat[i].set_visible(False)
    return fig


def _column(frame,names):
    if frame is None:return None
    available={str(c).lower():c for c in frame.columns}
    for name in names:
        if name.lower() in available:return np.asarray(frame[available[name.lower()]],dtype=float)
    return None


def budget_figure(runs,show_reported=True):
    """Independent grid mass and native MT3D mass-balance diagnostics.

    Solid curves integrate the stored UCN concentrations, porosity and cell
    volume, retaining signed concentrations. Dotted curves expose native MAS
    resident mass, which can differ from the concentration-grid integral for
    particle methods. Native discrepancy remains a separate reported metric.
    """
    named=_named_runs(runs)
    fig,axes=plt.subplots(1,2,figsize=(10,3.7),layout='constrained')
    _style(axes[0],'Time (d)','Mass (g)');_style(axes[1],'Time (d)','MT3D discrepancy (%)')
    any_budget=False
    for i,(label,run) in enumerate(named):
        frame=getattr(run,'mass',None);color=plt.get_cmap('tab10')(i%10)
        cfg=run.config
        porosity=cfg.arrays()[2]
        pore_volume=np.asarray(porosity,dtype=float)*cfg.dx*cfg.dy*cfg.dz
        grid_mass=np.einsum('tkij,kij->t',run.concentration,pore_volume,dtype=np.float64,optimize=True)
        axes[0].plot(run.times,grid_mass,color=color,lw=1.6,label=f'{label}: grid sum')
        any_budget=True
        t=_column(frame,['time','time_d','totim'])
        reported=_column(frame,['total_mass','mass_aqueous_g','aqueous_g','mass_in_aquifer_g','aqueous_phase'])
        disc=_column(frame,['discrepancy_pct','mass_discrepancy_pct','error_in-out','error_in-out2'])
        if show_reported and t is not None and reported is not None:
            axes[0].plot(t,reported,color=color,lw=1.2,ls=':',label=f'{label}: MT3D budget')
        if t is not None and disc is not None:
            axes[1].plot(t,disc,color=color,lw=1.3,label=label)
    if named:
        cfg=named[0][1].config;t=np.asarray(named[0][1].times,dtype=float)
        expected=np.full_like(t,cfg.source_mass) if cfg.source_kind=='dirac' else cfg.mass_rate*np.minimum(t,cfg.pulse_duration if cfg.source_kind=='pulse' else cfg.duration)
        axes[0].plot(t,expected,'k--',lw=1,label='Initial + injected mass (first run)')
    if not any_budget:axes[0].text(.5,.5,'Mass output unavailable',ha='center',transform=axes[0].transAxes)
    for ax in axes:
        ax.axhline(0,color='.5',lw=.5)
        handles,labels=ax.get_legend_handles_labels()
        if handles:
            if ax is axes[0]:ax.legend(loc='upper center',bbox_to_anchor=(.5,-.23),fontsize=7,ncol=2)
            else:ax.legend(loc='upper left',fontsize=7)
    axes[0].set_title('Resident mass: grid sum and MT3D budget',fontsize=10)
    axes[1].set_title('Reported mass-balance closure',fontsize=10)
    return fig
