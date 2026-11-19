## introduction

通过一个简单的一维模型，探索保守性溶质沿地下水流径的运移。将 MT3DMS 与解析解进行比较，了解离散方式和数值方法如何影响运移信号。

## concept_explanation

设想一条沿地下水流径延伸的狭窄流管，位于均质、完全饱和的含水层中。水沿流管作稳态流动。保守性溶质从上游入口进入，随对流向下游迁移，弥散则可使信号沿流径展宽。

这一理想化的一维模型用于考察数值运移方法、单元尺寸和时间步长对计算信号的影响。将 MT3DMS 与解析解比较，观察前缘展宽、振荡、运移时间和质量平衡。先确定入口信号与运移过程，再比较同一情景下最多十个数值方案。

## concept_caption

示意流管内为稳定一维流动，观测点位于 250 m 处。侧边界没有水或溶质交换；横向尺寸不按比例绘制。

## concept_response_caption

400 d 矩形输入的解析响应示例，其中 C/Cref = 1，v = 0.24 m/d。绿色：纯对流；蓝色：纵向弥散度 10 m，D = 2.4 m²/d，分子扩散为零。这些固定示例独立于当前模型设置。

## front_task

1. 选择连续输入、21 个单元、迎风有限差分，并关闭弥散。根据孔隙水流速预测第 2000 天的前缘位置。
2. 运行模型，观察解析前缘两侧的数值浓度。
3. 改用 TVD，再增加至 101 个单元。比较前缘宽度、剖面误差与质量平衡误差。

## spreading_task

1. 选择连续输入、10 m 纵向弥散度、零分子扩散，以及 21 个单元的 TVD。观察解析剖面。
2. 增加至 101 个单元，再改用迎风格式。哪部分展宽也出现在解析解中？
3. 查看 250 m 处的穿透曲线。关闭弥散后开始新的纯对流比较。“入口与运移”中的设置变化会清空已保存的方案。

## impulse_task

1. 选择持续 400 d 的矩形脉冲，在剖面及 250 m 处观察其前缘与后缘。
2. 开始新的 Dirac 情景，面积设为 50 d、数值宽度为 50 d、单元数为 101、弥散度为 10 m。记录实际脉冲和理想脉冲的 RMSE。
3. 保持面积，将宽度缩短至 10 d。运行新情景并比较所记录的误差。随后细化该情景的网格，再检查质量平衡。

## theory

承压含水层厚 1 m、宽 1 m。首尾单元中心相距 1000 m，给定水头约为 6.944 m 和 0 m。水力传导系数为 $K=10^{-4}$ m/s，有效孔隙度为 $n_e=0.25$，对应达西通量 0.06 m/d 和孔隙水流速 $v=0.24$ m/d。内部初始溶质浓度为零，流出水携带当地浓度。浓度基准为 $C_{\mathrm{ref}}=1$ g/m³，即 1 mg/L。

模型求解 $\partial C/\partial t=D\partial^2 C/\partial x^2-v\partial C/\partial x$，其中 $D=\alpha_Lv+D_e$。关闭弥散时，信号移动距离为 $vt$。当 $D>0$ 时，半无限介质中入口给定单位浓度阶跃的响应为

$$
S(x,t)=\tfrac12\left[\operatorname{erfc}\!\left(\frac{x-vt}{2\sqrt{Dt}}\right)
+e^{vx/D}\operatorname{erfc}\!\left(\frac{x+vt}{2\sqrt{Dt}}\right)\right],\quad t>0.
$$

高度为 $H$ 的连续输入给出 $HS(x,t)$。持续时间为 $\tau$ 的矩形脉冲给出 $H[S(x,t)-S(x,t-\tau)]$，输入停止前第二项为零。若入口理想 Dirac 脉冲的浓度时间面积为 $A=\int(C_{\mathrm{in}}/C_{\mathrm{ref}})dt$，内部响应为

$$
A\frac{\partial S}{\partial t}
=A\,\frac{x}{\sqrt{4\pi D t^3}}\exp\!\left[-\frac{(x-vt)^2}{4Dt}\right].
$$

MT3DMS 使用宽度为 $\varepsilon$、高度为 $A/\varepsilon$ 的矩形脉冲，使入口浓度时间曲线下的面积保持恒定。实际质量平衡还包括给定浓度边界上的弥散通量。当 $D=0$ 时，理想脉冲以速度 $v$ 移动，其点浓度峰值并非有限值。

## profile_hint

数值剖面显示单元中心浓度。中间时刻采用相邻已保存运移步之间的线性插值。第 2000 天直接使用最后一次计算结果。

## breakthrough_hint

每个运移时间步均被保存。在所选距离处，浓度由相邻单元中心值插值得到。该位置的对流运移时间为 {t:.1f} d。

## balance_hint

图中采用 MAS 文件 TOTAL IN–OUT 列的带符号累计质量误差，以总输入和总输出绝对值的平均值为分母，包含储存项。质量平衡误差很小时，数值前缘仍可能展宽。

## dirac_reading

虚线对应实际施加的有限矩形脉冲。点线对应理想 Dirac 响应。无弥散时，竖直点线表示脉冲的位置或到达时刻，线的高度不代表浓度。

## outlet_hint

对于 {ids}，1000 m 处的单位阶跃解析浓度到第 2000 天至少达到 1%。有限 MT3DMS 模型的出口可能影响下游剖面。该筛查也用于脉冲情景，实际脉冲的出口浓度可能更低。

## table_hint

所有方案均在 50 至 950 m 之间相同的 90 个 10 m 区间上评分。RMSE 和 MAE 比较最终数值剖面与实际入口信号的解析解，单位均为 C/Cref。

## mass_warning

{ids} 在第 2000 天的绝对质量误差超过 1%。请同时检查质量平衡曲线与浓度剖面。粒子方法在粗网格上可能漏掉短脉冲。

## metrics_notes

计算评分时，每个单元内的数值浓度视为常数，并按与各 10 m 区间的重叠长度加权平均。解析浓度在相同区间内积分。即使采用最粗网格，评分区间也避开两端边界单元。RMSE 为残差平方均值的平方根，MAE 为残差绝对值的均值。

Dirac 情景还计算相对于理想脉冲的 RMSE。无弥散时，脉冲的空间权重为 $vA$。若恰好位于区间公共边界，两侧各分一半。误差随输入幅值变化，因此比较数值方法时应保持信号及其强度一致。

耗时记录两个求解程序的实际运行时间，不含文件准备、读取、绘图和误差计算。水量平衡为 MODFLOW 的最后一次平衡误差。网格 Péclet 数为 $v\Delta x/D$，纯对流时为无穷大。中心差分可能产生超出入口浓度范围的值，图中会保留这些值。

## references

- `TRANS_1D_MT3D.ipynb`, MWW01.
- Zheng & Wang (1999), *MT3DMS*, 1. [MODFLOW benchmark](https://modflow6-examples.readthedocs.io/en/latest/_examples/ex-gwt-mt3dms-p01.html)
- Wexler (1992), *Analytical Solutions for One-, Two-, and Three-Dimensional Solute Transport in Ground-Water Systems with Uniform Flow*. [USGS TWRI 3-B7](https://pubs.usgs.gov/twri/twri3-b7/pdf/twri_3-B7_a.pdf)
- Pérez Guerrero et al. (2013), *Analytical solutions of the one-dimensional advection–dispersion solute transport equation subject to time-dependent boundary conditions*. [DOI](https://doi.org/10.1016/j.cej.2013.01.095)
- FloPy [MT3DMS ADV](https://flopy.readthedocs.io/en/latest/source/flopy.mt3d.mtadv.html), [MT3DMS SSM](https://flopy.readthedocs.io/en/latest/source/flopy.mt3d.mtssm.html).

## method_upwind

由上游浓度决定每个单元面的对流通量。关闭物理弥散后，观察数值前缘是否展宽。

## method_central

单元面通量使用两侧浓度。对流占优的粗网格可能在陡峭前缘附近产生振荡。

## method_tvd

三阶 ULTIMATE TVD 格式在陡峭梯度附近限制对流通量。请与迎风差分的前缘宽度比较。

## method_moc

特征线法向前追踪粒子。这里 MT3DMS 在浓度梯度足够大的单元内初始放置四个粒子。

## method_mmoc

修正特征线法向后追踪轨迹，以估算进入单元的浓度。

## method_hmoc

混合特征线法根据局部浓度梯度在 MOC 和 MMOC 之间切换。

