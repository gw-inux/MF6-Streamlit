# Code map — MODFLOW Solver Lab

These line numbers match this release. Open the named file and use your
editor's Go to line command. Each Python module also starts with its own contents.

Common edits: solver defaults and cell limit in `core.py`; widget labels and
page order in `app.py`; input layout in `inputs.py`; execution and inspection
in `results.py`; grid studies in `studies.py`; surface selection in `surfaces.py`;
web colours in `ui.py`; figures and marker thinning in `plots.py`;
integer spacing steps in `spacing.py`; closure markers in `diagnostic_guides.py`;
the bounded computed-map image cache in `map_rendering.py`;
Markdown text in `assets/md/en/` (see `CONTENT_GUIDE.md`); loading in `content.py`.
Guided experiment tabs and the document-only route in `experiments.py`.
iNUX question blocks in `assessments.py`; Markdown task rendering in `checklists.py`.
The commented FIGS example is in `app.py`. Native construction remains in `build_model`.

After manual changes, refresh these references with:

```sh
python tools/update_code_map.py
```

## __init__.py

| Editing location | Line |
|---|---:|

## app.py

| Editing location | Line |
|---|---:|
| `initialize_session` | 97 |
| `retain_comparable_runs` | 133 |
| `1 — Introduction and numerical background. Edit prose in assets/md/en.` | 157 |
| `Optional repository figure. Keep this block commented until the image` | 162 |
| `Guided workflows share Markdown with their independent reading tabs.` | 175 |
| `2 — Scenario, spatial discretization and numerical solver inputs.` | 179 |
| `3 — Additional complexity and live preview use the current validated inputs.` | 208 |
| `4 — Execution, plotted heads, run comparison and native diagnostics.` | 221 |
| `5 — Grid refinement is an independent subsection with a reviewable plan.` | 226 |
| `6 — Conclusion and primary documentation.` | 229 |

## inputs.py

| Editing location | Line |
|---|---:|
| `INITIAL_DISTRIBUTIONS` | 35 |
| `capture_input_values` | 43 |
| `scenario_controls` | 73 |
| `set_cell_spacing` | 162 |
| `spatial_controls` | 168 |
| `solver_controls` | 276 |
| `regenerate_k` | 322 |
| `select_k_preview` | 329 |
| `complexity_controls` | 335 |
| `render_model_preview` | 422 |

## results.py

| Editing location | Line |
|---|---:|
| `TIMEOUT_SECONDS` | 48 |
| `execute` | 51 |
| `keep_head_style` | 80 |
| `enable_analytical_points` | 85 |
| `model_summary` | 90 |
| `render_visibility` | 120 |
| `render_computed_map` | 189 |
| `initial_grid_notes` | 221 |
| `render_execution` | 228 |
| `render_run_comparison` | 332 |
| `render_diagnostics` | 398 |

## studies.py

| Editing location | Line |
|---|---:|
| `render_grid_study` | 29 |

## surfaces.py

| Editing location | Line |
|---|---:|
| `groundwater_surface` | 17 |

## ui.py

| Editing location | Line |
|---|---:|
| `APP_STYLE` | 20 |
| `apply_style` | 71 |
| `style_computed_map` | 75 |
| `show_fig` | 85 |
| `show_table` | 90 |

## spacing.py

| Editing location | Line |
|---|---:|
| `SPACING_STEPS` | 20 |
| `valid_spacing_steps` | 24 |
| `adjacent_spacing` | 36 |
| `integer_spacing_for_grid` | 44 |

## diagnostic_guides.py

| Editing location | Line |
|---|---:|
| `convergence_guides` | 16 |

## map_rendering.py

| Editing location | Line |
|---|---:|
| `HEAD_MAP_DPI` | 24 |
| `head_map_image` | 27 |

## core.py

| Editing location | Line |
|---|---:|
| `ROOT` | 82 |
| `ENGINE_NAMES` | 83 |
| `EXE_NAMES` | 84 |
| `SECONDS_PER_DAY` | 89 |
| `SECONDS_PER_YEAR` | 90 |
| `MAX_CELLS` | 91 |
| `DEFAULT_HEAD_CLOSE` | 92 |
| `DEFAULT_FLOW_CLOSE` | 94 |
| `Scenario` | 98 |
| `Scenario.validate` | 123 |
| `Scenario.nrow` | 156 |
| `Scenario.shape` | 160 |
| `Scenario.total_cells` | 164 |
| `Scenario.grid_label` | 168 |
| `Scenario.dy` | 172 |
| `Scenario.botm` | 176 |
| `Scenario.z_centres` | 180 |
| `Scenario.analytical_available` | 185 |
| `Scenario.comparison_group` | 191 |
| `Scenario.active_mask` | 196 |
| `Scenario.chd_mask` | 205 |
| `Scenario.k_field` | 210 |
| `Scenario.top` | 223 |
| `Scenario.bottom` | 227 |
| `Scenario.aquifer_label` | 231 |
| `Scenario.dx` | 235 |
| `Scenario.x` | 239 |
| `Scenario.recharge_ms` | 243 |
| `Scenario.transmissivity` | 247 |
| `Scenario.discharge_potential` | 251 |
| `Scenario.analytic` | 260 |
| `Scenario.starting_heads` | 274 |
| `Scenario.head_array` | 285 |
| `Scenario.heads_table` | 292 |
| `NWT_PRESETS` | 306 |
| `IMS_PRESETS` | 323 |
| `Solver` | 346 |
| `Solver.label` | 354 |
| `Solver.parameters` | 357 |
| `usable_executable` | 392 |
| `find_executable` | 413 |
| `find_library` | 445 |
| `build_model` | 457 |
| `fingerprint` | 541 |
| `head_metrics` | 545 |
| `read_native_budget` | 599 |
| `read_face_flows` | 625 |
| `NUMBER` | 632 |
| `parse_diagnostics` | 635 |
| `run_once` | 728 |
| `run_repeated` | 777 |
| `comparison_row` | 792 |
| `record_mf6` | 810 |

## settings.py

| Editing location | Line |
|---|---:|
| `METHODS` | 42 |
| `VARIANTS` | 43 |
| `MAX_RUNS` | 44 |
| `GRID_DEFAULTS` | 45 |
| `NWT_GMRES` | 46 |
| `NWT_XMD` | 47 |
| `new_profile` | 50 |
| `MAIN_FIELDS` | 88 |
| `remember_main_controls` | 96 |
| `capture_active_profile` | 102 |
| `select_profile` | 126 |
| `solver_from_profile` | 143 |
| `default_variants` | 168 |
| `effective_settings` | 172 |
| `limits_summary` | 185 |
| `preset_label` | 195 |
| `variant_plan` | 203 |
| `parse_grid_entries` | 217 |
| `append_run` | 232 |
| `parse_grid_spacings` | 237 |
| `remove_runs` | 261 |
| `run_table` | 266 |
| `display_number` | 275 |
| `settings_table` | 285 |
| `SPACING_COLUMNS` | 290 |
| `INTEGER_COLUMNS` | 292 |
| `formatted_csv` | 296 |

## controls.py

| Editing location | Line |
|---|---:|
| `number` | 16 |
| `basic_controls` | 42 |
| `expert_controls` | 109 |

## plots.py

| Editing location | Line |
|---|---:|
| `BLUE` | 43 |
| `ANALYTICAL_GREEN` | 44 |
| `CHD_BLUE` | 45 |
| `CHD_FILL` | 46 |
| `TEXT` | 47 |
| `PREVIOUS_BLUE` | 48 |
| `FAILED_RED` | 49 |
| `FAILED_FILL` | 50 |
| `MAX_VISIBLE_NODES` | 51 |
| `COLORS` | 52 |
| `STYLE` | 53 |
| `themed` | 59 |
| `display_stride` | 68 |
| `display_indices` | 73 |
| `profile_snapshot` | 78 |
| `head_plot` | 96 |
| `error_plot` | 258 |
| `convergence_plot` | 282 |
| `model_preview` | 322 |
| `computed_head_map` | 429 |
| `first_layer_head_map` | 482 |
| `grid_study_plot` | 488 |

## content.py

| Editing location | Line |
|---|---:|
| `English stays the default. A future language selector can pass a language` | 34 |
| `DEFAULT_LANGUAGE` | 36 |
| `MD_DIRECTORY` | 37 |
| `TEXT_FILES` | 38 |
| `LEARNING_TEXT_KEYS` | 47 |
| `SECTION_HEADER` | 57 |
| `ContentError` | 60 |
| `_language_directory` | 64 |
| `load_md` | 71 |
| `_sections` | 93 |
| `load_text` | 109 |
| `load_learning_text` | 126 |
| `These names keep the established presentation imports unchanged.` | 144 |
| `INTRODUCTION` | 147 |
| `ASSUMPTIONS` | 148 |
| `SOLVER_DETAILS` | 149 |
| `CONCLUSION` | 150 |
| `REFERENCES` | 151 |
| `TEXT` | 152 |

## experiments.py

| Editing location | Line |
|---|---:|
| `Keep this order aligned with the three tab labels below. These filenames` | 30 |
| `EXPERIMENT_FILES` | 32 |
| `EXPERIMENT_STYLE` | 34 |
| `document_url` | 56 |
| `render_prose` | 63 |
| `render_experiment_text` | 72 |
| `render_document_view` | 84 |
| `render_experiments` | 112 |

## assessments.py

| Editing location | Line |
|---|---:|
| `QUESTIONS_DIRECTORY` | 33 |
| `QUESTION_FIELDS` | 34 |
| `ANSWERS_KEY` | 35 |
| `unique_object` | 38 |
| `validate_questions` | 48 |
| `load_questions` | 69 |
| `evaluate_answer` | 86 |
| `question_signature` | 97 |
| `remember_option` | 102 |
| `toggle_assessment` | 109 |
| `render_question` | 113 |
| `render_assessment` | 141 |

## checklists.py

| Editing location | Line |
|---|---:|
| `TASK_LINE` | 26 |
| `FENCE_LINE` | 29 |
| `PROGRESS_KEY` | 30 |
| `ChecklistTask` | 34 |
| `parse_checklist` | 42 |
| `remember_check` | 79 |
| `render_checklist` | 85 |

## streamlit_app.py

| Editing location | Line |
|---|---:|
| `APP_ROOT` | 18 |
| `PACKAGE_PARENT` | 23 |

## install_engines.py

| Editing location | Line |
|---|---:|
| `main` | 16 |

## api_worker.py

| Editing location | Line |
|---|---:|
| `main` | 14 |

## tools/update_code_map.py

| Editing location | Line |
|---|---:|
| `ROOT` | 23 |
| `FILES` | 24 |
| `BEGIN` | 29 |
| `END` | 30 |
| `PATTERN` | 31 |
| `entries` | 34 |
| `refresh` | 55 |
| `main` | 76 |

## ../MODFLOW_Solver_lab.py

| Editing location | Line |
|---|---:|
| `APP_DIRECTORY` | 15 |

## tests/conftest.py

| Editing location | Line |
|---|---:|

## tests/test_complexity.py

| Editing location | Line |
|---|---:|
| `strict` | 31 |
| `independent_confined_solution` | 44 |
| `test_defaults_and_reproducible_fields` | 82 |
| `test_seconds_and_written_geometry` | 107 |
| `test_confined_models_against_independent_darcy_solution` | 138 |
| `test_unconfined_dry_layers_and_recharge_routing` | 151 |
| `test_sip_dry_start_failure_is_retained` | 167 |
| `test_invalid_complex_inputs_do_not_allocate_large_models` | 183 |
| `test_spacing_and_fixed_layer_geometry` | 188 |
| `test_plot_runtime_head_visibility_and_model_previews` | 200 |
| `test_ui_dimensions_latest_inspection_and_complex_grid_study` | 216 |

## tests/test_final_revision.py

| Editing location | Line |
|---|---:|
| `PROFILES` | 34 |
| `test_all_app_head_defaults_and_clean_si_flow_defaults` | 39 |
| `test_four_controls_follow_latest_edits_across_presets_and_methods` | 58 |
| `test_pcg_sip_share_head_and_iteration_limit_without_losing_flow_controls` | 87 |
| `test_spacing_count_switches_keep_geometry_and_dynamic_labels` | 101 |
| `test_full_cell_geometry_and_toggle_uses_native_node_heads` | 133 |
| `test_preview_equal_width_central_trace_actual_discrete_k` | 157 |
| `test_cloud_parent_bin_permissions_and_native_run` | 178 |
| `test_resolver_does_not_fallback_from_invalid_override` | 193 |
| `test_cloud_entrypoint_runs_same_interface` | 202 |
| `test_initial_heads_belong_to_scenario_and_repeats_are_beside_name` | 211 |

## tests/test_grid_guides_revision.py

| Editing location | Line |
|---|---:|
| `test_grid_guides_follow_cell_faces_and_preserve_model_grid` | 25 |
| `test_repeat_aggregation_keeps_an_earlier_failure` | 55 |
| `test_error_band_is_the_y_row_range_and_line_is_the_middle_row` | 69 |

## tests/test_guided_experiments.py

| Editing location | Line |
|---|---:|
| `APP` | 29 |
| `ENTRYPOINTS` | 30 |
| `start_app` | 33 |
| `test_three_tabs_share_the_document_view_content` | 41 |
| `test_document_view_stops_before_model_initialization` | 62 |
| `test_document_route_only_accepts_listed_experiments` | 82 |
| `test_other_query_parameters_leave_normal_model_available` | 92 |
| `test_missing_experiment_has_a_readable_error_without_breaking_model` | 102 |
| `test_reading_view_does_not_change_an_existing_model_run` | 120 |

## tests/test_head_map_revision.py

| Editing location | Line |
|---|---:|
| `test_preview_chd_is_opaque_and_uniform_in_both_views` | 27 |
| `test_head_map_uses_only_native_layer_one_without_mutating_heads` | 50 |
| `test_head_map_of_dry_first_layer_is_blank_with_an_explanation` | 73 |
| `test_heterogeneity_tag_matches_the_sampled_field` | 93 |
| `test_ui_surface_map_and_reordered_numeric_comparison` | 104 |

## tests/test_import_isolation.py

| Editing location | Line |
|---|---:|
| `APP` | 19 |
| `test_all_entrypoints_ignore_and_preserve_foreign_modules` | 23 |
| `test_partial_content_update_has_readable_message_and_cannot_run` | 43 |
| `test_missing_package_marker_has_readable_message` | 53 |

## tests/test_learning_revision.py

| Editing location | Line |
|---|---:|
| `APP` | 40 |
| `BANKS` | 41 |
| `EXAMPLE` | 43 |
| `start_app` | 47 |
| `select_answer` | 53 |
| `test_banks_use_the_existing_inux_schema_and_markdown` | 63 |
| `test_all_reviewed_questions_require_the_complete_correct_selection` | 74 |
| `test_invalid_question_banks_fail_clearly` | 96 |
| `test_duplicate_option_text_is_not_silently_overwritten` | 101 |
| `test_assessment_paths_are_confined_to_language_resources` | 117 |
| `test_assessment_translation_fallback_and_manual_edits` | 122 |
| `test_instruction_files_have_stable_checks_and_no_embedded_assessments` | 139 |
| `test_checklist_parser_retains_equations_tables_and_fenced_examples` | 151 |
| `test_invalid_checklist_ids_fail_clearly` | 166 |
| `test_question_blocks_feedback_and_choices_survive_collapsing_and_model_edits` | 171 |
| `test_progress_and_assessments_do_not_change_a_saved_native_run` | 198 |
| `test_missing_assessment_is_scoped_to_its_panel` | 229 |

## tests/test_learning_startup.py

| Editing location | Line |
|---|---:|
| `APP` | 21 |
| `ENTRIES` | 22 |
| `test_learning_views_load_their_own_markdown_with_an_older_registry` | 27 |
| `test_missing_learning_key_is_actionable_and_does_not_raise_keyerror` | 53 |
| `test_old_content_module_has_a_clear_startup_message` | 71 |
| `test_learning_labels_keep_markdown_translation_fallback_and_manual_edits` | 79 |

## tests/test_markdown_content.py

| Editing location | Line |
|---|---:|
| `editable_content` | 26 |
| `test_content_loading_is_independent_of_working_directory` | 33 |
| `test_partial_translation_falls_back_per_document_and_text_key` | 41 |
| `test_unknown_language_has_complete_english_fallback` | 58 |
| `test_manual_edits_are_read_on_the_next_load` | 63 |
| `test_missing_required_markdown_has_a_clear_error` | 69 |
| `test_invalid_snippet_documents_fail_clearly` | 83 |
| `test_duplicate_keys_across_files_are_rejected` | 88 |
| `test_language_argument_is_a_code_not_a_path` | 96 |
| `test_every_interface_key_is_used_and_every_reference_exists` | 101 |

## tests/test_minor_revision.py

| Editing location | Line |
|---|---:|
| `test_result_layer_interfaces` | 22 |
| `test_old_both_off_state_recovers_and_callbacks_stay_enabled` | 46 |

## tests/test_models.py

| Editing location | Line |
|---|---:|
| `baseline` | 24 |
| `CHOICES` | 29 |
| `executable` | 33 |
| `test_exact_discrete_equation` | 41 |
| `test_heads_counts_and_budgets` | 55 |
| `test_native_presets` | 97 |
| `test_nwt_specified_matches_native` | 105 |
| `test_nonconvergence_is_not_success` | 117 |
| `test_api_real_outer_heads` | 123 |
| `test_nwt_noflow_complex_nonexact_start` | 141 |
| `test_invalid_physical_inputs` | 149 |
| `test_missing_explicit_executable_does_not_fallback` | 154 |

## tests/test_polish_revision.py

| Editing location | Line |
|---|---:|
| `test_full_settings_lives_in_scenario_and_keeps_values` | 32 |
| `test_random_k_switches_preview_only_on_activation` | 45 |
| `test_preferred_spacing_sequence_both_directions` | 60 |
| `test_integer_initialization_keeps_length_and_integral_spacings` | 75 |
| `test_integer_spacing_buttons_manual_values_and_invalid_geometry` | 79 |
| `test_spacing_modes_honor_three_cell_and_active_cell_limits` | 110 |
| `test_guides_from_actual_saved_solver` | 132 |
| `test_residual_norms_are_not_conflated` | 147 |
| `test_plot_thresholds_preserve_data_and_handle_zero_values` | 155 |
| `test_inspected_run_threshold_is_not_replaced_by_current_inputs` | 171 |
| `test_head_map_cache_reuses_exact_source_and_invalidates_any_head` | 187 |

## tests/test_presentation_revision.py

| Editing location | Line |
|---|---:|
| `test_initial_guidance_disappears_after_scenario_edit_and_stays_dismissed` | 20 |
| `test_initial_guidance_dismisses_after_a_native_run_and_table_clear` | 31 |
| `test_plot_guidance_is_limited_to_the_initial_grid_and_preserves_geometry` | 45 |
| `test_failed_repeated_result_marks_status_and_legend_even_with_no_heads` | 58 |

## tests/test_revision.py

| Editing location | Line |
|---|---:|
| `baseline` | 29 |
| `tight_solver` | 35 |
| `test_unconfined_reference_matches_dupuit_and_confined_limits` | 48 |
| `test_reference_crossing_top_preserves_potential_balance_and_boundaries` | 59 |
| `test_native_unconfined_results_and_face_balances` | 77 |
| `test_unconfined_refinement_reduces_error` | 90 |
| `test_unconfined_ui_presets_with_real_engines` | 103 |
| `test_unconfined_diagnostics_reject_dry_heads_and_missing_flows` | 110 |
| `test_hidden_initial_heads_do_not_affect_plot_extent_or_model_guess` | 118 |
| `test_grid_fields_reject_invalid_studies` | 134 |
| `test_geometry_visibility_and_grid_field_workflow` | 139 |

## tests/test_settings.py

| Editing location | Line |
|---|---:|
| `PROFILES` | 18 |
| `test_ui_suggested_profiles_run_with_native_engines` | 24 |
| `test_nwt_basic_inner_edit_is_written_and_used` | 38 |
| `test_custom_grids_reject_invalid_counts` | 53 |
| `test_custom_grid_order_and_table_precision` | 58 |
| `test_mf6_expert_residual_option_and_damping_run` | 67 |

## tests/test_streamlined_revision.py

| Editing location | Line |
|---|---:|
| `APP` | 37 |
| `limited_app` | 40 |
| `dry_example` | 46 |
| `test_uppermost_wet_not_maximum_no_mutation` | 62 |
| `test_invalid_upper_cells_and_completely_dry_columns` | 73 |
| `test_at_bottom_is_dry_and_confined_head_is_potentiometric` | 82 |
| `test_surface_map_section_snapshot_and_wetted_cells_agree` | 92 |
| `test_stale_map_changes_palette_preserves_values_and_geometry` | 121 |
| `test_preview_updates_elevations_when_aquifer_type_changes` | 134 |
| `test_limited_scenario_retains_hidden_edits_and_initial_options` | 145 |
| `test_preview_and_k_realization_refresh_without_accidental_reseeding` | 172 |
| `test_analytical_enables_dots_and_green_reference` | 193 |
| `test_execution_timeout_and_repetition_dropdown` | 207 |
| `test_surface_map_stale_state_and_display_options_do_not_invalidate_run` | 226 |
| `test_native_dewatered_layers_surface_survives_dry_layer_one` | 257 |

## tests/test_ui.py

| Editing location | Line |
|---|---:|
| `app` | 16 |
| `test_solver_switching_presets_and_expert_controls` | 24 |
| `test_named_runs_cap_deletion_stale_plot_and_failed_run` | 65 |

## tests/test_view_revision.py

| Editing location | Line |
|---|---:|
| `result` | 28 |
| `test_head_styles_keep_identical_wetted_filling_without_major_grid` | 34 |
| `test_previous_profile_is_small_hollow_and_uses_original_physical_coordinates` | 54 |
| `test_dense_result_symbols_are_thinned_but_all_cell_heads_and_fill_remain` | 72 |
| `test_plan_equal_scales_and_width_with_thinned_grid` | 84 |
| `test_limit_and_comparison_group_requirements` | 102 |
| `test_plain_spacing_csv_format` | 114 |
| `test_ui_visibility_previous_run_and_retention` | 119 |

## tests/test_workflows.py

| Editing location | Line |
|---|---:|
| `test_grid_studies_use_saved_settings_and_exclude_unselected_variants` | 13 |
