"""v1.5 plotting semantics and comparisons; actual native runs for UI tests."""

# BEGIN CODE CONTENTS
# Manual edits: jump to these release line numbers (refresh with tools/update_code_map.py).
#   result: line 28
#   test_head_styles_keep_identical_wetted_filling_without_major_grid: line 34
#   test_previous_profile_is_small_hollow_and_uses_original_physical_coordinates: line 54
#   test_dense_result_symbols_are_thinned_but_all_cell_heads_and_fill_remain: line 72
#   test_plan_equal_scales_and_width_with_thinned_grid: line 84
#   test_limit_and_comparison_group_requirements: line 102
#   test_plain_spacing_csv_format: line 114
#   test_ui_visibility_previous_run_and_retention: line 119
# END CODE CONTENTS

from dataclasses import replace
import matplotlib.pyplot as plt
from matplotlib.collections import QuadMesh
import numpy as np
import pandas as pd
import pytest

from MODFLOW_Solver_lab.core import MAX_CELLS, Scenario
from MODFLOW_Solver_lab.settings import formatted_csv
from MODFLOW_Solver_lab.plots import head_plot, model_preview, display_indices, display_stride, profile_snapshot
from test_ui import app


def result(s, run_id=1):
    # Synthetic graphics fixture only. Scientific tests use native MODFLOW heads.
    return dict(run_id=run_id,heads=np.full(s.shape,19.).ravel().tolist(),success=True,status='Converged')


@pytest.mark.parametrize('dots,lines,shown',[(True,True,True),(True,False,True),(False,True,True),(True,True,False),(True,False,False)])
def test_head_styles_keep_identical_wetted_filling_without_major_grid(dots,lines,shown):
    s=Scenario(confined=False);r=result(s)
    fig=head_plot(s,[r],cell_heads=dots,cell_lines=lines,show_heads=shown,analytical=True)
    ax=fig.axes[0]
    assert any(l.get_gid()=='cell_head_dots' for l in ax.lines)==(dots and shown)
    segments=[c for c in ax.collections if c.get_gid()=='cell_head_lines']
    assert bool(segments)==(lines and shown)
    if segments:
        assert all(seg[0,1]==seg[1,1] for seg in segments[0].get_segments())
        assert segments[0].get_linewidths()[0]<1.
    assert next(l for l in ax.lines if l.get_label()=='Analytical solution').get_linewidth()<1.
    before=next(c for c in ax.collections if c.get_gid()=='wetted_cells').get_paths()[0].vertices
    other=head_plot(s,[r],show_heads=not shown)
    after=next(c for c in other.axes[0].collections if c.get_gid()=='wetted_cells').get_paths()[0].vertices
    np.testing.assert_array_equal(before,after)
    assert max(before[:,1])==19. and min(before[:,1])==0.
    assert not any(line.get_visible() for line in ax.get_ygridlines())
    plt.close(fig);plt.close(other)


def test_previous_profile_is_small_hollow_and_uses_original_physical_coordinates():
    old=Scenario(n=1001,complexity=True,nlay=3)
    r=result(old);heads=np.asarray(r['heads']).reshape(old.shape)
    heads[2,0,:]=np.linspace(18,22,old.n);r['heads']=heads.ravel().tolist()
    snapshot=profile_snapshot(old,r,layer=2)
    assert len(snapshot['head_m'])<=101 and snapshot['layer']==3 and snapshot['cell_y']==1
    np.testing.assert_allclose(snapshot['x_m'],old.x[display_indices(old.n)])
    current=replace(old,n=11,nlay=1,confined=False)
    fig=head_plot(current,[result(current,2)],previous=snapshot);ax=fig.axes[0]
    prev=next(l for l in ax.lines if l.get_gid()=='previous_heads')
    dots=next(l for l in ax.lines if l.get_gid()=='cell_head_dots')
    np.testing.assert_allclose((prev.get_xdata()-1)*current.dx,snapshot['x_m'])
    np.testing.assert_allclose(prev.get_ydata(),snapshot['head_m'])
    assert prev.get_linestyle()=='None' and prev.get_markerfacecolor()=='none'
    assert prev.get_markersize()>dots.get_markersize() and 'layer 3' in prev.get_label()
    plt.close(fig)


def test_dense_result_symbols_are_thinned_but_all_cell_heads_and_fill_remain():
    s=Scenario(n=1001);f=head_plot(s,[result(s)]);ax=f.axes[0]
    dots=next(l for l in ax.lines if l.get_gid()=='cell_head_dots')
    assert len(dots.get_xdata())<=101
    assert dots.get_xdata()[0]==1 and dots.get_xdata()[-1]==s.n
    lines=next(c for c in ax.collections if c.get_gid()=='cell_head_lines')
    assert len(lines.get_segments())==s.n and display_stride(s.n)>1
    assert 'Analytical solution' not in ax.get_legend_handles_labels()[1]
    plt.close(f)


@pytest.mark.parametrize('quantity',['Empty cells','K zones','Initial heads'])
def test_plan_equal_scales_and_width_with_thinned_grid(quantity):
    s=Scenario(n=501,complexity=True,horizontal_2d=True,random_k=True,k_zones=11)
    s.validate();f=model_preview(s,quantity);f.canvas.draw();plan,section=f.axes[:2]
    pixels=plan.transData.transform([[0,0],[s.dx,s.dy]])
    assert pixels[1,0]-pixels[0,0]==pytest.approx(pixels[1,1]-pixels[0,1],rel=1e-10)
    assert plan.get_position().width==pytest.approx(section.get_position().width,abs=1e-10)
    lines=next(c for c in plan.collections if c.get_gid()=='grid_faces_x')
    assert len(lines.get_segments())<105
    if quantity=='Empty cells':
        assert len(f.axes)==2 and not any(isinstance(c,QuadMesh) for c in plan.collections)
    elif quantity=='K zones':
        mesh=next(c for c in plan.collections if isinstance(c,QuadMesh))
        assert mesh.cmap.N==s.k_zones and len(mesh.norm.boundaries)==s.k_zones+1
        labels=[t.get_text() for t in f.axes[2].get_yticklabels()]
        assert labels[0].startswith('1 ·') and labels[-1].startswith('11 ·')
    plt.close(f)


def test_limit_and_comparison_group_requirements():
    assert MAX_CELLS==255000
    Scenario(n=501,complexity=True,horizontal_2d=True).validate()
    Scenario(n=8500,complexity=True,nlay=30).validate()
    with pytest.raises(ValueError,match='255,000'):
        Scenario(n=505,complexity=True,horizontal_2d=True).validate()
    s=Scenario()
    assert s.comparison_group==replace(s,confined=False).comparison_group
    assert s.comparison_group==replace(s,complexity=True,nlay=3).comparison_group
    assert s.comparison_group!=replace(s,complexity=True,horizontal_2d=True).comparison_group


def test_plain_spacing_csv_format():
    text=formatted_csv(pd.DataFrame({'Δx (m)':[5.,10.,.5],'Δy (m)':[5.,10.,.5]}))
    assert text.splitlines()[1:]==['5,5','10,10','0.5,0.5']


def test_ui_visibility_previous_run_and_retention():
    at=app()
    assert not at.toggle(key='analytical').value
    assert at.toggle(key='show_cell_heads').value and at.toggle(key='show_cell_lines').value
    assert at.toggle(key='show_previous').disabled
    assert not any(t.key=='show_computed_heads' for t in at.toggle)
    assert any(e.label=='**Numerical solver**' for e in at.expander)
    at.button(key='run').click().run()
    assert at.session_state['last_profile']['run_id']==1
    first=dict(at.session_state['last_profile'])
    original_heads=list(at.session_state['runs'][-1]['heads'])
    at.toggle(key='show_cell_heads').set_value(False).run()
    assert not at.toggle(key='show_cell_lines').disabled
    assert not at.toggle(key='show_cell_heads').value and at.toggle(key='show_cell_lines').value
    # Switching off the final active style enables the other in the same rerun.
    at.toggle(key='show_cell_lines').set_value(False).run()
    assert at.toggle(key='show_cell_heads').value and not at.toggle(key='show_cell_lines').value
    at.toggle(key='show_cell_heads').set_value(False).run()
    assert not at.toggle(key='show_cell_heads').value and at.toggle(key='show_cell_lines').value
    at.toggle(key='show_cell_heads').set_value(True).run()
    assert at.toggle(key='show_cell_heads').value and at.toggle(key='show_cell_lines').value
    at.toggle(key='show_cell_lines').set_value(False).run()
    assert not at.toggle(key='show_cell_heads').disabled
    assert at.session_state['runs'][-1]['heads']==original_heads and len(at.session_state['runs'])==1
    assert at.session_state['last_profile']==first and not at.exception
    at.number_input(key='recharge').set_value(250.).run()
    assert not at.toggle(key='show_previous').disabled
    at.toggle(key='show_previous').set_value(True).run()
    at.button(key='run').click().run()
    assert at.session_state['previous_profile']==first
    assert at.session_state['last_profile']['run_id']==2 and len(at.session_state['runs'])==2
    table=next(d for d in at.dataframe if 'Name' in d.value.columns and 'WB discrep.' in d.value.columns)
    assert len(table.value)==2
    at.toggle(key='confined').set_value(False).run()
    assert len(at.session_state['runs'])==2
    at.toggle(key='complexity').set_value(True).run()
    assert at.selectbox(key='preview_quantity').value=='Empty cells'
    at.toggle(key='add_layers').set_value(True).run()
    assert len(at.session_state['runs'])==2
    at.selectbox(key='inspect_run').set_value(1).run()
    assert not at.exception
    at.toggle(key='horizontal_2d').set_value(True).run()
    assert not at.session_state['runs']
    assert at.session_state['last_profile'] is None and at.session_state['previous_profile'] is None
    assert not at.exception
