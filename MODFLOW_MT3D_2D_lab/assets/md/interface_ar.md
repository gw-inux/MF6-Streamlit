<!-- key: title -->
MT3D – مختبر النقل ثنائي وثلاثي الأبعاد

<!-- key: intro_caption -->
رسم توضيحي تمهيدي لسحابة مذاب ومنحنى وصول، مستقل عن مدخلات النموذج الحالية.

<!-- key: Model & run -->
1 · النموذج والتشغيل

<!-- key: Results & method comparison -->
2 · النتائج ومقارنة الطرق

<!-- key: series_reset -->
بدأت سلسلة مقارنة جديدة بسبب تغيير الإشارة أو هندسة المجال/المصدر. حُذفت التشغيلات السابقة.

<!-- key: grid_summary -->
الشبكة: {nx} × {ny} × {nz} خلية. الأبعاد الفعلية: Δx = {dx:.3f} m؛ Δy = {dy:.3f} m؛ Δz = {dz:.3f} m.

<!-- key: velocity_summary -->
سرعة المسام المرجعية للوسط المتجانس: {velocity:.4f} m/يوم.

<!-- key: source_bounds -->
x = {x0:.2f}–{x1:.2f} m; y = {y0:.2f}–{y1:.2f} m; z = {z0:.2f}–{z1:.2f} m.

<!-- key: source_snap_hint -->
يشغل المصدر الخلايا المختارة. قد تتغير أبعاده الفعلية مع دقة الشبكة. إدخال عرض الخلية يحافظ على امتداد المجال ويعرض التباعد المنتظم الفعلي.

<!-- key: input_error -->
صحّح إعدادات النموذج المشار إليها قبل التشغيل.

<!-- key: missing_executables -->
برامج مفقودة: {names}. ضع الملفات التنفيذية المتوافقة في `bin/` للتطبيق أو المستودع. محليًا: `python setup_executables.py`.

<!-- key: label_placeholder -->
تلقائي: 01 TVD / Pulse (غير متجانس: / het.)

<!-- key: history_full -->
تم حفظ عشر تشغيلات. احذف تشغيلًا أو امسح السلسلة للمتابعة.

<!-- key: running -->
جارٍ تشغيل MODFLOW وMT3D وMODPATH الاختياري…

<!-- key: run_success -->
اكتمل التشغيل. تُعرض الآن أحدث النتائج.

<!-- key: run_failed -->
تعذّر إكمال هذا التشغيل ولم يُضف إلى المقارنة.

<!-- key: changed_source_footprint -->
غيّر تنعيم الشبكة الامتداد الفعلي للمصدر. راجع أبعاده في الجدول الموسّع.

<!-- key: nearest_time -->
{name}: أقرب زمن محفوظ {time:.3f} يوم (التشغيل المعروض: {target:.3f} يوم).

<!-- key: no_comparison_time -->
{name}: لا توجد نتائج عند {time:.3f} يوم؛ أُغفل.

<!-- key: evaluating_reference -->
جارٍ حساب المرجع التحليلي…

<!-- key: export_hint -->
يضم الأرشيف المدخلات والسجلات ومصفوفات التركيز والمنسوب وبيانات الميزانية والجسيمات، بما فيها تفاصيل الوصول.

<!-- key: no_runs -->
شغّل تجربة النبضة الأساسية لعرض السحابة والمقاطع ومنحنيات الوصول ومقارنة الطرق.

<!-- key: footer -->
MT3D 2D/3D · v0.4.0 · نسخة عمل للتدريس المباشر

<!-- key: transient_hint -->
يتوازن حقل الجريان الأولي؛ يتغير المنسوب الأيمن عند t = 0.

<!-- key: expert_flow_hint -->
فعّل الإعدادات المتقدمة لتعديل سماحات محلّل الجريان وتكراراته.

<!-- key: stochastic_hint -->
بذرة ثابتة تعطي مناطق قابلة للتكرار. تُسحب K وSs بانتظام لوغاريتمي والمسامية بانتظام خطي. يبقى التحقيق نفسه عند تنعيم الشبكة.

<!-- key: zones_hint -->
تحدد المستطيلات الخلايا بمراكزها؛ تتجاوز الصفوف اللاحقة السابقة. يبدأ ترقيم الطبقات من 1.

<!-- key: observation_hint -->
تستخدم منحنيات الرصد الخلية المحتوية على النقطة. يمكن تغيير المواقع دون إعادة تشغيل النماذج المحفوظة.

<!-- key: output_hint -->
يشمل t = 0 والزمن النهائي. يحدد مخرجات التركيز للرسوم والتصدير.

<!-- key: preset_homogeneous -->
متجانس

<!-- key: preset_lens -->
عدسة منخفضة K

<!-- key: preset_channel -->
قناة مرتفعة K

<!-- key: preset_barrier -->
حاجز جزئي منخفض K

<!-- key: preset_stochastic -->
تقسيم عشوائي للمناطق

<!-- key: preset_custom -->
مستطيلات مخصصة

<!-- key: preset_hint_lens -->
عدسة مركزية: K = 0.01 × K الخلفية؛ على كامل العمق.

<!-- key: preset_hint_channel -->
قناة طولية: K = 10 × K الخلفية؛ على كامل العمق.

<!-- key: preset_hint_barrier -->
حاجز جزئي يعترض الجريان: K = 0.01 × K الخلفية؛ يبقى مسار التفاف.

<!-- key: signal_pulse -->
نبضة / إدخال مستطيل

<!-- key: signal_continuous -->
إدخال مستمر

<!-- key: signal_dirac -->
ديراك / إطلاق لحظي

<!-- key: signal_short_pulse -->
نبضة

<!-- key: signal_short_continuous -->
مستمر

<!-- key: signal_short_dirac -->
ديراك

<!-- key: Concept, assumptions and equations -->
المفهوم والافتراضات والمعادلات

<!-- key: Guided experiments -->
تجارب موجّهة

<!-- key: Expert settings -->
إعدادات متقدمة

<!-- key: Use sliders for main parameters -->
منزلقات للمعاملات الرئيسية

<!-- key: Flow & domain -->
الجريان والمجال

<!-- key: Transport & source -->
النقل والمصدر

<!-- key: Post-processing & observations -->
المعالجة اللاحقة والرصد

<!-- key: Hydraulic properties -->
الخصائص الهيدروليكية

<!-- key: Hydraulic conductivity K (m/s) -->
الموصلية الهيدروليكية K (m/s)

<!-- key: Effective porosity (-) -->
المسامية الفعالة (-)

<!-- key: Specific storage Ss (1/m) -->
التخزين النوعي Ss (1/m)

<!-- key: Vertical / horizontal K -->
K الرأسي / الأفقي

<!-- key: Boundary conditions -->
الشروط الحدّية

<!-- key: Specified head left (m) -->
المنسوب المحدد يسارًا (m)

<!-- key: Specified head right (m) -->
المنسوب المحدد يمينًا (m)

<!-- key: Transient flow experiment -->
تجربة الجريان غير المستقر

<!-- key: Right head after t = 0 (m) -->
المنسوب الأيمن بعد t = 0 (m)

<!-- key: Model extent and spatial discretization -->
امتداد النموذج والتقسيم المكاني

<!-- key: Model length in x-direction (m) -->
طول النموذج باتجاه x (m)

<!-- key: Model width in y-direction (m) -->
عرض النموذج باتجاه y (m)

<!-- key: Aquifer thickness / top elevation (m) -->
سمك الخزان / منسوب سطحه العلوي (m)

<!-- key: Define the grid by -->
تعريف الشبكة بواسطة

<!-- key: Number of cells -->
عدد الخلايا

<!-- key: Cell width -->
عرض الخلية

<!-- key: Cells x -->
خلايا x

<!-- key: Cells y -->
خلايا y

<!-- key: Cell width x (m) -->
عرض الخلية x (m)

<!-- key: Cell width y (m) -->
عرض الخلية y (m)

<!-- key: Number of layers -->
عدد الطبقات

<!-- key: Numerical solution for flow -->
الحل العددي للجريان

<!-- key: Head tolerance (m) -->
سماح المنسوب (m)

<!-- key: Flow residual tolerance (m³/day) -->
سماح متبقي الجريان (m³/يوم)

<!-- key: PCG outer iterations -->
تكرارات PCG الخارجية

<!-- key: PCG inner iterations -->
تكرارات PCG الداخلية

<!-- key: Flow time steps (approximately total) -->
خطوات الجريان (المجموع التقريبي)

<!-- key: Hydrogeology and zonation -->
الهيدروجيولوجيا وعدم التجانس

<!-- key: Hydrogeology preset -->
إعداد هيدروجيولوجي مسبق

<!-- key: Number of zones -->
عدد المناطق

<!-- key: Random seed -->
البذرة العشوائية

<!-- key: K range (m/s) -->
مجال K (m/s)

<!-- key: Ss range (1/m) -->
مجال Ss (1/m)

<!-- key: Porosity range (-) -->
مجال المسامية (-)

<!-- key: Minimum -->
الحد الأدنى

<!-- key: Maximum -->
الحد الأقصى

<!-- key: Edit hydrogeological zones -->
تعديل المناطق

<!-- key: Zone name -->
اسم المنطقة

<!-- key: First layer -->
الطبقة الأولى

<!-- key: Last layer -->
الطبقة الأخيرة

<!-- key: Porosity -->
المسامية

<!-- key: Boundary conditions and source -->
الشروط الحدّية والمصدر

<!-- key: Input signal -->
إشارة الإدخال

<!-- key: Released mass (g) -->
الكتلة المطلقة (g)

<!-- key: Mass input rate (g/day) -->
معدل إدخال الكتلة (g/يوم)

<!-- key: Pulse duration (days) -->
مدة النبضة (يوم)

<!-- key: Source x (m) -->
المصدر x (m)

<!-- key: Source y (m) -->
المصدر y (m)

<!-- key: Source cells x -->
خلايا المصدر x

<!-- key: Source cells y -->
خلايا المصدر y

<!-- key: Source spans all layers -->
المصدر يشمل جميع الطبقات

<!-- key: Source layer (1 = top) -->
طبقة المصدر (1 = العليا)

<!-- key: Transport parameters -->
معاملات النقل

<!-- key: Dispersion -->
التشتت

<!-- key: Longitudinal dispersivity (m) -->
التشتتية الطولية (m)

<!-- key: Horizontal transverse / longitudinal -->
المستعرضة الأفقية / الطولية

<!-- key: Vertical transverse / longitudinal -->
المستعرضة الرأسية / الطولية

<!-- key: Temporal discretization -->
التقسيم الزمني

<!-- key: Transport duration (days) -->
مدة النقل (يوم)

<!-- key: DT0 · initial step (days; 0 = automatic) -->
DT0 · الخطوة الأولى (يوم؛ 0 = تلقائي)

<!-- key: TTSMAX · maximum step (days; 0 = automatic) -->
TTSMAX · أقصى خطوة (يوم؛ 0 = تلقائي)

<!-- key: TTSMULT · step multiplier -->
TTSMULT · مضاعف الخطوة

<!-- key: MXSTRN · maximum transport steps -->
MXSTRN · أقصى خطوات النقل

<!-- key: Numerical solution for transport -->
الحل العددي للنقل

<!-- key: MT3D advection method -->
طريقة الحمل في MT3D

<!-- key: MODPATH particle comparison -->
مقارنة جسيمات MODPATH

<!-- key: PERCEL · Courant number -->
PERCEL · عدد كورانت

<!-- key: CCLOSE · concentration tolerance -->
CCLOSE · سماح التركيز

<!-- key: Timeout per executable (seconds) -->
المهلة لكل برنامج (ثانية)

<!-- key: Expert transport solver settings -->
إعدادات محلّل النقل المتقدمة

<!-- key: MXPART · maximum particles -->
MXPART · أقصى عدد جسيمات

<!-- key: ITRACK · tracking algorithm -->
ITRACK · خوارزمية التتبع

<!-- key: WD · concentration weighting -->
WD · ترجيح التركيز

<!-- key: DCEPS · gradient threshold -->
DCEPS · عتبة التدرج

<!-- key: NPLANE · particle planes -->
NPLANE · مستويات الجسيمات

<!-- key: NPL · low-gradient particles -->
NPL · جسيمات التدرج المنخفض

<!-- key: NPH · high-gradient particles -->
NPH · جسيمات التدرج المرتفع

<!-- key: NPMIN · minimum particles/cell -->
NPMIN · أدنى جسيمات/خلية

<!-- key: NPMAX · maximum particles/cell -->
NPMAX · أقصى جسيمات/خلية

<!-- key: INTERP · interpolation -->
INTERP · الاستيفاء

<!-- key: NLSINK · sink planes -->
NLSINK · مستويات المصارف

<!-- key: NPSINK · sink particles -->
NPSINK · جسيمات المصارف

<!-- key: DCHMOC · HMOC threshold -->
DCHMOC · عتبة HMOC

<!-- key: MXITER · GCG outer iterations -->
MXITER · تكرارات GCG الخارجية

<!-- key: ITER1 · GCG inner iterations -->
ITER1 · تكرارات GCG الداخلية

<!-- key: ISOLVE · preconditioner -->
ISOLVE · المهيئ المسبق

<!-- key: NCRS · cross-dispersion -->
NCRS · التشتت المتقاطع

<!-- key: ACCL · relaxation -->
ACCL · الاسترخاء

<!-- key: IPRGCG · print interval -->
IPRGCG · فاصل الطباعة

<!-- key: MODPATH release settings -->
إعدادات إطلاق MODPATH

<!-- key: Particles per source cell -->
جسيمات لكل خلية مصدر

<!-- key: Release batches (pulse / continuous) -->
دفعات الإطلاق (نبضة / مستمر)

<!-- key: Observation points -->
نقاط الرصد

<!-- key: Number of observation points -->
عدد نقاط الرصد

<!-- key: Output settings -->
إعدادات المخرجات

<!-- key: Saved transport times -->
أزمنة النقل المحفوظة

<!-- key: Actual source footprint -->
الامتداد الفعلي للمصدر

<!-- key: Optional run label -->
اسم اختياري للتشغيل

<!-- key: Run model -->
تشغيل النموذج

<!-- key: Run diagnostic -->
تشخيص التشغيل

<!-- key: More comparison metrics -->
مقاييس مقارنة إضافية

<!-- key: Displayed run -->
التشغيل المعروض

<!-- key: Run to remove -->
التشغيل المراد حذفه

<!-- key: Remove -->
حذف

<!-- key: Clear comparison runs -->
مسح تشغيلات المقارنة

<!-- key: Plume & sections -->
السحابة والمقاطع

<!-- key: Observation curves -->
منحنيات الرصد

<!-- key: Mass & diagnostics -->
الكتلة والتشخيص

<!-- key: Export -->
تصدير

<!-- key: Time (days) -->
الزمن (يوم)

<!-- key: Top-view layer -->
طبقة المسقط الأفقي

<!-- key: Layer {number} -->
الطبقة {number}

<!-- key: Analytical reference -->
المرجع التحليلي

<!-- key: Plot settings and section positions -->
إعدادات الرسم ومواقع المقاطع

<!-- key: x-direction section · y (m) -->
مقطع باتجاه x · y (m)

<!-- key: y-direction section · x (m) -->
مقطع باتجاه y · x (m)

<!-- key: Colour fill -->
تعبئة لونية

<!-- key: Contour lines -->
خطوط تساوي التركيز

<!-- key: Log colours -->
ألوان لوغاريتمية

<!-- key: Particle paths -->
مسارات الجسيمات

<!-- key: Opacity -->
العتامة

<!-- key: Compare runs in x / y sections -->
مقارنة التشغيلات في مقاطع x / y

<!-- key: Compare section profiles -->
مقارنة المقاطع

<!-- key: Runs for section comparison -->
تشغيلات مقارنة المقاطع

<!-- key: Also overlay top-view contours -->
تراكب خطوط المسقط الأفقي أيضًا

<!-- key: Download plume figure (PNG) -->
تنزيل رسم السحابة (PNG)

<!-- key: Runs in breakthrough comparison -->
تشغيلات مقارنة منحنيات الوصول

<!-- key: Observation cells used by each run -->
خلايا الرصد لكل تشغيل

<!-- key: Download breakthrough curves (CSV) -->
تنزيل منحنيات الوصول (CSV)

<!-- key: Detailed mass-budget data -->
بيانات ميزانية الكتلة التفصيلية

<!-- key: Stored run configuration -->
إعدادات التشغيل المحفوظة

<!-- key: Download comparison table (CSV) -->
تنزيل جدول المقارنة (CSV)

<!-- key: Download run configuration (JSON) -->
تنزيل الإعدادات (JSON)

<!-- key: Prepare complete displayed-run archive -->
إعداد أرشيف كامل للتشغيل المعروض

<!-- key: Preparing archive… -->
جارٍ إعداد الأرشيف…

<!-- key: Download run archive (ZIP) -->
تنزيل الأرشيف (ZIP)

<!-- key: Run -->
التشغيل

<!-- key: Method -->
الطريقة

<!-- key: Signal -->
الإشارة

<!-- key: Grid -->
الشبكة

<!-- key: K zones -->
مناطق K

<!-- key: Flow -->
الجريان

<!-- key: MB disc. (%) -->
فرق الكتلة (%)

<!-- key: Flow disc. (%) -->
فرق الجريان (%)

<!-- key: MT3D (s) -->
MT3D (s)

<!-- key: MP7 (s) -->
MP7 (s)

<!-- key: Flow (s) -->
الجريان (s)

<!-- key: Total (s) -->
الإجمالي (s)

<!-- key: Ref. L1 (%) -->
مرجع L1 (%)

<!-- key: Mass (g) -->
الكتلة (g)

<!-- key: Input (g) -->
الإدخال (g)

<!-- key: Min. C (g/m³) -->
أدنى C (g/m³)

<!-- key: Neg. mass (g) -->
كتلة سالبة (g)

<!-- key: Centroid x (m) -->
مركز الكتلة x (m)

<!-- key: Steps -->
الخطوات

<!-- key: Source box (m) -->
أبعاد المصدر (m)

<!-- key: End (d) -->
النهاية (يوم)

<!-- key: Scenario -->
السيناريو

<!-- key: Point -->
النقطة

<!-- key: Requested x -->
x المطلوب

<!-- key: Requested y -->
y المطلوب

<!-- key: Requested z -->
z المطلوب

<!-- key: Cell centre x -->
مركز الخلية x

<!-- key: Cell centre y -->
مركز الخلية y

<!-- key: Cell centre z -->
مركز الخلية z

<!-- key: Layer -->
الطبقة

<!-- key: Row -->
الصف

<!-- key: Column -->
العمود

<!-- key: Cumulative in (g) -->
الإدخال التراكمي (g)

<!-- key: Cumulative out (g) -->
الإخراج التراكمي (g)

<!-- key: Sources (g) -->
المصادر (g)

<!-- key: Sinks (g) -->
المصارف (g)

<!-- key: Fluid storage (g) -->
تخزين المائع (g)

<!-- key: Native resident mass (g) -->
الكتلة المقيمة من البرنامج (g)

<!-- key: Alternative disc. (%) -->
الفرق البديل (%)

<!-- key: Analytical reference requires homogeneous steady flow. -->
يتطلب المرجع التحليلي جريانًا مستقرًا ومتجانسًا.

<!-- key: Source cells -->
خلايا المصدر

<!-- key: Specified head -->
منسوب محدد

<!-- key: Section locations -->
مواقع المقاطع

<!-- key: Background flow -->
الجريان الخلفي

<!-- key: Model preview: grid, boundaries and source -->
معاينة: الشبكة والحدود والمصدر

<!-- key: Computed head contours -->
خطوط المنسوب المحسوبة

<!-- key: Homogeneous steady head contours -->
خطوط المنسوب المستقر المتجانس

<!-- key: Time (d) -->
الزمن (يوم)

<!-- key: Mass rate (g/d) -->
معدل الكتلة (g/يوم)

<!-- key: Instantaneous mass (g) -->
الكتلة اللحظية (g)

<!-- key: Dirac input (initial cell mass) -->
إدخال ديراك (كتلة الخلايا الأولية)

<!-- key: Finite pulse input -->
إدخال نبضة محدودة

<!-- key: Continuous input -->
إدخال مستمر

<!-- key: Concentration (g/m³) -->
التركيز (g/m³)

<!-- key: Elevation z (m) -->
الارتفاع z (m)

<!-- key: MODPATH advection (slice) -->
حمل MODPATH (شريحة)

<!-- key: Analytical -->
تحليلي

<!-- key: Analytical (active run) -->
تحليلي (التشغيل النشط)

<!-- key: Mass output unavailable -->
مخرجات الكتلة غير متاحة

<!-- key: MT3D discrepancy (%) -->
فرق MT3D (%)

<!-- key: Initial + injected mass (first run) -->
الكتلة الأولية + المدخلة (أول تشغيل)

<!-- key: Resident mass: grid sum and MT3D budget -->
الكتلة المقيمة: مجموع الشبكة وميزانية MT3D

<!-- key: Reported mass-balance closure -->
إغلاق ميزانية الكتلة المبلغ عنه

<!-- key: Example: pulse plume after 600 days -->
مثال: سحابة نبضة بعد 600 يوم

<!-- key: Example: observation P1 -->
مثال: الرصد P1

<!-- key: P1 · x (m) -->
P1 · x (m)

<!-- key: P1 · y (m) -->
P1 · y (m)

<!-- key: P1 · elevation z (m) -->
P1 · الارتفاع z (m)

<!-- key: P2 · x (m) -->
P2 · x (m)

<!-- key: P2 · y (m) -->
P2 · y (m)

<!-- key: P2 · elevation z (m) -->
P2 · الارتفاع z (m)

<!-- key: P3 · x (m) -->
P3 · x (m)

<!-- key: P3 · y (m) -->
P3 · y (m)

<!-- key: P3 · elevation z (m) -->
P3 · الارتفاع z (m)

<!-- key: P4 · x (m) -->
P4 · x (m)

<!-- key: P4 · y (m) -->
P4 · y (m)

<!-- key: P4 · elevation z (m) -->
P4 · الارتفاع z (m)

<!-- key: P5 · x (m) -->
P5 · x (m)

<!-- key: P5 · y (m) -->
P5 · y (m)

<!-- key: P5 · elevation z (m) -->
P5 · الارتفاع z (m)

<!-- key: fig_head -->
المنسوب المحدد: {head:g} m

<!-- key: fig_layers -->
{layers} طبقة؛ المقياس الرأسي مبالغ فيه

<!-- key: fig_total -->
الإجمالي: {mass:g} g

<!-- key: fig_initial -->
{mass:g} g عند t = 0

<!-- key: fig_xprofile -->
مقطع x عند y = {y:.3g} m

<!-- key: fig_yprofile -->
مقطع y عند x = {x:.3g} m

<!-- key: fig_section -->
مقطع {axis}–z عند {other} = {value:.3g} m

<!-- key: fig_title -->
{method} · t = {time:g} يوم · طبقة {layer} (z = {z:.3g} m)

<!-- key: fig_gridmass -->
{label}: مجموع الشبكة

<!-- key: fig_nativemass -->
{label}: ميزانية MT3D

<!-- key: fig_nodata -->
{label}: خارج المجال — لا بيانات

<!-- key: table_help_MB disc. (%) -->
الفرق النهائي لميزانية الكتلة كما يبلّغه MT3D.

<!-- key: table_help_Flow disc. (%) -->
الفرق النهائي لميزانية المياه في MODFLOW.

<!-- key: table_help_MT3D (s) -->
الزمن الفعلي لتشغيل برنامج النقل.

<!-- key: table_help_MP7 (s) -->
زمن MODPATH؛ تصف الجسيمات الحمل فقط.

<!-- key: table_help_Ref. L1 (%) -->
خطأ التركيز المطلق المرجّح بحجم المسام مقسومًا على الكتلة المرجعية.

<!-- key: table_help_Mass (g) -->
الكتلة المذابة النهائية المتكاملة من شبكة التركيز.

<!-- key: MT3DMS final mass discrepancy exceeds 1%; inspect method and transport time step settings. -->
يتجاوز فرق الكتلة النهائي في MT3DMS نسبة 1%؛ راجع الطريقة وخطوة النقل الزمنية.

<!-- key: At least one MODFLOW water-budget discrepancy exceeds 0.1%. -->
يتجاوز فرق واحد على الأقل لميزانية MODFLOW نسبة 0.1%.

<!-- key: Negative concentrations occurred. They are retained in diagnostics and exports; central FD and particle methods can oscillate. -->
ظهرت تراكيز سالبة وتُحفظ في التشخيص والتصدير؛ قد تتذبذب FD المركزية وطرق الجسيمات.

<!-- key: Source coordinates must lie inside the domain. -->
يجب أن تقع إحداثيات المصدر داخل المجال.

<!-- key: This confined lab requires heads at or above aquifer top. -->
يتطلب هذا الخزان المحصور مناسيب عند سطحه العلوي أو فوقه.

<!-- key: Pulse duration must be between zero and model duration. -->
يجب أن تكون مدة النبضة بين الصفر ومدة النموذج.

<!-- key: Observation point is outside the model. -->
نقطة الرصد خارج النموذج.

<!-- key: TVD requires PERCEL no greater than 1. -->
يتطلب TVD أن يكون PERCEL ≤ 1.

<!-- key: language_fallback -->
يُستخدم النص الإنجليزي عند غياب الترجمة.

<!-- key: preset_random -->
معاملات عشوائية

<!-- key: Random unit x (m) -->
وحدة عشوائية x (m)

<!-- key: Random unit y (m) -->
وحدة عشوائية y (m)

<!-- key: random_hint -->
الوحدات الصغيرة تعطي نمطًا دقيقًا والكبيرة رقعًا أوسع. ثبّت البذرة والأبعاد الفيزيائية للحفاظ على التحقيق عند تنعيم الشبكة.

<!-- key: Active cells -->
الخلايا النشطة

<!-- key: table_help_Active cells -->
جميع الخلايا غير المعطلة، بما فيها خلايا المنسوب المحدد.

<!-- key: Random field -->
حقل عشوائي

<!-- key: Comparison runs -->
تشغيلات المقارنة

<!-- key: discard_tags_hint -->
احذف وسم التشغيل بعلامة × لإزالته. حذف جميع الوسوم يبدأ مقارنة جديدة. صدّر أولًا ما تريد الاحتفاظ به.

<!-- key: Head contours -->
خطوط تساوي المنسوب

<!-- key: Computed head contours (m) -->
خطوط المنسوب المحسوبة (m)

<!-- key: Head contours appear after running the model -->
تظهر خطوط المنسوب بعد التشغيل

<!-- key: fig_background_k -->
K الخلفية = {k:.2e} m/s

<!-- key: fig_low_lens_k -->
عدسة منخفضة K: K = {k:.2e} m/s

<!-- key: fig_high_channel_k -->
قناة مرتفعة K: K = {k:.2e} m/s

<!-- key: fig_low_barrier_k -->
حاجز منخفض K: K = {k:.2e} m/s

<!-- key: Focus on plume -->
التركيز على السحابة

<!-- key: Focus threshold (% of peak) -->
العتبة (% من الذروة)

<!-- key: focus_hint -->
تُستخدم الذروة الموجبة الحالية لكل سحابة معروضة مع هامش 20% لكل جانب. تُدرج مسارات MODPATH المرئية. عند غياب السحابة والمسارات يُعرض المجال كاملًا. يتغير المسقط الأفقي فقط.

<!-- key: Download plume figure (SVG) -->
تنزيل رسم السحابة (SVG)

<!-- key: steady -->
مستقر

<!-- key: transient -->
غير مستقر

<!-- key: fig_minimum -->
الحد الأدنى العددي: {minimum:.3g} g/m³

<!-- key: fig_minimum_log -->
الحد الأدنى العددي: {minimum:.3g} g/m³ (القيم غير الموجبة مخفية بالمقياس اللوغاريتمي)

<!-- key: The plume reaches an x specified-head boundary; enlarge the domain before treating the infinite-x analytical solution as a benchmark. -->
بلغت السحابة حد منسوب محدد في x؛ وسّع المجال قبل اعتماد المرجع التحليلي غير المحدود.

<!-- key: fig_reference_boundary -->
عُطلت الدقة التحليلية: تأثير حدود x يتجاوز عتبة {tolerance_percent:.2g}%.

<!-- key: Low K lens -->
عدسة منخفضة K

<!-- key: High K channel -->
قناة مرتفعة K

<!-- key: Low K barrier -->
حاجز جزئي منخفض K
