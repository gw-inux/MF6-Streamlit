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
MT3D 2D/3D-Transportlabor · v{version} · Arbeitsversion für die begleitete Lehre · Entwickelt von Thomas Reimann · TU Dresden · The Groundwater Project

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

<!-- key: MODPATH particle count -->
MODPATH-Partikelzahl

<!-- key: particle_count_cell -->
Je Quellzelle

<!-- key: particle_count_total -->
Gesamte Quelle je Freisetzung

<!-- key: Particles in the whole source per release -->
Partikel in der gesamten Quelle je Freisetzung

<!-- key: particle_count_summary -->
{count} Partikel in {cells} Quellzellen × {groups} Freisetzungen = {total} Partikel.

<!-- key: expert_transport_hint -->
Alle Transportlöser-Einstellungen sind sichtbar. NPL / NPH und NPMIN / NPMAX steuern MOC-/HMOC-Partikel; MXPART begrenzt ihre Gesamtzahl. Hinweise erläutern den Methodenbezug. MODPATH nutzt separate Partikel.

<!-- key: Plume animation -->
Schadstofffahne animieren

<!-- key: Animation view -->
Animationsansicht

<!-- key: animation_2d -->
Draufsicht und Schnitte

<!-- key: animation_3d -->
3D-Konzentrationen in Zellmitten

<!-- key: Animation frames -->
Animationsbilder

<!-- key: Playback speed (frames/s) -->
Wiedergabegeschwindigkeit (Bilder/s)

<!-- key: Vertical exaggeration -->
Vertikale Überhöhung

<!-- key: Generate / refresh animation -->
Animation erstellen / aktualisieren

<!-- key: Generating animation… -->
Animation wird erstellt…

<!-- key: Download animation (HTML) -->
Animation herunterladen (HTML)

<!-- key: Play -->
Abspielen

<!-- key: Pause -->
Pause

<!-- key: Animation frame -->
Animationsbild

<!-- key: animation_layers_hint -->
Für die 3D-Ansicht in den Experteneinstellungen weitere Schichten ergänzen.

<!-- key: animation_hint -->
Verwendet gespeicherte Zeiten des angezeigten Laufs. Farben und Zoom der Animation können unten unabhängig gewählt werden; die Farbskala bleibt zeitlich konstant. Andere 2D-Darstellungsoptionen werden übernommen. Vergleiche und analytische Überlagerungen bleiben in statischen Diagrammen. Die fertige Animation erscheint unter den Einstellungen; die heruntergeladene HTML-Datei funktioniert offline.

<!-- key: animation_3d_hint -->
3D zeigt Zellmitten-Konzentrationen oberhalb der Schwelle bei fester Kamera. Maximal {maximum} gleichmäßig ausgewählte Zellen werden dargestellt; Berechnungen und Exporte enthalten alle Zellen. Partikel dienen dem Advektionsvergleich. Die Überhöhung betrifft nur die Darstellung.

<!-- key: animation_refresh_hint -->
Plot- oder Animationseinstellungen geändert. Zum Aktualisieren erneut erstellen.

<!-- key: animation_failed -->
Animation konnte nicht erstellt werden. Die Modellergebnisse bleiben erhalten.

<!-- key: animation_size_limit -->
Animation überschreitet 45 MiB. Weniger Bilder wählen und erneut erstellen.

<!-- key: help_s_percel -->
Maximaler advektiver Weg je Transportschritt in Zellbreiten. TVD erfordert ≤ 1.

<!-- key: help_s_mxpart -->
MOC/HMOC: Kapazität für alle bewegten Partikel, keine Partikelzahl je Zelle.

<!-- key: help_s_itrack -->
MOC/MMOC/HMOC: 1 = Euler, 2 = Runge–Kutta 4. Ordnung, 3 = hybrides Tracking.

<!-- key: help_s_wd -->
Charakteristikenverfahren: Konzentrationsgewichtung bei Operatoraufspaltung; 0,5–1.

<!-- key: help_s_dceps -->
MOC/HMOC: Schwelle des relativen Konzentrationsgradienten zwischen NPL- und NPH-Belegung.

<!-- key: help_s_nplane -->
MOC/HMOC: 0 = zufällige Anordnung; positiv = horizontale Partikelebenen je Zelle.

<!-- key: help_s_npl -->
MOC/HMOC: Startpartikel je Zelle mit Gradient ≤ DCEPS; null zulässig.

<!-- key: help_s_nph -->
MOC/HMOC: Startpartikel je Zelle mit hohem Gradienten. Feste Muster können die Zahl runden.

<!-- key: help_s_npmin -->
MOC/HMOC: Partikel ergänzen, wenn die Zellbelegung dieses Minimum unterschreitet.

<!-- key: help_s_npmax -->
MOC/HMOC: Bei Überschreitung wird die Zellbelegung durch NPH Partikel ersetzt.

<!-- key: help_s_interp -->
MMOC/HMOC: Konzentrationsinterpolation; nur 1 (linear) wird unterstützt.

<!-- key: help_s_nlsink -->
MMOC/HMOC-Senkenzellen: 0 = zufällige Anordnung; positiv = Partikelebenen.

<!-- key: help_s_npsink -->
MMOC/HMOC: Partikel zur Darstellung jeder Senkenzelle.

<!-- key: help_s_dchmoc -->
HMOC: Oberhalb dieser relativen Gradientenschwelle MOC, darunter MMOC.

<!-- key: help_s_mxiter -->
Maximale äußere GCG-Iterationen. Für dieses lineare konservative Modell genügt eine.

<!-- key: help_s_iter1 -->
Maximale innere GCG-Iterationen zur Lösung der Transportgleichungen.

<!-- key: help_s_isolve -->
GCG-Vorkonditionierer: 1 = Jacobi, 2 = SSOR, 3 = modifiziertes unvollständiges Cholesky (MIC).

<!-- key: help_s_ncrs -->
Dispersions-Kreuzterme: 0 = Näherung auf rechter Seite; 1 = vollständiger Tensor in der Matrix.

<!-- key: help_s_accl -->
Relaxationsfaktor, nur für SSOR (ISOLVE = 2).

<!-- key: help_s_cclose -->
Relative Konzentrationsänderung für GCG-Konvergenz. Kleinere Werte verschärfen das Kriterium.

<!-- key: help_s_iprgcg -->
Konzentrationsänderungen alle N GCG-Iterationen ausgeben; 0 am Ende jeder Stressperiode.

<!-- key: help_s_dt0 -->
Anfängliche Transportschrittlänge in Tagen; 0 lässt MT3D automatisch wählen.

<!-- key: help_s_ttsmult -->
Schrittmultiplikator für impliziten FD-Transport; Charakteristikenverfahren und TVD verwenden ihn nicht.

<!-- key: help_s_ttsmax -->
Maximale Schrittlänge in Tagen bei TTSMULT > 1; 0 nutzt die automatische Begrenzung.

<!-- key: help_s_mxstrn -->
Maximale Transportschritte je Strömungszeitschritt; Erreichen der Grenze kann den Lauf stoppen.

<!-- key: help_s_timeout -->
Rechenzeitlimit je Programm. Größere Partikelzahlen benötigen gegebenenfalls mehr Zeit.

<!-- key: help_s_hclose -->
PCG-Konvergenztoleranz der Potenzialhöhenänderung in Metern.

<!-- key: help_s_rclose -->
PCG-Konvergenztoleranz des Strömungsresiduums in m³/Tag.

<!-- key: help_s_flow_mxiter -->
Maximale äußere Iterationen des MODFLOW-PCG-Strömungslösers.

<!-- key: help_s_flow_iter1 -->
Maximale innere PCG-Iterationen je äußerer Strömungsiteration.

<!-- key: help_particle_count_mode -->
Partikel je Quellzelle oder eine genaue Gesamtzahl für die Quelle je Freisetzungszeit wählen.

<!-- key: help_particles_per_cell -->
Partikel werden je Freisetzung gleichmäßig in jeder Quellzelle verteilt. Gilt nur für MODPATH, nicht MOC.

<!-- key: help_total_source_particles -->
Genaue Anzahl je Freisetzung für alle Quellzellen; mindestens eine je Zelle. Zellbelegungen unterscheiden sich höchstens um eins; Massegewichte folgen dem Porenvolumen.

<!-- key: help_release_groups -->
Gleichmäßige Freisetzungen zur Intervallmitte nähern Puls/Dauereintrag an. Mehr Gruppen verfeinern den Zeitverlauf; Dirac nutzt eine Freisetzung bei t = 0.

<!-- key: help_run_label -->
Leer lassen für den vorgeschlagenen Namen. Eigener Text ersetzt Methode/Signal; Nummerierung und Heterogenitätszusatz bleiben automatisch.

<!-- key: help_expert -->
Schichtsteuerung und alle unterstützten Strömungs-/Transportlöserparameter anzeigen. Verborgene Werte bleiben erhalten.

<!-- key: help_sliders -->
Zwischen Zahlenfeldern und Schiebereglern wechseln, ohne Modellwerte zu ändern.

<!-- key: help_extent -->
Physische Modellausdehnung in Metern. Eine Änderung beginnt eine neue Vergleichsserie.

<!-- key: help_thickness -->
Mächtigkeit des gespannten Aquifers; Sohle bei 0 m, Oberkante auf diesem Wert. Schichten teilen die Mächtigkeit gleichmäßig.

<!-- key: help_grid_mode -->
Zellzahl oder maximale Zellbreiten vorgeben. Bei Breitenvorgabe wird die Zellzahl aufgerundet; die Ausdehnung bleibt gleich.

<!-- key: help_grid_count -->
Anzahl gleich großer Zellen in dieser Richtung. Verfeinerung erhält frühere Vergleichsläufe.

<!-- key: help_cell_width -->
Gewünschte maximale Zellbreite in Metern. Die Vorschau zeigt die tatsächliche gleichmäßige Breite.

<!-- key: help_nlay -->
Eine Schicht ergibt ein Draufsichtmodell; mehrere gleich mächtige Schichten erlauben vertikalen Transport und 3D-Ansichten.

<!-- key: help_k -->
Horizontale Hintergrund-Durchlässigkeit. Eingabe in m/s; Umrechnung in m/Tag erfolgt intern.

<!-- key: help_porosity -->
Mobiler Porenvolumenanteil; bestimmt Abstandsgeschwindigkeit und gelöste Massenspeicherung.

<!-- key: help_ss -->
Wasserabgabe je Aquifervolumen und Potenzialhöhenabsenkung (1/m). In dieser stationären Oberfläche ist kein Speicherterm aktiv.

<!-- key: help_kv_ratio -->
Vertikale geteilt durch horizontale Durchlässigkeit, angewendet in jeder Schicht.

<!-- key: help_zones_preset -->
Homogene Eigenschaften, reproduzierbares Zufallsfeld oder definierte Linse/Kanal/Barriere wählen.

<!-- key: help_zone_seed -->
Startwert des Zufallsfelds. Gleicher Wert und gleiche Einstellungen reproduzieren das räumliche Muster.

<!-- key: help_random_unit -->
Physische Größe zufälliger Blöcke in dieser Richtung, unabhängig von der numerischen Gitterverfeinerung.

<!-- key: help_random_k -->
Grenzen zufälliger Durchlässigkeit; gleichmäßige Ziehung im logarithmischen Raum (m/s).

<!-- key: help_random_ss -->
Grenzen logarithmisch gleichverteilter spezifischer Speicherung (1/m). Im Modell gespeichert, bei stationärer Strömung inaktiv.

<!-- key: help_random_por -->
Grenzen gleichverteilter effektiver Porosität; Werte müssen zwischen null und eins liegen.

<!-- key: help_head -->
Vorgegebene Potenzialhöhe dieser Randspalte. Links muss höher als rechts sein; beide mindestens auf Aquiferoberkante.

<!-- key: help_duration -->
Gesamte simulierte Transportzeit in Tagen, unabhängig von der Animationsgeschwindigkeit.

<!-- key: help_dispersion -->
Mechanische Ausbreitung proportional zur Abstandsgeschwindigkeit einschalten. Ausgeschaltet bleiben Advektion und numerische Dispersion.

<!-- key: help_al -->
Longitudinale Dispersivität entlang der Strömung in Metern; zugehöriger Dispersionskoeffizient = αL × Geschwindigkeit.

<!-- key: help_trpt -->
Horizontale transversale geteilt durch longitudinale Dispersivität: αTH/αL.

<!-- key: help_trpv -->
Vertikale transversale geteilt durch longitudinale Dispersivität: αTV/αL. Bei mehreren Schichten relevant.

<!-- key: help_source_kind -->
Dirac: anfängliche gelöste Masse bei t = 0. Puls: konstanter Eintrag bis Pulsende. Kontinuierlich: konstanter Eintrag während des gesamten Laufs.

<!-- key: help_source_mass -->
Anfängliche gelöste Gesamtmasse im Porenvolumen der Quelle (Gramm).

<!-- key: help_mass_rate -->
Gesamter Stoffeintrag (g/Tag), verteilt nach Quell-Porenvolumen. Es wird kein Wasser injiziert.

<!-- key: help_pulse_duration -->
Nach dieser Zeit (Tage) endet der Eintrag; sie muss kürzer als die gesamte Transportdauer sein.

<!-- key: help_source_position -->
Absolute Quellmittelpunkt-Koordinate in Metern, einer Modellzelle zugeordnet. Randspalten mit vorgegebenem Potenzial sind ausgeschlossen.

<!-- key: help_source_cells -->
Quellzellenzahl in dieser Richtung. Tatsächliche Ausdehnung in Vorschau prüfen; Geometrieänderung startet neue Serie.

<!-- key: help_source_all_layers -->
Quelle über alle Schichten verteilen; sonst nur die ausgewählte Schicht verwenden.

<!-- key: help_src_layer -->
Schicht mit Stoffquelle; 1 ist die oberste Schicht.

<!-- key: help_method -->
MT3D-Advektion wählen: FD up/zentral, TVD, vorwärts MOC, rückwärts MMOC oder hybrid HMOC. Unabhängig von MODPATH.

<!-- key: help_track_particles -->
MODPATH 7 im berechneten Strömungsfeld ausführen. Partikel zeigen nur Advektion; MODPATH berechnet keine Dispersion oder Konzentrationen.

<!-- key: help_observation -->
Absolute Beobachtungskoordinate in Metern. Konzentration wird aus der zugehörigen Zelle entnommen, nicht interpoliert.

<!-- key: help_nobs -->
Konzentrationen an einem bis fünf Beobachtungspunkten anhand gespeicherter Läufe vergleichen.

<!-- key: help_outputs -->
Gespeicherte Transportzeiten einschließlich t = 0; Pulsende wird zusätzlich gespeichert. Mehr Ausgaben verfeinern Animation und Kurven, nicht die Solver-Zeitschrittgenauigkeit.

<!-- key: help_length -->
Physische Modellausdehnung in Metern. Eine Änderung beginnt eine neue Vergleichsserie.

<!-- key: help_width -->
Physische Modellausdehnung in Metern. Eine Änderung beginnt eine neue Vergleichsserie.

<!-- key: help_ncol -->
Anzahl gleich großer Zellen in dieser Richtung. Verfeinerung erhält frühere Vergleichsläufe.

<!-- key: help_nrow -->
Anzahl gleich großer Zellen in dieser Richtung. Verfeinerung erhält frühere Vergleichsläufe.

<!-- key: help_cell_x -->
Gewünschte maximale Zellbreite in Metern. Die Vorschau zeigt die tatsächliche gleichmäßige Breite.

<!-- key: help_cell_y -->
Gewünschte maximale Zellbreite in Metern. Die Vorschau zeigt die tatsächliche gleichmäßige Breite.

<!-- key: help_random_unit_x -->
Physische Größe zufälliger Blöcke in dieser Richtung, unabhängig von der numerischen Gitterverfeinerung.

<!-- key: help_random_unit_y -->
Physische Größe zufälliger Blöcke in dieser Richtung, unabhängig von der numerischen Gitterverfeinerung.

<!-- key: help_zone_k_min -->
Grenzen zufälliger Durchlässigkeit; gleichmäßige Ziehung im logarithmischen Raum (m/s).

<!-- key: help_zone_k_max -->
Grenzen zufälliger Durchlässigkeit; gleichmäßige Ziehung im logarithmischen Raum (m/s).

<!-- key: help_zone_ss_min -->
Grenzen logarithmisch gleichverteilter spezifischer Speicherung (1/m). Im Modell gespeichert, bei stationärer Strömung inaktiv.

<!-- key: help_zone_ss_max -->
Grenzen logarithmisch gleichverteilter spezifischer Speicherung (1/m). Im Modell gespeichert, bei stationärer Strömung inaktiv.

<!-- key: help_zone_por_min -->
Grenzen gleichverteilter effektiver Porosität; Werte müssen zwischen null und eins liegen.

<!-- key: help_zone_por_max -->
Grenzen gleichverteilter effektiver Porosität; Werte müssen zwischen null und eins liegen.

<!-- key: help_head_left -->
Vorgegebene Potenzialhöhe dieser Randspalte. Links muss höher als rechts sein; beide mindestens auf Aquiferoberkante.

<!-- key: help_head_right -->
Vorgegebene Potenzialhöhe dieser Randspalte. Links muss höher als rechts sein; beide mindestens auf Aquiferoberkante.

<!-- key: help_src_x -->
Absolute Quellmittelpunkt-Koordinate in Metern, einer Modellzelle zugeordnet. Randspalten mit vorgegebenem Potenzial sind ausgeschlossen.

<!-- key: help_src_y -->
Absolute Quellmittelpunkt-Koordinate in Metern, einer Modellzelle zugeordnet. Randspalten mit vorgegebenem Potenzial sind ausgeschlossen.

<!-- key: help_src_ncol -->
Quellzellenzahl in dieser Richtung. Tatsächliche Ausdehnung in Vorschau prüfen; Geometrieänderung startet neue Serie.

<!-- key: help_src_nrow -->
Quellzellenzahl in dieser Richtung. Tatsächliche Ausdehnung in Vorschau prüfen; Geometrieänderung startet neue Serie.

<!-- key: help_animation_mode -->
2D animiert Draufsicht und Profile/Schnitte. 3D zeigt berechnete Zellmitten-Konzentrationen aus fester Perspektive und benötigt mehrere Schichten.

<!-- key: help_animation_frames -->
Bis zu 80 gespeicherte Zustände einschließlich Anfang und Ende wählen. Keine zeitliche Konzentrationsinterpolation.

<!-- key: help_animation_fps -->
Bilder je realer Sekunde. Jedes Bild zeigt die tatsächliche Modellzeit; Wiedergabe verändert das Modell nicht.

<!-- key: help_animation_exaggeration -->
Dargestellte Höhe des 3D-Gebiets skalieren. Höhenkoordinaten und Berechnungen bleiben unverändert.

<!-- key: help_generate_animation -->
Gespeicherte Ergebnisse erst auf Anforderung rendern. Nach Ansichtänderung neu erstellen; kein neuer Modelllauf.

<!-- key: help_view_time -->
Gespeicherte Transportzeit wählen; kein neuer Modelllauf.

<!-- key: help_view_layer -->
In Draufsicht gezeigte Schicht; 1 ist oben.

<!-- key: help_section -->
Absolute Schnittposition in Metern, aus zugehöriger Zeile/Spalte. Relative Achsen verschieben den Schnitt nicht.

<!-- key: help_fill -->
Modellzellen nach Konzentrationsfarbskala füllen; Konzentration null bleibt weiß.

<!-- key: help_lines -->
Konzentrations-Isolinien über der Farbfüllung anzeigen.

<!-- key: help_show_heads -->
Dünne berechnete Potenzialhöhenlinien mit Beschriftung in Metern anzeigen.

<!-- key: help_log -->
Logarithmische Farben für positive Konzentrationen. Nichtpositive Zellen werden nur in dieser Darstellung ausgeblendet.

<!-- key: help_particle_paths -->
MODPATH-Positionen und dünne Bahnen bis zur gewählten Zeit anzeigen. Maximal 120 Bahnen dargestellt; Exporte enthalten alle Partikel.

<!-- key: help_opacity -->
Deckkraft der Farbfüllung: 1 ist undurchsichtig; kleinere Werte zeigen den Hintergrund.

<!-- key: help_focus_plume -->
Auf positive Fahne und gezeigte MODPATH-Bahnen mit Rand zoomen. Animation nutzt ein festes Fenster über alle gewählten Zeiten.

<!-- key: help_focus_threshold -->
Statischer Fokus: Prozent des jeweiligen Fahnenmaximums. In 3D-Animation: Prozent des maximalen Betrags der festen Farbskala zur Zellauswahl.

<!-- key: help_analytical -->
Mit homogener stationärer analytischer Referenz vergleichen. Heterogene oder instationäre Strömung liegt außerhalb ihrer Annahmen.

<!-- key: help_compare -->
Gespeicherte Läufe zur nächstverfügbaren Zeit an den Schnittpositionen des angezeigten Laufs vergleichen.

<!-- key: help_analytic_on -->
Mit homogener stationärer analytischer Referenz vergleichen. Heterogene oder instationäre Strömung liegt außerhalb ihrer Annahmen.

<!-- key: help_btc_analytical -->
Mit homogener stationärer analytischer Referenz vergleichen. Heterogene oder instationäre Strömung liegt außerhalb ihrer Annahmen.

<!-- key: help_compare_sections -->
Gespeicherte Läufe zur nächstverfügbaren Zeit an den Schnittpositionen des angezeigten Laufs vergleichen.

<!-- key: help_overlay_runs -->
Gespeicherte Läufe zur nächstverfügbaren Zeit an den Schnittpositionen des angezeigten Laufs vergleichen.

<!-- key: help_compare_top -->
Gespeicherte Läufe zur nächstverfügbaren Zeit an den Schnittpositionen des angezeigten Laufs vergleichen.

<!-- key: help_btc_runs -->
Konzentrationen an einem bis fünf Beobachtungspunkten anhand gespeicherter Läufe vergleichen.

<!-- key: Animation settings -->
Animationseinstellungen

<!-- key: Animation colour scale -->
Farbskala der Animation

<!-- key: animation_colour_enhanced -->
Kleine Konzentrationen verstärkt (feste Skala)

<!-- key: animation_colour_linear -->
Linear (feste Skala)

<!-- key: animation_colour_log -->
Logarithmisch (feste Skala)

<!-- key: help_animation_colour -->
Die verstärkte Darstellung verwendet eine Potenzabbildung (Exponent 0,35), um kleine Konzentrationen sichtbar zu machen. Alle Bilder haben dieselben physikalischen Konzentrationsgrenzen; Null bleibt weiß. Lineare und verstärkte Skalen zeigen auch negative numerische Werte; logarithmische Farben blenden nichtpositive Werte aus. Die berechneten Daten bleiben unverändert.

<!-- key: Zoom animation to plume -->
Animation auf die Schadstofffahne zoomen

<!-- key: help_animation_focus -->
Ein fester Ausschnitt umfasst die positive Schadstofffahne und dargestellte MODPATH-Pfade über alle ausgewählten Zeiten, mit 20 % Rand. Unabhängig vom Zoom des statischen Diagramms. Ausschalten zeigt das gesamte Modellgebiet. Für 2D und 3D verfügbar.

<!-- key: Plume threshold (% of peak) -->
Schwellenwert der Fahne (% des Maximums)

<!-- key: help_animation_threshold -->
Der Zoom umfasst Konzentrationen oberhalb dieses Anteils des positiven Maximums jedes Bildes. In 3D legt dieser Wert zusätzlich die Sichtbarkeitsgrenze der Zellen als Anteil der maximalen absoluten Konzentration der festen Skala fest. Standard: 0,1 %. Betrifft nur die Darstellung.

<!-- key: animation_progress -->
Animation wird erstellt… {percent} %

<!-- key: MODPATH settings -->
MODPATH-Einstellungen

<!-- key: expert_transport_location_hint -->
Die MT3D-Expertenparameter befinden sich im separaten Aufklappbereich **Experteneinstellungen des Transportlösers** direkt darunter. Die MODPATH-Einstellungen folgen anschließend.
