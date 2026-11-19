## title

1D-Labor für Stofftransport

## experiments

Geführte Experimente

## experiment_front

Advektionsfront

## experiment_spreading

Physikalische Dispersion

## experiment_impulse

Puls und Impuls

## theory_title

Strömungsfeld und analytische Lösungen

## setup

Modelleingabe

## inlet_processes

Einlass und Transport

## grid_time

Raum und Zeit

## solver

MT3DMS-Verfahren

## signal

Eingangssignal

## continuous

Kontinuierliche Eingabe

## block

Rechteckpuls

## dirac

Dirac-Impuls

## amplitude

Einlasskonzentration C/Cref [–]

## block_days

Pulsdauer [d]

## impulse_area

Impulsfläche A [d]

## impulse_days

Numerische Pulsbreite ε [d]

## rectangle

Pulshöhe in MT3DMS = {height:.4g} C/Cref.

## dispersion

Dispersion aktivieren

## dispersivity

Longitudinale Dispersivität αL [m]

## diffusion

Effektive Diffusion Dₑ [m²/d]

## grid_by

Gitter vorgeben über

## cells

Zellenzahl

## spacing

Zellweite

## cell_count

Zellen

## target_spacing

Gewünschte Zellweite [m]

## grid_summary

{n} Zellen · tatsächliches Δx = {dx:.3g} m

## courant

Courant-Zahl (Obergrenze)

## time_hint

Alle Varianten enden an Tag 2000. Ein endlicher Eingangspuls wird während der Eingabe in mindestens acht Transportschritte aufgeteilt.

## scheme

Advektionsverfahren

## upwind

FD · Upwind

## central

FD · zentriert

## tvd

TVD · ULTIMATE

## moc

MOC

## mmoc

MMOC

## hmoc

HMOC

## solver_hint

MODFLOW-2005 berechnet das stationäre Strömungsfeld. MT3DMS löst die impliziten Gleichungen mit GCG.

## preview

Modellvorschau

## preview_summary

{signal} · {scheme} · {n} Zellen · Δx = {dx:.3g} m · D = {D:.4g} m²/d

## distance

Entfernung vom Einlass [m]

## time

Zeit [d]

## inlet_axis

Einlass C/Cref [–]

## optional_name

Bezeichnung der Variante (optional)

## name_example

z. B. Feines Gitter mit TVD

## limit

Zehn Varianten sind gespeichert. Unter „Varianten verwalten“ können Sie einen Platz für einen weiteren Lauf freigeben.

## missing

Benötigte Programmdatei fehlt oder ist auf diesem System nicht ausführbar — {names}. Legen Sie sie im gemeinsamen bin-Ordner ab oder setzen Sie TRANSPORT_LAB_BIN auf das entsprechende Verzeichnis.

## run

Modell starten

## running

MODFLOW-2005 und MT3DMS rechnen …

## failed

Der Modelllauf konnte nicht abgeschlossen werden. Bisher gespeicherte Varianten stehen unten zur Verfügung.

## diagnostic

Programmausgabe

## results

Transportergebnisse

## visible

Varianten in den Diagrammen

## cells_unit

Zellen

## show_analytical

Analytische Lösung

## show_markers

Numerische Stützstellen

## profile

Konzentrationsprofil

## breakthrough

Durchbruchskurve

## budget

Stoffmassenbilanz

## profile_time

Zeitpunkt des Profils [d]

## observation

Beobachtungsentfernung [m]

## applied_curve

Analytisch · angelegtes Signal

## ideal_curve

Idealer Dirac-Impuls

## mass_axis

Massenbilanzfehler [%]

## no_selection

Wählen Sie oben eine Variante für die Diagramme aus.

## comparison

Abschlussvergleich · Tag 2000

## variant

Variante

## rmse

RMSE

## mae

MAE

## ideal_rmse

RMSE · idealer Dirac

## mass_error

Massenbilanzfehler [%]

## seconds

Rechenzeit [s]

## run_name

Bezeichnung

## dx_col

Δx [m]

## height_col

Einlass C/Cref

## duration_col

Eingabedauer [d]

## area_col

Dirac A [d]

## alpha_col

αL [m]

## dm_col

Dₑ [m²/d]

## d_col

D [m²/d]

## pe_col

Gitter-Péclet-Zahl

## co_col

Courant-Obergrenze

## count_col

Transportschritte

## flow_s

MODFLOW [s]

## mt_s

MT3DMS [s]

## flow_error

Wasserbilanzfehler [%]

## min_c

Endwert min. C/Cref

## max_c

Endwert max. C/Cref

## detail_heading

Laufeinstellungen und Definition der Kennzahlen

## download

Vergleich herunterladen (CSV)

## manage

Varianten verwalten

## remove_choice

Zu entfernende Variante

## remove

Gewählte Variante entfernen

## references_title

Quellen

## saved

V{number} wurde für den Vergleich gespeichert.

## applied_color_key

Analytisch · Farbe der Variante

## ideal_color_key

Idealer Dirac · Farbe der Variante

## pulse_cells

Pulslänge [Zellen]

## pulse_resolution

Während der Eingabe legt der Puls advektiv {length:.3g} m zurück. Das entspricht {cells:.3g} Gitterzellen.

## specified_head

Vorgegebene Höhe · {head:.4g} m

## hydraulic_summary

Hydraulische Leitfähigkeit K = {k:.0e} m/s

## scenario_reset_hint

Änderungen hier löschen die gespeicherten Vergleichsvarianten.

## comparison_cleared

Die Einlass- oder Transporteinstellungen wurden geändert. Der Vergleich wurde für das neue Szenario geleert.

## concept_title

Modellkonzept und typische Ergebnisse

## concept_inlet

Einlass

## concept_outlet

Auslass

## concept_observation

Beobachtung

## concept_profile

Profil bei t = {time:g} d

## concept_breakthrough

Durchbruch bei x = {distance:g} m

## concept_advection

Reine Advektion

## concept_dispersion

Advektion + Dispersion
