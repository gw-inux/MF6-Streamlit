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
MT3D 2D/3D · v0.4.0 · Version de travail pour l'enseignement en direct

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
