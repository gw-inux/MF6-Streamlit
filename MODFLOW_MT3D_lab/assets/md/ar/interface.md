## title

مختبر انتقال المذاب أحادي البعد

## experiments

تجارب إرشادية

## experiment_front

جبهة الحمل

## experiment_spreading

التشتت الفيزيائي

## experiment_impulse

النبضة المستطيلة ونبضة ديراك

## theory_title

مجال الجريان والحلول التحليلية

## setup

إعداد النموذج

## inlet_processes

المدخل والانتقال

## grid_time

الشبكة والزمن

## solver

طريقة MT3DMS

## signal

إشارة المدخل

## continuous

إدخال مستمر

## block

نبضة مستطيلة

## dirac

نبضة ديراك

## amplitude

تركيز المدخل C/Cref [–]

## block_days

مدة النبضة [d]

## impulse_area

مساحة النبضة A [d]

## impulse_days

عرض النبضة العددية ε [d]

## rectangle

ارتفاع نبضة المدخل في MT3DMS = {height:.4g} C/Cref.

## dispersion

تفعيل التشتت

## dispersivity

التشتتية الطولية αL [m]

## diffusion

الانتشار الفعال Dₑ [m²/d]

## grid_by

تحديد الشبكة حسب

## cells

عدد الخلايا

## spacing

التباعد

## cell_count

الخلايا

## target_spacing

عرض الخلية المطلوب [m]

## grid_summary

{n} خلية · Δx الفعلي = {dx:.3g} m

## courant

حد عدد كورانت

## time_hint

تنتهي جميع الحالات في اليوم 2000. تُقسّم فترة تطبيق النبضة المحدودة إلى ثماني خطوات انتقال على الأقل.

## scheme

مخطط الحمل

## upwind

فروق منتهية · المنبع

## central

فروق منتهية · مركزي

## tvd

TVD · ULTIMATE

## moc

MOC

## mmoc

MMOC

## hmoc

HMOC

## solver_hint

يوفر MODFLOW-2005 مجال الجريان المستقر. ويحل MT3DMS معادلاته الضمنية باستخدام GCG.

## preview

معاينة النموذج

## preview_summary

{signal} · {scheme} · {n} خلية · Δx = {dx:.3g} m · D = {D:.4g} m²/d

## distance

المسافة من المدخل [m]

## time

الزمن [d]

## inlet_axis

المدخل C/Cref [–]

## optional_name

اسم الحالة (اختياري)

## name_example

مثلاً شبكة دقيقة مع TVD

## limit

تم حفظ عشر حالات. احذف حالة من «إدارة الحالات» لتشغيل حالة أخرى.

## missing

البرنامج المطلوب مفقود أو غير متوافق — {names}. استخدم مجلد bin المشترك أو عيّن TRANSPORT_LAB_BIN.

## run

تشغيل النموذج

## running

جارٍ تشغيل MODFLOW-2005 وMT3DMS…

## failed

تعذر إكمال الحساب. تتوفر الحالات المحفوظة أدناه.

## diagnostic

تفاصيل الحساب

## results

نتائج الانتقال

## visible

الحالات المعروضة

## cells_unit

خلية

## show_analytical

الحل التحليلي

## show_markers

النقاط العددية

## profile

منحنى التركيز المكاني

## breakthrough

منحنى الاختراق

## budget

ميزانية كتلة المذاب

## profile_time

زمن المنحنى [d]

## observation

مسافة الرصد [m]

## applied_curve

تحليلي · إشارة المدخل المطبقة

## ideal_curve

ديراك المثالي

## mass_axis

خطأ ميزانية الكتلة [%]

## no_selection

اختر حالة لعرض منحنياتها.

## comparison

المقارنة النهائية · اليوم 2000

## variant

الحالة

## rmse

RMSE

## mae

MAE

## ideal_rmse

RMSE · ديراك المثالي

## mass_error

خطأ الكتلة [%]

## seconds

مدة الحساب [s]

## run_name

الاسم

## dx_col

Δx [m]

## height_col

المدخل C/Cref

## duration_col

مدة الإدخال [d]

## area_col

ديراك A [d]

## alpha_col

αL [m]

## dm_col

Dₑ [m²/d]

## d_col

D [m²/d]

## pe_col

عدد بيكليه للشبكة

## co_col

حد كورانت

## count_col

خطوات الانتقال

## flow_s

MODFLOW [s]

## mt_s

MT3DMS [s]

## flow_error

ميزانية المياه [%]

## min_c

أدنى C/Cref نهائي

## max_c

أعلى C/Cref نهائي

## detail_heading

الإعدادات وتعريف المؤشرات

## download

تنزيل المقارنة (CSV)

## manage

إدارة الحالات

## remove_choice

الحالة المراد حذفها

## remove

حذف الحالة المحددة

## references_title

المراجع

## saved

تم حفظ V{number} للمقارنة.

## applied_color_key

تحليلي · بلون الحالة

## ideal_color_key

ديراك المثالي · بلون الحالة

## pulse_cells

طول النبضة [خلايا]

## pulse_resolution

خلال الإدخال تنقل حركة الماء النبضة مسافة {length:.3g} m، أي {cells:.3g} خلية.

## specified_head

منسوب بيزومتري محدد · {head:.4g} m

## hydraulic_summary

الموصلية الهيدروليكية K = {k:.0e} m/s

## scenario_reset_hint

التغييرات هنا تمسح حالات المقارنة المحفوظة.

## comparison_cleared

تغيرت إعدادات المدخل أو الانتقال. تم مسح المقارنة لبدء السيناريو الجديد.

## concept_title

النموذج المفاهيمي والاستجابات النموذجية

## concept_inlet

المدخل

## concept_outlet

المخرج

## concept_observation

الرصد

## concept_profile

القطاع عند t = {time:g} d

## concept_breakthrough

الوصول عند x = {distance:g} m

## concept_advection

حمل فقط

## concept_dispersion

حمل + تشتت
