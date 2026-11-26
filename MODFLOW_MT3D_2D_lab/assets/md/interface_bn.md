<!-- key: title -->
MT3D – 2D/3D পরিবহন পরীক্ষাগার

<!-- key: intro_caption -->
পরিচিতিমূলক চিত্র: প্লুম ও ব্রেকথ্রু বক্ররেখার উদাহরণ; বর্তমান মডেলের ইনপুট থেকে স্বাধীন।

<!-- key: Model & run -->
1 · মডেল ও গণনা

<!-- key: Results & method comparison -->
2 · ফলাফল ও পদ্ধতির তুলনা

<!-- key: series_reset -->
ইনপুট সংকেত বা মডেল/উৎসের জ্যামিতি পরিবর্তিত হওয়ায় নতুন তুলনা শুরু হয়েছে। আগের রানগুলি মুছে ফেলা হয়েছে।

<!-- key: grid_summary -->
গ্রিড: {nx} × {ny} × {nz} সেল। প্রকৃত সেলের মাপ: Δx = {dx:.3f} m; Δy = {dy:.3f} m; Δz = {dz:.3f} m।

<!-- key: velocity_summary -->
সমসত্ত্ব মাধ্যমের রেফারেন্স রন্ধ্রবেগ: {velocity:.4f} m/দিন।

<!-- key: source_bounds -->
x = {x0:.2f}–{x1:.2f} m; y = {y0:.2f}–{y1:.2f} m; z = {z0:.2f}–{z1:.2f} m.

<!-- key: source_snap_hint -->
উৎস নির্বাচিত সেলগুলিতে থাকে। বিভেদন বদলালে তার প্রকৃত আকার বদলাতে পারে। সেলের মাপ দিয়ে ইনপুটে মোট বিস্তার অপরিবর্তিত থাকে ও প্রকৃত সমান ব্যবধান দেখানো হয়।

<!-- key: input_error -->
গণনার আগে চিহ্নিত সেটিংগুলি সংশোধন করুন।

<!-- key: missing_executables -->
প্রয়োজনীয় প্রোগ্রাম পাওয়া যায়নি: {names}। অ্যাপ বা রিপোজিটরির `bin/`-এ সামঞ্জস্যপূর্ণ এক্সিকিউটেবল রাখুন। স্থানীয়ভাবে: `python setup_executables.py`।

<!-- key: label_placeholder -->
স্বয়ংক্রিয়: 01 TVD / Pulse (বিষমসত্ত্ব: / het.)

<!-- key: history_full -->
দশটি রান সংরক্ষিত আছে। চালিয়ে যেতে একটি রান সরান বা তুলনার তালিকা খালি করুন।

<!-- key: running -->
MODFLOW, MT3D ও ঐচ্ছিক MODPATH চলছে…

<!-- key: run_success -->
গণনা সম্পূর্ণ। সর্বশেষ ফলাফল দেখানো হচ্ছে।

<!-- key: run_failed -->
এই রান সম্পূর্ণ হয়নি এবং তুলনায় যোগ করা হয়নি।

<!-- key: changed_source_footprint -->
গ্রিড সূক্ষ্ম করায় উৎসের প্রকৃত বিস্তার বদলেছে। বিস্তারিত সারণিতে উৎসের মাপ দেখুন।

<!-- key: nearest_time -->
{name}: নিকটতম সংরক্ষিত সময় {time:.3f} দিন (প্রদর্শিত রান: {target:.3f} দিন)।

<!-- key: no_comparison_time -->
{name}: {time:.3f} দিনে আউটপুট নেই; বাদ দেওয়া হয়েছে।

<!-- key: evaluating_reference -->
বিশ্লেষণাত্মক রেফারেন্স গণনা হচ্ছে…

<!-- key: export_hint -->
আর্কাইভে মডেল ইনপুট, লগ, ঘনত্ব/হেড অ্যারে, ভর নির্ণয় ও কণার তথ্য রয়েছে; আগমনের বিবরণও সংরক্ষিত থাকে।

<!-- key: no_runs -->
প্লুম, প্রোফাইল, ব্রেকথ্রু বক্ররেখা ও পদ্ধতির তুলনা দেখতে প্রাথমিক পালস পরীক্ষা চালান।

<!-- key: footer -->
MT3D 2D/3D · v0.5.0 · সরাসরি শিক্ষাদানের কার্যকরী সংস্করণ

<!-- key: transient_hint -->
প্রাথমিক প্রবাহ ভারসাম্যে পৌঁছায়; ডান হেড t = 0-তে বদলায়।

<!-- key: expert_flow_hint -->
প্রবাহ সলভারের সহনসীমা ও পুনরাবৃত্তি বদলাতে বিশেষজ্ঞ সেটিং চালু করুন।

<!-- key: stochastic_hint -->
স্থির বীজে অঞ্চল পুনরুৎপাদনযোগ্য। K ও Ss লগ-স্কেলে সমবণ্টিত, রন্ধ্রতা সাধারণ সমবণ্টিত। গ্রিড সূক্ষ্ম করলেও একই বিন্যাস থাকে।

<!-- key: zones_hint -->
আয়তক্ষেত্র সেলের কেন্দ্র দিয়ে নির্বাচন করে; পরের সারি আগেরটি প্রতিস্থাপন করে। স্তর গণনা 1 থেকে।

<!-- key: observation_hint -->
পর্যবেক্ষণ বক্ররেখা বিন্দু ধারণকারী সেলের মান ব্যবহার করে। সংরক্ষিত মডেল আবার না চালিয়েই অবস্থান বদলানো যায়।

<!-- key: output_hint -->
t = 0 ও শেষ সময় অন্তর্ভুক্ত। চিত্র ও রপ্তানির জন্য ঘনত্ব আউটপুট নিয়ন্ত্রণ করে।

<!-- key: preset_homogeneous -->
সমসত্ত্ব

<!-- key: preset_lens -->
নিম্ন K লেন্স

<!-- key: preset_channel -->
উচ্চ K চ্যানেল

<!-- key: preset_barrier -->
আংশিক নিম্ন K বাধা

<!-- key: preset_stochastic -->
দৈব অঞ্চলবিভাগ

<!-- key: preset_custom -->
নিজস্ব আয়তক্ষেত্র

<!-- key: preset_hint_lens -->
কেন্দ্রীয় লেন্স: K = 0.01 × পটভূমি K; পুরো গভীরতা।

<!-- key: preset_hint_channel -->
অনুদৈর্ঘ্য চ্যানেল: K = 10 × পটভূমি K; পুরো গভীরতা।

<!-- key: preset_hint_barrier -->
আংশিক আড়াআড়ি বাধা: K = 0.01 × পটভূমি K; পাশ দিয়ে প্রবাহের পথ থাকে।

<!-- key: signal_pulse -->
পালস / আয়তাকার ইনপুট

<!-- key: signal_continuous -->
অবিরাম ইনপুট

<!-- key: signal_dirac -->
ডিরাক / তাৎক্ষণিক নিঃসরণ

<!-- key: signal_short_pulse -->
পালস

<!-- key: signal_short_continuous -->
অবিরাম

<!-- key: signal_short_dirac -->
ডিরাক

<!-- key: Concept, assumptions and equations -->
ধারণা, অনুমান ও সমীকরণ

<!-- key: Guided experiments -->
নির্দেশিত পরীক্ষা

<!-- key: Expert settings -->
বিশেষজ্ঞ সেটিং

<!-- key: Use sliders for main parameters -->
মূল মানের জন্য স্লাইডার

<!-- key: Flow & domain -->
প্রবাহ ও ক্ষেত্র

<!-- key: Transport & source -->
পরিবহন ও উৎস

<!-- key: Post-processing & observations -->
পরবর্তী বিশ্লেষণ ও পর্যবেক্ষণ

<!-- key: Hydraulic properties -->
জলীয় ধর্ম

<!-- key: Hydraulic conductivity K (m/s) -->
জলীয় পরিবাহিতা K (m/s)

<!-- key: Effective porosity (-) -->
কার্যকর রন্ধ্রতা (-)

<!-- key: Specific storage Ss (1/m) -->
নির্দিষ্ট সঞ্চয় Ss (1/m)

<!-- key: Vertical / horizontal K -->
উল্লম্ব / অনুভূমিক K

<!-- key: Boundary conditions -->
সীমানা শর্ত

<!-- key: Specified head left (m) -->
নির্দিষ্ট বাম হেড (m)

<!-- key: Specified head right (m) -->
নির্দিষ্ট ডান হেড (m)

<!-- key: Transient flow experiment -->
অস্থায়ী প্রবাহ পরীক্ষা

<!-- key: Right head after t = 0 (m) -->
t = 0-এর পর ডান হেড (m)

<!-- key: Model extent and spatial discretization -->
মডেলের বিস্তার ও স্থানিক বিচ্ছিন্নীকরণ

<!-- key: Model length in x-direction (m) -->
x দিকে দৈর্ঘ্য (m)

<!-- key: Model width in y-direction (m) -->
y দিকে প্রস্থ (m)

<!-- key: Aquifer thickness / top elevation (m) -->
জলাধারের পুরুত্ব / শীর্ষ উচ্চতা (m)

<!-- key: Define the grid by -->
গ্রিড নির্ধারণের উপায়

<!-- key: Number of cells -->
সেলের সংখ্যা

<!-- key: Cell width -->
সেলের মাপ

<!-- key: Cells x -->
x সেল

<!-- key: Cells y -->
y সেল

<!-- key: Cell width x (m) -->
x সেলের মাপ (m)

<!-- key: Cell width y (m) -->
y সেলের মাপ (m)

<!-- key: Number of layers -->
স্তরের সংখ্যা

<!-- key: Numerical solution for flow -->
প্রবাহের সাংখ্যিক সমাধান

<!-- key: Head tolerance (m) -->
হেড সহনসীমা (m)

<!-- key: Flow residual tolerance (m³/day) -->
প্রবাহ অবশিষ্ট সহনসীমা (m³/দিন)

<!-- key: PCG outer iterations -->
PCG বাইরের পুনরাবৃত্তি

<!-- key: PCG inner iterations -->
PCG ভিতরের পুনরাবৃত্তি

<!-- key: Flow time steps (approximately total) -->
প্রবাহের সময়ধাপ (প্রায় মোট)

<!-- key: Hydrogeology and zonation -->
জলভূতত্ত্ব ও বিষমতা

<!-- key: Hydrogeology preset -->
জলভূতাত্ত্বিক পূর্বনির্ধারণ

<!-- key: Number of zones -->
অঞ্চলের সংখ্যা

<!-- key: Random seed -->
দৈব বীজ

<!-- key: K range (m/s) -->
K সীমা (m/s)

<!-- key: Ss range (1/m) -->
Ss সীমা (1/m)

<!-- key: Porosity range (-) -->
রন্ধ্রতার সীমা (-)

<!-- key: Minimum -->
সর্বনিম্ন

<!-- key: Maximum -->
সর্বোচ্চ

<!-- key: Edit hydrogeological zones -->
অঞ্চল সম্পাদনা

<!-- key: Zone name -->
অঞ্চলের নাম

<!-- key: First layer -->
প্রথম স্তর

<!-- key: Last layer -->
শেষ স্তর

<!-- key: Porosity -->
রন্ধ্রতা

<!-- key: Boundary conditions and source -->
সীমানা শর্ত ও উৎস

<!-- key: Input signal -->
ইনপুট সংকেত

<!-- key: Released mass (g) -->
নিঃসৃত ভর (g)

<!-- key: Mass input rate (g/day) -->
ভর প্রবেশের হার (g/দিন)

<!-- key: Pulse duration (days) -->
পালসের সময়কাল (দিন)

<!-- key: Source x (m) -->
উৎস x (m)

<!-- key: Source y (m) -->
উৎস y (m)

<!-- key: Source cells x -->
উৎস সেল x

<!-- key: Source cells y -->
উৎস সেল y

<!-- key: Source spans all layers -->
উৎস সব স্তরে

<!-- key: Source layer (1 = top) -->
উৎস স্তর (1 = শীর্ষ)

<!-- key: Transport parameters -->
পরিবহন পরামিতি

<!-- key: Dispersion -->
বিচ্ছুরণ

<!-- key: Longitudinal dispersivity (m) -->
অনুদৈর্ঘ্য বিচ্ছুরণ দৈর্ঘ্য (m)

<!-- key: Horizontal transverse / longitudinal -->
অনুভূমিক আড়াআড়ি / অনুদৈর্ঘ্য

<!-- key: Vertical transverse / longitudinal -->
উল্লম্ব আড়াআড়ি / অনুদৈর্ঘ্য

<!-- key: Temporal discretization -->
সময়ের বিচ্ছিন্নীকরণ

<!-- key: Transport duration (days) -->
পরিবহনের সময়কাল (দিন)

<!-- key: DT0 · initial step (days; 0 = automatic) -->
DT0 · প্রাথমিক ধাপ (দিন; 0 = স্বয়ংক্রিয়)

<!-- key: TTSMAX · maximum step (days; 0 = automatic) -->
TTSMAX · সর্বোচ্চ ধাপ (দিন; 0 = স্বয়ংক্রিয়)

<!-- key: TTSMULT · step multiplier -->
TTSMULT · ধাপের গুণক

<!-- key: MXSTRN · maximum transport steps -->
MXSTRN · সর্বোচ্চ পরিবহন ধাপ

<!-- key: Numerical solution for transport -->
পরিবহনের সাংখ্যিক সমাধান

<!-- key: MT3D advection method -->
MT3D অভিবহন পদ্ধতি

<!-- key: MODPATH particle comparison -->
MODPATH কণার তুলনা

<!-- key: PERCEL · Courant number -->
PERCEL · কুরান্ট সংখ্যা

<!-- key: CCLOSE · concentration tolerance -->
CCLOSE · ঘনত্ব সহনসীমা

<!-- key: Timeout per executable (seconds) -->
প্রতি প্রোগ্রামের সময়সীমা (সেকেন্ড)

<!-- key: Expert transport solver settings -->
বিশেষজ্ঞ পরিবহন সলভার সেটিং

<!-- key: MXPART · maximum particles -->
MXPART · সর্বোচ্চ কণা

<!-- key: ITRACK · tracking algorithm -->
ITRACK · অনুসরণ অ্যালগরিদম

<!-- key: WD · concentration weighting -->
WD · ঘনত্বের ওজন

<!-- key: DCEPS · gradient threshold -->
DCEPS · গ্রেডিয়েন্ট সীমা

<!-- key: NPLANE · particle planes -->
NPLANE · কণার তল

<!-- key: NPL · low-gradient particles -->
NPL · নিম্ন গ্রেডিয়েন্ট কণা

<!-- key: NPH · high-gradient particles -->
NPH · উচ্চ গ্রেডিয়েন্ট কণা

<!-- key: NPMIN · minimum particles/cell -->
NPMIN · সর্বনিম্ন কণা/সেল

<!-- key: NPMAX · maximum particles/cell -->
NPMAX · সর্বোচ্চ কণা/সেল

<!-- key: INTERP · interpolation -->
INTERP · অন্তর্বেশন

<!-- key: NLSINK · sink planes -->
NLSINK · নিষ্কাশন তল

<!-- key: NPSINK · sink particles -->
NPSINK · নিষ্কাশন কণা

<!-- key: DCHMOC · HMOC threshold -->
DCHMOC · HMOC সীমা

<!-- key: MXITER · GCG outer iterations -->
MXITER · GCG বাইরের পুনরাবৃত্তি

<!-- key: ITER1 · GCG inner iterations -->
ITER1 · GCG ভিতরের পুনরাবৃত্তি

<!-- key: ISOLVE · preconditioner -->
ISOLVE · প্রি-কন্ডিশনার

<!-- key: NCRS · cross-dispersion -->
NCRS · ক্রস-বিচ্ছুরণ

<!-- key: ACCL · relaxation -->
ACCL · রিল্যাক্সেশন

<!-- key: IPRGCG · print interval -->
IPRGCG · মুদ্রণ ব্যবধান

<!-- key: MODPATH release settings -->
MODPATH কণা নিঃসরণ সেটিং

<!-- key: Particles per source cell -->
প্রতি উৎস সেলের কণা

<!-- key: Release batches (pulse / continuous) -->
নিঃসরণ ব্যাচ (পালস / অবিরাম)

<!-- key: Observation points -->
পর্যবেক্ষণ বিন্দু

<!-- key: Number of observation points -->
পর্যবেক্ষণ বিন্দুর সংখ্যা

<!-- key: Output settings -->
আউটপুট সেটিং

<!-- key: Saved transport times -->
সংরক্ষিত পরিবহন সময়

<!-- key: Actual source footprint -->
উৎসের প্রকৃত বিস্তার

<!-- key: Optional run label -->
ঐচ্ছিক রানের নাম

<!-- key: Run model -->
মডেল চালান

<!-- key: Run diagnostic -->
রানের নির্ণয়

<!-- key: More comparison metrics -->
আরও তুলনার সূচক

<!-- key: Displayed run -->
প্রদর্শিত রান

<!-- key: Run to remove -->
সরানোর রান

<!-- key: Remove -->
সরান

<!-- key: Clear comparison runs -->
তুলনার রান খালি করুন

<!-- key: Plume & sections -->
প্লুম ও ছেদ

<!-- key: Observation curves -->
পর্যবেক্ষণ বক্ররেখা

<!-- key: Mass & diagnostics -->
ভর ও নির্ণয়

<!-- key: Export -->
রপ্তানি

<!-- key: Time (days) -->
সময় (দিন)

<!-- key: Top-view layer -->
উপরের দৃশ্যের স্তর

<!-- key: Layer {number} -->
স্তর {number}

<!-- key: Analytical reference -->
বিশ্লেষণাত্মক রেফারেন্স

<!-- key: Plot settings and section positions -->
চিত্র সেটিং ও ছেদের অবস্থান

<!-- key: x-direction section · y (m) -->
x দিকের ছেদ · y (m)

<!-- key: y-direction section · x (m) -->
y দিকের ছেদ · x (m)

<!-- key: Colour fill -->
রঙ ভরাট

<!-- key: Contour lines -->
সমমান রেখা

<!-- key: Log colours -->
লগারিদমিক রঙ

<!-- key: Particle paths -->
কণার পথ

<!-- key: Opacity -->
অস্বচ্ছতা

<!-- key: Compare runs in x / y sections -->
x / y ছেদে রানের তুলনা

<!-- key: Compare section profiles -->
প্রোফাইল তুলনা

<!-- key: Runs for section comparison -->
ছেদ তুলনার রান

<!-- key: Also overlay top-view contours -->
উপরের সমমান রেখাও দেখান

<!-- key: Download plume figure (PNG) -->
প্লুম চিত্র ডাউনলোড (PNG)

<!-- key: Runs in breakthrough comparison -->
ব্রেকথ্রু তুলনার রান

<!-- key: Observation cells used by each run -->
প্রতি রানের পর্যবেক্ষণ সেল

<!-- key: Download breakthrough curves (CSV) -->
ব্রেকথ্রু বক্ররেখা ডাউনলোড (CSV)

<!-- key: Detailed mass-budget data -->
বিস্তারিত ভর ভারসাম্য তথ্য

<!-- key: Stored run configuration -->
সংরক্ষিত রানের বিন্যাস

<!-- key: Download comparison table (CSV) -->
তুলনার সারণি ডাউনলোড (CSV)

<!-- key: Download run configuration (JSON) -->
রানের বিন্যাস ডাউনলোড (JSON)

<!-- key: Prepare complete displayed-run archive -->
প্রদর্শিত রানের পূর্ণ আর্কাইভ তৈরি

<!-- key: Preparing archive… -->
আর্কাইভ তৈরি হচ্ছে…

<!-- key: Download run archive (ZIP) -->
রানের আর্কাইভ ডাউনলোড (ZIP)

<!-- key: Run -->
রান

<!-- key: Method -->
পদ্ধতি

<!-- key: Signal -->
সংকেত

<!-- key: Grid -->
গ্রিড

<!-- key: K zones -->
K অঞ্চল

<!-- key: Flow -->
প্রবাহ

<!-- key: MB disc. (%) -->
ভর বিচ্যুতি (%)

<!-- key: Flow disc. (%) -->
প্রবাহ বিচ্যুতি (%)

<!-- key: MT3D (s) -->
MT3D (s)

<!-- key: MP7 (s) -->
MP7 (s)

<!-- key: Flow (s) -->
প্রবাহ (s)

<!-- key: Total (s) -->
মোট (s)

<!-- key: Ref. L1 (%) -->
রেফা. L1 (%)

<!-- key: Mass (g) -->
ভর (g)

<!-- key: Input (g) -->
ইনপুট (g)

<!-- key: Min. C (g/m³) -->
সর্বনিম্ন C (g/m³)

<!-- key: Neg. mass (g) -->
ঋণাত্মক ভর (g)

<!-- key: Centroid x (m) -->
ভরকেন্দ্র x (m)

<!-- key: Steps -->
ধাপ

<!-- key: Source box (m) -->
উৎসের বিস্তার (m)

<!-- key: End (d) -->
শেষ (দিন)

<!-- key: Scenario -->
পরিস্থিতি

<!-- key: Point -->
বিন্দু

<!-- key: Requested x -->
নির্ধারিত x

<!-- key: Requested y -->
নির্ধারিত y

<!-- key: Requested z -->
নির্ধারিত z

<!-- key: Cell centre x -->
সেলের কেন্দ্র x

<!-- key: Cell centre y -->
সেলের কেন্দ্র y

<!-- key: Cell centre z -->
সেলের কেন্দ্র z

<!-- key: Layer -->
স্তর

<!-- key: Row -->
সারি

<!-- key: Column -->
কলাম

<!-- key: Cumulative in (g) -->
পুঞ্জীভূত প্রবেশ (g)

<!-- key: Cumulative out (g) -->
পুঞ্জীভূত নির্গমন (g)

<!-- key: Sources (g) -->
উৎস (g)

<!-- key: Sinks (g) -->
নিষ্কাশন (g)

<!-- key: Fluid storage (g) -->
তরল সঞ্চয় (g)

<!-- key: Native resident mass (g) -->
প্রোগ্রামের অবশিষ্ট ভর (g)

<!-- key: Alternative disc. (%) -->
বিকল্প বিচ্যুতি (%)

<!-- key: Analytical reference requires homogeneous steady flow. -->
বিশ্লেষণাত্মক রেফারেন্সের জন্য সমসত্ত্ব স্থির প্রবাহ দরকার।

<!-- key: Source cells -->
উৎস সেল

<!-- key: Specified head -->
নির্দিষ্ট হেড

<!-- key: Section locations -->
ছেদের অবস্থান

<!-- key: Background flow -->
পটভূমির প্রবাহ

<!-- key: Model preview: grid, boundaries and source -->
পূর্বরূপ: গ্রিড, সীমানা ও উৎস

<!-- key: Computed head contours -->
গণনাকৃত হেড সমমান রেখা

<!-- key: Homogeneous steady head contours -->
সমসত্ত্ব স্থির হেড সমমান রেখা

<!-- key: Time (d) -->
সময় (দিন)

<!-- key: Mass rate (g/d) -->
ভরের হার (g/দিন)

<!-- key: Instantaneous mass (g) -->
তাৎক্ষণিক ভর (g)

<!-- key: Dirac input (initial cell mass) -->
ডিরাক ইনপুট (সেলের প্রাথমিক ভর)

<!-- key: Finite pulse input -->
সসীম পালস ইনপুট

<!-- key: Continuous input -->
অবিরাম ইনপুট

<!-- key: Concentration (g/m³) -->
ঘনত্ব (g/m³)

<!-- key: Elevation z (m) -->
উচ্চতা z (m)

<!-- key: MODPATH advection (slice) -->
MODPATH অভিবহন (ছেদ)

<!-- key: Analytical -->
বিশ্লেষণাত্মক

<!-- key: Analytical (active run) -->
বিশ্লেষণাত্মক (সক্রিয় রান)

<!-- key: Mass output unavailable -->
ভরের আউটপুট নেই

<!-- key: MT3D discrepancy (%) -->
MT3D বিচ্যুতি (%)

<!-- key: Initial + injected mass (first run) -->
প্রাথমিক + প্রবেশিত ভর (প্রথম রান)

<!-- key: Resident mass: grid sum and MT3D budget -->
অবশিষ্ট ভর: গ্রিড যোগফল ও MT3D ভারসাম্য

<!-- key: Reported mass-balance closure -->
প্রতিবেদিত ভর ভারসাম্যের সমাপতন

<!-- key: Example: pulse plume after 600 days -->
উদাহরণ: 600 দিন পরে পালস প্লুম

<!-- key: Example: observation P1 -->
উদাহরণ: পর্যবেক্ষণ P1

<!-- key: P1 · x (m) -->
P1 · x (m)

<!-- key: P1 · y (m) -->
P1 · y (m)

<!-- key: P1 · elevation z (m) -->
P1 · উচ্চতা z (m)

<!-- key: P2 · x (m) -->
P2 · x (m)

<!-- key: P2 · y (m) -->
P2 · y (m)

<!-- key: P2 · elevation z (m) -->
P2 · উচ্চতা z (m)

<!-- key: P3 · x (m) -->
P3 · x (m)

<!-- key: P3 · y (m) -->
P3 · y (m)

<!-- key: P3 · elevation z (m) -->
P3 · উচ্চতা z (m)

<!-- key: P4 · x (m) -->
P4 · x (m)

<!-- key: P4 · y (m) -->
P4 · y (m)

<!-- key: P4 · elevation z (m) -->
P4 · উচ্চতা z (m)

<!-- key: P5 · x (m) -->
P5 · x (m)

<!-- key: P5 · y (m) -->
P5 · y (m)

<!-- key: P5 · elevation z (m) -->
P5 · উচ্চতা z (m)

<!-- key: fig_head -->
নির্দিষ্ট হেড: {head:g} m

<!-- key: fig_layers -->
{layers} স্তর; উল্লম্ব স্কেল বর্ধিত

<!-- key: fig_total -->
মোট: {mass:g} g

<!-- key: fig_initial -->
t = 0-তে {mass:g} g

<!-- key: fig_xprofile -->
y = {y:.3g} m-এ x প্রোফাইল

<!-- key: fig_yprofile -->
x = {x:.3g} m-এ y প্রোফাইল

<!-- key: fig_section -->
{other} = {value:.3g} m-এ {axis}–z ছেদ

<!-- key: fig_title -->
{method} · t = {time:g} দিন · স্তর {layer} (z = {z:.3g} m)

<!-- key: fig_gridmass -->
{label}: গ্রিড যোগফল

<!-- key: fig_nativemass -->
{label}: MT3D ভারসাম্য

<!-- key: fig_nodata -->
{label}: ক্ষেত্রের বাইরে — তথ্য নেই

<!-- key: table_help_MB disc. (%) -->
MT3D-এর প্রতিবেদিত চূড়ান্ত ভর ভারসাম্য বিচ্যুতি।

<!-- key: table_help_Flow disc. (%) -->
MODFLOW-এর চূড়ান্ত জল ভারসাম্য বিচ্যুতি।

<!-- key: table_help_MT3D (s) -->
পরিবহন প্রোগ্রামের প্রকৃত চলার সময়।

<!-- key: table_help_MP7 (s) -->
MODPATH সময়; কণা কেবল অভিবহন দেখায়।

<!-- key: table_help_Ref. L1 (%) -->
রন্ধ্র-আয়তনে ভারযুক্ত পরম ঘনত্ব ত্রুটি, রেফারেন্স ভর দিয়ে ভাগ করা।

<!-- key: table_help_Mass (g) -->
ঘনত্ব গ্রিড থেকে সমাকলিত চূড়ান্ত দ্রবীভূত ভর।

<!-- key: MT3DMS final mass discrepancy exceeds 1%; inspect method and transport time step settings. -->
MT3DMS-এর চূড়ান্ত ভর বিচ্যুতি 1% ছাড়িয়েছে; পদ্ধতি ও পরিবহন সময়ধাপ দেখুন।

<!-- key: At least one MODFLOW water-budget discrepancy exceeds 0.1%. -->
অন্তত একটি MODFLOW জল ভারসাম্য বিচ্যুতি 0.1% ছাড়িয়েছে।

<!-- key: Negative concentrations occurred. They are retained in diagnostics and exports; central FD and particle methods can oscillate. -->
ঋণাত্মক ঘনত্ব পাওয়া গেছে; নির্ণয় ও রপ্তানিতে তা রাখা হয়। কেন্দ্রীয় FD ও কণা পদ্ধতিতে দোলন হতে পারে।

<!-- key: Source coordinates must lie inside the domain. -->
উৎসের স্থানাঙ্ক ক্ষেত্রের ভিতরে হতে হবে।

<!-- key: This confined lab requires heads at or above aquifer top. -->
এই আবদ্ধ জলাধারে হেড শীর্ষ উচ্চতার সমান বা বেশি হতে হবে।

<!-- key: Pulse duration must be between zero and model duration. -->
পালসের সময়কাল শূন্য ও মডেলের সময়কালের মধ্যে হতে হবে।

<!-- key: Observation point is outside the model. -->
পর্যবেক্ষণ বিন্দু মডেলের বাইরে।

<!-- key: TVD requires PERCEL no greater than 1. -->
TVD-এর জন্য PERCEL ≤ 1 দরকার।

<!-- key: language_fallback -->
অনুবাদ না থাকলে ইংরেজি পাঠ ব্যবহৃত হয়।

<!-- key: preset_random -->
দৈব পরামিতি

<!-- key: Random unit x (m) -->
দৈব একক x (m)

<!-- key: Random unit y (m) -->
দৈব একক y (m)

<!-- key: random_hint -->
ছোট এককে সূক্ষ্ম বিন্যাস, বড় এককে বড় খণ্ড হয়। গ্রিড সূক্ষ্ম করার সময় একই বাস্তব বিন্যাস রাখতে বীজ ও এককের মাপ স্থির রাখুন।

<!-- key: Active cells -->
সক্রিয় সেল

<!-- key: table_help_Active cells -->
সব অ-নিষ্ক্রিয় সেল, নির্দিষ্ট হেড সেলসহ।

<!-- key: Random field -->
দৈব ক্ষেত্র

<!-- key: Comparison runs -->
তুলনার রান

<!-- key: discard_tags_hint -->
× দিয়ে ট্যাগ সরিয়ে রান মুছুন। সব ট্যাগ সরালে নতুন তুলনা শুরু হবে। রাখতে চাইলে আগে রপ্তানি করুন।

<!-- key: Head contours -->
হেড সমমান রেখা

<!-- key: Computed head contours (m) -->
গণনাকৃত হেড সমমান রেখা (m)

<!-- key: Head contours appear after running the model -->
মডেল চালানোর পরে হেড রেখা দেখা যাবে

<!-- key: fig_background_k -->
পটভূমি K = {k:.2e} m/s

<!-- key: fig_low_lens_k -->
নিম্ন K লেন্স: K = {k:.2e} m/s

<!-- key: fig_high_channel_k -->
উচ্চ K চ্যানেল: K = {k:.2e} m/s

<!-- key: fig_low_barrier_k -->
নিম্ন K বাধা: K = {k:.2e} m/s

<!-- key: Focus on plume -->
প্লুমে ফোকাস

<!-- key: Focus threshold (% of peak) -->
সীমা (সর্বোচ্চের %)

<!-- key: focus_hint -->
প্রতিটি প্রদর্শিত প্লুমের বর্তমান ধনাত্মক সর্বোচ্চ দিয়ে সীমা নির্ধারিত হয়; প্রতি পাশে 20% ফাঁকা থাকে। দৃশ্যমান MODPATH পথ অন্তর্ভুক্ত থাকে। প্লুম ও পথ না থাকলে পুরো ক্ষেত্র দেখা যায়। শুধু উপরের দৃশ্য বদলায়।

<!-- key: Download plume figure (SVG) -->
প্লুম চিত্র ডাউনলোড (SVG)

<!-- key: steady -->
স্থির

<!-- key: transient -->
অস্থায়ী

<!-- key: fig_minimum -->
সাংখ্যিক সর্বনিম্ন: {minimum:.3g} g/m³

<!-- key: fig_minimum_log -->
সাংখ্যিক সর্বনিম্ন: {minimum:.3g} g/m³ (লগ-স্কেলে অ-ধনাত্মক মান লুকানো)

<!-- key: The plume reaches an x specified-head boundary; enlarge the domain before treating the infinite-x analytical solution as a benchmark. -->
প্লুম x-এর নির্দিষ্ট হেড সীমানায় পৌঁছেছে; অসীম-x রেফারেন্স ব্যবহারের আগে ক্ষেত্র বাড়ান।

<!-- key: fig_reference_boundary -->
বিশ্লেষণাত্মক নির্ভুলতা বন্ধ: x-সীমানার প্রভাব {tolerance_percent:.2g}% সীমা ছাড়িয়েছে।

<!-- key: Low K lens -->
নিম্ন K লেন্স

<!-- key: High K channel -->
উচ্চ K চ্যানেল

<!-- key: Low K barrier -->
আংশিক নিম্ন K বাধা

<!-- key: Page width -->
পাতার প্রস্থ

<!-- key: width_1 -->
সরু

<!-- key: width_2 -->
সংকুচিত

<!-- key: width_3 -->
মানক

<!-- key: width_4 -->
বড়

<!-- key: width_5 -->
পুরো প্রস্থ

<!-- key: page_width_hint -->
সরু থেকে পুরো প্রস্থ পর্যন্ত পাঁচটি বিকল্প। মানকে আগের প্রস্থ থাকে। ছোট পর্দায় উপলব্ধ জায়গা অনুযায়ী মানিয়ে নেয়।

<!-- key: Show model grid -->
মডেল গ্রিড দেখান

<!-- key: grid_hint -->
প্রদর্শিত রানের সেল সীমানা হালকা রেখায় দেখা যায়। এক স্তরের ঘনত্ব প্রোফাইলে সেলের প্রান্তে উল্লম্ব রেখা থাকে।

<!-- key: Plume-centered x/y -->
প্লুম-কেন্দ্রিক x/y

<!-- key: relative_hint -->
শূন্য হলো প্রদর্শিত স্তরের ধনাত্মক দ্রবীভূত ভরের কেন্দ্র। সব তুলনার চিত্র একই মূলবিন্দু ব্যবহার করে। ইনপুট স্থানাঙ্ক ও উচ্চতা পরম থাকে।

<!-- key: relative_mass_origin -->
আপেক্ষিক মূলবিন্দু: x = {x:.2f} m; y = {y:.2f} m (প্লুমের ভরকেন্দ্র)।

<!-- key: relative_source_origin -->
এই স্তরে ধনাত্মক প্লুম ভর নেই: গ্রিডে উৎসের কেন্দ্রই মূলবিন্দু, x = {x:.2f} m; y = {y:.2f} m।

<!-- key: fig_relative_xprofile -->
y′ = {y:.3g} m-এ x প্রোফাইল

<!-- key: fig_relative_yprofile -->
x′ = {x:.3g} m-এ y প্রোফাইল

<!-- key: fig_relative_section -->
{other}′ = {value:.3g} m-এ {axis}–z ছেদ
