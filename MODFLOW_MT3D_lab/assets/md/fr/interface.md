## title

Laboratoire de transport 1D

## experiments

Expériences guidées

## experiment_front

Front d’advection

## experiment_spreading

Dispersion physique

## experiment_impulse

Créneau et impulsion

## theory_title

Écoulement et solutions analytiques

## setup

Configuration du modèle

## inlet_processes

Entrée et transport

## grid_time

Maillage et temps

## solver

Méthode MT3DMS

## signal

Signal d’entrée

## continuous

Entrée continue

## block

Créneau

## dirac

Impulsion de Dirac

## amplitude

Concentration d’entrée C/Cref [–]

## block_days

Durée du créneau [j]

## impulse_area

Aire de l’impulsion A [j]

## impulse_days

Largeur numérique ε [j]

## rectangle

Hauteur d’entrée MT3DMS = {height:.4g} C/Cref.

## dispersion

Activer la dispersion

## dispersivity

Dispersivité longitudinale αL [m]

## diffusion

Diffusion effective Dₑ [m²/j]

## grid_by

Définir le maillage par

## cells

Nombre de cellules

## spacing

Pas spatial

## cell_count

Cellules

## target_spacing

Largeur souhaitée [m]

## grid_summary

{n} cellules · Δx réel = {dx:.3g} m

## courant

Limite de Courant

## time_hint

Toutes les variantes se terminent au jour 2000. Un créneau utilise au moins huit pas de transport pendant son application.

## scheme

Schéma d’advection

## upwind

DF · amont

## central

DF · centré

## tvd

TVD · ULTIMATE

## moc

MOC

## mmoc

MMOC

## hmoc

HMOC

## solver_hint

MODFLOW-2005 fournit l’écoulement permanent. MT3DMS résout ses équations implicites avec GCG.

## preview

Aperçu du modèle

## preview_summary

{signal} · {scheme} · {n} cellules · Δx = {dx:.3g} m · D = {D:.4g} m²/j

## distance

Distance depuis l’entrée [m]

## time

Temps [j]

## inlet_axis

Entrée C/Cref [–]

## optional_name

Nom de la variante (facultatif)

## name_example

p. ex. Maillage fin avec TVD

## limit

Dix variantes sont enregistrées. Supprimez-en une dans « Gérer les variantes » pour lancer un autre calcul.

## missing

Exécutable requis absent ou incompatible — {names}. Utilisez le dossier partagé bin ou définissez TRANSPORT_LAB_BIN.

## run

Lancer le modèle

## running

Calcul MODFLOW-2005 et MT3DMS en cours…

## failed

Le calcul n’a pas abouti. Les variantes précédentes restent disponibles ci-dessous.

## diagnostic

Détails du calcul

## results

Résultats du transport

## visible

Variantes sur les graphiques

## cells_unit

cellules

## show_analytical

Solution analytique

## show_markers

Points numériques

## profile

Profil de concentration

## breakthrough

Courbe de restitution

## budget

Bilan de masse du soluté

## profile_time

Temps du profil [j]

## observation

Distance d’observation [m]

## applied_curve

Analytique · entrée appliquée

## ideal_curve

Dirac idéal

## mass_axis

Écart de masse [%]

## no_selection

Sélectionnez une variante pour afficher ses courbes.

## comparison

Comparaison finale · jour 2000

## variant

Variante

## rmse

RMSE

## mae

MAE

## ideal_rmse

RMSE · Dirac idéal

## mass_error

Écart de masse [%]

## seconds

Durée du calcul [s]

## run_name

Nom

## dx_col

Δx [m]

## height_col

Entrée C/Cref

## duration_col

Durée d’entrée [j]

## area_col

Dirac A [j]

## alpha_col

αL [m]

## dm_col

Dₑ [m²/j]

## d_col

D [m²/j]

## pe_col

Péclet de maille

## co_col

Limite de Courant

## count_col

Pas de transport

## flow_s

MODFLOW [s]

## mt_s

MT3DMS [s]

## flow_error

Bilan d’eau [%]

## min_c

Min. final C/Cref

## max_c

Max. final C/Cref

## detail_heading

Paramètres et définition des indicateurs

## download

Télécharger la comparaison (CSV)

## manage

Gérer les variantes

## remove_choice

Variante à supprimer

## remove

Supprimer la variante sélectionnée

## references_title

Références

## saved

V{number} enregistrée pour la comparaison.

## applied_color_key

Analytique · couleur de la variante

## ideal_color_key

Dirac idéal · couleur de la variante

## pulse_cells

Longueur du signal [cellules]

## pulse_resolution

Pendant l’entrée, l’advection transporte le signal sur {length:.3g} m, soit {cells:.3g} cellules.

## specified_head

Charge imposée · {head:.4g} m

## hydraulic_summary

Conductivité hydraulique K = {k:.0e} m/s

## scenario_reset_hint

Toute modification ici efface les variantes enregistrées.

## comparison_cleared

L’entrée ou le transport a changé. La comparaison a été effacée pour le nouveau scénario.

## concept_title

Modèle conceptuel et réponses typiques

## concept_inlet

Entrée

## concept_outlet

Sortie

## concept_observation

Observation

## concept_profile

Profil à t = {time:g} d

## concept_breakthrough

Percée à x = {distance:g} m

## concept_advection

Advection seule

## concept_dispersion

Advection + dispersion
