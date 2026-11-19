## title

一维溶质运移实验室

## experiments

引导实验

## experiment_front

对流前缘

## experiment_spreading

物理弥散

## experiment_impulse

矩形脉冲与瞬时脉冲

## theory_title

流场与解析解

## setup

模型设置

## inlet_processes

入口与运移

## grid_time

网格与时间

## solver

MT3DMS 方法

## signal

入口信号

## continuous

连续输入

## block

矩形脉冲

## dirac

Dirac 瞬时脉冲

## amplitude

入口浓度 C/Cref [–]

## block_days

脉冲持续时间 [d]

## impulse_area

脉冲面积 A [d]

## impulse_days

数值脉冲宽度 ε [d]

## rectangle

MT3DMS 入口脉冲高度 = {height:.4g} C/Cref。

## dispersion

启用弥散

## dispersivity

纵向弥散度 αL [m]

## diffusion

有效分子扩散系数 Dₑ [m²/d]

## grid_by

网格定义方式

## cells

单元数

## spacing

单元宽度

## cell_count

单元

## target_spacing

目标单元宽度 [m]

## grid_summary

{n} 个单元 · 实际 Δx = {dx:.3g} m

## courant

Courant 数上限

## time_hint

所有方案均在第 2000 天结束。有限脉冲的输入期间至少包含八个运移时间步。

## scheme

对流格式

## upwind

有限差分 · 迎风

## central

有限差分 · 中心

## tvd

TVD · ULTIMATE

## moc

MOC

## mmoc

MMOC

## hmoc

HMOC

## solver_hint

MODFLOW-2005 提供稳态流场。MT3DMS 使用 GCG 求解隐式方程。

## preview

模型预览

## preview_summary

{signal} · {scheme} · {n} 个单元 · Δx = {dx:.3g} m · D = {D:.4g} m²/d

## distance

距入口距离 [m]

## time

时间 [d]

## inlet_axis

入口 C/Cref [–]

## optional_name

方案名称（可选）

## name_example

例如，细网格 TVD

## limit

已保存十个方案。请在“管理方案”中删除一个方案，再运行新方案。

## missing

所需可执行文件缺失或不兼容 — {names}。请放入共享 bin 文件夹或设置 TRANSPORT_LAB_BIN。

## run

运行模型

## running

正在运行 MODFLOW-2005 和 MT3DMS…

## failed

本次计算未完成。之前保存的方案可在下方查看。

## diagnostic

计算详情

## results

运移结果

## visible

图中显示的方案

## cells_unit

单元

## show_analytical

解析解

## show_markers

数值点

## profile

浓度剖面

## breakthrough

穿透曲线

## budget

溶质质量平衡

## profile_time

剖面时刻 [d]

## observation

观测距离 [m]

## applied_curve

解析解 · 实际输入

## ideal_curve

理想 Dirac 脉冲

## mass_axis

质量平衡误差 [%]

## no_selection

请选择一个方案以显示曲线。

## comparison

最终比较 · 第 2000 天

## variant

方案

## rmse

RMSE

## mae

MAE

## ideal_rmse

RMSE · 理想 Dirac

## mass_error

质量误差 [%]

## seconds

计算耗时 [s]

## run_name

名称

## dx_col

Δx [m]

## height_col

入口 C/Cref

## duration_col

输入时长 [d]

## area_col

Dirac A [d]

## alpha_col

αL [m]

## dm_col

Dₑ [m²/d]

## d_col

D [m²/d]

## pe_col

网格 Péclet 数

## co_col

Courant 数上限

## count_col

运移步数

## flow_s

MODFLOW [s]

## mt_s

MT3DMS [s]

## flow_error

水量平衡误差 [%]

## min_c

最终最小 C/Cref

## max_c

最终最大 C/Cref

## detail_heading

设置与指标定义

## download

下载比较表（CSV）

## manage

管理方案

## remove_choice

选择待删除方案

## remove

删除所选方案

## references_title

参考文献

## saved

已保存 V{number} 供比较。

## applied_color_key

解析解 · 方案颜色

## ideal_color_key

理想 Dirac · 方案颜色

## pulse_cells

脉冲长度 [单元]

## pulse_resolution

输入期间，脉冲随对流移动 {length:.3g} m，相当于 {cells:.3g} 个单元。

## specified_head

给定水头 · {head:.4g} m

## hydraulic_summary

水力传导系数 K = {k:.0e} m/s

## scenario_reset_hint

修改此处设置将清空已保存的比较方案。

## comparison_cleared

入口或运移设置已更改。比较结果已清空，可开始新情景。

## concept_title

概念模型与典型响应

## concept_inlet

入口

## concept_outlet

出口

## concept_observation

观测点

## concept_profile

t = {time:g} d 时的剖面

## concept_breakthrough

x = {distance:g} m 处的穿透曲线

## concept_advection

纯对流

## concept_dispersion

对流 + 弥散
