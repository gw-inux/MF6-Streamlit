"""v2.0: retained settings, groundwater surfaces and streamlined workflows."""

# BEGIN CODE CONTENTS
# Manual edits: jump to these release line numbers (refresh with tools/update_code_map.py).
#   APP: line 37
#   limited_app: line 40
#   dry_example: line 46
#   test_uppermost_wet_not_maximum_no_mutation: line 62
#   test_invalid_upper_cells_and_completely_dry_columns: line 73
#   test_at_bottom_is_dry_and_confined_head_is_potentiometric: line 82
#   test_surface_map_section_snapshot_and_wetted_cells_agree: line 92
#   test_stale_map_changes_palette_preserves_values_and_geometry: line 121
#   test_preview_updates_elevations_when_aquifer_type_changes: line 134
#   test_limited_scenario_retains_hidden_edits_and_initial_options: line 145
#   test_preview_and_k_realization_refresh_without_accidental_reseeding: line 172
#   test_analytical_enables_dots_and_green_reference: line 193
#   test_execution_timeout_and_repetition_dropdown: line 207
#   test_surface_map_stale_state_and_display_options_do_not_invalidate_run: line 226
#   test_native_dewatered_layers_surface_survives_dry_layer_one: line 257
# END CODE CONTENTS

from copy import deepcopy
from dataclasses import replace
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import pytest
from streamlit.testing.v1 import AppTest

from MODFLOW_Solver_lab.core import Scenario, Solver, run_once
from MODFLOW_Solver_lab.plots import (head_plot, computed_head_map, model_preview, profile_snapshot,
                   ANALYTICAL_GREEN, display_indices)
from MODFLOW_Solver_lab.surfaces import groundwater_surface
from test_models import executable
from test_complexity import strict

APP = str(Path(__file__).resolve().parents[1] / 'app.py')


def limited_app():
    at = AppTest.from_file(APP, default_timeout=90).run()
    assert not at.exception
    return at


def dry_example():
    s = Scenario(n=5, complexity=True, horizontal_2d=True, nlay=3,
                 confined=False, aquifer_top=30., left=18., right=16.)
    h = np.full(s.shape, 6.)
    h[0, :, 1] = 24.             # Perched upper wet cell: do not choose max head.
    h[1, :, 1] = 27.
    h[0, :, 2] = -1.e30          # MODFLOW dry sentinel.
    h[1, :, 2] = 15.
    h[:, :, 3] = 1.e30           # Entirely dry/invalid column must stay blank.
    h[0, :, 0] = 99.             # Inactive boundary cells must be ignored.
    h[1:, :, 0] = s.left
    h[0, :, -1] = 99.
    h[1:, :, -1] = s.right
    return s, h


def test_uppermost_wet_not_maximum_no_mutation():
    s, h = dry_example()
    original = h.copy()
    water, layers = groundwater_surface(s, h)
    expected = np.tile([18., 24., 15., np.nan, 16.], (s.nrow, 1))
    np.testing.assert_allclose(water, expected, equal_nan=True)
    np.testing.assert_array_equal(layers, np.tile([2, 1, 2, 0, 2], (s.nrow, 1)))
    np.testing.assert_array_equal(h, original)


@pytest.mark.parametrize('invalid', [np.nan, np.inf, -np.inf, 1e30, -1e30, 0.])
def test_invalid_upper_cells_and_completely_dry_columns(invalid):
    s = Scenario(n=5, complexity=True, nlay=3, confined=False, aquifer_top=30.)
    h = np.full(s.shape, invalid)
    h[2, 0, 2] = 3.
    water, layer = groundwater_surface(s, h)
    assert water[0, 2] == 3 and layer[0, 2] == 3
    assert np.isnan(water[0, 1]) and layer[0, 1] == 0


def test_at_bottom_is_dry_and_confined_head_is_potentiometric():
    s = Scenario(n=5, complexity=True, nlay=3, confined=False, aquifer_top=30.)
    h = np.full(s.shape, 5.)
    h[0, 0, 2], h[1, 0, 2] = 20., 10.  # Exactly the cell bottoms.
    assert groundwater_surface(s, h)[0][0, 2] == 5.
    confined = replace(s, confined=True)
    h[:, 0, 2] = [18., 19., 20.]
    assert groundwater_surface(confined, h)[0][0, 2] == 18.


def test_surface_map_section_snapshot_and_wetted_cells_agree():
    s, h = dry_example()
    r = dict(heads=h.ravel().tolist(), success=True, run_id=1, run_name='Dry upper cells')
    water, _ = groundwater_surface(s, h)
    map_fig = computed_head_map(s, h)
    mesh = next(c for c in map_fig.axes[0].collections if c.get_gid() == 'groundwater_surface')
    np.testing.assert_allclose(mesh.get_array().filled(np.nan), water, equal_nan=True)
    fig = head_plot(s, [r], surface=True, initial=False)
    dots = next(l for l in fig.axes[0].lines if l.get_gid() == 'cell_head_dots')
    np.testing.assert_allclose(dots.get_ydata(), water[s.nrow//2], equal_nan=True)
    saved = profile_snapshot(s, r, surface=True)
    assert saved['surface']
    np.testing.assert_allclose(saved['head_m'], water[s.nrow//2, display_indices(s.n)], equal_nan=True)
    fills = [c for c in fig.axes[0].collections if c.get_gid() == 'wetted_cells']
    assert len(fills) == 3
    # Upper layer has exactly one wet cell; isolated wet cells must still fill.
    assert len(fills[0].get_paths()) == 1
    top_cell = fills[0].get_paths()[0].vertices
    assert min(top_cell[:, 0]) == 1.5 and max(top_cell[:, 0]) == 2.5
    assert min(top_cell[:, 1]) == 20. and max(top_cell[:, 1]) == 24.
    for fill in fills:
        assert all(not (p.vertices[:, 0].min() == 3.5) for p in fill.get_paths())
    preview = model_preview(s, 'Computed heads', heads=h)
    np.testing.assert_allclose(preview.axes[0].collections[0].get_array().filled(np.nan), water, equal_nan=True)
    assert len([p for p in preview.axes[0].patches if p.get_gid() == 'preview_chd']) == 2
    for f in (map_fig, fig, preview):
        plt.close(f)


def test_stale_map_changes_palette_preserves_values_and_geometry():
    s, h = dry_example()
    fig = computed_head_map(s, h, stale=True)
    mesh = next(c for c in fig.axes[0].collections if c.get_gid() == 'groundwater_surface')
    assert mesh.cmap.name == 'Greys'
    np.testing.assert_allclose(mesh.get_array().filled(np.nan), groundwater_surface(s, h)[0], equal_nan=True)
    assert 'rerun required' in fig.axes[0].get_title()
    assert fig.axes[0].get_aspect() == 1.
    assert fig.axes[0].get_xlim() == (-s.dx/2, s.length+s.dx/2)
    plt.close(fig)


@pytest.mark.parametrize('quantity', ['Empty cells', 'K zones', 'Initial heads'])
def test_preview_updates_elevations_when_aquifer_type_changes(quantity):
    s = Scenario(complexity=True, horizontal_2d=True, nlay=3, random_k=True)
    first = model_preview(s, quantity)
    second = model_preview(replace(s, confined=False, aquifer_top=35.), quantity)
    assert first.axes[1].get_ylim() == (-20., 0.)
    assert second.axes[1].get_ylim() == (0., 35.)
    assert first.axes[0].get_aspect() == second.axes[0].get_aspect() == 1.
    plt.close(first)
    plt.close(second)


def test_limited_scenario_retains_hidden_edits_and_initial_options():
    at = limited_app()
    assert not at.toggle(key='full_settings').value
    assert not any(w.key in ('k', 'recharge', 'left', 'thickness') for w in at.number_input)
    assert any('1.00E-04' in m.value and '150' in m.value for m in at.markdown)
    at.toggle(key='full_settings').set_value(True).run()
    for key, value in dict(k=2e-4, recharge=180., left=19., thickness=25.).items():
        at.number_input(key=key).set_value(value)
    at.selectbox(key='initial').set_value('Random distribution').run()
    at.number_input(key='initial_min').set_value(12.)
    at.number_input(key='initial_max').set_value(32.)
    at.number_input(key='initial_seed').set_value(39)
    at.toggle(key='full_settings').set_value(False).run()
    at.run()  # A further rerun after Streamlit cleans up hidden widget keys.
    expected = dict(k=2e-4, recharge=180., left=19., thickness=25., initial_min=12., initial_max=32., initial_seed=39)
    for key, value in expected.items():
        assert at.session_state['scenario_values'][key] == value
    at.toggle(key='confined').set_value(False).run()
    at.number_input(key='aquifer_top').set_value(35.).run()
    at.toggle(key='full_settings').set_value(True).run()
    assert at.number_input(key='k').value == 2e-4
    assert at.number_input(key='initial_seed').value == 39
    at.toggle(key='confined').set_value(True).run()
    assert at.number_input(key='thickness').value == 25.
    assert not at.exception


def test_preview_and_k_realization_refresh_without_accidental_reseeding():
    at = limited_app()
    at.toggle(key='complexity').set_value(True).run()
    at.toggle(key='random_k').set_value(True).run()
    assert not any(w.key == 'k_seed' for w in at.number_input)
    first = deepcopy(at.session_state['complexity_options'])
    at.toggle(key='confined').set_value(False).run()
    assert any('top 20 m · bottom 0 m' in c.value for c in at.caption)
    at.number_input(key='aquifer_top').set_value(35.).run()
    assert any('top 35 m · bottom 0 m' in c.value for c in at.caption)
    assert at.session_state['complexity_options']['k_seed'] == first['k_seed']
    at.button(key='regenerate_k').click().run()
    assert at.session_state['complexity_options']['k_seed'] == first['k_seed'] + 1
    at.toggle(key='complexity').set_value(False).run()
    at.run()
    at.toggle(key='complexity').set_value(True).run()
    assert at.session_state['complexity_options']['k_seed'] == first['k_seed'] + 1
    assert at.toggle(key='random_k').value
    assert not at.exception


def test_analytical_enables_dots_and_green_reference():
    at = limited_app()
    at.toggle(key='show_cell_heads').set_value(False).run()
    at.toggle(key='analytical').set_value(True).run()
    assert at.toggle(key='show_cell_heads').value and at.toggle(key='show_cell_lines').value
    at.toggle(key='show_cell_heads').set_value(False).run()
    at.toggle(key='show_cell_lines').set_value(False).run()
    assert at.toggle(key='show_cell_heads').value
    fig = head_plot(Scenario(), analytical=True, initial=False)
    line = next(l for l in fig.axes[0].lines if l.get_label() == 'Analytical solution')
    assert line.get_color() == ANALYTICAL_GREEN and line.get_linewidth() < 1.
    plt.close(fig)


def test_execution_timeout_and_repetition_dropdown(monkeypatch, tmp_path):
    from MODFLOW_Solver_lab import results
    received = []
    def record(*args):
        received.append(args)
        return {'success': True}
    monkeypatch.setattr(results, 'run_repeated', record)
    assert results.execute(Scenario(), Solver('mf2005'), tmp_path, 10, {'mf2005': '/engine'})['success']
    assert received[0][-2:] == (10, 120.)
    at = limited_app()
    count = at.selectbox(key='repeats')
    assert count.value == 1 and count.options == [str(i) for i in range(1, 11)]
    assert not any(w.key == 'timeout' for w in at.number_input)
    assert not any('execution**' in e.label for e in at.expander)
    headings = [v.value for v in at.subheader]
    assert headings[-4:] == ['Model execution and postprocessing', 'Further run analysis and comparison',
                             'Grid refinement experiment', 'Conclusion and references']


def test_surface_map_stale_state_and_display_options_do_not_invalidate_run():
    at = limited_app()
    at.toggle(key='complexity').set_value(True).run()
    at.toggle(key='horizontal_2d').set_value(True).run()
    at.toggle(key='add_layers').set_value(True).run()
    at.button(key='run').click().run()
    assert at.session_state['runs'][-1]['success']
    label = '**Computed heads · groundwater surface (x–y)**'
    def stale():
        box = next(e for e in at.expander if e.label == label)
        return any('grey map' in c.value for c in box.caption)
    assert not stale()
    for edit in (lambda: at.selectbox(key='repeats').set_value(2),
                 lambda: at.number_input(key='plot_layer').set_value(3),
                 lambda: at.text_input(key='run_name').set_value('Next experiment')):
        edit().run()
        assert not stale()
    at.toggle(key='confined').set_value(False).run()
    assert stale() and len(at.session_state['runs']) == 1
    at.button(key='run').click().run()
    assert at.session_state['runs'][-1]['success'] and not stale()
    at.toggle(key='random_k').set_value(True).run()
    assert stale()
    at.button(key='run').click().run()
    assert not stale()
    at.button(key='regenerate_k').click().run()
    assert stale() and len(at.session_state['runs']) == 3
    assert not at.exception


@pytest.mark.parametrize('engine,method', [('mf2005','PCG'), ('mfnwt','GMRES'), ('mf6','CG')])
def test_native_dewatered_layers_surface_survives_dry_layer_one(engine, method, tmp_path):
    s = Scenario(n=7, complexity=True, horizontal_2d=True, nlay=5, confined=False,
                 left=8., right=5., recharge_mmy=10., initial='Specified uniform head', initial_head=20.)
    r = run_once(s, strict(engine,method), tmp_path, executable(engine))
    assert r['success']
    h = s.head_array(r['heads'])
    water, source = groundwater_surface(s, h)
    assert np.isfinite(water).all()
    assert np.all(source[:,0] == 4) and np.all(source[:,-1] == 4)
    for row in range(s.nrow):
        for col in range(s.n):
            wet = [v for v in h[:,row,col] if np.isfinite(v)]
            assert water[row,col] == wet[0]
    assert np.isnan(h[0]).any()
    assert abs(r['budget_percent']) < .01
