<!-- key: title -->
MT3D – 2D/3D परिवहन प्रयोगशाला

<!-- key: intro_caption -->
परिचयात्मक चित्र: प्लूम और ब्रेकथ्रू वक्र का उदाहरण। यह वर्तमान मॉडल इनपुट से स्वतंत्र है।

<!-- key: Model & run -->
1 · मॉडल और गणना

<!-- key: Results & method comparison -->
2 · परिणाम और विधियों की तुलना

<!-- key: series_reset -->
इनपुट संकेत या मॉडल/स्रोत की ज्यामिति बदलने से नई तुलना शृंखला शुरू हुई है। पिछली गणनाएँ हटा दी गई हैं।

<!-- key: grid_summary -->
ग्रिड: {nx} × {ny} × {nz} सेल। वास्तविक सेल चौड़ाई: Δx = {dx:.3f} m; Δy = {dy:.3f} m; Δz = {dz:.3f} m।

<!-- key: velocity_summary -->
समांगी संदर्भ रंध्र वेग: {velocity:.4f} m/दिन।

<!-- key: source_bounds -->
x = {x0:.2f}–{x1:.2f} m; y = {y0:.2f}–{y1:.2f} m; z = {z0:.2f}–{z1:.2f} m.

<!-- key: source_snap_hint -->
स्रोत चुने हुए सेल में है। विभेदन बदलने से उसका वास्तविक आकार बदल सकता है। सेल चौड़ाई के इनपुट में कुल मॉडल विस्तार बना रहता है और वास्तविक समान अंतराल दिखता है।

<!-- key: input_error -->
गणना से पहले चिह्नित मॉडल सेटिंग सुधारें।

<!-- key: missing_executables -->
आवश्यक प्रोग्राम नहीं मिले: {names}। संगत निष्पादन फ़ाइलें ऐप या रिपॉज़िटरी के `bin/` में रखें। स्थानीय स्थापना: `python setup_executables.py`।

<!-- key: label_placeholder -->
स्वतः: 01 TVD / Pulse (विषमांगी: / het.)

<!-- key: history_full -->
दस गणनाएँ संग्रहीत हैं। आगे बढ़ने के लिए कोई गणना हटाएँ या शृंखला खाली करें।

<!-- key: running -->
MODFLOW, MT3D और वैकल्पिक MODPATH चल रहे हैं…

<!-- key: run_success -->
गणना पूर्ण हुई। नवीनतम परिणाम दिख रहा है।

<!-- key: run_failed -->
यह गणना पूरी नहीं हुई और तुलना में नहीं जोड़ी गई।

<!-- key: changed_source_footprint -->
ग्रिड परिष्करण से स्रोत का वास्तविक विस्तार बदला है। विस्तृत तालिका में स्रोत का आकार जाँचें।

<!-- key: nearest_time -->
{name}: निकटतम सहेजा समय {time:.3f} दिन (प्रदर्शित गणना: {target:.3f} दिन)।

<!-- key: no_comparison_time -->
{name}: {time:.3f} दिन पर आउटपुट नहीं; छोड़ा गया।

<!-- key: evaluating_reference -->
विश्लेषणात्मक संदर्भ की गणना…

<!-- key: export_hint -->
संग्रह में मॉडल इनपुट, लॉग, सांद्रता/हेड एरे, द्रव्यमान निदान और कण डेटा हैं। कणों के आगमन का विवरण भी निर्यात में है।

<!-- key: no_runs -->
प्लूम, प्रोफ़ाइल, ब्रेकथ्रू वक्र और विधियों की तुलना देखने के लिए प्रारंभिक पल्स प्रयोग चलाएँ।

<!-- key: footer -->
MT3D 2D/3D · v{version} · प्रत्यक्ष शिक्षण के लिए कार्यशील संस्करण · विकसित किया: Thomas Reimann · TU Dresden · The Groundwater Project

<!-- key: transient_hint -->
प्रारंभिक प्रवाह संतुलित होता है; दायाँ हेड t = 0 पर बदलता है।

<!-- key: expert_flow_hint -->
प्रवाह सॉल्वर की सहनशीलता और पुनरावृत्तियाँ बदलने के लिए विशेषज्ञ सेटिंग चालू करें।

<!-- key: stochastic_hint -->
नियत बीज से क्षेत्र पुनरुत्पाद्य हैं। K और Ss लघुगणकीय पैमाने पर समान वितरण से, सरंध्रता समान वितरण से ली जाती है। परिष्करण में यही प्रतिरूप रहता है।

<!-- key: zones_hint -->
आयत सेल केंद्र चुनते हैं; बाद की पंक्तियाँ पहले वाली को बदलती हैं। परत क्रम 1 से है।

<!-- key: observation_hint -->
प्रेक्षण वक्र उस सेल का मान लेते हैं जिसमें बिंदु है। संग्रहीत मॉडल दोबारा चलाए बिना स्थान बदल सकते हैं।

<!-- key: output_hint -->
t = 0 और अंतिम समय शामिल हैं। चित्रों और निर्यात के लिए सांद्रता आउटपुट नियंत्रित करता है।

<!-- key: preset_homogeneous -->
समांगी

<!-- key: preset_lens -->
कम K का लेंस

<!-- key: preset_channel -->
उच्च K की वाहिका

<!-- key: preset_barrier -->
कम K का आंशिक अवरोध

<!-- key: preset_stochastic -->
यादृच्छिक क्षेत्रीकरण

<!-- key: preset_custom -->
स्वनिर्धारित आयत

<!-- key: preset_hint_lens -->
केंद्रीय लेंस: K = 0.01 × पृष्ठभूमि K; पूरी गहराई।

<!-- key: preset_hint_channel -->
अनुदैर्ध्य वाहिका: K = 10 × पृष्ठभूमि K; पूरी गहराई।

<!-- key: preset_hint_barrier -->
आंशिक अनुप्रस्थ अवरोध: K = 0.01 × पृष्ठभूमि K; किनारे से मार्ग खुला है।

<!-- key: signal_pulse -->
पल्स / आयताकार इनपुट

<!-- key: signal_continuous -->
सतत इनपुट

<!-- key: signal_dirac -->
डिराक / तात्कालिक विमोचन

<!-- key: signal_short_pulse -->
पल्स

<!-- key: signal_short_continuous -->
सतत

<!-- key: signal_short_dirac -->
डिराक

<!-- key: Concept, assumptions and equations -->
संकल्पना, मान्यताएँ और समीकरण

<!-- key: Guided experiments -->
निर्देशित प्रयोग

<!-- key: Expert settings -->
विशेषज्ञ सेटिंग

<!-- key: Use sliders for main parameters -->
मुख्य मानों के लिए स्लाइडर

<!-- key: Flow & domain -->
प्रवाह और क्षेत्र

<!-- key: Transport & source -->
परिवहन और स्रोत

<!-- key: Post-processing & observations -->
पश्च-प्रसंस्करण और प्रेक्षण

<!-- key: Hydraulic properties -->
जलीय गुण

<!-- key: Hydraulic conductivity K (m/s) -->
जलीय चालकता K (m/s)

<!-- key: Effective porosity (-) -->
प्रभावी सरंध्रता (-)

<!-- key: Specific storage Ss (1/m) -->
विशिष्ट भंडारण Ss (1/m)

<!-- key: Vertical / horizontal K -->
ऊर्ध्वाधर / क्षैतिज K

<!-- key: Boundary conditions -->
सीमा शर्तें

<!-- key: Specified head left (m) -->
निर्दिष्ट बायाँ हेड (m)

<!-- key: Specified head right (m) -->
निर्दिष्ट दायाँ हेड (m)

<!-- key: Transient flow experiment -->
अस्थायी प्रवाह प्रयोग

<!-- key: Right head after t = 0 (m) -->
t = 0 के बाद दायाँ हेड (m)

<!-- key: Model extent and spatial discretization -->
मॉडल विस्तार और स्थानिक विविक्तीकरण

<!-- key: Model length in x-direction (m) -->
x दिशा में लंबाई (m)

<!-- key: Model width in y-direction (m) -->
y दिशा में चौड़ाई (m)

<!-- key: Aquifer thickness / top elevation (m) -->
जलभृत मोटाई / शीर्ष ऊँचाई (m)

<!-- key: Define the grid by -->
ग्रिड निर्धारण

<!-- key: Number of cells -->
सेल संख्या

<!-- key: Cell width -->
सेल चौड़ाई

<!-- key: Cells x -->
x सेल

<!-- key: Cells y -->
y सेल

<!-- key: Cell width x (m) -->
x सेल चौड़ाई (m)

<!-- key: Cell width y (m) -->
y सेल चौड़ाई (m)

<!-- key: Number of layers -->
परतों की संख्या

<!-- key: Numerical solution for flow -->
प्रवाह का संख्यात्मक समाधान

<!-- key: Head tolerance (m) -->
हेड सहनशीलता (m)

<!-- key: Flow residual tolerance (m³/day) -->
प्रवाह अवशेष सहनशीलता (m³/दिन)

<!-- key: PCG outer iterations -->
PCG बाहरी पुनरावृत्तियाँ

<!-- key: PCG inner iterations -->
PCG आंतरिक पुनरावृत्तियाँ

<!-- key: Flow time steps (approximately total) -->
प्रवाह समय चरण (लगभग कुल)

<!-- key: Hydrogeology and zonation -->
जलभूविज्ञान और विषमता

<!-- key: Hydrogeology preset -->
जलभूवैज्ञानिक पूर्वनिर्धारण

<!-- key: Number of zones -->
क्षेत्रों की संख्या

<!-- key: Random seed -->
यादृच्छिक बीज

<!-- key: K range (m/s) -->
K सीमा (m/s)

<!-- key: Ss range (1/m) -->
Ss सीमा (1/m)

<!-- key: Porosity range (-) -->
सरंध्रता सीमा (-)

<!-- key: Minimum -->
न्यूनतम

<!-- key: Maximum -->
अधिकतम

<!-- key: Edit hydrogeological zones -->
क्षेत्र संपादित करें

<!-- key: Zone name -->
क्षेत्र नाम

<!-- key: First layer -->
पहली परत

<!-- key: Last layer -->
अंतिम परत

<!-- key: Porosity -->
सरंध्रता

<!-- key: Boundary conditions and source -->
सीमा शर्तें और स्रोत

<!-- key: Input signal -->
इनपुट संकेत

<!-- key: Released mass (g) -->
विमोचित द्रव्यमान (g)

<!-- key: Mass input rate (g/day) -->
द्रव्यमान इनपुट दर (g/दिन)

<!-- key: Pulse duration (days) -->
पल्स अवधि (दिन)

<!-- key: Source x (m) -->
स्रोत x (m)

<!-- key: Source y (m) -->
स्रोत y (m)

<!-- key: Source cells x -->
स्रोत सेल x

<!-- key: Source cells y -->
स्रोत सेल y

<!-- key: Source spans all layers -->
स्रोत सभी परतों में

<!-- key: Source layer (1 = top) -->
स्रोत परत (1 = शीर्ष)

<!-- key: Transport parameters -->
परिवहन पैरामीटर

<!-- key: Dispersion -->
परिक्षेपण

<!-- key: Longitudinal dispersivity (m) -->
अनुदैर्ध्य परिक्षेपण लंबाई (m)

<!-- key: Horizontal transverse / longitudinal -->
क्षैतिज अनुप्रस्थ / अनुदैर्ध्य

<!-- key: Vertical transverse / longitudinal -->
ऊर्ध्वाधर अनुप्रस्थ / अनुदैर्ध्य

<!-- key: Temporal discretization -->
कालिक विविक्तीकरण

<!-- key: Transport duration (days) -->
परिवहन अवधि (दिन)

<!-- key: DT0 · initial step (days; 0 = automatic) -->
DT0 · प्रारंभिक चरण (दिन; 0 = स्वतः)

<!-- key: TTSMAX · maximum step (days; 0 = automatic) -->
TTSMAX · अधिकतम चरण (दिन; 0 = स्वतः)

<!-- key: TTSMULT · step multiplier -->
TTSMULT · चरण गुणक

<!-- key: MXSTRN · maximum transport steps -->
MXSTRN · अधिकतम परिवहन चरण

<!-- key: Numerical solution for transport -->
परिवहन का संख्यात्मक समाधान

<!-- key: MT3D advection method -->
MT3D अभिवहन विधि

<!-- key: MODPATH particle comparison -->
MODPATH कण तुलना

<!-- key: PERCEL · Courant number -->
PERCEL · कूरांत संख्या

<!-- key: CCLOSE · concentration tolerance -->
CCLOSE · सांद्रता सहनशीलता

<!-- key: Timeout per executable (seconds) -->
प्रति प्रोग्राम समय सीमा (सेकंड)

<!-- key: Expert transport solver settings -->
विशेषज्ञ परिवहन सॉल्वर सेटिंग

<!-- key: MXPART · maximum particles -->
MXPART · अधिकतम कण

<!-- key: ITRACK · tracking algorithm -->
ITRACK · ट्रैकिंग एल्गोरिदम

<!-- key: WD · concentration weighting -->
WD · सांद्रता भार

<!-- key: DCEPS · gradient threshold -->
DCEPS · प्रवणता सीमा

<!-- key: NPLANE · particle planes -->
NPLANE · कण तल

<!-- key: NPL · low-gradient particles -->
NPL · कम प्रवणता कण

<!-- key: NPH · high-gradient particles -->
NPH · उच्च प्रवणता कण

<!-- key: NPMIN · minimum particles/cell -->
NPMIN · न्यूनतम कण/सेल

<!-- key: NPMAX · maximum particles/cell -->
NPMAX · अधिकतम कण/सेल

<!-- key: INTERP · interpolation -->
INTERP · अंतर्वेशन

<!-- key: NLSINK · sink planes -->
NLSINK · निकास तल

<!-- key: NPSINK · sink particles -->
NPSINK · निकास कण

<!-- key: DCHMOC · HMOC threshold -->
DCHMOC · HMOC सीमा

<!-- key: MXITER · GCG outer iterations -->
MXITER · GCG बाहरी पुनरावृत्तियाँ

<!-- key: ITER1 · GCG inner iterations -->
ITER1 · GCG आंतरिक पुनरावृत्तियाँ

<!-- key: ISOLVE · preconditioner -->
ISOLVE · पूर्व-अनुकूलक

<!-- key: NCRS · cross-dispersion -->
NCRS · क्रॉस-परिक्षेपण

<!-- key: ACCL · relaxation -->
ACCL · शिथिलीकरण

<!-- key: IPRGCG · print interval -->
IPRGCG · मुद्रण अंतराल

<!-- key: MODPATH release settings -->
MODPATH कण विमोचन सेटिंग

<!-- key: Particles per source cell -->
प्रति स्रोत सेल कण

<!-- key: Release batches (pulse / continuous) -->
विमोचन समूह (पल्स / सतत)

<!-- key: Observation points -->
प्रेक्षण बिंदु

<!-- key: Number of observation points -->
प्रेक्षण बिंदुओं की संख्या

<!-- key: Output settings -->
आउटपुट सेटिंग

<!-- key: Saved transport times -->
सहेजे परिवहन समय

<!-- key: Actual source footprint -->
वास्तविक स्रोत विस्तार

<!-- key: Optional run label -->
वैकल्पिक गणना नाम

<!-- key: Run model -->
मॉडल चलाएँ

<!-- key: Run diagnostic -->
गणना निदान

<!-- key: More comparison metrics -->
अधिक तुलना मापदंड

<!-- key: Displayed run -->
प्रदर्शित गणना

<!-- key: Run to remove -->
हटाने की गणना

<!-- key: Remove -->
हटाएँ

<!-- key: Clear comparison runs -->
तुलना गणनाएँ साफ़ करें

<!-- key: Plume & sections -->
प्लूम और काट

<!-- key: Observation curves -->
प्रेक्षण वक्र

<!-- key: Mass & diagnostics -->
द्रव्यमान और निदान

<!-- key: Export -->
निर्यात

<!-- key: Time (days) -->
समय (दिन)

<!-- key: Top-view layer -->
ऊपरी दृश्य परत

<!-- key: Layer {number} -->
परत {number}

<!-- key: Analytical reference -->
विश्लेषणात्मक संदर्भ

<!-- key: Plot settings and section positions -->
चित्र सेटिंग और काट स्थान

<!-- key: x-direction section · y (m) -->
x दिशा काट · y (m)

<!-- key: y-direction section · x (m) -->
y दिशा काट · x (m)

<!-- key: Colour fill -->
रंग भराव

<!-- key: Contour lines -->
सममान रेखाएँ

<!-- key: Log colours -->
लघुगणकीय रंग

<!-- key: Particle paths -->
कण पथ

<!-- key: Opacity -->
अपारदर्शिता

<!-- key: Compare runs in x / y sections -->
x / y काट में गणनाओं की तुलना

<!-- key: Compare section profiles -->
काट प्रोफ़ाइल तुलना

<!-- key: Runs for section comparison -->
काट तुलना के लिए गणनाएँ

<!-- key: Also overlay top-view contours -->
ऊपरी सममान रेखाएँ भी दिखाएँ

<!-- key: Download plume figure (PNG) -->
प्लूम चित्र डाउनलोड (PNG)

<!-- key: Runs in breakthrough comparison -->
ब्रेकथ्रू तुलना में गणनाएँ

<!-- key: Observation cells used by each run -->
प्रत्येक गणना के प्रेक्षण सेल

<!-- key: Download breakthrough curves (CSV) -->
ब्रेकथ्रू वक्र डाउनलोड (CSV)

<!-- key: Detailed mass-budget data -->
विस्तृत द्रव्यमान संतुलन डेटा

<!-- key: Stored run configuration -->
संग्रहीत गणना विन्यास

<!-- key: Download comparison table (CSV) -->
तुलना तालिका डाउनलोड (CSV)

<!-- key: Download run configuration (JSON) -->
गणना विन्यास डाउनलोड (JSON)

<!-- key: Prepare complete displayed-run archive -->
प्रदर्शित गणना का पूरा संग्रह बनाएँ

<!-- key: Preparing archive… -->
संग्रह बन रहा है…

<!-- key: Download run archive (ZIP) -->
गणना संग्रह डाउनलोड (ZIP)

<!-- key: Run -->
गणना

<!-- key: Method -->
विधि

<!-- key: Signal -->
संकेत

<!-- key: Grid -->
ग्रिड

<!-- key: K zones -->
K क्षेत्र

<!-- key: Flow -->
प्रवाह

<!-- key: MB disc. (%) -->
द्रव्यमान त्रुटि (%)

<!-- key: Flow disc. (%) -->
प्रवाह त्रुटि (%)

<!-- key: MT3D (s) -->
MT3D (s)

<!-- key: MP7 (s) -->
MP7 (s)

<!-- key: Flow (s) -->
प्रवाह (s)

<!-- key: Total (s) -->
कुल (s)

<!-- key: Ref. L1 (%) -->
संदर्भ L1 (%)

<!-- key: Mass (g) -->
द्रव्यमान (g)

<!-- key: Input (g) -->
इनपुट (g)

<!-- key: Min. C (g/m³) -->
न्यूनतम C (g/m³)

<!-- key: Neg. mass (g) -->
ऋणात्मक द्रव्यमान (g)

<!-- key: Centroid x (m) -->
केंद्रक x (m)

<!-- key: Steps -->
चरण

<!-- key: Source box (m) -->
स्रोत विस्तार (m)

<!-- key: End (d) -->
अंत (दिन)

<!-- key: Scenario -->
परिदृश्य

<!-- key: Point -->
बिंदु

<!-- key: Requested x -->
निर्दिष्ट x

<!-- key: Requested y -->
निर्दिष्ट y

<!-- key: Requested z -->
निर्दिष्ट z

<!-- key: Cell centre x -->
सेल केंद्र x

<!-- key: Cell centre y -->
सेल केंद्र y

<!-- key: Cell centre z -->
सेल केंद्र z

<!-- key: Layer -->
परत

<!-- key: Row -->
पंक्ति

<!-- key: Column -->
स्तंभ

<!-- key: Cumulative in (g) -->
संचयी इनपुट (g)

<!-- key: Cumulative out (g) -->
संचयी निकास (g)

<!-- key: Sources (g) -->
स्रोत (g)

<!-- key: Sinks (g) -->
निकास (g)

<!-- key: Fluid storage (g) -->
द्रव भंडारण (g)

<!-- key: Native resident mass (g) -->
प्रोग्राम का अवशिष्ट द्रव्यमान (g)

<!-- key: Alternative disc. (%) -->
वैकल्पिक त्रुटि (%)

<!-- key: Analytical reference requires homogeneous steady flow. -->
विश्लेषणात्मक संदर्भ के लिए समांगी स्थिर प्रवाह आवश्यक है।

<!-- key: Source cells -->
स्रोत सेल

<!-- key: Specified head -->
निर्दिष्ट हेड

<!-- key: Section locations -->
काट स्थान

<!-- key: Background flow -->
पृष्ठभूमि प्रवाह

<!-- key: Model preview: grid, boundaries and source -->
पूर्वावलोकन: ग्रिड, सीमाएँ और स्रोत

<!-- key: Computed head contours -->
गणित हेड सममान रेखाएँ

<!-- key: Homogeneous steady head contours -->
समांगी स्थिर हेड सममान रेखाएँ

<!-- key: Time (d) -->
समय (दिन)

<!-- key: Mass rate (g/d) -->
द्रव्यमान दर (g/दिन)

<!-- key: Instantaneous mass (g) -->
तात्कालिक द्रव्यमान (g)

<!-- key: Dirac input (initial cell mass) -->
डिराक इनपुट (प्रारंभिक सेल द्रव्यमान)

<!-- key: Finite pulse input -->
सीमित पल्स इनपुट

<!-- key: Continuous input -->
सतत इनपुट

<!-- key: Concentration (g/m³) -->
सांद्रता (g/m³)

<!-- key: Elevation z (m) -->
ऊँचाई z (m)

<!-- key: MODPATH advection (slice) -->
MODPATH अभिवहन (काट)

<!-- key: Analytical -->
विश्लेषणात्मक

<!-- key: Analytical (active run) -->
विश्लेषणात्मक (सक्रिय गणना)

<!-- key: Mass output unavailable -->
द्रव्यमान आउटपुट उपलब्ध नहीं

<!-- key: MT3D discrepancy (%) -->
MT3D त्रुटि (%)

<!-- key: Initial + injected mass (first run) -->
प्रारंभिक + दिया द्रव्यमान (पहली गणना)

<!-- key: Resident mass: grid sum and MT3D budget -->
अवशिष्ट द्रव्यमान: ग्रिड योग और MT3D संतुलन

<!-- key: Reported mass-balance closure -->
रिपोर्ट किया द्रव्यमान संतुलन

<!-- key: Example: pulse plume after 600 days -->
उदाहरण: 600 दिन बाद पल्स प्लूम

<!-- key: Example: observation P1 -->
उदाहरण: प्रेक्षण P1

<!-- key: P1 · x (m) -->
P1 · x (m)

<!-- key: P1 · y (m) -->
P1 · y (m)

<!-- key: P1 · elevation z (m) -->
P1 · ऊँचाई z (m)

<!-- key: P2 · x (m) -->
P2 · x (m)

<!-- key: P2 · y (m) -->
P2 · y (m)

<!-- key: P2 · elevation z (m) -->
P2 · ऊँचाई z (m)

<!-- key: P3 · x (m) -->
P3 · x (m)

<!-- key: P3 · y (m) -->
P3 · y (m)

<!-- key: P3 · elevation z (m) -->
P3 · ऊँचाई z (m)

<!-- key: P4 · x (m) -->
P4 · x (m)

<!-- key: P4 · y (m) -->
P4 · y (m)

<!-- key: P4 · elevation z (m) -->
P4 · ऊँचाई z (m)

<!-- key: P5 · x (m) -->
P5 · x (m)

<!-- key: P5 · y (m) -->
P5 · y (m)

<!-- key: P5 · elevation z (m) -->
P5 · ऊँचाई z (m)

<!-- key: fig_head -->
निर्दिष्ट हेड: {head:g} m

<!-- key: fig_layers -->
{layers} परतें; ऊर्ध्वाधर पैमाना बढ़ाया गया

<!-- key: fig_total -->
कुल: {mass:g} g

<!-- key: fig_initial -->
t = 0 पर {mass:g} g

<!-- key: fig_xprofile -->
y = {y:.3g} m पर x प्रोफ़ाइल

<!-- key: fig_yprofile -->
x = {x:.3g} m पर y प्रोफ़ाइल

<!-- key: fig_section -->
{other} = {value:.3g} m पर {axis}–z काट

<!-- key: fig_title -->
{method} · t = {time:g} दिन · परत {layer} (z = {z:.3g} m)

<!-- key: fig_gridmass -->
{label}: ग्रिड योग

<!-- key: fig_nativemass -->
{label}: MT3D संतुलन

<!-- key: fig_nodata -->
{label}: क्षेत्र से बाहर — डेटा नहीं

<!-- key: table_help_MB disc. (%) -->
MT3D द्वारा रिपोर्ट किया अंतिम द्रव्यमान संतुलन अंतर।

<!-- key: table_help_Flow disc. (%) -->
MODFLOW का अंतिम जल संतुलन अंतर।

<!-- key: table_help_MT3D (s) -->
परिवहन प्रोग्राम का वास्तविक निष्पादन समय।

<!-- key: table_help_MP7 (s) -->
MODPATH समय; कण केवल अभिवहन दर्शाते हैं।

<!-- key: table_help_Ref. L1 (%) -->
रंध्र आयतन से भारित निरपेक्ष सांद्रता त्रुटि, संदर्भ द्रव्यमान से विभाजित।

<!-- key: table_help_Mass (g) -->
सांद्रता ग्रिड से समाकलित अंतिम घुलित द्रव्यमान।

<!-- key: MT3DMS final mass discrepancy exceeds 1%; inspect method and transport time step settings. -->
MT3DMS की अंतिम द्रव्यमान त्रुटि 1% से अधिक है; विधि और परिवहन समय चरण जाँचें।

<!-- key: At least one MODFLOW water-budget discrepancy exceeds 0.1%. -->
MODFLOW का कम से कम एक जल संतुलन अंतर 0.1% से अधिक है।

<!-- key: Negative concentrations occurred. They are retained in diagnostics and exports; central FD and particle methods can oscillate. -->
ऋणात्मक सांद्रताएँ मिलीं। ये निदान और निर्यात में बनी रहती हैं; केंद्रीय FD और कण विधियों में दोलन हो सकता है।

<!-- key: Source coordinates must lie inside the domain. -->
स्रोत निर्देशांक क्षेत्र के अंदर होने चाहिए।

<!-- key: This confined lab requires heads at or above aquifer top. -->
इस परिबद्ध जलभृत में हेड शीर्ष ऊँचाई से कम नहीं हो सकते।

<!-- key: Pulse duration must be between zero and model duration. -->
पल्स अवधि शून्य और मॉडल अवधि के बीच होनी चाहिए।

<!-- key: Observation point is outside the model. -->
प्रेक्षण बिंदु मॉडल से बाहर है।

<!-- key: TVD requires PERCEL no greater than 1. -->
TVD के लिए PERCEL ≤ 1 चाहिए।

<!-- key: language_fallback -->
अनुवाद न होने पर अंग्रेज़ी पाठ प्रयोग होता है।

<!-- key: preset_random -->
यादृच्छिक पैरामीटर

<!-- key: Random unit x (m) -->
यादृच्छिक इकाई x (m)

<!-- key: Random unit y (m) -->
यादृच्छिक इकाई y (m)

<!-- key: random_hint -->
छोटी इकाइयाँ महीन, बड़ी इकाइयाँ बड़े पैच बनाती हैं। ग्रिड परिष्करण में भौतिक प्रतिरूप बनाए रखने के लिए बीज और इकाई आकार स्थिर रखें।

<!-- key: Active cells -->
सक्रिय सेल

<!-- key: table_help_Active cells -->
सभी गैर-निष्क्रिय सेल, निर्दिष्ट हेड वाले सेल सहित।

<!-- key: Random field -->
यादृच्छिक क्षेत्र

<!-- key: Comparison runs -->
तुलना गणनाएँ

<!-- key: discard_tags_hint -->
× से टैग हटाकर गणना मिटाएँ। सभी टैग हटाने से नई तुलना शुरू होगी। रखने वाली गणनाएँ पहले निर्यात करें।

<!-- key: Head contours -->
हेड सममान रेखाएँ

<!-- key: Computed head contours (m) -->
गणित हेड सममान रेखाएँ (m)

<!-- key: Head contours appear after running the model -->
मॉडल चलने के बाद हेड रेखाएँ दिखेंगी

<!-- key: fig_background_k -->
पृष्ठभूमि K = {k:.2e} m/s

<!-- key: fig_low_lens_k -->
कम K लेंस: K = {k:.2e} m/s

<!-- key: fig_high_channel_k -->
उच्च K वाहिका: K = {k:.2e} m/s

<!-- key: fig_low_barrier_k -->
कम K अवरोध: K = {k:.2e} m/s

<!-- key: Focus on plume -->
प्लूम पर केंद्रित करें

<!-- key: Focus threshold (% of peak) -->
सीमा (शिखर का %)

<!-- key: focus_hint -->
हर प्रदर्शित प्लूम के वर्तमान धनात्मक शिखर से सीमा तय होती है; हर ओर 20% अंतर है। दिखते MODPATH पथ शामिल रहते हैं। प्लूम या पथ न होने पर पूरा क्षेत्र दिखता है। केवल ऊपरी दृश्य बदलता है।

<!-- key: Download plume figure (SVG) -->
प्लूम चित्र डाउनलोड (SVG)

<!-- key: steady -->
स्थिर

<!-- key: transient -->
अस्थायी

<!-- key: fig_minimum -->
संख्यात्मक न्यूनतम: {minimum:.3g} g/m³

<!-- key: fig_minimum_log -->
संख्यात्मक न्यूनतम: {minimum:.3g} g/m³ (लॉग पैमाने पर गैर-धनात्मक मान छिपे हैं)

<!-- key: The plume reaches an x specified-head boundary; enlarge the domain before treating the infinite-x analytical solution as a benchmark. -->
प्लूम x के निर्दिष्ट हेड सीमा तक पहुँच गया; अनंत-x संदर्भ प्रयोग करने से पहले क्षेत्र बढ़ाएँ।

<!-- key: fig_reference_boundary -->
विश्लेषणात्मक शुद्धता बंद: x-सीमा प्रभाव {tolerance_percent:.2g}% सीमा से अधिक है।

<!-- key: Low K lens -->
कम K का लेंस

<!-- key: High K channel -->
उच्च K की वाहिका

<!-- key: Low K barrier -->
कम K का आंशिक अवरोध

<!-- key: Page width -->
पृष्ठ चौड़ाई

<!-- key: width_1 -->
संकीर्ण

<!-- key: width_2 -->
सघन

<!-- key: width_3 -->
मानक

<!-- key: width_4 -->
बड़ा

<!-- key: width_5 -->
पूरी चौड़ाई

<!-- key: page_width_hint -->
संकीर्ण से पूरी चौड़ाई तक पाँच विकल्प। मानक में पिछली चौड़ाई रहती है। छोटे पर्दे पर उपलब्ध जगह के अनुसार आकार बदलता है।

<!-- key: Show model grid -->
मॉडल ग्रिड दिखाएँ

<!-- key: grid_hint -->
प्रदर्शित गणना की हल्की सेल सीमाएँ। एक-परत सांद्रता प्रोफ़ाइल में सेल किनारों पर ऊर्ध्वाधर रेखाएँ दिखती हैं।

<!-- key: Plume-centered x/y -->
प्लूम-केंद्रित x/y

<!-- key: relative_hint -->
शून्य प्रदर्शित परत के धनात्मक घुलित द्रव्यमान का केंद्र है। सभी तुलना चित्र यही मूल बिंदु लेते हैं। इनपुट निर्देशांक और ऊँचाई निरपेक्ष रहते हैं।

<!-- key: relative_mass_origin -->
सापेक्ष मूल: x = {x:.2f} m; y = {y:.2f} m (प्लूम का द्रव्यमान केंद्र)।

<!-- key: relative_source_origin -->
इस परत में धनात्मक प्लूम द्रव्यमान नहीं है: ग्रिड में स्रोत का केंद्र मूल है, x = {x:.2f} m; y = {y:.2f} m।

<!-- key: fig_relative_xprofile -->
y′ = {y:.3g} m पर x प्रोफ़ाइल

<!-- key: fig_relative_yprofile -->
x′ = {x:.3g} m पर y प्रोफ़ाइल

<!-- key: fig_relative_section -->
{other}′ = {value:.3g} m पर {axis}–z काट

<!-- key: MODPATH particle count -->
MODPATH कण संख्या

<!-- key: particle_count_cell -->
प्रति स्रोत सेल

<!-- key: particle_count_total -->
प्रति विमोचन पूरे स्रोत में

<!-- key: Particles in the whole source per release -->
प्रति विमोचन पूरे स्रोत में कण

<!-- key: particle_count_summary -->
{cells} स्रोत सेलों में {count} कण × {groups} विमोचन = {total} कण।

<!-- key: expert_transport_hint -->
परिवहन सॉल्वर के सभी नियंत्रण दिखाए गए हैं। NPL / NPH और NPMIN / NPMAX, MOC / HMOC कण नियंत्रित करते हैं; MXPART कुल सीमा है। सहायता चिह्न लागू विधियाँ बताते हैं। MODPATH के कण अलग हैं।

<!-- key: Plume animation -->
प्लूम ऐनिमेशन

<!-- key: Animation view -->
ऐनिमेशन दृश्य

<!-- key: animation_2d -->
शीर्ष दृश्य और अनुभाग

<!-- key: animation_3d -->
सेल केंद्रों पर 3D सांद्रता

<!-- key: Animation frames -->
ऐनिमेशन फ़्रेम

<!-- key: Playback speed (frames/s) -->
गति (फ़्रेम/सेकंड)

<!-- key: Vertical exaggeration -->
ऊर्ध्वाधर अतिशयोक्ति

<!-- key: Generate / refresh animation -->
ऐनिमेशन बनाएँ / अपडेट करें

<!-- key: Generating animation… -->
ऐनिमेशन बनाया जा रहा है…

<!-- key: Download animation (HTML) -->
ऐनिमेशन डाउनलोड करें (HTML)

<!-- key: Play -->
चलाएँ

<!-- key: Pause -->
रोकें

<!-- key: Animation frame -->
ऐनिमेशन फ़्रेम

<!-- key: animation_layers_hint -->
3D दृश्य के लिए विशेषज्ञ सेटिंग में परतें जोड़ें।

<!-- key: animation_hint -->
दिखाए गए रन के सहेजे गए समयों का उपयोग होता है। नीचे एनिमेशन के रंग और ज़ूम स्वतंत्र रूप से चुनें; रंग पैमाना समय के साथ स्थिर रहता है। अन्य 2D चित्र सेटिंग बनी रहती हैं। तुलनाएँ और विश्लेषणात्मक संदर्भ स्थिर चित्रों में रहते हैं। तैयार प्लेयर सेटिंग के नीचे दिखाई देता है; डाउनलोड किया गया HTML ऑफ़लाइन चलता है।

<!-- key: animation_3d_hint -->
3D में स्थिर कैमरे से सीमा से ऊपर की सेल-केंद्र सांद्रता दिखती है। अधिकतम {maximum} समान रूप से चुने सेल दिखते हैं; गणना और निर्यात में सभी सेल रहते हैं। कण अभिवहन तुलना हैं। ऊर्ध्वाधर विस्तार केवल दृश्य बदलता है।

<!-- key: animation_refresh_hint -->
सेटिंग बदली है। प्लेयर अपडेट करने के लिए फिर बनाएँ।

<!-- key: animation_failed -->
ऐनिमेशन नहीं बन सका। मॉडल परिणाम सुरक्षित हैं।

<!-- key: animation_size_limit -->
ऐनिमेशन 45 MiB से बड़ा है। कम फ़्रेम चुनें।

<!-- key: help_s_percel -->
प्रति चरण अधिकतम अभिवहन दूरी, सेल चौड़ाई में। TVD के लिए ≤ 1।

<!-- key: help_s_mxpart -->
MOC/HMOC: कुल गतिशील कण क्षमता, प्रति सेल संख्या नहीं।

<!-- key: help_s_itrack -->
MOC/MMOC/HMOC: 1 = Euler, 2 = चौथे क्रम का Runge–Kutta, 3 = संकर ट्रैकिंग।

<!-- key: help_s_wd -->
विशेषता विधियाँ: ऑपरेटर विभाजन में सांद्रता भार; 0.5–1।

<!-- key: help_s_dceps -->
MOC/HMOC: NPL और NPH के लिए सापेक्ष सांद्रता ढाल की सीमा।

<!-- key: help_s_nplane -->
MOC/HMOC: 0 = यादृच्छिक; धनात्मक = प्रति सेल क्षैतिज कण तल।

<!-- key: help_s_npl -->
MOC/HMOC: ढाल ≤ DCEPS वाले सेल में प्रारंभिक कण; शून्य मान्य।

<!-- key: help_s_nph -->
MOC/HMOC: उच्च ढाल सेल में प्रारंभिक कण। निश्चित पैटर्न संख्या पूर्णांकित कर सकते हैं।

<!-- key: help_s_npmin -->
MOC/HMOC: सेल संख्या इस न्यूनतम से कम होने पर कण जोड़ें।

<!-- key: help_s_npmax -->
MOC/HMOC: सीमा पार होने पर सेल में NPH कणों का नया समूह बनता है।

<!-- key: help_s_interp -->
MMOC/HMOC: सांद्रता अंतर्वेशन; केवल 1 (रैखिक) समर्थित।

<!-- key: help_s_nlsink -->
MMOC/HMOC सिंक सेल: 0 = यादृच्छिक; धनात्मक = कण तल।

<!-- key: help_s_npsink -->
MMOC/HMOC: प्रत्येक सिंक सेल दर्शाने वाले कण।

<!-- key: help_s_dchmoc -->
HMOC: इस सापेक्ष ढाल सीमा के ऊपर MOC, नीचे MMOC।

<!-- key: help_s_mxiter -->
GCG बाहरी पुनरावृत्ति सीमा। इस रैखिक संरक्षी परिवहन मॉडल के लिए एक पर्याप्त है।

<!-- key: help_s_iter1 -->
परिवहन समीकरणों के लिए GCG आंतरिक पुनरावृत्ति सीमा।

<!-- key: help_s_isolve -->
GCG प्रीकंडीशनर: 1 = Jacobi, 2 = SSOR, 3 = संशोधित अपूर्ण Cholesky (MIC)।

<!-- key: help_s_ncrs -->
प्रकीर्णन क्रॉस पद: 0 = दाएँ पक्ष का सन्निकटन; 1 = मैट्रिक्स में पूर्ण टेंसर।

<!-- key: help_s_accl -->
शिथिलीकरण गुणक, केवल SSOR (ISOLVE = 2) के लिए।

<!-- key: help_s_cclose -->
GCG अभिसरण के लिए सापेक्ष सांद्रता परिवर्तन सहनशीलता। छोटा मान अधिक कठोर है।

<!-- key: help_s_iprgcg -->
हर N GCG पुनरावृत्ति पर परिवर्तन छापें; 0 पर प्रत्येक तनाव अवधि के अंत में।

<!-- key: help_s_dt0 -->
प्रारंभिक परिवहन चरण, दिन में; 0 पर MT3D स्वतः चुनेगा।

<!-- key: help_s_ttsmult -->
अंतर्निहित FD के क्रमिक चरण गुणक; TVD और विशेषता विधियाँ इसे नहीं लेतीं।

<!-- key: help_s_ttsmax -->
TTSMULT > 1 पर अधिकतम चरण, दिन में; 0 पर स्वतः सीमा।

<!-- key: help_s_mxstrn -->
प्रति प्रवाह चरण अधिकतम परिवहन चरण; सीमा पर रन रुक सकता है।

<!-- key: help_s_timeout -->
प्रत्येक निष्पादन की समय सीमा। अधिक कणों के लिए अधिक समय लग सकता है।

<!-- key: help_s_hclose -->
PCG हेड परिवर्तन अभिसरण सहनशीलता, मीटर में।

<!-- key: help_s_rclose -->
PCG प्रवाह अवशेष सहनशीलता, m³/दिन में।

<!-- key: help_s_flow_mxiter -->
MODFLOW PCG प्रवाह सॉल्वर की अधिकतम बाहरी पुनरावृत्तियाँ।

<!-- key: help_s_flow_iter1 -->
प्रति बाहरी प्रवाह पुनरावृत्ति अधिकतम आंतरिक PCG पुनरावृत्तियाँ।

<!-- key: help_particle_count_mode -->
प्रति स्रोत सेल या प्रत्येक विमोचन पर पूरे स्रोत की सटीक कुल संख्या चुनें।

<!-- key: help_particles_per_cell -->
हर विमोचन पर प्रत्येक स्रोत सेल में समान वितरण। केवल MODPATH, MOC नहीं।

<!-- key: help_total_source_particles -->
प्रति विमोचन सटीक कुल संख्या; हर स्रोत सेल में कम से कम एक। सेल संख्याओं में अधिकतम एक का अंतर; द्रव्यमान भार छिद्र आयतन अनुसार।

<!-- key: help_release_groups -->
समान समयांतर के मध्य में विमोचन पल्स/सतत इनपुट का सन्निकटन है। अधिक समूह समय सुधारते हैं; Dirac में t = 0 पर एक विमोचन।

<!-- key: help_run_label -->
सुझाया नाम लेने के लिए खाली छोड़ें। अपना नाम विधि/संकेत पाठ बदलेगा; क्रमांक और विषम प्रत्यय स्वतः रहेंगे।

<!-- key: help_expert -->
परत नियंत्रण और सभी समर्थित सॉल्वर पैरामीटर दिखाएँ। छिपाने पर मान सुरक्षित रहते हैं।

<!-- key: help_sliders -->
मॉडल मान बदले बिना संख्या फ़ील्ड और स्लाइडर बदलें।

<!-- key: help_extent -->
भौतिक क्षेत्र विस्तार, मीटर में। इसे बदलने पर नई तुलना श्रृंखला शुरू होती है।

<!-- key: help_thickness -->
दाबयुक्त जलभृत की मोटाई; तल 0 m, शीर्ष इस मान पर। परतें समान मोटाई की हैं।

<!-- key: help_grid_mode -->
सेल संख्या या अधिकतम चौड़ाई दें। चौड़ाई मोड में संख्या ऊपर पूर्णांकित होती है, क्षेत्र स्थिर रहता है।

<!-- key: help_grid_count -->
इस दिशा में समान सेल संख्या। परिष्करण से पुराने तुलना रन सुरक्षित रहते हैं।

<!-- key: help_cell_width -->
वांछित अधिकतम सेल चौड़ाई, मीटर में। पूर्वावलोकन वास्तविक समान चौड़ाई बताता है।

<!-- key: help_nlay -->
एक परत शीर्ष-दृश्य मॉडल है; कई समान परतें ऊर्ध्वाधर परिवहन और 3D दृश्य देती हैं।

<!-- key: help_k -->
पृष्ठभूमि क्षैतिज हाइड्रोलिक चालकता। m/s में दें; मॉडल m/दिन में बदलता है।

<!-- key: help_porosity -->
गतिशील छिद्र आयतन अंश; छिद्र-जल वेग और विलेय भंडारण नियंत्रित करता है।

<!-- key: help_ss -->
प्रति आयतन प्रति इकाई हेड गिरावट जल विमोचन (1/m)। यहाँ स्थिर प्रवाह में भंडारण पद सक्रिय नहीं।

<!-- key: help_kv_ratio -->
ऊर्ध्वाधर/क्षैतिज चालकता अनुपात, हर परत में लागू।

<!-- key: help_zones_preset -->
समरूप गुण, दोहराने योग्य यादृच्छिक क्षेत्र या लेंस/चैनल/बाधा चुनें।

<!-- key: help_zone_seed -->
यादृच्छिक बीज। समान बीज और सेटिंग से वही भौतिक पैटर्न बनता है।

<!-- key: help_random_unit -->
इस दिशा में यादृच्छिक खंडों का भौतिक आकार, संख्यात्मक ग्रिड से स्वतंत्र।

<!-- key: help_random_k -->
यादृच्छिक चालकता सीमाएँ, लॉग स्थान में समान नमूना (m/s)।

<!-- key: help_random_ss -->
लॉग-समान विशिष्ट भंडारण सीमा (1/m)। मॉडल में सुरक्षित, स्थिर प्रवाह में निष्क्रिय।

<!-- key: help_random_por -->
समान नमूने वाली प्रभावी सरंध्रता सीमा; शून्य और एक के बीच।

<!-- key: help_head -->
बाहरी कॉलम पर निर्धारित हेड। बायाँ दाएँ से अधिक; दोनों जलभृत शीर्ष पर या ऊपर।

<!-- key: help_duration -->
कुल अनुकरणित परिवहन समय, दिन में; ऐनिमेशन गति से स्वतंत्र।

<!-- key: help_dispersion -->
छिद्र-जल वेग के अनुपात में यांत्रिक फैलाव जोड़ें। बंद करने पर अभिवहन और संख्यात्मक फैलाव रहते हैं।

<!-- key: help_al -->
प्रवाह दिशा की अनुदैर्ध्य प्रकीर्णन लंबाई, मीटर; गुणांक = αL × वेग।

<!-- key: help_trpt -->
क्षैतिज अनुप्रस्थ/अनुदैर्ध्य प्रकीर्णन अनुपात: αTH/αL।

<!-- key: help_trpv -->
ऊर्ध्वाधर अनुप्रस्थ/अनुदैर्ध्य अनुपात: αTV/αL। कई परतों में प्रासंगिक।

<!-- key: help_source_kind -->
Dirac: t = 0 पर प्रारंभिक घुला द्रव्यमान। पल्स: पल्स अंत तक स्थिर इनपुट। सतत: पूरे रन में स्थिर इनपुट।

<!-- key: help_source_mass -->
स्रोत छिद्र आयतन में प्रारंभिक कुल घुला द्रव्यमान (ग्राम)।

<!-- key: help_mass_rate -->
कुल विलेय इनपुट (g/दिन), स्रोत छिद्र आयतन अनुसार वितरित। पानी का इंजेक्शन नहीं।

<!-- key: help_pulse_duration -->
इस समय (दिन) बाद इनपुट रुकता है; कुल परिवहन समय से कम होना चाहिए।

<!-- key: help_source_position -->
निरपेक्ष स्रोत-केंद्र निर्देशांक, मीटर; मॉडल सेल पर समायोजित। निर्धारित हेड कॉलम से दूर रखें।

<!-- key: help_source_cells -->
इस दिशा में स्रोत सेल संख्या। वास्तविक क्षेत्र पूर्वावलोकन में देखें; ज्यामिति बदलने पर नई श्रृंखला।

<!-- key: help_source_all_layers -->
स्रोत सभी परतों में फैलाएँ; अन्यथा केवल चुनी परत में।

<!-- key: help_src_layer -->
स्रोत वाली परत; 1 सबसे ऊपरी परत है।

<!-- key: help_method -->
MT3D अभिवहन चुनें: FD up/central, TVD, अग्र MOC, पश्च MMOC या संकर HMOC। MODPATH अलग है।

<!-- key: help_track_particles -->
गणित प्रवाह क्षेत्र में MODPATH 7 चलाएँ। केवल अभिवहन; MODPATH प्रकीर्णन या सांद्रता नहीं गणता।

<!-- key: help_observation -->
निरपेक्ष प्रेक्षण निर्देशांक, मीटर। सांद्रता उसी सेल से ली जाती है, अंतर्वेशन नहीं।

<!-- key: help_nobs -->
सहेजे रन से एक से पाँच प्रेक्षण बिंदुओं पर सांद्रता तुलना।

<!-- key: help_outputs -->
सहेजे परिवहन समय, t = 0 सहित; पल्स अंत भी सुरक्षित। अधिक आउटपुट ऐनिमेशन/वक्र सुधारते हैं, सॉल्वर चरण सटीकता नहीं।

<!-- key: help_length -->
भौतिक क्षेत्र विस्तार, मीटर में। इसे बदलने पर नई तुलना श्रृंखला शुरू होती है।

<!-- key: help_width -->
भौतिक क्षेत्र विस्तार, मीटर में। इसे बदलने पर नई तुलना श्रृंखला शुरू होती है।

<!-- key: help_ncol -->
इस दिशा में समान सेल संख्या। परिष्करण से पुराने तुलना रन सुरक्षित रहते हैं।

<!-- key: help_nrow -->
इस दिशा में समान सेल संख्या। परिष्करण से पुराने तुलना रन सुरक्षित रहते हैं।

<!-- key: help_cell_x -->
वांछित अधिकतम सेल चौड़ाई, मीटर में। पूर्वावलोकन वास्तविक समान चौड़ाई बताता है।

<!-- key: help_cell_y -->
वांछित अधिकतम सेल चौड़ाई, मीटर में। पूर्वावलोकन वास्तविक समान चौड़ाई बताता है।

<!-- key: help_random_unit_x -->
इस दिशा में यादृच्छिक खंडों का भौतिक आकार, संख्यात्मक ग्रिड से स्वतंत्र।

<!-- key: help_random_unit_y -->
इस दिशा में यादृच्छिक खंडों का भौतिक आकार, संख्यात्मक ग्रिड से स्वतंत्र।

<!-- key: help_zone_k_min -->
यादृच्छिक चालकता सीमाएँ, लॉग स्थान में समान नमूना (m/s)।

<!-- key: help_zone_k_max -->
यादृच्छिक चालकता सीमाएँ, लॉग स्थान में समान नमूना (m/s)।

<!-- key: help_zone_ss_min -->
लॉग-समान विशिष्ट भंडारण सीमा (1/m)। मॉडल में सुरक्षित, स्थिर प्रवाह में निष्क्रिय।

<!-- key: help_zone_ss_max -->
लॉग-समान विशिष्ट भंडारण सीमा (1/m)। मॉडल में सुरक्षित, स्थिर प्रवाह में निष्क्रिय।

<!-- key: help_zone_por_min -->
समान नमूने वाली प्रभावी सरंध्रता सीमा; शून्य और एक के बीच।

<!-- key: help_zone_por_max -->
समान नमूने वाली प्रभावी सरंध्रता सीमा; शून्य और एक के बीच।

<!-- key: help_head_left -->
बाहरी कॉलम पर निर्धारित हेड। बायाँ दाएँ से अधिक; दोनों जलभृत शीर्ष पर या ऊपर।

<!-- key: help_head_right -->
बाहरी कॉलम पर निर्धारित हेड। बायाँ दाएँ से अधिक; दोनों जलभृत शीर्ष पर या ऊपर।

<!-- key: help_src_x -->
निरपेक्ष स्रोत-केंद्र निर्देशांक, मीटर; मॉडल सेल पर समायोजित। निर्धारित हेड कॉलम से दूर रखें।

<!-- key: help_src_y -->
निरपेक्ष स्रोत-केंद्र निर्देशांक, मीटर; मॉडल सेल पर समायोजित। निर्धारित हेड कॉलम से दूर रखें।

<!-- key: help_src_ncol -->
इस दिशा में स्रोत सेल संख्या। वास्तविक क्षेत्र पूर्वावलोकन में देखें; ज्यामिति बदलने पर नई श्रृंखला।

<!-- key: help_src_nrow -->
इस दिशा में स्रोत सेल संख्या। वास्तविक क्षेत्र पूर्वावलोकन में देखें; ज्यामिति बदलने पर नई श्रृंखला।

<!-- key: help_animation_mode -->
2D शीर्ष दृश्य और अनुभाग दिखाता है। 3D स्थिर दृश्य से सेल-केंद्र सांद्रता दिखाता है; कई परतें आवश्यक।

<!-- key: help_animation_frames -->
पहले और अंतिम सहित अधिकतम 80 सहेजे फ़्रेम। समय के बीच सांद्रता अंतर्वेशन नहीं।

<!-- key: help_animation_fps -->
वास्तविक सेकंड में फ़्रेम। हर फ़्रेम वास्तविक अनुकरण समय दिखाता है; मॉडल नहीं बदलता।

<!-- key: help_animation_exaggeration -->
3D क्षेत्र की दृश्य ऊँचाई बढ़ाएँ। ऊँचाई निर्देशांक और गणना अपरिवर्तित।

<!-- key: help_generate_animation -->
माँग पर सहेजे परिणाम दिखाएँ। सेटिंग बदलने पर फिर बनाएँ; मॉडल दोबारा नहीं चलता।

<!-- key: help_view_time -->
सहेजा परिवहन समय चुनें; मॉडल फिर नहीं चलेगा।

<!-- key: help_view_layer -->
शीर्ष दृश्य की परत; 1 सबसे ऊपर।

<!-- key: help_section -->
निरपेक्ष अनुभाग स्थिति, मीटर; संबंधित पंक्ति/कॉलम से। सापेक्ष अक्ष अनुभाग नहीं खिसकाते।

<!-- key: help_fill -->
सांद्रता रंग पैमाने से सेल भरें; शून्य सफेद।

<!-- key: help_lines -->
रंग भराव पर समान सांद्रता रेखाएँ दिखाएँ।

<!-- key: help_show_heads -->
गणित हेड की पतली समरेखाएँ, मीटर लेबल सहित।

<!-- key: help_log -->
धनात्मक सांद्रता के लॉग रंग। अधनात्मक सेल केवल दृश्य में छिपते हैं।

<!-- key: help_particle_paths -->
चुने समय तक MODPATH स्थिति और पतले पथ। अधिकतम 120 पथ दिखते हैं; निर्यात में सभी कण।

<!-- key: help_opacity -->
रंग अपारदर्शिता: 1 अपारदर्शी; छोटा मान नीचे के तत्व दिखाता है।

<!-- key: help_focus_plume -->
धनात्मक प्लूम और MODPATH पथों पर किनारा जोड़कर ज़ूम। ऐनिमेशन सभी समयों का एक स्थिर क्षेत्र दिखाता है।

<!-- key: help_focus_threshold -->
स्थिर फोकस: प्लूम शिखर का प्रतिशत। 3D ऐनिमेशन: सेल दिखाने हेतु स्थिर रंग पैमाने के अधिकतम परिमाण का प्रतिशत।

<!-- key: help_analytical -->
समरूप स्थिर प्रवाह के विश्लेषणात्मक संदर्भ से तुलना। विषम या अस्थायी प्रवाह मान्यताओं से बाहर।

<!-- key: help_compare -->
दिखाए रन के अनुभागों पर निकटतम सहेजे समयों में तुलना करें।

<!-- key: help_analytic_on -->
समरूप स्थिर प्रवाह के विश्लेषणात्मक संदर्भ से तुलना। विषम या अस्थायी प्रवाह मान्यताओं से बाहर।

<!-- key: help_btc_analytical -->
समरूप स्थिर प्रवाह के विश्लेषणात्मक संदर्भ से तुलना। विषम या अस्थायी प्रवाह मान्यताओं से बाहर।

<!-- key: help_compare_sections -->
दिखाए रन के अनुभागों पर निकटतम सहेजे समयों में तुलना करें।

<!-- key: help_overlay_runs -->
दिखाए रन के अनुभागों पर निकटतम सहेजे समयों में तुलना करें।

<!-- key: help_compare_top -->
दिखाए रन के अनुभागों पर निकटतम सहेजे समयों में तुलना करें।

<!-- key: help_btc_runs -->
सहेजे रन से एक से पाँच प्रेक्षण बिंदुओं पर सांद्रता तुलना।

<!-- key: Animation settings -->
एनिमेशन सेटिंग

<!-- key: Animation colour scale -->
एनिमेशन रंग पैमाना

<!-- key: animation_colour_enhanced -->
कम सांद्रताओं को उभारें (स्थिर पैमाना)

<!-- key: animation_colour_linear -->
रैखिक (स्थिर पैमाना)

<!-- key: animation_colour_log -->
लघुगणकीय (स्थिर पैमाना)

<!-- key: help_animation_colour -->
उन्नत रंग छोटी सांद्रताओं को दिखाने के लिए घात रूपांतरण (घातांक 0.35) का उपयोग करते हैं। सभी फ़्रेम में वास्तविक सांद्रता की सीमाएँ समान रहती हैं; शून्य सफेद रहता है। रैखिक और उन्नत पैमाने ऋणात्मक संख्यात्मक मान दिखाते हैं; लघुगणकीय पैमाना गैर-धनात्मक मान छिपाता है। गणना के डेटा नहीं बदलते।

<!-- key: Zoom animation to plume -->
एनिमेशन को प्लूम पर ज़ूम करें

<!-- key: help_animation_focus -->
एक स्थिर दृश्य-सीमा सभी चुने गए समयों की धनात्मक सांद्रता वाली प्लूम और दिखाई गई MODPATH पथरेखाओं को 20% अतिरिक्त किनारे के साथ समेटती है। स्थिर चित्र के ज़ूम से स्वतंत्र। पूरा क्षेत्र देखने के लिए बंद करें। 2D और 3D में उपलब्ध।

<!-- key: Plume threshold (% of peak) -->
प्लूम सीमा (अधिकतम का %)

<!-- key: help_animation_threshold -->
ज़ूम प्रत्येक फ़्रेम की अधिकतम धनात्मक सांद्रता के इस प्रतिशत से ऊपर के मानों को शामिल करता है। 3D में यह स्थिर पैमाने की अधिकतम निरपेक्ष सांद्रता के प्रतिशत के रूप में कोशिकाओं के प्रदर्शन की सीमा भी तय करता है। प्रारंभिक मान 0.1%। केवल दृश्य बदलता है।

<!-- key: animation_progress -->
एनिमेशन बन रहा है… {percent}%

<!-- key: MODPATH settings -->
MODPATH सेटिंग

<!-- key: expert_transport_location_hint -->
MT3D के विशेषज्ञ पैरामीटर ठीक नीचे अलग **विशेषज्ञ परिवहन सॉल्वर सेटिंग** विस्तार योग्य पैनल में हैं। उसके बाद MODPATH सेटिंग आती हैं।
