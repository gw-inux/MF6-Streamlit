<!-- key: title -->
MT3D – 二维/三维运移实验室

<!-- key: intro_caption -->
示意图：羽流和突破曲线示例，与当前模型输入无关。

<!-- key: Model & run -->
1 · 模型与运行

<!-- key: Results & method comparison -->
2 · 结果与方法比较

<!-- key: series_reset -->
输入信号或模型/源区几何发生变化，已开始新的比较系列，并清除之前的运行。

<!-- key: grid_summary -->
网格：{nx} × {ny} × {nz} 个单元。实际尺寸：Δx = {dx:.3f} m；Δy = {dy:.3f} m；Δz = {dz:.3f} m。

<!-- key: velocity_summary -->
均质参考孔隙水流速：{velocity:.4f} m/天。

<!-- key: source_bounds -->
x = {x0:.2f}–{x1:.2f} m; y = {y0:.2f}–{y1:.2f} m; z = {z0:.2f}–{z1:.2f} m.

<!-- key: source_snap_hint -->
源区由所选单元构成，网格分辨率变化可能改变其实际尺寸。按单元宽度输入时保持模型总范围不变，并显示实际均匀间距。

<!-- key: input_error -->
运行前请修正提示的模型设置。

<!-- key: missing_executables -->
缺少程序：{names}。请将兼容的可执行文件放入应用或仓库的 `bin/`。本地安装可运行 `python setup_executables.py`。

<!-- key: label_placeholder -->
自动：01 TVD / Pulse（非均质：/ het.）

<!-- key: history_full -->
已保存十次运行。请移除一次运行或清空系列后继续。

<!-- key: running -->
正在运行 MODFLOW、MT3D 及可选的 MODPATH…

<!-- key: run_success -->
运行完成，现显示最新结果。

<!-- key: run_failed -->
本次运行未完成，未加入比较。

<!-- key: changed_source_footprint -->
网格加密改变了源区的实际范围，请在扩展表格中核对源区尺寸。

<!-- key: nearest_time -->
{name}：最近的保存时刻为 {time:.3f} 天（当前运行：{target:.3f} 天）。

<!-- key: no_comparison_time -->
{name}：{time:.3f} 天时无输出，已略过。

<!-- key: evaluating_reference -->
正在计算解析参考解…

<!-- key: export_hint -->
归档包含模型输入、日志、浓度/水头数组、质量诊断和粒子数据，也保留粒子到达信息。

<!-- key: no_runs -->
运行默认脉冲实验，以查看羽流、剖面、突破曲线及方法比较。

<!-- key: footer -->
MT3D 二维/三维 · v0.5.1 · 课堂教学工作版本

<!-- key: transient_hint -->
初始流场先达到平衡，右侧水头在 t = 0 时改变。

<!-- key: expert_flow_hint -->
启用专家设置以修改流动求解器的容差和迭代次数。

<!-- key: stochastic_hint -->
固定随机种子使分区可复现。K 和 Ss 在对数空间均匀采样，孔隙度均匀采样；网格加密时保持同一实现。

<!-- key: zones_hint -->
矩形按单元中心选择单元；后续行覆盖先前行。层号从 1 开始。

<!-- key: observation_hint -->
观测曲线取自观测点所在单元。改变观测位置无需重新运行已保存的模型。

<!-- key: output_hint -->
包含 t = 0 和最终时刻，控制用于绘图和导出的浓度输出。

<!-- key: preset_homogeneous -->
均质

<!-- key: preset_lens -->
低 K 透镜体

<!-- key: preset_channel -->
高 K 通道

<!-- key: preset_barrier -->
局部低 K 屏障

<!-- key: preset_stochastic -->
随机分区

<!-- key: preset_custom -->
自定义矩形

<!-- key: preset_hint_lens -->
中央透镜体：K = 背景 K 的 0.01 倍，贯穿全厚度。

<!-- key: preset_hint_channel -->
纵向通道：K = 背景 K 的 10 倍，贯穿全厚度。

<!-- key: preset_hint_barrier -->
局部横向屏障：K = 背景 K 的 0.01 倍，保留绕流通道。

<!-- key: signal_pulse -->
脉冲 / 矩形输入

<!-- key: signal_continuous -->
连续输入

<!-- key: signal_dirac -->
Dirac / 瞬时释放

<!-- key: signal_short_pulse -->
脉冲

<!-- key: signal_short_continuous -->
连续

<!-- key: signal_short_dirac -->
Dirac

<!-- key: Concept, assumptions and equations -->
概念、假设与方程

<!-- key: Guided experiments -->
引导实验

<!-- key: Expert settings -->
专家设置

<!-- key: Use sliders for main parameters -->
主要参数使用滑块

<!-- key: Flow & domain -->
流动与模型范围

<!-- key: Transport & source -->
运移与源区

<!-- key: Post-processing & observations -->
后处理与观测

<!-- key: Hydraulic properties -->
水力参数

<!-- key: Hydraulic conductivity K (m/s) -->
渗透系数 K (m/s)

<!-- key: Effective porosity (-) -->
有效孔隙度 (-)

<!-- key: Specific storage Ss (1/m) -->
比贮水量 Ss (1/m)

<!-- key: Vertical / horizontal K -->
垂向 / 水平 K

<!-- key: Boundary conditions -->
边界条件

<!-- key: Specified head left (m) -->
左侧指定水头 (m)

<!-- key: Specified head right (m) -->
右侧指定水头 (m)

<!-- key: Transient flow experiment -->
非稳定流实验

<!-- key: Right head after t = 0 (m) -->
t = 0 后右侧水头 (m)

<!-- key: Model extent and spatial discretization -->
模型范围与空间离散

<!-- key: Model length in x-direction (m) -->
x 方向模型长度 (m)

<!-- key: Model width in y-direction (m) -->
y 方向模型宽度 (m)

<!-- key: Aquifer thickness / top elevation (m) -->
含水层厚度 / 顶面高程 (m)

<!-- key: Define the grid by -->
网格定义方式

<!-- key: Number of cells -->
单元数量

<!-- key: Cell width -->
单元宽度

<!-- key: Cells x -->
x 向单元数

<!-- key: Cells y -->
y 向单元数

<!-- key: Cell width x (m) -->
x 向单元宽度 (m)

<!-- key: Cell width y (m) -->
y 向单元宽度 (m)

<!-- key: Number of layers -->
层数

<!-- key: Numerical solution for flow -->
流动数值求解

<!-- key: Head tolerance (m) -->
水头容差 (m)

<!-- key: Flow residual tolerance (m³/day) -->
流量残差容差 (m³/天)

<!-- key: PCG outer iterations -->
PCG 外迭代次数

<!-- key: PCG inner iterations -->
PCG 内迭代次数

<!-- key: Flow time steps (approximately total) -->
流动时间步数（近似总数）

<!-- key: Hydrogeology and zonation -->
水文地质与非均质性

<!-- key: Hydrogeology preset -->
水文地质预设

<!-- key: Number of zones -->
分区数量

<!-- key: Random seed -->
随机种子

<!-- key: K range (m/s) -->
K 范围 (m/s)

<!-- key: Ss range (1/m) -->
Ss 范围 (1/m)

<!-- key: Porosity range (-) -->
孔隙度范围 (-)

<!-- key: Minimum -->
最小值

<!-- key: Maximum -->
最大值

<!-- key: Edit hydrogeological zones -->
编辑分区

<!-- key: Zone name -->
分区名称

<!-- key: First layer -->
首层

<!-- key: Last layer -->
末层

<!-- key: Porosity -->
孔隙度

<!-- key: Boundary conditions and source -->
边界条件与源区

<!-- key: Input signal -->
输入信号

<!-- key: Released mass (g) -->
释放质量 (g)

<!-- key: Mass input rate (g/day) -->
质量输入速率 (g/天)

<!-- key: Pulse duration (days) -->
脉冲持续时间（天）

<!-- key: Source x (m) -->
源区 x (m)

<!-- key: Source y (m) -->
源区 y (m)

<!-- key: Source cells x -->
源区 x 向单元数

<!-- key: Source cells y -->
源区 y 向单元数

<!-- key: Source spans all layers -->
源区贯穿所有层

<!-- key: Source layer (1 = top) -->
源区所在层（1 = 顶层）

<!-- key: Transport parameters -->
运移参数

<!-- key: Dispersion -->
弥散

<!-- key: Longitudinal dispersivity (m) -->
纵向弥散度 (m)

<!-- key: Horizontal transverse / longitudinal -->
水平横向 / 纵向

<!-- key: Vertical transverse / longitudinal -->
垂向横向 / 纵向

<!-- key: Temporal discretization -->
时间离散

<!-- key: Transport duration (days) -->
运移模拟时长（天）

<!-- key: DT0 · initial step (days; 0 = automatic) -->
DT0 · 初始步长（天；0 = 自动）

<!-- key: TTSMAX · maximum step (days; 0 = automatic) -->
TTSMAX · 最大步长（天；0 = 自动）

<!-- key: TTSMULT · step multiplier -->
TTSMULT · 步长乘数

<!-- key: MXSTRN · maximum transport steps -->
MXSTRN · 最大运移步数

<!-- key: Numerical solution for transport -->
运移数值求解

<!-- key: MT3D advection method -->
MT3D 对流计算方法

<!-- key: MODPATH particle comparison -->
MODPATH 粒子比较

<!-- key: PERCEL · Courant number -->
PERCEL · Courant 数

<!-- key: CCLOSE · concentration tolerance -->
CCLOSE · 浓度容差

<!-- key: Timeout per executable (seconds) -->
单个程序超时限制（秒）

<!-- key: Expert transport solver settings -->
运移求解器专家设置

<!-- key: MXPART · maximum particles -->
MXPART · 最大粒子数

<!-- key: ITRACK · tracking algorithm -->
ITRACK · 追踪算法

<!-- key: WD · concentration weighting -->
WD · 浓度权重

<!-- key: DCEPS · gradient threshold -->
DCEPS · 梯度阈值

<!-- key: NPLANE · particle planes -->
NPLANE · 粒子平面数

<!-- key: NPL · low-gradient particles -->
NPL · 低梯度粒子数

<!-- key: NPH · high-gradient particles -->
NPH · 高梯度粒子数

<!-- key: NPMIN · minimum particles/cell -->
NPMIN · 每单元最少粒子数

<!-- key: NPMAX · maximum particles/cell -->
NPMAX · 每单元最多粒子数

<!-- key: INTERP · interpolation -->
INTERP · 插值

<!-- key: NLSINK · sink planes -->
NLSINK · 汇单元平面数

<!-- key: NPSINK · sink particles -->
NPSINK · 汇单元粒子数

<!-- key: DCHMOC · HMOC threshold -->
DCHMOC · HMOC 阈值

<!-- key: MXITER · GCG outer iterations -->
MXITER · GCG 外迭代次数

<!-- key: ITER1 · GCG inner iterations -->
ITER1 · GCG 内迭代次数

<!-- key: ISOLVE · preconditioner -->
ISOLVE · 预条件器

<!-- key: NCRS · cross-dispersion -->
NCRS · 交叉弥散

<!-- key: ACCL · relaxation -->
ACCL · 松弛

<!-- key: IPRGCG · print interval -->
IPRGCG · 打印间隔

<!-- key: MODPATH release settings -->
MODPATH 释放设置

<!-- key: Particles per source cell -->
每个源单元粒子数

<!-- key: Release batches (pulse / continuous) -->
释放批次数（脉冲 / 连续）

<!-- key: Observation points -->
观测点

<!-- key: Number of observation points -->
观测点数量

<!-- key: Output settings -->
输出设置

<!-- key: Saved transport times -->
保存的运移时刻数

<!-- key: Actual source footprint -->
实际源区范围

<!-- key: Optional run label -->
可选运行名称

<!-- key: Run model -->
运行模型

<!-- key: Run diagnostic -->
运行诊断

<!-- key: More comparison metrics -->
更多比较指标

<!-- key: Displayed run -->
显示的运行

<!-- key: Run to remove -->
待移除运行

<!-- key: Remove -->
移除

<!-- key: Clear comparison runs -->
清空比较运行

<!-- key: Plume & sections -->
羽流与剖面

<!-- key: Observation curves -->
观测曲线

<!-- key: Mass & diagnostics -->
质量与诊断

<!-- key: Export -->
导出

<!-- key: Time (days) -->
时间（天）

<!-- key: Top-view layer -->
俯视层

<!-- key: Layer {number} -->
第 {number} 层

<!-- key: Analytical reference -->
解析参考解

<!-- key: Plot settings and section positions -->
绘图设置与剖面位置

<!-- key: x-direction section · y (m) -->
x 向剖面 · y (m)

<!-- key: y-direction section · x (m) -->
y 向剖面 · x (m)

<!-- key: Colour fill -->
颜色填充

<!-- key: Contour lines -->
等值线

<!-- key: Log colours -->
对数色标

<!-- key: Particle paths -->
粒子轨迹

<!-- key: Opacity -->
不透明度

<!-- key: Compare runs in x / y sections -->
在 x / y 剖面比较运行

<!-- key: Compare section profiles -->
比较剖面

<!-- key: Runs for section comparison -->
剖面比较运行

<!-- key: Also overlay top-view contours -->
同时叠加俯视等值线

<!-- key: Download plume figure (PNG) -->
下载羽流图（PNG）

<!-- key: Runs in breakthrough comparison -->
突破曲线比较运行

<!-- key: Observation cells used by each run -->
各次运行使用的观测单元

<!-- key: Download breakthrough curves (CSV) -->
下载突破曲线（CSV）

<!-- key: Detailed mass-budget data -->
详细质量收支数据

<!-- key: Stored run configuration -->
已保存运行配置

<!-- key: Download comparison table (CSV) -->
下载比较表（CSV）

<!-- key: Download run configuration (JSON) -->
下载运行配置（JSON）

<!-- key: Prepare complete displayed-run archive -->
准备当前运行的完整归档

<!-- key: Preparing archive… -->
正在准备归档…

<!-- key: Download run archive (ZIP) -->
下载运行归档（ZIP）

<!-- key: Run -->
运行

<!-- key: Method -->
方法

<!-- key: Signal -->
信号

<!-- key: Grid -->
网格

<!-- key: K zones -->
K 分区

<!-- key: Flow -->
流动

<!-- key: MB disc. (%) -->
质量偏差 (%)

<!-- key: Flow disc. (%) -->
水量偏差 (%)

<!-- key: MT3D (s) -->
MT3D (s)

<!-- key: MP7 (s) -->
MP7 (s)

<!-- key: Flow (s) -->
流动 (s)

<!-- key: Total (s) -->
总计 (s)

<!-- key: Ref. L1 (%) -->
参考 L1 (%)

<!-- key: Mass (g) -->
质量 (g)

<!-- key: Input (g) -->
输入 (g)

<!-- key: Min. C (g/m³) -->
最小 C (g/m³)

<!-- key: Neg. mass (g) -->
负质量 (g)

<!-- key: Centroid x (m) -->
质心 x (m)

<!-- key: Steps -->
步数

<!-- key: Source box (m) -->
源区范围 (m)

<!-- key: End (d) -->
终止（天）

<!-- key: Scenario -->
情景

<!-- key: Point -->
点

<!-- key: Requested x -->
请求 x

<!-- key: Requested y -->
请求 y

<!-- key: Requested z -->
请求 z

<!-- key: Cell centre x -->
单元中心 x

<!-- key: Cell centre y -->
单元中心 y

<!-- key: Cell centre z -->
单元中心 z

<!-- key: Layer -->
层

<!-- key: Row -->
行

<!-- key: Column -->
列

<!-- key: Cumulative in (g) -->
累计流入 (g)

<!-- key: Cumulative out (g) -->
累计流出 (g)

<!-- key: Sources (g) -->
源项 (g)

<!-- key: Sinks (g) -->
汇项 (g)

<!-- key: Fluid storage (g) -->
流体贮存 (g)

<!-- key: Native resident mass (g) -->
程序报告的域内质量 (g)

<!-- key: Alternative disc. (%) -->
替代偏差 (%)

<!-- key: Analytical reference requires homogeneous steady flow. -->
解析参考解要求均质稳定流。

<!-- key: Source cells -->
源单元

<!-- key: Specified head -->
指定水头

<!-- key: Section locations -->
剖面位置

<!-- key: Background flow -->
背景流动

<!-- key: Model preview: grid, boundaries and source -->
模型预览：网格、边界与源区

<!-- key: Computed head contours -->
计算水头等值线

<!-- key: Homogeneous steady head contours -->
均质稳定流水头等值线

<!-- key: Time (d) -->
时间（天）

<!-- key: Mass rate (g/d) -->
质量速率 (g/天)

<!-- key: Instantaneous mass (g) -->
瞬时质量 (g)

<!-- key: Dirac input (initial cell mass) -->
Dirac 输入（单元初始质量）

<!-- key: Finite pulse input -->
有限脉冲输入

<!-- key: Continuous input -->
连续输入

<!-- key: Concentration (g/m³) -->
浓度 (g/m³)

<!-- key: Elevation z (m) -->
高程 z (m)

<!-- key: MODPATH advection (slice) -->
MODPATH 对流（切片）

<!-- key: Analytical -->
解析解

<!-- key: Analytical (active run) -->
解析解（当前运行）

<!-- key: Mass output unavailable -->
质量输出不可用

<!-- key: MT3D discrepancy (%) -->
MT3D 偏差 (%)

<!-- key: Initial + injected mass (first run) -->
初始 + 输入质量（首次运行）

<!-- key: Resident mass: grid sum and MT3D budget -->
域内质量：网格积分与 MT3D 收支

<!-- key: Reported mass-balance closure -->
报告的质量平衡闭合

<!-- key: Example: pulse plume after 600 days -->
示例：600 天后的脉冲羽流

<!-- key: Example: observation P1 -->
示例：观测点 P1

<!-- key: P1 · x (m) -->
P1 · x (m)

<!-- key: P1 · y (m) -->
P1 · y (m)

<!-- key: P1 · elevation z (m) -->
P1 · 高程 z (m)

<!-- key: P2 · x (m) -->
P2 · x (m)

<!-- key: P2 · y (m) -->
P2 · y (m)

<!-- key: P2 · elevation z (m) -->
P2 · 高程 z (m)

<!-- key: P3 · x (m) -->
P3 · x (m)

<!-- key: P3 · y (m) -->
P3 · y (m)

<!-- key: P3 · elevation z (m) -->
P3 · 高程 z (m)

<!-- key: P4 · x (m) -->
P4 · x (m)

<!-- key: P4 · y (m) -->
P4 · y (m)

<!-- key: P4 · elevation z (m) -->
P4 · 高程 z (m)

<!-- key: P5 · x (m) -->
P5 · x (m)

<!-- key: P5 · y (m) -->
P5 · y (m)

<!-- key: P5 · elevation z (m) -->
P5 · 高程 z (m)

<!-- key: fig_head -->
指定水头：{head:g} m

<!-- key: fig_layers -->
{layers} 层；垂向比例已放大

<!-- key: fig_total -->
总计：{mass:g} g

<!-- key: fig_initial -->
t = 0 时 {mass:g} g

<!-- key: fig_xprofile -->
y = {y:.3g} m 处的 x 向剖面

<!-- key: fig_yprofile -->
x = {x:.3g} m 处的 y 向剖面

<!-- key: fig_section -->
{other} = {value:.3g} m 处的 {axis}–z 剖面

<!-- key: fig_title -->
{method} · t = {time:g} 天 · 第 {layer} 层 (z = {z:.3g} m)

<!-- key: fig_gridmass -->
{label}：网格积分

<!-- key: fig_nativemass -->
{label}：MT3D 收支

<!-- key: fig_nodata -->
{label}：域外，无数据

<!-- key: table_help_MB disc. (%) -->
MT3D 程序报告的最终质量平衡偏差。

<!-- key: table_help_Flow disc. (%) -->
MODFLOW 最终水量平衡偏差。

<!-- key: table_help_MT3D (s) -->
运移程序的实际运行耗时。

<!-- key: table_help_MP7 (s) -->
MODPATH 耗时；粒子仅描述对流。

<!-- key: table_help_Ref. L1 (%) -->
按孔隙体积加权的浓度绝对误差，除以参考质量。

<!-- key: table_help_Mass (g) -->
对浓度网格积分得到的最终溶解质量。

<!-- key: MT3DMS final mass discrepancy exceeds 1%; inspect method and transport time step settings. -->
MT3DMS 最终质量偏差超过 1%；请检查方法和运移时间步设置。

<!-- key: At least one MODFLOW water-budget discrepancy exceeds 0.1%. -->
至少一个 MODFLOW 水量平衡偏差超过 0.1%。

<!-- key: Negative concentrations occurred. They are retained in diagnostics and exports; central FD and particle methods can oscillate. -->
出现负浓度，已保留在诊断和导出中；中心差分及粒子方法可能产生振荡。

<!-- key: Source coordinates must lie inside the domain. -->
源区坐标必须位于模型域内。

<!-- key: This confined lab requires heads at or above aquifer top. -->
本承压模型要求水头不低于含水层顶面。

<!-- key: Pulse duration must be between zero and model duration. -->
脉冲持续时间必须在零与模拟时长之间。

<!-- key: Observation point is outside the model. -->
观测点位于模型外。

<!-- key: TVD requires PERCEL no greater than 1. -->
TVD 要求 PERCEL ≤ 1。

<!-- key: language_fallback -->
缺失译文时使用英文回退。

<!-- key: preset_random -->
随机参数

<!-- key: Random unit x (m) -->
随机单元 x (m)

<!-- key: Random unit y (m) -->
随机单元 y (m)

<!-- key: random_hint -->
小单元形成细密随机图案，大单元形成较大斑块。网格加密时保持种子和物理单元尺寸不变，以保留同一材料实现。

<!-- key: Active cells -->
活动单元数

<!-- key: table_help_Active cells -->
所有非停用单元，包括指定水头单元。

<!-- key: Random field -->
随机场

<!-- key: Comparison runs -->
比较运行

<!-- key: discard_tags_hint -->
点击标签的 × 删除该次运行。清除全部标签会开始新的比较，请先导出需要保留的运行。

<!-- key: Head contours -->
水头等值线

<!-- key: Computed head contours (m) -->
计算水头等值线 (m)

<!-- key: Head contours appear after running the model -->
运行模型后显示水头等值线

<!-- key: fig_background_k -->
背景 K = {k:.2e} m/s

<!-- key: fig_low_lens_k -->
低 K 透镜体：K = {k:.2e} m/s

<!-- key: fig_high_channel_k -->
高 K 通道：K = {k:.2e} m/s

<!-- key: fig_low_barrier_k -->
低 K 屏障：K = {k:.2e} m/s

<!-- key: Focus on plume -->
聚焦羽流

<!-- key: Focus threshold (% of peak) -->
聚焦阈值（峰值百分比）

<!-- key: focus_hint -->
按各显示羽流当前正浓度峰值确定阈值，每侧留 20% 边距，并包含可见 MODPATH 轨迹。无羽流和轨迹时显示全域。仅改变俯视范围。

<!-- key: Download plume figure (SVG) -->
下载羽流图（SVG）

<!-- key: steady -->
稳定流

<!-- key: transient -->
非稳定流

<!-- key: fig_minimum -->
数值最小值：{minimum:.3g} g/m³

<!-- key: fig_minimum_log -->
数值最小值：{minimum:.3g} g/m³（对数图隐藏非正值）

<!-- key: The plume reaches an x specified-head boundary; enlarge the domain before treating the infinite-x analytical solution as a benchmark. -->
羽流已到达 x 指定水头边界；采用无限 x 解析基准前请扩大模型域。

<!-- key: fig_reference_boundary -->
已停用解析精度评估：x 边界影响超过 {tolerance_percent:.2g}% 阈值。

<!-- key: Low K lens -->
低 K 透镜体

<!-- key: High K channel -->
高 K 通道

<!-- key: Low K barrier -->
局部低 K 屏障

<!-- key: Page width -->
页面宽度

<!-- key: width_1 -->
窄

<!-- key: width_2 -->
紧凑

<!-- key: width_3 -->
标准

<!-- key: width_4 -->
宽

<!-- key: width_5 -->
全宽

<!-- key: page_width_hint -->
从窄到全宽共五档。标准档保留之前的宽度，小屏幕会自动适应可用空间。

<!-- key: Show model grid -->
显示模型网格

<!-- key: grid_hint -->
以浅灰线显示当前运行的单元边界。单层浓度剖面用垂线标示单元边缘。

<!-- key: Plume-centered x/y -->
羽流中心相对 x/y

<!-- key: relative_hint -->
以显示层中正浓度对应的溶解质量质心为零点。所有叠加共用此原点，输入坐标和高程保持绝对值。

<!-- key: relative_mass_origin -->
相对原点：x = {x:.2f} m；y = {y:.2f} m（羽流质心）。

<!-- key: relative_source_origin -->
此层无正羽流质量：以贴合网格的源区中心为原点，x = {x:.2f} m；y = {y:.2f} m。

<!-- key: fig_relative_xprofile -->
y′ = {y:.3g} m 处的 x 向剖面

<!-- key: fig_relative_yprofile -->
x′ = {x:.3g} m 处的 y 向剖面

<!-- key: fig_relative_section -->
{other}′ = {value:.3g} m 处的 {axis}–z 剖面
