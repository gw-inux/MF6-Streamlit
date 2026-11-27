<!-- key: title -->
MT3D – Laboratoire de transport 2D/3D

<!-- key: intro_caption -->
Illustration introductive : exemple de panache et de courbe de restitution, indépendant des paramètres actuels du modèle.

<!-- key: Model & run -->
1 · Modèle et calcul

<!-- key: Results & method comparison -->
2 · Résultats et comparaison des méthodes

<!-- key: series_reset -->
Le signal ou la géométrie du domaine/de la source a changé : une nouvelle série commence. Les calculs précédents ont été effacés.

<!-- key: grid_summary -->
Maillage : {nx} × {ny} × {nz} cellules. Pas réel : Δx = {dx:.3f} m ; Δy = {dy:.3f} m ; Δz = {dz:.3f} m.

<!-- key: velocity_summary -->
Vitesse interstitielle de référence homogène : {velocity:.4f} m/j.

<!-- key: source_bounds -->
x = {x0:.2f}–{x1:.2f} m; y = {y0:.2f}–{y1:.2f} m; z = {z0:.2f}–{z1:.2f} m.

<!-- key: source_snap_hint -->
La source occupe les cellules sélectionnées. La résolution peut modifier ses dimensions effectives. La saisie du pas conserve l'étendue totale et indique le pas uniforme réel.

<!-- key: input_error -->
Corrigez les paramètres signalés avant le calcul.

<!-- key: missing_executables -->
Programmes manquants : {names}. Fournissez les exécutables compatibles dans `bin/` de l'application ou du dépôt. En local : `python setup_executables.py`.

<!-- key: label_placeholder -->
Automatique : 01 TVD / Pulse (hétérogène : / het.)

<!-- key: history_full -->
Dix calculs sont conservés. Supprimez un calcul ou videz la série pour continuer.

<!-- key: running -->
Calcul MODFLOW, MT3D et éventuellement MODPATH…

<!-- key: run_success -->
Calcul terminé. Le dernier résultat est affiché.

<!-- key: run_failed -->
Ce calcul n'a pas abouti et n'a pas été ajouté à la comparaison.

<!-- key: changed_source_footprint -->
Le raffinement a modifié l'emprise réelle de la source. Vérifiez ses dimensions dans le tableau détaillé.

<!-- key: nearest_time -->
{name} : temps enregistré le plus proche {time:.3f} j (calcul affiché : {target:.3f} j).

<!-- key: no_comparison_time -->
{name} : aucune sortie à {time:.3f} j ; omis.

<!-- key: evaluating_reference -->
Évaluation de la référence analytique…

<!-- key: export_hint -->
L'archive contient entrées, journaux, concentrations, charges, bilans et particules, y compris leurs arrivées.

<!-- key: no_runs -->
Lancez l'expérience de base avec un créneau pour voir panache, profils, courbes et comparaison des méthodes.

<!-- key: footer -->
MT3D 2D/3D · v{version} · Version de travail pour l'enseignement en direct · Développé par Thomas Reimann · TU Dresden · The Groundwater Project

<!-- key: transient_hint -->
Le champ initial s'équilibre ; la charge à droite change à t = 0.

<!-- key: expert_flow_hint -->
Activez le mode expert pour modifier tolérances et itérations du solveur d'écoulement.

<!-- key: stochastic_hint -->
Graine fixe : zones reproductibles. K et Ss sont uniformes en espace logarithmique ; la porosité est uniforme. Le raffinement conserve la réalisation.

<!-- key: zones_hint -->
Les rectangles sélectionnent les centres de cellules ; les dernières lignes remplacent les précédentes. Les couches commencent à 1.

<!-- key: observation_hint -->
Les observations utilisent la cellule contenant le point. Déplacez les points sans recalculer les modèles conservés.

<!-- key: output_hint -->
Inclut t = 0 et le temps final. Contrôle les sorties de concentration pour figures et export.

<!-- key: preset_homogeneous -->
Homogène

<!-- key: preset_lens -->
Lentille à faible K

<!-- key: preset_channel -->
Chenal à K élevée

<!-- key: preset_barrier -->
Barrière partielle à faible K

<!-- key: preset_stochastic -->
Zonation stochastique

<!-- key: preset_custom -->
Rectangles personnalisés

<!-- key: preset_hint_lens -->
Lentille centrale : K = 0,01 × K de fond ; toute la profondeur.

<!-- key: preset_hint_channel -->
Chenal longitudinal : K = 10 × K de fond ; toute la profondeur.

<!-- key: preset_hint_barrier -->
Barrière transversale partielle : K = 0,01 × K de fond ; contournement possible.

<!-- key: signal_pulse -->
Impulsion / créneau

<!-- key: signal_continuous -->
Apport continu

<!-- key: signal_dirac -->
Dirac / apport instantané

<!-- key: signal_short_pulse -->
Créneau

<!-- key: signal_short_continuous -->
Continu

<!-- key: signal_short_dirac -->
Dirac

<!-- key: Concept, assumptions and equations -->
Concept, hypothèses et équations

<!-- key: Guided experiments -->
Expériences guidées

<!-- key: Expert settings -->
Paramètres experts

<!-- key: Use sliders for main parameters -->
Curseurs pour les paramètres principaux

<!-- key: Flow & domain -->
Écoulement et domaine

<!-- key: Transport & source -->
Transport et source

<!-- key: Post-processing & observations -->
Post-traitement et observations

<!-- key: Hydraulic properties -->
Propriétés hydrauliques

<!-- key: Hydraulic conductivity K (m/s) -->
Conductivité hydraulique K (m/s)

<!-- key: Effective porosity (-) -->
Porosité efficace (-)

<!-- key: Specific storage Ss (1/m) -->
Emmagasinement spécifique Ss (1/m)

<!-- key: Vertical / horizontal K -->
K vertical / horizontal

<!-- key: Boundary conditions -->
Conditions aux limites

<!-- key: Specified head left (m) -->
Charge imposée à gauche (m)

<!-- key: Specified head right (m) -->
Charge imposée à droite (m)

<!-- key: Transient flow experiment -->
Écoulement transitoire

<!-- key: Right head after t = 0 (m) -->
Charge droite après t = 0 (m)

<!-- key: Model extent and spatial discretization -->
Étendue et discrétisation spatiale

<!-- key: Model length in x-direction (m) -->
Longueur selon x (m)

<!-- key: Model width in y-direction (m) -->
Largeur selon y (m)

<!-- key: Aquifer thickness / top elevation (m) -->
Épaisseur / cote du toit (m)

<!-- key: Define the grid by -->
Définir le maillage par

<!-- key: Number of cells -->
Nombre de cellules

<!-- key: Cell width -->
Largeur des cellules

<!-- key: Cells x -->
Cellules x

<!-- key: Cells y -->
Cellules y

<!-- key: Cell width x (m) -->
Pas x (m)

<!-- key: Cell width y (m) -->
Pas y (m)

<!-- key: Number of layers -->
Nombre de couches

<!-- key: Numerical solution for flow -->
Résolution numérique de l'écoulement

<!-- key: Head tolerance (m) -->
Tolérance de charge (m)

<!-- key: Flow residual tolerance (m³/day) -->
Tolérance du résidu (m³/j)

<!-- key: PCG outer iterations -->
Itérations externes PCG

<!-- key: PCG inner iterations -->
Itérations internes PCG

<!-- key: Flow time steps (approximately total) -->
Pas d'écoulement (total approximatif)

<!-- key: Hydrogeology and zonation -->
Hydrogéologie et hétérogénéité

<!-- key: Hydrogeology preset -->
Préréglage hydrogéologique

<!-- key: Number of zones -->
Nombre de zones

<!-- key: Random seed -->
Graine aléatoire

<!-- key: K range (m/s) -->
Plage K (m/s)

<!-- key: Ss range (1/m) -->
Plage Ss (1/m)

<!-- key: Porosity range (-) -->
Plage de porosité (-)

<!-- key: Minimum -->
Minimum

<!-- key: Maximum -->
Maximum

<!-- key: Edit hydrogeological zones -->
Modifier les zones

<!-- key: Zone name -->
Nom de zone

<!-- key: First layer -->
Première couche

<!-- key: Last layer -->
Dernière couche

<!-- key: Porosity -->
Porosité

<!-- key: Boundary conditions and source -->
Conditions aux limites et source

<!-- key: Input signal -->
Signal d'entrée

<!-- key: Released mass (g) -->
Masse libérée (g)

<!-- key: Mass input rate (g/day) -->
Débit massique (g/j)

<!-- key: Pulse duration (days) -->
Durée du créneau (j)

<!-- key: Source x (m) -->
Source x (m)

<!-- key: Source y (m) -->
Source y (m)

<!-- key: Source cells x -->
Cellules source x

<!-- key: Source cells y -->
Cellules source y

<!-- key: Source spans all layers -->
Source sur toutes les couches

<!-- key: Source layer (1 = top) -->
Couche source (1 = toit)

<!-- key: Transport parameters -->
Paramètres de transport

<!-- key: Dispersion -->
Dispersion

<!-- key: Longitudinal dispersivity (m) -->
Dispersivité longitudinale (m)

<!-- key: Horizontal transverse / longitudinal -->
Transversale horizontale / longitudinale

<!-- key: Vertical transverse / longitudinal -->
Transversale verticale / longitudinale

<!-- key: Temporal discretization -->
Discrétisation temporelle

<!-- key: Transport duration (days) -->
Durée du transport (j)

<!-- key: DT0 · initial step (days; 0 = automatic) -->
DT0 · pas initial (j ; 0 = auto)

<!-- key: TTSMAX · maximum step (days; 0 = automatic) -->
TTSMAX · pas maximal (j ; 0 = auto)

<!-- key: TTSMULT · step multiplier -->
TTSMULT · multiplicateur du pas

<!-- key: MXSTRN · maximum transport steps -->
MXSTRN · pas de transport maximaux

<!-- key: Numerical solution for transport -->
Résolution numérique du transport

<!-- key: MT3D advection method -->
Méthode d'advection MT3D

<!-- key: MODPATH particle comparison -->
Comparaison particulaire MODPATH

<!-- key: PERCEL · Courant number -->
PERCEL · nombre de Courant

<!-- key: CCLOSE · concentration tolerance -->
CCLOSE · tolérance de concentration

<!-- key: Timeout per executable (seconds) -->
Durée limite par programme (s)

<!-- key: Expert transport solver settings -->
Paramètres experts du solveur de transport

<!-- key: MXPART · maximum particles -->
MXPART · particules maximales

<!-- key: ITRACK · tracking algorithm -->
ITRACK · algorithme de suivi

<!-- key: WD · concentration weighting -->
WD · pondération de concentration

<!-- key: DCEPS · gradient threshold -->
DCEPS · seuil de gradient

<!-- key: NPLANE · particle planes -->
NPLANE · plans de particules

<!-- key: NPL · low-gradient particles -->
NPL · particules à faible gradient

<!-- key: NPH · high-gradient particles -->
NPH · particules à fort gradient

<!-- key: NPMIN · minimum particles/cell -->
NPMIN · particules min./cellule

<!-- key: NPMAX · maximum particles/cell -->
NPMAX · particules max./cellule

<!-- key: INTERP · interpolation -->
INTERP · interpolation

<!-- key: NLSINK · sink planes -->
NLSINK · plans de puits

<!-- key: NPSINK · sink particles -->
NPSINK · particules de puits

<!-- key: DCHMOC · HMOC threshold -->
DCHMOC · seuil HMOC

<!-- key: MXITER · GCG outer iterations -->
MXITER · itérations externes GCG

<!-- key: ITER1 · GCG inner iterations -->
ITER1 · itérations internes GCG

<!-- key: ISOLVE · preconditioner -->
ISOLVE · préconditionneur

<!-- key: NCRS · cross-dispersion -->
NCRS · dispersion croisée

<!-- key: ACCL · relaxation -->
ACCL · relaxation

<!-- key: IPRGCG · print interval -->
IPRGCG · intervalle d'impression

<!-- key: MODPATH release settings -->
Libération des particules MODPATH

<!-- key: Particles per source cell -->
Particules par cellule source

<!-- key: Release batches (pulse / continuous) -->
Lots de libération (créneau / continu)

<!-- key: Observation points -->
Points d'observation

<!-- key: Number of observation points -->
Nombre de points d'observation

<!-- key: Output settings -->
Paramètres de sortie

<!-- key: Saved transport times -->
Temps de transport enregistrés

<!-- key: Actual source footprint -->
Emprise réelle de la source

<!-- key: Optional run label -->
Nom facultatif du calcul

<!-- key: Run model -->
Lancer le modèle

<!-- key: Run diagnostic -->
Diagnostic du calcul

<!-- key: More comparison metrics -->
Autres indicateurs de comparaison

<!-- key: Displayed run -->
Calcul affiché

<!-- key: Run to remove -->
Calcul à supprimer

<!-- key: Remove -->
Supprimer

<!-- key: Clear comparison runs -->
Vider les calculs comparés

<!-- key: Plume & sections -->
Panache et coupes

<!-- key: Observation curves -->
Courbes d'observation

<!-- key: Mass & diagnostics -->
Masse et diagnostics

<!-- key: Export -->
Exporter

<!-- key: Time (days) -->
Temps (jours)

<!-- key: Top-view layer -->
Couche en vue de dessus

<!-- key: Layer {number} -->
Couche {number}

<!-- key: Analytical reference -->
Référence analytique

<!-- key: Plot settings and section positions -->
Affichage et positions des coupes

<!-- key: x-direction section · y (m) -->
Coupe selon x · y (m)

<!-- key: y-direction section · x (m) -->
Coupe selon y · x (m)

<!-- key: Colour fill -->
Remplissage coloré

<!-- key: Contour lines -->
Isoconcentrations

<!-- key: Log colours -->
Couleurs logarithmiques

<!-- key: Particle paths -->
Trajectoires particulaires

<!-- key: Opacity -->
Opacité

<!-- key: Compare runs in x / y sections -->
Comparer les calculs en coupes x / y

<!-- key: Compare section profiles -->
Comparer les profils

<!-- key: Runs for section comparison -->
Calculs à comparer en coupe

<!-- key: Also overlay top-view contours -->
Superposer aussi les contours en plan

<!-- key: Download plume figure (PNG) -->
Télécharger le panache (PNG)

<!-- key: Runs in breakthrough comparison -->
Calculs comparés en restitution

<!-- key: Observation cells used by each run -->
Cellules d'observation par calcul

<!-- key: Download breakthrough curves (CSV) -->
Télécharger les courbes (CSV)

<!-- key: Detailed mass-budget data -->
Données détaillées du bilan massique

<!-- key: Stored run configuration -->
Configuration conservée

<!-- key: Download comparison table (CSV) -->
Télécharger le tableau comparatif (CSV)

<!-- key: Download run configuration (JSON) -->
Télécharger la configuration (JSON)

<!-- key: Prepare complete displayed-run archive -->
Préparer l'archive complète du calcul affiché

<!-- key: Preparing archive… -->
Préparation de l'archive…

<!-- key: Download run archive (ZIP) -->
Télécharger l'archive (ZIP)

<!-- key: Run -->
Calcul

<!-- key: Method -->
Méthode

<!-- key: Signal -->
Signal

<!-- key: Grid -->
Maillage

<!-- key: K zones -->
Zones K

<!-- key: Flow -->
Écoulement

<!-- key: MB disc. (%) -->
Écart masse (%)

<!-- key: Flow disc. (%) -->
Écart eau (%)

<!-- key: MT3D (s) -->
MT3D (s)

<!-- key: MP7 (s) -->
MP7 (s)

<!-- key: Flow (s) -->
Écoulement (s)

<!-- key: Total (s) -->
Total (s)

<!-- key: Ref. L1 (%) -->
Réf. L1 (%)

<!-- key: Mass (g) -->
Masse (g)

<!-- key: Input (g) -->
Apport (g)

<!-- key: Min. C (g/m³) -->
C min. (g/m³)

<!-- key: Neg. mass (g) -->
Masse nég. (g)

<!-- key: Centroid x (m) -->
Barycentre x (m)

<!-- key: Steps -->
Pas

<!-- key: Source box (m) -->
Emprise source (m)

<!-- key: End (d) -->
Fin (j)

<!-- key: Scenario -->
Scénario

<!-- key: Point -->
Point

<!-- key: Requested x -->
x demandé

<!-- key: Requested y -->
y demandé

<!-- key: Requested z -->
z demandé

<!-- key: Cell centre x -->
Centre cellule x

<!-- key: Cell centre y -->
Centre cellule y

<!-- key: Cell centre z -->
Centre cellule z

<!-- key: Layer -->
Couche

<!-- key: Row -->
Ligne

<!-- key: Column -->
Colonne

<!-- key: Cumulative in (g) -->
Entrée cumulée (g)

<!-- key: Cumulative out (g) -->
Sortie cumulée (g)

<!-- key: Sources (g) -->
Sources (g)

<!-- key: Sinks (g) -->
Puits (g)

<!-- key: Fluid storage (g) -->
Stockage fluide (g)

<!-- key: Native resident mass (g) -->
Masse résidente native (g)

<!-- key: Alternative disc. (%) -->
Écart alternatif (%)

<!-- key: Analytical reference requires homogeneous steady flow. -->
La référence analytique exige un écoulement permanent homogène.

<!-- key: Source cells -->
Cellules source

<!-- key: Specified head -->
Charge imposée

<!-- key: Section locations -->
Positions des coupes

<!-- key: Background flow -->
Écoulement de fond

<!-- key: Model preview: grid, boundaries and source -->
Aperçu : maillage, limites et source

<!-- key: Computed head contours -->
Isopièzes calculées

<!-- key: Homogeneous steady head contours -->
Isopièzes permanentes homogènes

<!-- key: Time (d) -->
Temps (j)

<!-- key: Mass rate (g/d) -->
Débit massique (g/j)

<!-- key: Instantaneous mass (g) -->
Masse instantanée (g)

<!-- key: Dirac input (initial cell mass) -->
Apport Dirac (masse initiale des cellules)

<!-- key: Finite pulse input -->
Apport en créneau

<!-- key: Continuous input -->
Apport continu

<!-- key: Concentration (g/m³) -->
Concentration (g/m³)

<!-- key: Elevation z (m) -->
Cote z (m)

<!-- key: MODPATH advection (slice) -->
Advection MODPATH (tranche)

<!-- key: Analytical -->
Analytique

<!-- key: Analytical (active run) -->
Analytique (calcul actif)

<!-- key: Mass output unavailable -->
Sortie massique indisponible

<!-- key: MT3D discrepancy (%) -->
Écart MT3D (%)

<!-- key: Initial + injected mass (first run) -->
Masse initiale + injectée (premier calcul)

<!-- key: Resident mass: grid sum and MT3D budget -->
Masse résidente : somme maillée et bilan MT3D

<!-- key: Reported mass-balance closure -->
Fermeture du bilan massique rapportée

<!-- key: Example: pulse plume after 600 days -->
Exemple : panache après 600 jours

<!-- key: Example: observation P1 -->
Exemple : observation P1

<!-- key: P1 · x (m) -->
P1 · x (m)

<!-- key: P1 · y (m) -->
P1 · y (m)

<!-- key: P1 · elevation z (m) -->
P1 · Cote z (m)

<!-- key: P2 · x (m) -->
P2 · x (m)

<!-- key: P2 · y (m) -->
P2 · y (m)

<!-- key: P2 · elevation z (m) -->
P2 · Cote z (m)

<!-- key: P3 · x (m) -->
P3 · x (m)

<!-- key: P3 · y (m) -->
P3 · y (m)

<!-- key: P3 · elevation z (m) -->
P3 · Cote z (m)

<!-- key: P4 · x (m) -->
P4 · x (m)

<!-- key: P4 · y (m) -->
P4 · y (m)

<!-- key: P4 · elevation z (m) -->
P4 · Cote z (m)

<!-- key: P5 · x (m) -->
P5 · x (m)

<!-- key: P5 · y (m) -->
P5 · y (m)

<!-- key: P5 · elevation z (m) -->
P5 · Cote z (m)

<!-- key: fig_head -->
Charge imposée : {head:g} m

<!-- key: fig_layers -->
{layers} couche(s) ; échelle verticale exagérée

<!-- key: fig_total -->
Total : {mass:g} g

<!-- key: fig_initial -->
{mass:g} g à t = 0

<!-- key: fig_xprofile -->
Profil x à y = {y:.3g} m

<!-- key: fig_yprofile -->
Profil y à x = {x:.3g} m

<!-- key: fig_section -->
Coupe {axis}–z à {other} = {value:.3g} m

<!-- key: fig_title -->
{method} · t = {time:g} j · couche {layer} (z = {z:.3g} m)

<!-- key: fig_gridmass -->
{label} : somme maillée

<!-- key: fig_nativemass -->
{label} : bilan MT3D

<!-- key: fig_nodata -->
{label} : hors domaine — aucune donnée

<!-- key: table_help_MB disc. (%) -->
Écart final du bilan massique rapporté par MT3D.

<!-- key: table_help_Flow disc. (%) -->
Écart final du bilan hydrique MODFLOW.

<!-- key: table_help_MT3D (s) -->
Durée réelle du programme de transport.

<!-- key: table_help_MP7 (s) -->
Durée MODPATH ; les particules décrivent uniquement l'advection.

<!-- key: table_help_Ref. L1 (%) -->
Erreur absolue de concentration pondérée par le volume poreux, divisée par la masse de référence.

<!-- key: table_help_Mass (g) -->
Masse dissoute finale intégrée sur le maillage de concentration.

<!-- key: MT3DMS final mass discrepancy exceeds 1%; inspect method and transport time step settings. -->
L'écart massique final MT3DMS dépasse 1 % ; vérifiez méthode et pas de transport.

<!-- key: At least one MODFLOW water-budget discrepancy exceeds 0.1%. -->
Au moins un écart du bilan hydrique MODFLOW dépasse 0,1 %.

<!-- key: Negative concentrations occurred. They are retained in diagnostics and exports; central FD and particle methods can oscillate. -->
Des concentrations négatives sont conservées dans diagnostics et exports. FD centré et méthodes particulaires peuvent osciller.

<!-- key: Source coordinates must lie inside the domain. -->
Les coordonnées de la source doivent être dans le domaine.

<!-- key: This confined lab requires heads at or above aquifer top. -->
Ce modèle captif exige des charges au moins égales à la cote du toit.

<!-- key: Pulse duration must be between zero and model duration. -->
La durée du créneau doit être comprise entre zéro et la durée du modèle.

<!-- key: Observation point is outside the model. -->
Le point d'observation est hors du modèle.

<!-- key: TVD requires PERCEL no greater than 1. -->
TVD impose PERCEL ≤ 1.

<!-- key: language_fallback -->
Une traduction manquante utilise le texte anglais.

<!-- key: preset_random -->
Paramètres aléatoires stochastiques

<!-- key: Random unit x (m) -->
Unité aléatoire x (m)

<!-- key: Random unit y (m) -->
Unité aléatoire y (m)

<!-- key: random_hint -->
Petites unités : motif fin ; grandes unités : plages plus larges. Conservez graine et tailles physiques lors du raffinement pour préserver la réalisation.

<!-- key: Active cells -->
Cellules actives

<!-- key: table_help_Active cells -->
Toutes les cellules non inactives, y compris celles à charge imposée.

<!-- key: Random field -->
Champ aléatoire

<!-- key: Comparison runs -->
Calculs comparés

<!-- key: discard_tags_hint -->
Retirez une étiquette avec × pour supprimer le calcul. Tout retirer commence une nouvelle comparaison. Exportez d'abord les calculs à conserver.

<!-- key: Head contours -->
Isopièzes

<!-- key: Computed head contours (m) -->
Isopièzes calculées (m)

<!-- key: Head contours appear after running the model -->
Les isopièzes apparaissent après le calcul

<!-- key: fig_background_k -->
K de fond = {k:.2e} m/s

<!-- key: fig_low_lens_k -->
Lentille faible K : K = {k:.2e} m/s

<!-- key: fig_high_channel_k -->
Chenal K élevé : K = {k:.2e} m/s

<!-- key: fig_low_barrier_k -->
Barrière faible K : K = {k:.2e} m/s

<!-- key: Focus on plume -->
Zoom sur le panache

<!-- key: Focus threshold (% of peak) -->
Seuil (% du maximum)

<!-- key: focus_hint -->
Le zoom utilise le pic positif actuel de chaque panache affiché, avec 20 % de marge de chaque côté. Les trajectoires MODPATH visibles restent incluses. Sans panache ni trajectoire, tout le domaine est affiché. Seule la vue de dessus change.

<!-- key: Download plume figure (SVG) -->
Télécharger le panache (SVG)

<!-- key: steady -->
permanent

<!-- key: transient -->
transitoire

<!-- key: fig_minimum -->
Minimum numérique : {minimum:.3g} g/m³

<!-- key: fig_minimum_log -->
Minimum numérique : {minimum:.3g} g/m³ (valeurs non positives masquées en échelle logarithmique)

<!-- key: The plume reaches an x specified-head boundary; enlarge the domain before treating the infinite-x analytical solution as a benchmark. -->
Le panache atteint une limite x à charge imposée ; agrandissez le domaine avant de prendre la solution infinie comme référence.

<!-- key: fig_reference_boundary -->
Erreur analytique désactivée : interaction aux limites x supérieure au seuil de {tolerance_percent:.2g}%.

<!-- key: Low K lens -->
Lentille à faible K

<!-- key: High K channel -->
Chenal à K élevée

<!-- key: Low K barrier -->
Barrière partielle à faible K

<!-- key: Page width -->
Largeur de page

<!-- key: width_1 -->
Étroite

<!-- key: width_2 -->
Compacte

<!-- key: width_3 -->
Standard

<!-- key: width_4 -->
Large

<!-- key: width_5 -->
Pleine largeur

<!-- key: page_width_hint -->
Cinq largeurs, d’étroite à pleine largeur. Standard conserve la largeur précédente. La page s’adapte aux petits écrans.

<!-- key: Show model grid -->
Afficher le maillage

<!-- key: grid_hint -->
Limites discrètes des cellules du calcul affiché. Les profils monocouches montrent des repères verticaux aux bords des cellules.

<!-- key: Plume-centered x/y -->
x/y centrés sur le panache

<!-- key: relative_hint -->
Le zéro est le barycentre de la masse dissoute positive dans la couche affichée. Les superpositions partagent cette origine. Coordonnées saisies et cotes restent absolues.

<!-- key: relative_mass_origin -->
Origine relative : x = {x:.2f} m ; y = {y:.2f} m (barycentre du panache).

<!-- key: relative_source_origin -->
Aucune masse positive dans cette couche : origine au centre de la source maillée, x = {x:.2f} m ; y = {y:.2f} m.

<!-- key: fig_relative_xprofile -->
Profil x à y′ = {y:.3g} m

<!-- key: fig_relative_yprofile -->
Profil y à x′ = {x:.3g} m

<!-- key: fig_relative_section -->
Coupe {axis}–z à {other}′ = {value:.3g} m

<!-- key: MODPATH particle count -->
Nombre de particules MODPATH

<!-- key: particle_count_cell -->
Par cellule source

<!-- key: particle_count_total -->
Source entière par lâcher

<!-- key: Particles in the whole source per release -->
Particules dans toute la source par lâcher

<!-- key: particle_count_summary -->
{count} particules dans {cells} cellules sources × {groups} lâchers = {total} particules.

<!-- key: expert_transport_hint -->
Tous les réglages du solveur de transport sont visibles. NPL / NPH et NPMIN / NPMAX contrôlent les particules MOC / HMOC ; MXPART limite leur total. Les aides précisent les méthodes concernées. MODPATH utilise des particules distinctes.

<!-- key: Plume animation -->
Animation du panache

<!-- key: Animation view -->
Vue de l’animation

<!-- key: animation_2d -->
Vue en plan et coupes

<!-- key: animation_3d -->
Concentrations 3D aux centres des cellules

<!-- key: Animation frames -->
Images de l’animation

<!-- key: Playback speed (frames/s) -->
Vitesse (images/s)

<!-- key: Vertical exaggeration -->
Exagération verticale

<!-- key: Generate / refresh animation -->
Générer / actualiser l’animation

<!-- key: Generating animation… -->
Création de l’animation…

<!-- key: Download animation (HTML) -->
Télécharger l’animation (HTML)

<!-- key: Play -->
Lire

<!-- key: Pause -->
Pause

<!-- key: Animation frame -->
Image de l’animation

<!-- key: animation_layers_hint -->
Ajoutez des couches dans les réglages experts pour la vue 3D.

<!-- key: animation_hint -->
Utilise les instants enregistrés du calcul affiché. Choisissez ci-dessous les couleurs et le zoom propres à l’animation ; l’échelle reste fixe dans le temps. Les autres paramètres 2D sont conservés. Comparaisons et références analytiques restent dans les figures statiques. Le lecteur apparaît sous les paramètres ; le fichier HTML téléchargé fonctionne hors ligne.

<!-- key: animation_3d_hint -->
La vue 3D montre les concentrations aux centres des cellules au-dessus du seuil, avec caméra fixe. Au plus {maximum} cellules régulièrement échantillonnées sont affichées ; calculs et exports conservent toutes les cellules. Les particules comparent l’advection. L’exagération est uniquement visuelle.

<!-- key: animation_refresh_hint -->
Les réglages ont changé. Générez à nouveau pour actualiser le lecteur.

<!-- key: animation_failed -->
Impossible de créer l’animation. Les résultats restent conservés.

<!-- key: animation_size_limit -->
L’animation dépasse 45 Mio. Réduisez le nombre d’images.

<!-- key: help_s_percel -->
Déplacement advectif maximal par pas, en largeurs de cellule. TVD exige ≤ 1.

<!-- key: help_s_mxpart -->
MOC/HMOC : capacité totale de particules mobiles, non par cellule.

<!-- key: help_s_itrack -->
MOC/MMOC/HMOC : 1 = Euler, 2 = Runge–Kutta d’ordre 4, 3 = suivi hybride.

<!-- key: help_s_wd -->
Méthodes caractéristiques : pondération de concentration lors du fractionnement ; 0,5–1.

<!-- key: help_s_dceps -->
MOC/HMOC : seuil du gradient relatif séparant les placements NPL et NPH.

<!-- key: help_s_nplane -->
MOC/HMOC : 0 = placement aléatoire ; positif = plans horizontaux par cellule.

<!-- key: help_s_npl -->
MOC/HMOC : particules initiales par cellule à gradient ≤ DCEPS ; zéro permis.

<!-- key: help_s_nph -->
MOC/HMOC : particules initiales par cellule à fort gradient. Les motifs fixes peuvent arrondir ce nombre.

<!-- key: help_s_npmin -->
MOC/HMOC : ajout de particules sous ce minimum par cellule.

<!-- key: help_s_npmax -->
MOC/HMOC : au-delà, remplacement des particules de la cellule par un ensemble de taille NPH.

<!-- key: help_s_interp -->
MMOC/HMOC : interpolation de concentration ; seule 1 (linéaire) est disponible.

<!-- key: help_s_nlsink -->
Cellules puits MMOC/HMOC : 0 = aléatoire ; positif = plans de particules.

<!-- key: help_s_npsink -->
MMOC/HMOC : particules représentant chaque cellule puits.

<!-- key: help_s_dchmoc -->
HMOC : MOC au-dessus de ce seuil de gradient relatif, MMOC en dessous.

<!-- key: help_s_mxiter -->
Limite d’itérations externes GCG. Une suffit pour ce transport conservatif linéaire.

<!-- key: help_s_iter1 -->
Limite d’itérations internes GCG pour les équations de transport.

<!-- key: help_s_isolve -->
Préconditionneur GCG : 1 = Jacobi, 2 = SSOR, 3 = Cholesky incomplet modifié (MIC).

<!-- key: help_s_ncrs -->
Termes croisés : 0 = approximation au second membre ; 1 = tenseur complet dans la matrice.

<!-- key: help_s_accl -->
Facteur de relaxation, uniquement pour SSOR (ISOLVE = 2).

<!-- key: help_s_cclose -->
Tolérance relative de variation de concentration GCG. Une valeur plus petite est plus stricte.

<!-- key: help_s_iprgcg -->
Imprime les variations toutes les N itérations GCG ; 0 en fin de période.

<!-- key: help_s_dt0 -->
Pas initial en jours ; 0 laisse MT3D le choisir.

<!-- key: help_s_ttsmult -->
Multiplicateur des pas pour les différences finies implicites ; ignoré par TVD et les caractéristiques.

<!-- key: help_s_ttsmax -->
Pas maximal en jours si TTSMULT > 1 ; 0 utilise la limite automatique.

<!-- key: help_s_mxstrn -->
Nombre maximal de pas de transport par pas d’écoulement ; la limite peut arrêter le calcul.

<!-- key: help_s_timeout -->
Durée maximale par exécutable. Plus de particules peuvent nécessiter plus de temps.

<!-- key: help_s_hclose -->
Tolérance PCG de variation de charge, en mètres.

<!-- key: help_s_rclose -->
Tolérance du résidu de débit PCG, en m³/jour.

<!-- key: help_s_flow_mxiter -->
Itérations externes maximales du solveur d’écoulement MODFLOW PCG.

<!-- key: help_s_flow_iter1 -->
Itérations internes PCG maximales par itération externe.

<!-- key: help_particle_count_mode -->
Choisir par cellule source ou un total exact pour toute la source à chaque lâcher.

<!-- key: help_particles_per_cell -->
Particules réparties régulièrement dans chaque cellule source à chaque lâcher. MODPATH uniquement, pas MOC.

<!-- key: help_total_source_particles -->
Total exact par lâcher sur toutes les cellules sources ; au moins une par cellule. Écart maximal d’une particule entre cellules ; masses pondérées par volume poreux.

<!-- key: help_release_groups -->
Lâchers aux milieux d’intervalles égaux pour impulsion ou apport continu. Plus de groupes affinent le temps ; Dirac utilise t = 0.

<!-- key: help_run_label -->
Laisser vide pour le nom suggéré. Un libellé remplace méthode/signal ; numéro et suffixe hétérogène restent automatiques.

<!-- key: help_expert -->
Afficher les couches et tous les paramètres des solveurs. Les valeurs masquées sont conservées.

<!-- key: help_sliders -->
Changer entre champs numériques et curseurs sans modifier les valeurs.

<!-- key: help_extent -->
Étendue physique en mètres. La modifier commence une nouvelle série.

<!-- key: help_thickness -->
Épaisseur captive ; base à 0 m, sommet à cette valeur. Couches d’épaisseur égale.

<!-- key: help_grid_mode -->
Fixer le nombre ou la largeur maximale des cellules. Le nombre est arrondi vers le haut en conservant le domaine.

<!-- key: help_grid_count -->
Nombre de cellules uniformes dans cette direction. Les calculs précédents sont conservés.

<!-- key: help_cell_width -->
Largeur maximale souhaitée en mètres. L’aperçu donne la largeur uniforme réelle.

<!-- key: help_nlay -->
Une couche donne un modèle en plan ; plusieurs couches égales permettent transport vertical et vues 3D.

<!-- key: help_k -->
Conductivité hydraulique horizontale de fond. Saisie en m/s, conversion en m/jour.

<!-- key: help_porosity -->
Fraction poreuse mobile ; contrôle vitesse interstitielle et stockage du soluté.

<!-- key: help_ss -->
Eau libérée par volume et baisse unitaire de charge (1/m). Aucun stockage en régime permanent ici.

<!-- key: help_kv_ratio -->
Conductivité verticale divisée par l’horizontale, dans chaque couche.

<!-- key: help_zones_preset -->
Choisir homogénéité, champ aléatoire reproductible ou lentille/chenal/barrière.

<!-- key: help_zone_seed -->
Graine aléatoire. Mêmes graine et réglages reproduisent le motif physique.

<!-- key: help_random_unit -->
Taille physique des blocs aléatoires dans cette direction, indépendante du maillage.

<!-- key: help_random_k -->
Bornes de conductivité aléatoire, tirage uniforme en espace logarithmique (m/s).

<!-- key: help_random_ss -->
Bornes du stockage spécifique log-uniforme (1/m). Conservé, inactif en écoulement permanent.

<!-- key: help_random_por -->
Bornes de porosité efficace uniforme, entre zéro et un.

<!-- key: help_head -->
Charge imposée sur cette colonne externe. Gauche supérieure à droite ; les deux au-dessus du toit.

<!-- key: help_duration -->
Durée totale du transport en jours, indépendante de la vitesse de l’animation.

<!-- key: help_dispersion -->
Inclure l’étalement mécanique proportionnel à la vitesse interstitielle. Sans cela restent advection et dispersion numérique.

<!-- key: help_al -->
Dispersivité longitudinale en mètres ; coefficient associé = αL × vitesse.

<!-- key: help_trpt -->
Dispersivité transversale horizontale divisée par longitudinale : αTH/αL.

<!-- key: help_trpv -->
Dispersivité transversale verticale divisée par longitudinale : αTV/αL. Utile en multicouche.

<!-- key: help_source_kind -->
Dirac : masse initiale à t = 0. Impulsion : apport constant jusqu’à sa fin. Continu : apport constant tout le calcul.

<!-- key: help_source_mass -->
Masse dissoute initiale répartie dans le volume poreux source (grammes).

<!-- key: help_mass_rate -->
Apport total (g/jour), réparti selon le volume poreux source. Aucune injection d’eau.

<!-- key: help_pulse_duration -->
L’apport cesse après ce temps (jours), inférieur à la durée totale.

<!-- key: help_source_position -->
Coordonnée absolue du centre source en mètres, ramenée à une cellule. Éviter les colonnes à charge imposée.

<!-- key: help_source_cells -->
Nombre de cellules sources dans cette direction. Vérifier l’emprise ; changer la géométrie commence une nouvelle série.

<!-- key: help_source_all_layers -->
Répartir la source sur toutes les couches, sinon sur la seule couche choisie.

<!-- key: help_src_layer -->
Couche recevant la source ; 1 est la couche supérieure.

<!-- key: help_method -->
Choisir l’advection MT3D : FD amont/centré, TVD, MOC avant, MMOC arrière ou HMOC hybride. Indépendant de MODPATH.

<!-- key: help_track_particles -->
Exécuter MODPATH 7 dans l’écoulement calculé. Advection seule, sans dispersion ni concentration calculée par MODPATH.

<!-- key: help_observation -->
Coordonnée absolue d’observation en mètres. Concentration de la cellule contenant le point, sans interpolation.

<!-- key: help_nobs -->
Comparer les concentrations en un à cinq points avec les calculs sauvegardés.

<!-- key: help_outputs -->
Temps sauvegardés, dont t = 0 ; fin d’impulsion aussi conservée. Plus de sorties affinent animation et courbes, pas les pas du solveur.

<!-- key: help_length -->
Étendue physique en mètres. La modifier commence une nouvelle série.

<!-- key: help_width -->
Étendue physique en mètres. La modifier commence une nouvelle série.

<!-- key: help_ncol -->
Nombre de cellules uniformes dans cette direction. Les calculs précédents sont conservés.

<!-- key: help_nrow -->
Nombre de cellules uniformes dans cette direction. Les calculs précédents sont conservés.

<!-- key: help_cell_x -->
Largeur maximale souhaitée en mètres. L’aperçu donne la largeur uniforme réelle.

<!-- key: help_cell_y -->
Largeur maximale souhaitée en mètres. L’aperçu donne la largeur uniforme réelle.

<!-- key: help_random_unit_x -->
Taille physique des blocs aléatoires dans cette direction, indépendante du maillage.

<!-- key: help_random_unit_y -->
Taille physique des blocs aléatoires dans cette direction, indépendante du maillage.

<!-- key: help_zone_k_min -->
Bornes de conductivité aléatoire, tirage uniforme en espace logarithmique (m/s).

<!-- key: help_zone_k_max -->
Bornes de conductivité aléatoire, tirage uniforme en espace logarithmique (m/s).

<!-- key: help_zone_ss_min -->
Bornes du stockage spécifique log-uniforme (1/m). Conservé, inactif en écoulement permanent.

<!-- key: help_zone_ss_max -->
Bornes du stockage spécifique log-uniforme (1/m). Conservé, inactif en écoulement permanent.

<!-- key: help_zone_por_min -->
Bornes de porosité efficace uniforme, entre zéro et un.

<!-- key: help_zone_por_max -->
Bornes de porosité efficace uniforme, entre zéro et un.

<!-- key: help_head_left -->
Charge imposée sur cette colonne externe. Gauche supérieure à droite ; les deux au-dessus du toit.

<!-- key: help_head_right -->
Charge imposée sur cette colonne externe. Gauche supérieure à droite ; les deux au-dessus du toit.

<!-- key: help_src_x -->
Coordonnée absolue du centre source en mètres, ramenée à une cellule. Éviter les colonnes à charge imposée.

<!-- key: help_src_y -->
Coordonnée absolue du centre source en mètres, ramenée à une cellule. Éviter les colonnes à charge imposée.

<!-- key: help_src_ncol -->
Nombre de cellules sources dans cette direction. Vérifier l’emprise ; changer la géométrie commence une nouvelle série.

<!-- key: help_src_nrow -->
Nombre de cellules sources dans cette direction. Vérifier l’emprise ; changer la géométrie commence une nouvelle série.

<!-- key: help_animation_mode -->
2D anime plan et coupes. 3D montre les concentrations calculées aux centres, avec vue fixe ; plusieurs couches nécessaires.

<!-- key: help_animation_frames -->
Jusqu’à 80 états sauvegardés, premier et dernier compris. Pas d’interpolation temporelle des concentrations.

<!-- key: help_animation_fps -->
Images par seconde réelle. Chaque image indique le temps simulé ; la lecture ne change pas le modèle.

<!-- key: help_animation_exaggeration -->
Étirer visuellement la hauteur 3D. Altitudes et calculs restent inchangés.

<!-- key: help_generate_animation -->
Rendu à la demande des résultats sauvegardés. Régénérer après réglage ; sans relancer le modèle.

<!-- key: help_view_time -->
Choisir un temps sauvegardé, sans relancer le modèle.

<!-- key: help_view_layer -->
Couche affichée en plan ; 1 est en haut.

<!-- key: help_section -->
Position absolue en mètres, dans la ligne/colonne contenant la coordonnée. Les axes relatifs ne déplacent pas la coupe.

<!-- key: help_fill -->
Colorer les cellules selon la concentration ; le zéro reste blanc.

<!-- key: help_lines -->
Tracer les isolignes de concentration sur les couleurs.

<!-- key: help_show_heads -->
Superposer les isopièzes calculées fines, étiquetées en mètres.

<!-- key: help_log -->
Couleurs logarithmiques pour concentrations positives. Valeurs non positives masquées uniquement à l’affichage.

<!-- key: help_particle_paths -->
Afficher positions et trajectoires MODPATH jusqu’au temps choisi. Maximum 120 trajectoires affichées ; exports complets.

<!-- key: help_opacity -->
Opacité : 1 est opaque ; plus petit révèle les éléments sous-jacents.

<!-- key: help_focus_plume -->
Zoom sur le panache positif et les trajectoires avec marge. Animation dans une fenêtre fixe sur les temps choisis.

<!-- key: help_focus_threshold -->
Zoom statique : pourcentage du pic du panache. En animation 3D : pourcentage du maximum absolu de l’échelle fixe pour afficher les cellules.

<!-- key: help_analytical -->
Comparer à la référence analytique homogène permanente. Écoulements hétérogènes ou transitoires hors hypothèses.

<!-- key: help_compare -->
Comparer les calculs au temps disponible le plus proche, aux coupes du calcul affiché.

<!-- key: help_analytic_on -->
Comparer à la référence analytique homogène permanente. Écoulements hétérogènes ou transitoires hors hypothèses.

<!-- key: help_btc_analytical -->
Comparer à la référence analytique homogène permanente. Écoulements hétérogènes ou transitoires hors hypothèses.

<!-- key: help_compare_sections -->
Comparer les calculs au temps disponible le plus proche, aux coupes du calcul affiché.

<!-- key: help_overlay_runs -->
Comparer les calculs au temps disponible le plus proche, aux coupes du calcul affiché.

<!-- key: help_compare_top -->
Comparer les calculs au temps disponible le plus proche, aux coupes du calcul affiché.

<!-- key: help_btc_runs -->
Comparer les concentrations en un à cinq points avec les calculs sauvegardés.

<!-- key: Animation settings -->
Paramètres de l’animation

<!-- key: Animation colour scale -->
Échelle de couleurs de l’animation

<!-- key: animation_colour_enhanced -->
Faibles concentrations renforcées (échelle fixe)

<!-- key: animation_colour_linear -->
Linéaire (échelle fixe)

<!-- key: animation_colour_log -->
Logarithmique (échelle fixe)

<!-- key: help_animation_colour -->
Le renforcement utilise une transformation puissance (exposant 0,35) pour révéler les faibles concentrations. Toutes les images conservent les mêmes limites physiques de concentration ; zéro reste blanc. Les échelles linéaire et renforcée montrent les valeurs numériques négatives ; l’échelle logarithmique masque les valeurs non positives. Les données calculées ne changent pas.

<!-- key: Zoom animation to plume -->
Zoomer l’animation sur le panache

<!-- key: help_animation_focus -->
Un cadrage fixe englobe le panache positif et les trajectoires MODPATH affichées à tous les instants sélectionnés, avec une marge de 20 %. Indépendant du zoom statique. Désactiver pour voir tout le domaine. Disponible en 2D et 3D.

<!-- key: Plume threshold (% of peak) -->
Seuil du panache (% du maximum)

<!-- key: help_animation_threshold -->
Le zoom inclut les concentrations supérieures à ce pourcentage du maximum positif de chaque image. En 3D, ce seuil définit aussi les cellules affichées par rapport à la concentration absolue maximale de l’échelle fixe. Valeur initiale : 0,1 %. Effet uniquement visuel.

<!-- key: animation_progress -->
Création de l’animation… {percent} %

<!-- key: MODPATH settings -->
Paramètres MODPATH

<!-- key: expert_transport_location_hint -->
Les paramètres experts MT3D se trouvent dans le volet dépliable séparé **Paramètres experts du solveur de transport**, juste en dessous. Les paramètres MODPATH viennent ensuite.
