<!-- key: title -->
MT3D – 2D/3D-Transportlabor

<!-- key: intro_caption -->
Einführende Illustration: beispielhafte Stofffahne und Durchbruchskurve. Diese Illustration ist unabhängig von den aktuellen Modelleingaben.

<!-- key: Model & run -->
1 · Modell und Berechnung

<!-- key: Results & method comparison -->
2 · Ergebnisse und Methodenvergleich

<!-- key: series_reset -->
Eine neue Vergleichsreihe wurde begonnen, weil sich das Eingangssignal oder die Modell-/Quellgeometrie geändert hat. Frühere Läufe wurden entfernt.

<!-- key: grid_summary -->
Gitter: {nx} × {ny} × {nz} Zellen. Tatsächliche Zellweite: Δx = {dx:.3f} m; Δy = {dy:.3f} m; Δz = {dz:.3f} m.

<!-- key: velocity_summary -->
Homogene Referenz-Abstandsgeschwindigkeit: {velocity:.4f} m/Tag.

<!-- key: source_bounds -->
x = {x0:.2f}–{x1:.2f} m; y = {y0:.2f}–{y1:.2f} m; z = {z0:.2f}–{z1:.2f} m.

<!-- key: source_snap_hint -->
Die Quelle belegt die ausgewählten Zellen. Eine andere Auflösung kann ihre tatsächlichen Abmessungen ändern. Die Eingabe der Zellweite erhält die gesamte Modellausdehnung; angezeigt wird die tatsächliche gleichmäßige Zellweite.

<!-- key: input_error -->
Bitte korrigieren Sie die angegebenen Modelleinstellungen vor der Berechnung.

<!-- key: missing_executables -->
Erforderliche Programme fehlen: {names}. Passende ausführbare Dateien in `bin/` der App oder des Repositorys bereitstellen. Lokale Einrichtung: `python setup_executables.py`.

<!-- key: label_placeholder -->
Automatisch: 01 TVD / Pulse (heterogen: / het.)

<!-- key: history_full -->
Zehn Läufe sind gespeichert. Entfernen Sie einen Lauf oder leeren Sie die Vergleichsreihe.

<!-- key: running -->
MODFLOW, MT3D und optional MODPATH werden ausgeführt…

<!-- key: run_success -->
Berechnung abgeschlossen. Der neueste Lauf wird jetzt angezeigt.

<!-- key: run_failed -->
Dieser Lauf konnte nicht abgeschlossen werden und wurde nicht in den Vergleich aufgenommen.

<!-- key: changed_source_footprint -->
Die Gitterverfeinerung hat die tatsächlich abgebildete Quellgröße verändert. Beachten Sie beim Auflösungsvergleich die Quellgröße in der erweiterten Tabelle.

<!-- key: nearest_time -->
{name}: nächste gespeicherte Zeit {time:.3f} Tage (angezeigter Lauf: {target:.3f} Tage).

<!-- key: no_comparison_time -->
{name}: keine Ausgabe bei {time:.3f} Tagen; ausgelassen.

<!-- key: evaluating_reference -->
Analytische Referenz wird berechnet…

<!-- key: export_hint -->
Das Laufarchiv enthält Modelleingaben, Protokolle, Konzentrations-/Potentialhöhenfelder, Massenbilanzen und Partikeldaten. Details zu Partikelankünften bleiben im Export verfügbar.

<!-- key: no_runs -->
Starten Sie das voreingestellte Pulsexperiment, um Stofffahne, Profile, Beobachtungskurven und Methodenvergleich anzuzeigen.

<!-- key: footer -->
MT3D 2D/3D-Transportlabor · v0.5.0 · Arbeitsversion für die begleitete Lehre

<!-- key: transient_hint -->
Das ursprüngliche Strömungsfeld wird zuerst stationär berechnet; die rechte Potentialhöhe ändert sich bei t = 0.

<!-- key: expert_flow_hint -->
Experteneinstellungen aktivieren, um Toleranzen und Iterationen des Strömungslösers zu ändern.

<!-- key: stochastic_hint -->
Fester Startwert = reproduzierbare Zonen. K und Ss werden logarithmisch gleichverteilt, die Porosität gleichverteilt gezogen. Bei Gitterverfeinerung bleibt dieselbe Realisierung erhalten.

<!-- key: zones_hint -->
Rechteckige Zonen wählen Zellen über ihre Mittelpunkte; spätere Zeilen überschreiben frühere. Schichtnummern beginnen bei 1.

<!-- key: observation_hint -->
Beobachtungskurven verwenden die jeweilige Zelle. Positionen können ohne Neuberechnung gespeicherter Modelle geändert werden.

<!-- key: output_hint -->
Enthält t = 0 und die Endzeit. Hier wird die Konzentrationsausgabe für Diagramme und Export festgelegt.

<!-- key: preset_homogeneous -->
Homogen

<!-- key: preset_lens -->
Linse mit kleinem K

<!-- key: preset_channel -->
Rinne mit hohem K

<!-- key: preset_barrier -->
Teilweise Barriere mit kleinem K

<!-- key: preset_stochastic -->
Stochastische Zonierung

<!-- key: preset_custom -->
Eigene Rechtecke

<!-- key: preset_hint_lens -->
Zentrale Linse: K = 0,01 × Hintergrund-K; gesamte Modelltiefe.

<!-- key: preset_hint_channel -->
Längsrinne: K = 10 × Hintergrund-K; gesamte Modelltiefe.

<!-- key: preset_hint_barrier -->
Teilweise Querbarriere: K = 0,01 × Hintergrund-K; ein seitlicher Durchflussbereich bleibt frei.

<!-- key: signal_pulse -->
Puls / Blockeingabe

<!-- key: signal_continuous -->
Kontinuierliche Eingabe

<!-- key: signal_dirac -->
Dirac / momentane Stoffzugabe

<!-- key: signal_short_pulse -->
Puls

<!-- key: signal_short_continuous -->
Kont.

<!-- key: signal_short_dirac -->
Dirac

<!-- key: Concept, assumptions and equations -->
Konzept, Annahmen und Gleichungen

<!-- key: Guided experiments -->
Geführte Experimente

<!-- key: Expert settings -->
Experteneinstellungen

<!-- key: Use sliders for main parameters -->
Schieberegler für Hauptparameter

<!-- key: Flow & domain -->
Strömung und Modellgebiet

<!-- key: Transport & source -->
Transport und Quelle

<!-- key: Post-processing & observations -->
Auswertung und Beobachtungen

<!-- key: Hydraulic properties -->
Hydraulische Eigenschaften

<!-- key: Hydraulic conductivity K (m/s) -->
Hydraulische Leitfähigkeit K (m/s)

<!-- key: Effective porosity (-) -->
Effektive Porosität (-)

<!-- key: Specific storage Ss (1/m) -->
Spezifischer Speicherkoeffizient Ss (1/m)

<!-- key: Vertical / horizontal K -->
Vertikales / horizontales K

<!-- key: Boundary conditions -->
Randbedingungen

<!-- key: Specified head left (m) -->
Vorgegebene Potentialhöhe links (m)

<!-- key: Specified head right (m) -->
Vorgegebene Potentialhöhe rechts (m)

<!-- key: Transient flow experiment -->
Instationäres Strömungsexperiment

<!-- key: Right head after t = 0 (m) -->
Potentialhöhe rechts nach t = 0 (m)

<!-- key: Model extent and spatial discretization -->
Modellausdehnung und räumliche Diskretisierung

<!-- key: Model length in x-direction (m) -->
Modelllänge in x-Richtung (m)

<!-- key: Model width in y-direction (m) -->
Modellbreite in y-Richtung (m)

<!-- key: Aquifer thickness / top elevation (m) -->
Aquifermächtigkeit / Oberkante (m)

<!-- key: Define the grid by -->
Gitter definieren über

<!-- key: Number of cells -->
Zellanzahl

<!-- key: Cell width -->
Zellweite

<!-- key: Cells x -->
Zellen x

<!-- key: Cells y -->
Zellen y

<!-- key: Cell width x (m) -->
Zellweite x (m)

<!-- key: Cell width y (m) -->
Zellweite y (m)

<!-- key: Number of layers -->
Anzahl der Schichten

<!-- key: Numerical solution for flow -->
Numerische Lösung der Strömung

<!-- key: Head tolerance (m) -->
Toleranz der Potentialhöhe (m)

<!-- key: Flow residual tolerance (m³/day) -->
Toleranz des Fließresiduums (m³/Tag)

<!-- key: PCG outer iterations -->
Äußere PCG-Iterationen

<!-- key: PCG inner iterations -->
Innere PCG-Iterationen

<!-- key: Flow time steps (approximately total) -->
Strömungszeitschritte (ungefähre Gesamtzahl)

<!-- key: Hydrogeology and zonation -->
Hydrogeologie und Heterogenität

<!-- key: Hydrogeology preset -->
Hydrogeologische Voreinstellung

<!-- key: Number of zones -->
Anzahl der Zonen

<!-- key: Random seed -->
Zufallsstartwert

<!-- key: K range (m/s) -->
K-Bereich (m/s)

<!-- key: Ss range (1/m) -->
Ss-Bereich (1/m)

<!-- key: Porosity range (-) -->
Porositätsbereich (-)

<!-- key: Minimum -->
Minimum

<!-- key: Maximum -->
Maximum

<!-- key: Edit hydrogeological zones -->
Hydrogeologische Zonen bearbeiten

<!-- key: Zone name -->
Zonenname

<!-- key: First layer -->
Erste Schicht

<!-- key: Last layer -->
Letzte Schicht

<!-- key: Porosity -->
Porosität

<!-- key: Boundary conditions and source -->
Randbedingungen und Quelle

<!-- key: Input signal -->
Eingangssignal

<!-- key: Released mass (g) -->
Freigesetzte Masse (g)

<!-- key: Mass input rate (g/day) -->
Masseneintragsrate (g/Tag)

<!-- key: Pulse duration (days) -->
Pulsdauer (Tage)

<!-- key: Source x (m) -->
Quelle x (m)

<!-- key: Source y (m) -->
Quelle y (m)

<!-- key: Source cells x -->
Quellzellen x

<!-- key: Source cells y -->
Quellzellen y

<!-- key: Source spans all layers -->
Quelle über alle Schichten

<!-- key: Source layer (1 = top) -->
Quellschicht (1 = oben)

<!-- key: Transport parameters -->
Transportparameter

<!-- key: Dispersion -->
Dispersion

<!-- key: Longitudinal dispersivity (m) -->
Longitudinale Dispersivität (m)

<!-- key: Horizontal transverse / longitudinal -->
Horizontal transversal / longitudinal

<!-- key: Vertical transverse / longitudinal -->
Vertikal transversal / longitudinal

<!-- key: Temporal discretization -->
Zeitliche Diskretisierung

<!-- key: Transport duration (days) -->
Transportdauer (Tage)

<!-- key: DT0 · initial step (days; 0 = automatic) -->
DT0 · erster Zeitschritt (Tage; 0 = automatisch)

<!-- key: TTSMAX · maximum step (days; 0 = automatic) -->
TTSMAX · maximaler Zeitschritt (Tage; 0 = automatisch)

<!-- key: TTSMULT · step multiplier -->
TTSMULT · Zeitschrittfaktor

<!-- key: MXSTRN · maximum transport steps -->
MXSTRN · maximale Transportzeitschritte

<!-- key: Numerical solution for transport -->
Numerische Lösung des Transports

<!-- key: MT3D advection method -->
MT3D-Advektionsverfahren

<!-- key: MODPATH particle comparison -->
MODPATH-Partikelvergleich

<!-- key: PERCEL · Courant number -->
PERCEL · Courant-Zahl

<!-- key: CCLOSE · concentration tolerance -->
CCLOSE · Konzentrationstoleranz

<!-- key: Timeout per executable (seconds) -->
Zeitlimit je Programm (Sekunden)

<!-- key: Expert transport solver settings -->
Experteneinstellungen des Transportlösers

<!-- key: MXPART · maximum particles -->
MXPART · maximale Partikelanzahl

<!-- key: ITRACK · tracking algorithm -->
ITRACK · Verfolgungsalgorithmus

<!-- key: WD · concentration weighting -->
WD · Konzentrationsgewichtung

<!-- key: DCEPS · gradient threshold -->
DCEPS · Gradientenschwelle

<!-- key: NPLANE · particle planes -->
NPLANE · Partikelebenen

<!-- key: NPL · low-gradient particles -->
NPL · Partikel bei kleinem Gradienten

<!-- key: NPH · high-gradient particles -->
NPH · Partikel bei großem Gradienten

<!-- key: NPMIN · minimum particles/cell -->
NPMIN · minimale Partikel/Zelle

<!-- key: NPMAX · maximum particles/cell -->
NPMAX · maximale Partikel/Zelle

<!-- key: INTERP · interpolation -->
INTERP · Interpolation

<!-- key: NLSINK · sink planes -->
NLSINK · Senkenebenen

<!-- key: NPSINK · sink particles -->
NPSINK · Senkenpartikel

<!-- key: DCHMOC · HMOC threshold -->
DCHMOC · HMOC-Schwelle

<!-- key: MXITER · GCG outer iterations -->
MXITER · äußere GCG-Iterationen

<!-- key: ITER1 · GCG inner iterations -->
ITER1 · innere GCG-Iterationen

<!-- key: ISOLVE · preconditioner -->
ISOLVE · Vorkonditionierer

<!-- key: NCRS · cross-dispersion -->
NCRS · Kreuzdispersion

<!-- key: ACCL · relaxation -->
ACCL · Relaxation

<!-- key: IPRGCG · print interval -->
IPRGCG · Ausgabeintervall

<!-- key: MODPATH release settings -->
MODPATH-Freisetzungseinstellungen

<!-- key: Particles per source cell -->
Partikel je Quellzelle

<!-- key: Release batches (pulse / continuous) -->
Freisetzungsgruppen (Puls / kontinuierlich)

<!-- key: Observation points -->
Beobachtungspunkte

<!-- key: Number of observation points -->
Anzahl der Beobachtungspunkte

<!-- key: Output settings -->
Ausgabeeinstellungen

<!-- key: Saved transport times -->
Gespeicherte Transportzeitpunkte

<!-- key: Actual source footprint -->
Tatsächliche Quellabmessungen

<!-- key: Optional run label -->
Optionale Laufbezeichnung

<!-- key: Run model -->
Modell berechnen

<!-- key: Run diagnostic -->
Berechnungsdiagnose

<!-- key: More comparison metrics -->
Weitere Vergleichskennwerte

<!-- key: Displayed run -->
Angezeigter Lauf

<!-- key: Run to remove -->
Zu entfernender Lauf

<!-- key: Remove -->
Entfernen

<!-- key: Clear comparison runs -->
Vergleichsreihe leeren

<!-- key: Plume & sections -->
Stofffahne und Schnitte

<!-- key: Observation curves -->
Beobachtungskurven

<!-- key: Mass & diagnostics -->
Masse und Diagnose

<!-- key: Export -->
Export

<!-- key: Time (days) -->
Zeit (Tage)

<!-- key: Top-view layer -->
Schicht für Draufsicht

<!-- key: Layer {number} -->
Schicht {number}

<!-- key: Analytical reference -->
Analytische Referenz

<!-- key: Plot settings and section positions -->
Darstellung und Schnittpositionen

<!-- key: x-direction section · y (m) -->
Schnitt in x-Richtung · y (m)

<!-- key: y-direction section · x (m) -->
Schnitt in y-Richtung · x (m)

<!-- key: Colour fill -->
Farbfüllung

<!-- key: Contour lines -->
Isolinien

<!-- key: Log colours -->
Logarithmische Farbskala

<!-- key: Particle paths -->
Partikelbahnen

<!-- key: Opacity -->
Deckkraft

<!-- key: Compare runs in x / y sections -->
Läufe in x-/y-Schnitten vergleichen

<!-- key: Compare section profiles -->
Schnittprofile vergleichen

<!-- key: Runs for section comparison -->
Läufe für den Schnittvergleich

<!-- key: Also overlay top-view contours -->
Auch Isolinien in der Draufsicht überlagern

<!-- key: Download plume figure (PNG) -->
Stofffahnen-Abbildung herunterladen (PNG)

<!-- key: Runs in breakthrough comparison -->
Läufe für Durchbruchskurvenvergleich

<!-- key: Observation cells used by each run -->
Beobachtungszellen je Lauf

<!-- key: Download breakthrough curves (CSV) -->
Durchbruchskurven herunterladen (CSV)

<!-- key: Detailed mass-budget data -->
Detaillierte Massenbilanzdaten

<!-- key: Stored run configuration -->
Gespeicherte Laufkonfiguration

<!-- key: Download comparison table (CSV) -->
Vergleichstabelle herunterladen (CSV)

<!-- key: Download run configuration (JSON) -->
Laufkonfiguration herunterladen (JSON)

<!-- key: Prepare complete displayed-run archive -->
Vollständiges Archiv des angezeigten Laufs vorbereiten

<!-- key: Preparing archive… -->
Archiv wird vorbereitet…

<!-- key: Download run archive (ZIP) -->
Laufarchiv herunterladen (ZIP)

<!-- key: Run -->
Lauf

<!-- key: Method -->
Methode

<!-- key: Signal -->
Signal

<!-- key: Grid -->
Gitter

<!-- key: K zones -->
K-Zonen

<!-- key: Flow -->
Strömung

<!-- key: MB disc. (%) -->
MB-Abw. (%)

<!-- key: Flow disc. (%) -->
Fluss-Abw. (%)

<!-- key: MT3D (s) -->
MT3D (s)

<!-- key: MP7 (s) -->
MP7 (s)

<!-- key: Flow (s) -->
Strömung (s)

<!-- key: Total (s) -->
Gesamt (s)

<!-- key: Ref. L1 (%) -->
Ref. L1 (%)

<!-- key: Mass (g) -->
Masse (g)

<!-- key: Input (g) -->
Eintrag (g)

<!-- key: Min. C (g/m³) -->
Min. C (g/m³)

<!-- key: Neg. mass (g) -->
Neg. Masse (g)

<!-- key: Centroid x (m) -->
Schwerpunkt x (m)

<!-- key: Steps -->
Schritte

<!-- key: Source box (m) -->
Quellgröße (m)

<!-- key: End (d) -->
Ende (d)

<!-- key: Scenario -->
Szenario

<!-- key: Point -->
Punkt

<!-- key: Requested x -->
Gewünschtes x

<!-- key: Requested y -->
Gewünschtes y

<!-- key: Requested z -->
Gewünschtes z

<!-- key: Cell centre x -->
Zellmitte x

<!-- key: Cell centre y -->
Zellmitte y

<!-- key: Cell centre z -->
Zellmitte z

<!-- key: Layer -->
Schicht

<!-- key: Row -->
Zeile

<!-- key: Column -->
Spalte

<!-- key: Cumulative in (g) -->
Kumulativer Eintritt (g)

<!-- key: Cumulative out (g) -->
Kumulativer Austritt (g)

<!-- key: Sources (g) -->
Quellen (g)

<!-- key: Sinks (g) -->
Senken (g)

<!-- key: Fluid storage (g) -->
Wasserspeicherung (g)

<!-- key: Native resident mass (g) -->
Masse laut MT3D (g)

<!-- key: Alternative disc. (%) -->
Alternative Abw. (%)

<!-- key: Analytical reference requires homogeneous steady flow. -->
Die analytische Referenz erfordert homogene stationäre Strömung.

<!-- key: Source cells -->
Quellzellen

<!-- key: Specified head -->
Vorgegebene Potentialhöhe

<!-- key: Section locations -->
Schnittpositionen

<!-- key: Background flow -->
Hintergrundströmung

<!-- key: Model preview: grid, boundaries and source -->
Modellvorschau: Gitter, Randbedingungen und Quelle

<!-- key: Computed head contours -->
Berechnete Potentiallinien

<!-- key: Homogeneous steady head contours -->
Homogene stationäre Potentiallinien

<!-- key: Time (d) -->
Zeit (d)

<!-- key: Mass rate (g/d) -->
Masseneintragsrate (g/d)

<!-- key: Instantaneous mass (g) -->
Momentane Stoffmasse (g)

<!-- key: Dirac input (initial cell mass) -->
Dirac-Eingabe (anfängliche Zellmasse)

<!-- key: Finite pulse input -->
Endliche Pulseingabe

<!-- key: Continuous input -->
Kontinuierliche Eingabe

<!-- key: Concentration (g/m³) -->
Konzentration (g/m³)

<!-- key: Elevation z (m) -->
Höhe z (m)

<!-- key: MODPATH advection (slice) -->
MODPATH-Advektion (Schnitt)

<!-- key: Analytical -->
Analytisch

<!-- key: Analytical (active run) -->
Analytisch (aktiver Lauf)

<!-- key: Mass output unavailable -->
Massenausgabe nicht verfügbar

<!-- key: MT3D discrepancy (%) -->
MT3D-Abweichung (%)

<!-- key: Initial + injected mass (first run) -->
Anfangsmasse + Eintrag (erster Lauf)

<!-- key: Resident mass: grid sum and MT3D budget -->
Verbleibende Masse: Gittersumme und MT3D-Bilanz

<!-- key: Reported mass-balance closure -->
Ausgegebener Massenbilanzabschluss

<!-- key: Example: pulse plume after 600 days -->
Beispiel: Pulsfahne nach 600 Tagen

<!-- key: Example: observation P1 -->
Beispiel: Beobachtung P1

<!-- key: P1 · x (m) -->
P1 · x (m)

<!-- key: P1 · y (m) -->
P1 · y (m)

<!-- key: P1 · elevation z (m) -->
P1 · Höhe z (m)

<!-- key: P2 · x (m) -->
P2 · x (m)

<!-- key: P2 · y (m) -->
P2 · y (m)

<!-- key: P2 · elevation z (m) -->
P2 · Höhe z (m)

<!-- key: P3 · x (m) -->
P3 · x (m)

<!-- key: P3 · y (m) -->
P3 · y (m)

<!-- key: P3 · elevation z (m) -->
P3 · Höhe z (m)

<!-- key: P4 · x (m) -->
P4 · x (m)

<!-- key: P4 · y (m) -->
P4 · y (m)

<!-- key: P4 · elevation z (m) -->
P4 · Höhe z (m)

<!-- key: P5 · x (m) -->
P5 · x (m)

<!-- key: P5 · y (m) -->
P5 · y (m)

<!-- key: P5 · elevation z (m) -->
P5 · Höhe z (m)

<!-- key: fig_head -->
Vorgegebene Potentialhöhe: {head:g} m

<!-- key: fig_layers -->
{layers} Schicht(en); vertikaler Maßstab überhöht

<!-- key: fig_total -->
Gesamt: {mass:g} g

<!-- key: fig_initial -->
{mass:g} g bei t = 0

<!-- key: fig_xprofile -->
x-Profil bei y = {y:.3g} m

<!-- key: fig_yprofile -->
y-Profil bei x = {x:.3g} m

<!-- key: fig_section -->
{axis}–z-Schnitt bei {other} = {value:.3g} m

<!-- key: fig_title -->
{method} · t = {time:g} d · Schicht {layer} (z = {z:.3g} m)

<!-- key: fig_gridmass -->
{label}: Gittersumme

<!-- key: fig_nativemass -->
{label}: MT3D-Bilanz

<!-- key: fig_nodata -->
{label}: außerhalb des Gebiets — keine Daten

<!-- key: table_help_MB disc. (%) -->
Endgültige Massenbilanzabweichung laut MT3D.

<!-- key: table_help_Flow disc. (%) -->
Endgültige MODFLOW-Wasserbilanzabweichung.

<!-- key: table_help_MT3D (s) -->
Laufzeit des Transportprogramms.

<!-- key: table_help_MP7 (s) -->
MODPATH-Laufzeit; Partikel beschreiben nur Advektion.

<!-- key: table_help_Ref. L1 (%) -->
Porenvolumengewichteter absoluter Konzentrationsfehler bezogen auf die Referenzmasse.

<!-- key: table_help_Mass (g) -->
Endgültige gelöste Masse, integriert über das Konzentrationsgitter.

<!-- key: MT3DMS final mass discrepancy exceeds 1%; inspect method and transport time step settings. -->
Die endgültige MT3DMS-Massenabweichung übersteigt 1 %; Methode und Transportzeitschritte prüfen.

<!-- key: At least one MODFLOW water-budget discrepancy exceeds 0.1%. -->
Mindestens eine MODFLOW-Wasserbilanzabweichung übersteigt 0,1 %.

<!-- key: Negative concentrations occurred. They are retained in diagnostics and exports; central FD and particle methods can oscillate. -->
Negative Konzentrationen sind aufgetreten. Sie bleiben in Diagnose und Export erhalten; zentrale FD und Partikelverfahren können oszillieren.

<!-- key: Source coordinates must lie inside the domain. -->
Die Quellkoordinaten müssen innerhalb des Modellgebiets liegen.

<!-- key: This confined lab requires heads at or above aquifer top. -->
Dieses gespannte Modell erfordert Potentialhöhen auf oder oberhalb der Aquiferoberkante.

<!-- key: Pulse duration must be between zero and model duration. -->
Die Pulsdauer muss zwischen null und der Modelldauer liegen.

<!-- key: Observation point is outside the model. -->
Ein Beobachtungspunkt liegt außerhalb des Modells.

<!-- key: TVD requires PERCEL no greater than 1. -->
TVD erfordert PERCEL kleiner oder gleich 1.

<!-- key: language_fallback -->
Fehlende Übersetzungen verwenden den englischen Ersatztext.

<!-- key: preset_random -->
Zufällige stochastische Parameter

<!-- key: Random unit x (m) -->
Zufallseinheit x (m)

<!-- key: Random unit y (m) -->
Zufallseinheit y (m)

<!-- key: random_hint -->
Kleine Einheiten ergeben ein feines Zufallsmuster, größere Einheiten größere Bereiche. Für dieselbe physische Realisierung bei Netzverfeinerung Seed und Einheitengröße beibehalten.

<!-- key: Active cells -->
Aktive Zellen

<!-- key: table_help_Active cells -->
Alle nicht inaktiven Modellzellen einschließlich der Zellen mit vorgegebener Potentialhöhe.

<!-- key: Random field -->
Zufallsfeld

<!-- key: Comparison runs -->
Vergleichsläufe

<!-- key: discard_tags_hint -->
Ein Lauf wird durch × an seiner Markierung entfernt. Alle Markierungen löschen beginnt einen neuen Vergleich. Gewünschte Ergebnisse vorher exportieren.

<!-- key: Head contours -->
Potentiallinien

<!-- key: Computed head contours (m) -->
Berechnete Potentiallinien (m)

<!-- key: Head contours appear after running the model -->
Potentiallinien erscheinen nach der Modellberechnung

<!-- key: fig_background_k -->
Hintergrund-K = {k:.2e} m/s

<!-- key: fig_low_lens_k -->
Linse mit geringem K: K = {k:.2e} m/s

<!-- key: fig_high_channel_k -->
Kanal mit hohem K: K = {k:.2e} m/s

<!-- key: fig_low_barrier_k -->
Barriere mit geringem K: K = {k:.2e} m/s

<!-- key: Focus on plume -->
Auf die Fahne zoomen

<!-- key: Focus threshold (% of peak) -->
Schwelle (% des Maximums)

<!-- key: focus_hint -->
Bezug ist das aktuelle positive Maximum jeder dargestellten Fahne; auf jeder Seite kommen 20 % Rand hinzu. Sichtbare MODPATH-Bahnen bleiben enthalten. Ohne Fahne und Bahnen bleibt die Gesamtansicht erhalten. Nur die Draufsicht ändert sich.

<!-- key: Download plume figure (SVG) -->
Fahnenabbildung herunterladen (SVG)

<!-- key: steady -->
stationär

<!-- key: transient -->
instationär

<!-- key: fig_minimum -->
Numerisches Minimum: {minimum:.3g} g/m³

<!-- key: fig_minimum_log -->
Numerisches Minimum: {minimum:.3g} g/m³ (nichtpositive Werte in Logansicht verborgen)

<!-- key: The plume reaches an x specified-head boundary; enlarge the domain before treating the infinite-x analytical solution as a benchmark. -->
Die Fahne erreicht einen x-Festpotentialrand. Das Gebiet vor Nutzung der unendlichen analytischen Referenz vergrößern.

<!-- key: fig_reference_boundary -->
Analytische Genauigkeit deaktiviert: Einfluss der x-Ränder überschreitet die Schwelle von {tolerance_percent:.2g}%.

<!-- key: Low K lens -->
Linse mit kleinem K

<!-- key: High K channel -->
Rinne mit hohem K

<!-- key: Low K barrier -->
Teilweise Barriere mit kleinem K

<!-- key: Page width -->
Seitenbreite

<!-- key: width_1 -->
Schmal

<!-- key: width_2 -->
Kompakt

<!-- key: width_3 -->
Standard

<!-- key: width_4 -->
Breit

<!-- key: width_5 -->
Volle Breite

<!-- key: page_width_hint -->
Fünf Seitenbreiten von schmal bis zur vollen Breite. Standard entspricht der bisherigen Breite. Auf kleinen Bildschirmen wird die Breite angepasst.

<!-- key: Show model grid -->
Modellraster anzeigen

<!-- key: grid_hint -->
Dezente Zellgrenzen des angezeigten Laufs. Einschichtige Konzentrationsprofile zeigen vertikale Hilfslinien an den Zellrändern.

<!-- key: Plume-centered x/y -->
Fahnenzentrierte x/y

<!-- key: relative_hint -->
Nullpunkt ist der Schwerpunkt der positiven gelösten Masse in der angezeigten Schicht. Alle Überlagerungen nutzen denselben Ursprung. Eingabekoordinaten und Höhen bleiben absolut.

<!-- key: relative_mass_origin -->
Relativer Ursprung: x = {x:.2f} m; y = {y:.2f} m (Massenschwerpunkt der Fahne).

<!-- key: relative_source_origin -->
Keine positive Fahnenmasse in dieser Schicht: Ursprung im Rastermittelpunkt der Quelle, x = {x:.2f} m; y = {y:.2f} m.

<!-- key: fig_relative_xprofile -->
x-Profil bei y′ = {y:.3g} m

<!-- key: fig_relative_yprofile -->
y-Profil bei x′ = {x:.3g} m

<!-- key: fig_relative_section -->
{axis}–z-Schnitt bei {other}′ = {value:.3g} m
