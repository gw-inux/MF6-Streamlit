"""v1.4: retain edited controls, exact grids, full cells and cloud binaries."""

# BEGIN CODE CONTENTS
# Manual edits: jump to these release line numbers (refresh with tools/update_code_map.py).
#   PROFILES: line 34
#   test_all_app_head_defaults_and_clean_si_flow_defaults: line 39
#   test_four_controls_follow_latest_edits_across_presets_and_methods: line 58
#   test_pcg_sip_share_head_and_iteration_limit_without_losing_flow_controls: line 87
#   test_spacing_count_switches_keep_geometry_and_dynamic_labels: line 101
#   test_full_cell_geometry_and_toggle_uses_native_node_heads: line 133
#   test_preview_equal_width_central_trace_actual_discrete_k: line 157
#   test_cloud_parent_bin_permissions_and_native_run: line 178
#   test_resolver_does_not_fallback_from_invalid_override: line 193
#   test_cloud_entrypoint_runs_same_interface: line 202
#   test_initial_heads_belong_to_scenario_and_repeats_are_beside_name: line 211
# END CODE CONTENTS

from pathlib import Path
import os
import shutil

import matplotlib.pyplot as plt
from matplotlib.colors import BoundaryNorm
import numpy as np
import pytest
from streamlit.testing.v1 import AppTest

from MODFLOW_Solver_lab import core
from MODFLOW_Solver_lab.core import Scenario, Solver, find_executable, run_once
from MODFLOW_Solver_lab.plots import head_plot, model_preview
from MODFLOW_Solver_lab.settings import (METHODS, new_profile, solver_from_profile, limits_summary)
from test_ui import app

PROFILES = [(e, m, p) for e, methods in METHODS.items() for m in methods
            for p in (['SIMPLE'] if e == 'mf2005' else ['SIMPLE','MODERATE','COMPLEX'])]


@pytest.mark.parametrize('engine,method,preset', PROFILES)
def test_all_app_head_defaults_and_clean_si_flow_defaults(engine, method, preset):
    profile = new_profile(engine, method, preset)
    for expert in (False, True):
        profile['expert_enabled'] = expert
        cfg = solver_from_profile(profile)
        h, flow, _, _ = limits_summary(cfg)
        assert h == 1e-4
        assert flow == (None if method == 'SIP' else {'mf2005':1e-4, 'mfnwt':5e-3, 'mf6':1e-4}[engine])
        if method == 'XMD':
            assert cfg.nwt_specified
            assert cfg.parameters()['hclosexmd'] == 1e-4
        if engine == 'mf6':
            assert cfg.parameters()['inner_dvclose'] == 1e-4


@pytest.mark.parametrize('engine,method,fields,other', [
    ('mfnwt','GMRES',('headtol','fluxtol','maxiterout','maxitinner'),'XMD'),
    ('mf6','CG',('outer_dvclose','rcloserecord','outer_maximum','inner_maximum'),'BICGSTAB'),
])
def test_four_controls_follow_latest_edits_across_presets_and_methods(engine,method,fields,other):
    at=app()
    at.selectbox(key='engine').set_value(engine).run()
    values=(2e-6, 3e-8, 173, 237)
    for field, value in zip(fields, values):
        at.number_input(key=f'{engine}_{method}_SIMPLE_basic_{field}').set_value(value)
    # Deliver edits and a new preset together: no intermediate rerun to save.
    at.selectbox(key=f'preset_{engine}').set_value('COMPLEX').run()
    cfg=Solver(**at.session_state['variants'][f'{engine}/{method}'])
    assert limits_summary(cfg) == values
    assert at.selectbox(key=f'method_{engine}').value == method
    at.selectbox(key=f'method_{engine}').set_value(other).run()
    assert limits_summary(Solver(**at.session_state['variants'][f'{engine}/{other}'])) == values
    second=(7e-5, 9e-7, 127, 349)
    other_fields=fields[:-1]+(('mxiterxmd',) if engine=='mfnwt' else (fields[-1],))
    for field,value in zip(other_fields,second):
        at.number_input(key=f'{engine}_{other}_COMPLEX_basic_{field}').set_value(value)
    at.toggle(key=f'{engine}_{other}_COMPLEX_expert_on').set_value(True).run()
    # Visit an old cached destination; it must use the new controls.
    at.selectbox(key=f'preset_{engine}').set_value('SIMPLE').run()
    at.selectbox(key=f'method_{engine}').set_value(method).run()
    assert limits_summary(Solver(**at.session_state['variants'][f'{engine}/{method}'])) == second
    # Switch model and return: keep that model's latest values.
    at.selectbox(key='engine').set_value('mf2005').run()
    at.selectbox(key='engine').set_value(engine).run()
    assert limits_summary(Solver(**at.session_state['variants'][f'{engine}/{method}'])) == second
    assert not at.exception


def test_pcg_sip_share_head_and_iteration_limit_without_losing_flow_controls():
    at=app()
    at.number_input(key='mf2005_PCG_SIMPLE_basic_hclose').set_value(3e-6)
    at.number_input(key='mf2005_PCG_SIMPLE_basic_rclose').set_value(2e-12)
    at.number_input(key='mf2005_PCG_SIMPLE_basic_iter1').set_value(456)
    at.selectbox(key='method_mf2005').set_value('SIP').run()
    assert at.number_input(key='mf2005_SIP_SIMPLE_basic_hclose').value==3e-6
    at.number_input(key='mf2005_SIP_SIMPLE_basic_mxiter').set_value(567)
    at.selectbox(key='method_mf2005').set_value('PCG').run()
    cfg=Solver(**at.session_state['variants']['mf2005/PCG'])
    assert limits_summary(cfg)==(3e-6,2e-12,567,456)
    assert not at.exception


def test_spacing_count_switches_keep_geometry_and_dynamic_labels():
    at=app()
    assert at.number_input(key='recharge').value == 150.
    assert not any(w.key=='width' for w in at.number_input)
    at.number_input(key='n').set_value(21).run()
    at.toggle(key='spacing_mode').set_value(True).run()
    assert at.number_input(key='cell_spacing').value==250.
    at.number_input(key='cell_spacing').set_value(125).run()
    assert at.session_state['grid_n']==41
    at.toggle(key='spacing_mode').set_value(False).run()
    assert at.number_input(key='n').value==41
    at.toggle(key='complexity').set_value(True).run()
    at.toggle(key='horizontal_2d').set_value(True).run()
    assert at.number_input(key='n').label=='Number of cells along x and y'
    assert not any(w.key=='plot_row' for w in at.number_input)
    at.toggle(key='spacing_mode').set_value(True).run()
    assert at.number_input(key='cell_spacing').label=='Cell spacing Δx / Δy (m)'
    at.number_input(key='cell_spacing').set_value(123).run()
    assert any('divide' in e.value for e in at.error)
    assert not any(b.key=='run' for b in at.button)
    at.number_input(key='cell_spacing').set_value(500)
    at.run()
    at.button(key='run').click().run()
    result=at.session_state['runs'][-1]
    assert result['success']
    assert result['scenario']['n']==11 and result['scenario']['horizontal_2d']
    at.toggle(key='show_cell_heads').set_value(False).run()
    assert len(at.session_state['runs'])==1
    assert any('Run 01:' in c.value for c in at.caption)
    assert not at.exception


def test_full_cell_geometry_and_toggle_uses_native_node_heads(tmp_path):
    s=Scenario(n=11)
    cfg=solver_from_profile(new_profile('mf2005','PCG'))
    r=run_once(s,cfg,tmp_path,find_executable('mf2005'))
    assert r['success']
    fig=head_plot(s,[r],settings=cfg)
    ax=fig.axes[0]
    assert ax.get_xlim()==(.5,11.5)
    dots=next(line for line in ax.lines if line.get_gid()=='cell_head_dots')
    np.testing.assert_array_equal(dots.get_xdata(),np.arange(1,12))
    np.testing.assert_array_equal(dots.get_ydata(),s.head_array(r['heads'])[0,0])
    domain=next(p for p in ax.patches if p.get_gid()=='model_domain')
    assert domain.get_x()==.5 and domain.get_width()==11
    assert len([p for p in ax.patches if p.get_gid()=='chd_cell'])==2
    fig.canvas.draw()
    top=ax.child_axes[0]
    np.testing.assert_allclose(top._functions[0](np.array([1.,11.])),[0.,s.length])
    hidden=head_plot(s,[r],cell_heads=False)
    assert not any(line.get_gid()=='cell_head_dots' for line in hidden.axes[0].lines)
    assert any(p.get_gid()=='cell_head_lines' for p in hidden.axes[0].collections)
    for f in [fig,hidden]: plt.close(f)


@pytest.mark.parametrize('horizontal,nlay',[(False,1),(True,1),(True,3)])
def test_preview_equal_width_central_trace_actual_discrete_k(horizontal,nlay):
    s=Scenario(n=11,complexity=True,horizontal_2d=horizontal,nlay=nlay,random_k=True,k_zones=3)
    before=s.k_field().copy()
    fig=model_preview(s,"K zones")
    fig.canvas.draw()
    plan,section,colorbar=fig.axes
    assert plan.get_position().width==pytest.approx(section.get_position().width,abs=1e-8)
    trace=next(l for l in plan.lines if l.get_gid()=='section_trace')
    np.testing.assert_allclose(trace.get_ydata(),s.nrow//2*s.dy)
    mesh=plan.collections[0]
    assert isinstance(mesh.norm,BoundaryNorm)
    assert mesh.cmap.N==s.k_zones
    assert colorbar.get_yticklabels()[0].get_text().startswith("1 · ")
    assert colorbar.get_yticklabels()[-1].get_text().startswith(f"{s.k_zones} · ")
    assert any(c.get_gid()=='grid_faces_x' for c in plan.collections)
    np.testing.assert_array_equal(s.k_field(),before)
    plt.close(fig)


@pytest.mark.skipif(os.name=='nt',reason='POSIX repository-bin deployment')
@pytest.mark.parametrize('engine,method,name', [('mf2005','PCG','mf2005dbl'),('mfnwt','GMRES','mfnwtdbl'),('mf6','CG','mf6')])
def test_cloud_parent_bin_permissions_and_native_run(engine,method,name,tmp_path,monkeypatch):
    source=find_executable(engine)
    assert source, f'{engine} required for deployment verification'
    root=tmp_path/'repository'/'solver_lab_v14';root.mkdir(parents=True)
    bindir=root.parent/'bin';bindir.mkdir()
    target=bindir/name;shutil.copyfile(source,target);target.chmod(0o644)
    monkeypatch.setattr(core,'ROOT',root)
    monkeypatch.chdir(tmp_path)
    for suffix in ['_EXE','_EXECUTABLE']: monkeypatch.delenv(engine.upper()+suffix,raising=False)
    found=find_executable(engine)
    assert found==str(target) and os.access(target,os.X_OK)
    r=run_once(Scenario(),solver_from_profile(new_profile(engine,method)),tmp_path/'isolated_run',found)
    assert r['success'] and r['metrics']['max_error_m']<.01


def test_resolver_does_not_fallback_from_invalid_override(tmp_path,monkeypatch):
    monkeypatch.setenv('MFNWT_EXE',str(tmp_path/'missing'))
    assert find_executable('mfnwt') is None
    if os.name!='nt':
        path=tmp_path/'mfnwt';path.write_bytes(b'MZ'+bytes(100));path.chmod(0o755)
        monkeypatch.setenv('MFNWT_EXE',str(path))
        assert find_executable('mfnwt') is None


def test_cloud_entrypoint_runs_same_interface():
    at=AppTest.from_file(str(Path(__file__).resolve().parents[1]/'streamlit_app.py'),default_timeout=90).run()
    assert not at.exception
    assert at.session_state['scenario_values']['recharge']==150.
    at.button(key='run').click().run()
    assert at.session_state['runs'][-1]['success']
    assert at.selectbox(key='inspect_run').value==1


def test_initial_heads_belong_to_scenario_and_repeats_are_beside_name():
    at=app()
    scenario=next(e for e in at.expander if e.label=='**Parameters for the scenario**')
    assert not any('Options for numerical model execution' in e.label for e in at.expander)
    assert scenario.selectbox(key='initial').value=='Mean boundary head'
    assert at.selectbox(key='repeats').value==1
    assert not any(w.key=='timeout' for w in at.number_input)
    at.selectbox(key='initial').set_value('Specified uniform head').run()
    at.number_input(key='initial_head').set_value(40.)
    at.button(key='run').click().run()
    assert not at.exception
    assert at.session_state['runs'][-1]['scenario']['initial_head']==40.
    assert at.session_state['runs'][-1]['success']
