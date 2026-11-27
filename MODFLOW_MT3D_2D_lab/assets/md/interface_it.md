<!-- key: title -->
MT3D – Laboratorio di trasporto 2D/3D

<!-- key: intro_caption -->
Illustrazione introduttiva: esempio di pennacchio e curva di arrivo, indipendente dagli input attuali del modello.

<!-- key: Model & run -->
1 · Modello ed esecuzione

<!-- key: Results & method comparison -->
2 · Risultati e confronto dei metodi

<!-- key: series_reset -->
Il segnale o la geometria del dominio/della sorgente è cambiato: inizia una nuova serie. Le esecuzioni precedenti sono state eliminate.

<!-- key: grid_summary -->
Griglia: {nx} × {ny} × {nz} celle. Passo effettivo: Δx = {dx:.3f} m; Δy = {dy:.3f} m; Δz = {dz:.3f} m.

<!-- key: velocity_summary -->
Velocità interstiziale omogenea di riferimento: {velocity:.4f} m/giorno.

<!-- key: source_bounds -->
x = {x0:.2f}–{x1:.2f} m; y = {y0:.2f}–{y1:.2f} m; z = {z0:.2f}–{z1:.2f} m.

<!-- key: source_snap_hint -->
La sorgente occupa le celle selezionate. La risoluzione può modificarne le dimensioni effettive. L'input del passo conserva l'estensione totale e riporta il passo uniforme reale.

<!-- key: input_error -->
Correggere i parametri segnalati prima dell'esecuzione.

<!-- key: missing_executables -->
Programmi mancanti: {names}. Inserire eseguibili compatibili in `bin/` dell'app o del repository. In locale: `python setup_executables.py`.

<!-- key: label_placeholder -->
Automatico: 01 TVD / Pulse (eterogeneo: / het.)

<!-- key: history_full -->
Sono memorizzate dieci esecuzioni. Eliminarne una o svuotare la serie per continuare.

<!-- key: running -->
Esecuzione di MODFLOW, MT3D e MODPATH opzionale…

<!-- key: run_success -->
Esecuzione completata. È visualizzato l'ultimo risultato.

<!-- key: run_failed -->
Questa esecuzione non è stata completata né aggiunta al confronto.

<!-- key: changed_source_footprint -->
Il raffinamento ha modificato l'estensione effettiva della sorgente. Verificarla nella tabella estesa.

<!-- key: nearest_time -->
{name}: tempo salvato più vicino {time:.3f} giorni (esecuzione visualizzata: {target:.3f} giorni).

<!-- key: no_comparison_time -->
{name}: nessun output a {time:.3f} giorni; omesso.

<!-- key: evaluating_reference -->
Calcolo del riferimento analitico…

<!-- key: export_hint -->
L'archivio contiene input, log, concentrazioni, carichi, bilanci e particelle, inclusi gli arrivi.

<!-- key: no_runs -->
Eseguire l'esperimento iniziale a impulso per vedere pennacchio, profili, curve di arrivo e confronto dei metodi.

<!-- key: footer -->
MT3D 2D/3D · v{version} · Versione di lavoro per lezioni dal vivo · Sviluppato da Thomas Reimann · TU Dresden · The Groundwater Project

<!-- key: transient_hint -->
Il campo iniziale si equilibra; il carico a destra cambia a t = 0.

<!-- key: expert_flow_hint -->
Attivare le impostazioni esperte per modificare tolleranze e iterazioni del solutore di flusso.

<!-- key: stochastic_hint -->
Seme fisso: zone riproducibili. K e Ss sono uniformi in scala logaritmica; la porosità è uniforme. Il raffinamento conserva la realizzazione.

<!-- key: zones_hint -->
I rettangoli selezionano i centri delle celle; le righe successive prevalgono. Gli strati iniziano da 1.

<!-- key: observation_hint -->
Le osservazioni usano la cella contenente il punto. Le posizioni si modificano senza rieseguire i modelli salvati.

<!-- key: output_hint -->
Include t = 0 e il tempo finale. Controlla le concentrazioni salvate per grafici ed esportazione.

<!-- key: preset_homogeneous -->
Omogeneo

<!-- key: preset_lens -->
Lente a K bassa

<!-- key: preset_channel -->
Canale a K elevata

<!-- key: preset_barrier -->
Barriera parziale a K bassa

<!-- key: preset_stochastic -->
Zonazione stocastica

<!-- key: preset_custom -->
Rettangoli personalizzati

<!-- key: preset_hint_lens -->
Lente centrale: K = 0,01 × K di fondo; intero spessore.

<!-- key: preset_hint_channel -->
Canale longitudinale: K = 10 × K di fondo; intero spessore.

<!-- key: preset_hint_barrier -->
Barriera trasversale parziale: K = 0,01 × K di fondo; rimane un passaggio laterale.

<!-- key: signal_pulse -->
Impulso / ingresso rettangolare

<!-- key: signal_continuous -->
Ingresso continuo

<!-- key: signal_dirac -->
Dirac / rilascio istantaneo

<!-- key: signal_short_pulse -->
Impulso

<!-- key: signal_short_continuous -->
Cont.

<!-- key: signal_short_dirac -->
Dirac

<!-- key: Concept, assumptions and equations -->
Concetto, ipotesi ed equazioni

<!-- key: Guided experiments -->
Esperimenti guidati

<!-- key: Expert settings -->
Impostazioni esperte

<!-- key: Use sliders for main parameters -->
Cursori per i parametri principali

<!-- key: Flow & domain -->
Flusso e dominio

<!-- key: Transport & source -->
Trasporto e sorgente

<!-- key: Post-processing & observations -->
Post-elaborazione e osservazioni

<!-- key: Hydraulic properties -->
Proprietà idrauliche

<!-- key: Hydraulic conductivity K (m/s) -->
Conducibilità idraulica K (m/s)

<!-- key: Effective porosity (-) -->
Porosità efficace (-)

<!-- key: Specific storage Ss (1/m) -->
Immagazzinamento specifico Ss (1/m)

<!-- key: Vertical / horizontal K -->
K verticale / orizzontale

<!-- key: Boundary conditions -->
Condizioni al contorno

<!-- key: Specified head left (m) -->
Carico imposto a sinistra (m)

<!-- key: Specified head right (m) -->
Carico imposto a destra (m)

<!-- key: Transient flow experiment -->
Flusso transitorio

<!-- key: Right head after t = 0 (m) -->
Carico destro dopo t = 0 (m)

<!-- key: Model extent and spatial discretization -->
Estensione e discretizzazione spaziale

<!-- key: Model length in x-direction (m) -->
Lunghezza lungo x (m)

<!-- key: Model width in y-direction (m) -->
Larghezza lungo y (m)

<!-- key: Aquifer thickness / top elevation (m) -->
Spessore / quota del tetto (m)

<!-- key: Define the grid by -->
Definire la griglia tramite

<!-- key: Number of cells -->
Numero di celle

<!-- key: Cell width -->
Dimensione della cella

<!-- key: Cells x -->
Celle x

<!-- key: Cells y -->
Celle y

<!-- key: Cell width x (m) -->
Passo x (m)

<!-- key: Cell width y (m) -->
Passo y (m)

<!-- key: Number of layers -->
Numero di strati

<!-- key: Numerical solution for flow -->
Soluzione numerica del flusso

<!-- key: Head tolerance (m) -->
Tolleranza del carico (m)

<!-- key: Flow residual tolerance (m³/day) -->
Tolleranza del residuo (m³/giorno)

<!-- key: PCG outer iterations -->
Iterazioni esterne PCG

<!-- key: PCG inner iterations -->
Iterazioni interne PCG

<!-- key: Flow time steps (approximately total) -->
Passi di flusso (totale approssimativo)

<!-- key: Hydrogeology and zonation -->
Idrogeologia ed eterogeneità

<!-- key: Hydrogeology preset -->
Scenario idrogeologico

<!-- key: Number of zones -->
Numero di zone

<!-- key: Random seed -->
Seme casuale

<!-- key: K range (m/s) -->
Intervallo K (m/s)

<!-- key: Ss range (1/m) -->
Intervallo Ss (1/m)

<!-- key: Porosity range (-) -->
Intervallo di porosità (-)

<!-- key: Minimum -->
Minimo

<!-- key: Maximum -->
Massimo

<!-- key: Edit hydrogeological zones -->
Modificare le zone

<!-- key: Zone name -->
Nome della zona

<!-- key: First layer -->
Primo strato

<!-- key: Last layer -->
Ultimo strato

<!-- key: Porosity -->
Porosità

<!-- key: Boundary conditions and source -->
Condizioni al contorno e sorgente

<!-- key: Input signal -->
Segnale di ingresso

<!-- key: Released mass (g) -->
Massa rilasciata (g)

<!-- key: Mass input rate (g/day) -->
Portata massica (g/giorno)

<!-- key: Pulse duration (days) -->
Durata dell'impulso (giorni)

<!-- key: Source x (m) -->
Sorgente x (m)

<!-- key: Source y (m) -->
Sorgente y (m)

<!-- key: Source cells x -->
Celle sorgente x

<!-- key: Source cells y -->
Celle sorgente y

<!-- key: Source spans all layers -->
Sorgente in tutti gli strati

<!-- key: Source layer (1 = top) -->
Strato sorgente (1 = superiore)

<!-- key: Transport parameters -->
Parametri di trasporto

<!-- key: Dispersion -->
Dispersione

<!-- key: Longitudinal dispersivity (m) -->
Dispersività longitudinale (m)

<!-- key: Horizontal transverse / longitudinal -->
Trasversale orizzontale / longitudinale

<!-- key: Vertical transverse / longitudinal -->
Trasversale verticale / longitudinale

<!-- key: Temporal discretization -->
Discretizzazione temporale

<!-- key: Transport duration (days) -->
Durata del trasporto (giorni)

<!-- key: DT0 · initial step (days; 0 = automatic) -->
DT0 · passo iniziale (giorni; 0 = auto)

<!-- key: TTSMAX · maximum step (days; 0 = automatic) -->
TTSMAX · passo massimo (giorni; 0 = auto)

<!-- key: TTSMULT · step multiplier -->
TTSMULT · moltiplicatore del passo

<!-- key: MXSTRN · maximum transport steps -->
MXSTRN · massimo passi di trasporto

<!-- key: Numerical solution for transport -->
Soluzione numerica del trasporto

<!-- key: MT3D advection method -->
Metodo di advezione MT3D

<!-- key: MODPATH particle comparison -->
Confronto con particelle MODPATH

<!-- key: PERCEL · Courant number -->
PERCEL · numero di Courant

<!-- key: CCLOSE · concentration tolerance -->
CCLOSE · tolleranza di concentrazione

<!-- key: Timeout per executable (seconds) -->
Tempo limite per programma (s)

<!-- key: Expert transport solver settings -->
Impostazioni esperte del solutore di trasporto

<!-- key: MXPART · maximum particles -->
MXPART · massimo particelle

<!-- key: ITRACK · tracking algorithm -->
ITRACK · algoritmo di tracciamento

<!-- key: WD · concentration weighting -->
WD · ponderazione della concentrazione

<!-- key: DCEPS · gradient threshold -->
DCEPS · soglia del gradiente

<!-- key: NPLANE · particle planes -->
NPLANE · piani di particelle

<!-- key: NPL · low-gradient particles -->
NPL · particelle a basso gradiente

<!-- key: NPH · high-gradient particles -->
NPH · particelle ad alto gradiente

<!-- key: NPMIN · minimum particles/cell -->
NPMIN · particelle min./cella

<!-- key: NPMAX · maximum particles/cell -->
NPMAX · particelle max./cella

<!-- key: INTERP · interpolation -->
INTERP · interpolazione

<!-- key: NLSINK · sink planes -->
NLSINK · piani dei pozzi di estrazione

<!-- key: NPSINK · sink particles -->
NPSINK · particelle dei pozzi di estrazione

<!-- key: DCHMOC · HMOC threshold -->
DCHMOC · soglia HMOC

<!-- key: MXITER · GCG outer iterations -->
MXITER · iterazioni esterne GCG

<!-- key: ITER1 · GCG inner iterations -->
ITER1 · iterazioni interne GCG

<!-- key: ISOLVE · preconditioner -->
ISOLVE · precondizionatore

<!-- key: NCRS · cross-dispersion -->
NCRS · dispersione incrociata

<!-- key: ACCL · relaxation -->
ACCL · rilassamento

<!-- key: IPRGCG · print interval -->
IPRGCG · intervallo di stampa

<!-- key: MODPATH release settings -->
Rilascio delle particelle MODPATH

<!-- key: Particles per source cell -->
Particelle per cella sorgente

<!-- key: Release batches (pulse / continuous) -->
Gruppi di rilascio (impulso / continuo)

<!-- key: Observation points -->
Punti di osservazione

<!-- key: Number of observation points -->
Numero di punti di osservazione

<!-- key: Output settings -->
Impostazioni di output

<!-- key: Saved transport times -->
Tempi di trasporto salvati

<!-- key: Actual source footprint -->
Estensione effettiva della sorgente

<!-- key: Optional run label -->
Nome facoltativo dell'esecuzione

<!-- key: Run model -->
Esegui modello

<!-- key: Run diagnostic -->
Diagnostica dell'esecuzione

<!-- key: More comparison metrics -->
Altre metriche di confronto

<!-- key: Displayed run -->
Esecuzione visualizzata

<!-- key: Run to remove -->
Esecuzione da eliminare

<!-- key: Remove -->
Elimina

<!-- key: Clear comparison runs -->
Cancella esecuzioni confrontate

<!-- key: Plume & sections -->
Pennacchio e sezioni

<!-- key: Observation curves -->
Curve di osservazione

<!-- key: Mass & diagnostics -->
Massa e diagnostica

<!-- key: Export -->
Esporta

<!-- key: Time (days) -->
Tempo (giorni)

<!-- key: Top-view layer -->
Strato in pianta

<!-- key: Layer {number} -->
Strato {number}

<!-- key: Analytical reference -->
Riferimento analitico

<!-- key: Plot settings and section positions -->
Grafici e posizioni delle sezioni

<!-- key: x-direction section · y (m) -->
Sezione lungo x · y (m)

<!-- key: y-direction section · x (m) -->
Sezione lungo y · x (m)

<!-- key: Colour fill -->
Riempimento a colori

<!-- key: Contour lines -->
Isolinee

<!-- key: Log colours -->
Colori logaritmici

<!-- key: Particle paths -->
Traiettorie delle particelle

<!-- key: Opacity -->
Opacità

<!-- key: Compare runs in x / y sections -->
Confronta esecuzioni nelle sezioni x / y

<!-- key: Compare section profiles -->
Confronta profili

<!-- key: Runs for section comparison -->
Esecuzioni da confrontare in sezione

<!-- key: Also overlay top-view contours -->
Sovrapponi anche isolinee in pianta

<!-- key: Download plume figure (PNG) -->
Scarica figura del pennacchio (PNG)

<!-- key: Runs in breakthrough comparison -->
Esecuzioni per confronto delle curve di arrivo

<!-- key: Observation cells used by each run -->
Celle di osservazione per esecuzione

<!-- key: Download breakthrough curves (CSV) -->
Scarica curve di arrivo (CSV)

<!-- key: Detailed mass-budget data -->
Dati dettagliati del bilancio di massa

<!-- key: Stored run configuration -->
Configurazione salvata

<!-- key: Download comparison table (CSV) -->
Scarica tabella di confronto (CSV)

<!-- key: Download run configuration (JSON) -->
Scarica configurazione (JSON)

<!-- key: Prepare complete displayed-run archive -->
Prepara archivio completo dell'esecuzione visualizzata

<!-- key: Preparing archive… -->
Preparazione archivio…

<!-- key: Download run archive (ZIP) -->
Scarica archivio (ZIP)

<!-- key: Run -->
Esecuzione

<!-- key: Method -->
Metodo

<!-- key: Signal -->
Segnale

<!-- key: Grid -->
Griglia

<!-- key: K zones -->
Zone K

<!-- key: Flow -->
Flusso

<!-- key: MB disc. (%) -->
Scarto massa (%)

<!-- key: Flow disc. (%) -->
Scarto flusso (%)

<!-- key: MT3D (s) -->
MT3D (s)

<!-- key: MP7 (s) -->
MP7 (s)

<!-- key: Flow (s) -->
Flusso (s)

<!-- key: Total (s) -->
Totale (s)

<!-- key: Ref. L1 (%) -->
Rif. L1 (%)

<!-- key: Mass (g) -->
Massa (g)

<!-- key: Input (g) -->
Ingresso (g)

<!-- key: Min. C (g/m³) -->
C min. (g/m³)

<!-- key: Neg. mass (g) -->
Massa neg. (g)

<!-- key: Centroid x (m) -->
Baricentro x (m)

<!-- key: Steps -->
Passi

<!-- key: Source box (m) -->
Dimensioni sorgente (m)

<!-- key: End (d) -->
Fine (g)

<!-- key: Scenario -->
Scenario

<!-- key: Point -->
Punto

<!-- key: Requested x -->
x richiesto

<!-- key: Requested y -->
y richiesto

<!-- key: Requested z -->
z richiesto

<!-- key: Cell centre x -->
Centro cella x

<!-- key: Cell centre y -->
Centro cella y

<!-- key: Cell centre z -->
Centro cella z

<!-- key: Layer -->
Strato

<!-- key: Row -->
Riga

<!-- key: Column -->
Colonna

<!-- key: Cumulative in (g) -->
Ingresso cumulato (g)

<!-- key: Cumulative out (g) -->
Uscita cumulata (g)

<!-- key: Sources (g) -->
Sorgenti (g)

<!-- key: Sinks (g) -->
Pozzi di estrazione (g)

<!-- key: Fluid storage (g) -->
Immagazzinamento fluido (g)

<!-- key: Native resident mass (g) -->
Massa residente nativa (g)

<!-- key: Alternative disc. (%) -->
Scarto alternativo (%)

<!-- key: Analytical reference requires homogeneous steady flow. -->
Il riferimento analitico richiede flusso stazionario omogeneo.

<!-- key: Source cells -->
Celle sorgente

<!-- key: Specified head -->
Carico imposto

<!-- key: Section locations -->
Posizioni delle sezioni

<!-- key: Background flow -->
Flusso di fondo

<!-- key: Model preview: grid, boundaries and source -->
Anteprima: griglia, contorni e sorgente

<!-- key: Computed head contours -->
Isopieze calcolate

<!-- key: Homogeneous steady head contours -->
Isopieze stazionarie omogenee

<!-- key: Time (d) -->
Tempo (g)

<!-- key: Mass rate (g/d) -->
Portata massica (g/giorno)

<!-- key: Instantaneous mass (g) -->
Massa istantanea (g)

<!-- key: Dirac input (initial cell mass) -->
Ingresso Dirac (massa iniziale nelle celle)

<!-- key: Finite pulse input -->
Ingresso a impulso finito

<!-- key: Continuous input -->
Ingresso continuo

<!-- key: Concentration (g/m³) -->
Concentrazione (g/m³)

<!-- key: Elevation z (m) -->
Quota z (m)

<!-- key: MODPATH advection (slice) -->
Advezione MODPATH (fetta)

<!-- key: Analytical -->
Analitico

<!-- key: Analytical (active run) -->
Analitico (esecuzione attiva)

<!-- key: Mass output unavailable -->
Output di massa non disponibile

<!-- key: MT3D discrepancy (%) -->
Scarto MT3D (%)

<!-- key: Initial + injected mass (first run) -->
Massa iniziale + immessa (prima esecuzione)

<!-- key: Resident mass: grid sum and MT3D budget -->
Massa residente: somma sulla griglia e bilancio MT3D

<!-- key: Reported mass-balance closure -->
Chiusura del bilancio di massa riportata

<!-- key: Example: pulse plume after 600 days -->
Esempio: pennacchio dopo 600 giorni

<!-- key: Example: observation P1 -->
Esempio: osservazione P1

<!-- key: P1 · x (m) -->
P1 · x (m)

<!-- key: P1 · y (m) -->
P1 · y (m)

<!-- key: P1 · elevation z (m) -->
P1 · Quota z (m)

<!-- key: P2 · x (m) -->
P2 · x (m)

<!-- key: P2 · y (m) -->
P2 · y (m)

<!-- key: P2 · elevation z (m) -->
P2 · Quota z (m)

<!-- key: P3 · x (m) -->
P3 · x (m)

<!-- key: P3 · y (m) -->
P3 · y (m)

<!-- key: P3 · elevation z (m) -->
P3 · Quota z (m)

<!-- key: P4 · x (m) -->
P4 · x (m)

<!-- key: P4 · y (m) -->
P4 · y (m)

<!-- key: P4 · elevation z (m) -->
P4 · Quota z (m)

<!-- key: P5 · x (m) -->
P5 · x (m)

<!-- key: P5 · y (m) -->
P5 · y (m)

<!-- key: P5 · elevation z (m) -->
P5 · Quota z (m)

<!-- key: fig_head -->
Carico imposto: {head:g} m

<!-- key: fig_layers -->
{layers} strati; scala verticale esagerata

<!-- key: fig_total -->
Totale: {mass:g} g

<!-- key: fig_initial -->
{mass:g} g a t = 0

<!-- key: fig_xprofile -->
Profilo x a y = {y:.3g} m

<!-- key: fig_yprofile -->
Profilo y a x = {x:.3g} m

<!-- key: fig_section -->
Sezione {axis}–z a {other} = {value:.3g} m

<!-- key: fig_title -->
{method} · t = {time:g} g · strato {layer} (z = {z:.3g} m)

<!-- key: fig_gridmass -->
{label}: somma sulla griglia

<!-- key: fig_nativemass -->
{label}: bilancio MT3D

<!-- key: fig_nodata -->
{label}: fuori dominio — nessun dato

<!-- key: table_help_MB disc. (%) -->
Scarto finale del bilancio di massa riportato da MT3D.

<!-- key: table_help_Flow disc. (%) -->
Scarto finale del bilancio idrico MODFLOW.

<!-- key: table_help_MT3D (s) -->
Tempo reale del programma di trasporto.

<!-- key: table_help_MP7 (s) -->
Tempo MODPATH; le particelle descrivono solo l'advezione.

<!-- key: table_help_Ref. L1 (%) -->
Errore assoluto di concentrazione ponderato per volume dei pori, diviso per la massa di riferimento.

<!-- key: table_help_Mass (g) -->
Massa disciolta finale integrata sulla griglia di concentrazione.

<!-- key: MT3DMS final mass discrepancy exceeds 1%; inspect method and transport time step settings. -->
Lo scarto finale di massa MT3DMS supera l'1%; controllare metodo e passo di trasporto.

<!-- key: At least one MODFLOW water-budget discrepancy exceeds 0.1%. -->
Almeno uno scarto del bilancio idrico MODFLOW supera lo 0,1%.

<!-- key: Negative concentrations occurred. They are retained in diagnostics and exports; central FD and particle methods can oscillate. -->
Sono presenti concentrazioni negative, conservate in diagnostica ed esportazioni. FD centrale e metodi a particelle possono oscillare.

<!-- key: Source coordinates must lie inside the domain. -->
Le coordinate della sorgente devono essere nel dominio.

<!-- key: This confined lab requires heads at or above aquifer top. -->
Questo modello confinato richiede carichi almeno pari alla quota del tetto.

<!-- key: Pulse duration must be between zero and model duration. -->
La durata dell'impulso deve essere tra zero e la durata del modello.

<!-- key: Observation point is outside the model. -->
Il punto di osservazione è fuori dal modello.

<!-- key: TVD requires PERCEL no greater than 1. -->
TVD richiede PERCEL ≤ 1.

<!-- key: language_fallback -->
Se manca una traduzione viene usato il testo inglese.

<!-- key: preset_random -->
Parametri casuali stocastici

<!-- key: Random unit x (m) -->
Unità casuale x (m)

<!-- key: Random unit y (m) -->
Unità casuale y (m)

<!-- key: random_hint -->
Unità piccole: trama fine; grandi: zone più ampie. Mantenere seme e dimensioni fisiche durante il raffinamento per preservare la realizzazione.

<!-- key: Active cells -->
Celle attive

<!-- key: table_help_Active cells -->
Tutte le celle non inattive, incluse quelle a carico imposto.

<!-- key: Random field -->
Campo casuale

<!-- key: Comparison runs -->
Esecuzioni confrontate

<!-- key: discard_tags_hint -->
Rimuovere un'etichetta con × per eliminare l'esecuzione. Rimuoverle tutte avvia un nuovo confronto. Esportare prima ciò che si desidera conservare.

<!-- key: Head contours -->
Isopieze

<!-- key: Computed head contours (m) -->
Isopieze calcolate (m)

<!-- key: Head contours appear after running the model -->
Le isopieze appaiono dopo l'esecuzione

<!-- key: fig_background_k -->
K di fondo = {k:.2e} m/s

<!-- key: fig_low_lens_k -->
Lente a K bassa: K = {k:.2e} m/s

<!-- key: fig_high_channel_k -->
Canale a K elevata: K = {k:.2e} m/s

<!-- key: fig_low_barrier_k -->
Barriera a K bassa: K = {k:.2e} m/s

<!-- key: Focus on plume -->
Inquadra il pennacchio

<!-- key: Focus threshold (% of peak) -->
Soglia (% del picco)

<!-- key: focus_hint -->
Lo zoom usa il picco positivo attuale di ogni pennacchio visualizzato, con un margine del 20% per lato. Include le traiettorie MODPATH visibili. Senza pennacchio o traiettorie mostra tutto il dominio. Cambia solo la vista in pianta.

<!-- key: Download plume figure (SVG) -->
Scarica figura del pennacchio (SVG)

<!-- key: steady -->
stazionario

<!-- key: transient -->
transitorio

<!-- key: fig_minimum -->
Minimo numerico: {minimum:.3g} g/m³

<!-- key: fig_minimum_log -->
Minimo numerico: {minimum:.3g} g/m³ (valori non positivi nascosti nella scala logaritmica)

<!-- key: The plume reaches an x specified-head boundary; enlarge the domain before treating the infinite-x analytical solution as a benchmark. -->
Il pennacchio raggiunge un bordo x a carico imposto; ampliare il dominio prima di usare il riferimento infinito.

<!-- key: fig_reference_boundary -->
Errore analitico disattivato: interazione con bordi x oltre la soglia del {tolerance_percent:.2g}%.

<!-- key: Low K lens -->
Lente a K bassa

<!-- key: High K channel -->
Canale a K elevata

<!-- key: Low K barrier -->
Barriera parziale a K bassa

<!-- key: Page width -->
Larghezza pagina

<!-- key: width_1 -->
Stretta

<!-- key: width_2 -->
Compatta

<!-- key: width_3 -->
Standard

<!-- key: width_4 -->
Ampia

<!-- key: width_5 -->
Intera larghezza

<!-- key: page_width_hint -->
Cinque larghezze, da stretta a piena. Standard mantiene la larghezza precedente. La pagina si adatta agli schermi piccoli.

<!-- key: Show model grid -->
Mostra griglia

<!-- key: grid_hint -->
Bordi discreti delle celle dell’esecuzione visualizzata. I profili a uno strato mostrano guide verticali ai bordi delle celle.

<!-- key: Plume-centered x/y -->
x/y centrati sul pennacchio

<!-- key: relative_hint -->
Lo zero è il baricentro della massa disciolta positiva nello strato mostrato. Tutte le sovrapposizioni usano questa origine. Coordinate di input e quote restano assolute.

<!-- key: relative_mass_origin -->
Origine relativa: x = {x:.2f} m; y = {y:.2f} m (baricentro del pennacchio).

<!-- key: relative_source_origin -->
Nessuna massa positiva in questo strato: origine al centro della sorgente sulla griglia, x = {x:.2f} m; y = {y:.2f} m.

<!-- key: fig_relative_xprofile -->
Profilo x a y′ = {y:.3g} m

<!-- key: fig_relative_yprofile -->
Profilo y a x′ = {x:.3g} m

<!-- key: fig_relative_section -->
Sezione {axis}–z a {other}′ = {value:.3g} m

<!-- key: MODPATH particle count -->
Numero di particelle MODPATH

<!-- key: particle_count_cell -->
Per cella sorgente

<!-- key: particle_count_total -->
Intera sorgente per rilascio

<!-- key: Particles in the whole source per release -->
Particelle nell’intera sorgente per rilascio

<!-- key: particle_count_summary -->
{count} particelle in {cells} celle sorgente × {groups} rilasci = {total} particelle.

<!-- key: expert_transport_hint -->
Sono visibili tutte le impostazioni del solutore di trasporto. NPL / NPH e NPMIN / NPMAX controllano le particelle MOC / HMOC; MXPART ne limita il totale. Gli aiuti indicano i metodi applicabili. MODPATH usa particelle separate.

<!-- key: Plume animation -->
Animazione del pennacchio

<!-- key: Animation view -->
Vista dell’animazione

<!-- key: animation_2d -->
Pianta e sezioni

<!-- key: animation_3d -->
Concentrazioni 3D nei centri delle celle

<!-- key: Animation frames -->
Fotogrammi

<!-- key: Playback speed (frames/s) -->
Velocità (fotogrammi/s)

<!-- key: Vertical exaggeration -->
Esagerazione verticale

<!-- key: Generate / refresh animation -->
Genera / aggiorna animazione

<!-- key: Generating animation… -->
Generazione dell’animazione…

<!-- key: Download animation (HTML) -->
Scarica animazione (HTML)

<!-- key: Play -->
Riproduci

<!-- key: Pause -->
Pausa

<!-- key: Animation frame -->
Fotogramma

<!-- key: animation_layers_hint -->
Aggiungere strati nelle impostazioni esperte per la vista 3D.

<!-- key: animation_hint -->
Usa i tempi salvati della simulazione visualizzata. Scegliere colori e zoom indipendenti per l’animazione; la scala resta fissa nel tempo. Le altre impostazioni 2D sono mantenute. Confronti e riferimenti analitici restano nei grafici statici. Il lettore appare sotto le impostazioni; il file HTML scaricato funziona offline.

<!-- key: animation_3d_hint -->
La vista 3D mostra concentrazioni nei centri delle celle sopra la soglia, con camera fissa. Si visualizzano al massimo {maximum} celle campionate uniformemente; calcoli ed esportazioni mantengono tutte le celle. Le particelle confrontano l’advezione. L’esagerazione è solo grafica.

<!-- key: animation_refresh_hint -->
Le impostazioni sono cambiate. Generare nuovamente per aggiornare.

<!-- key: animation_failed -->
Impossibile generare l’animazione. I risultati rimangono disponibili.

<!-- key: animation_size_limit -->
L’animazione supera 45 MiB. Ridurre i fotogrammi.

<!-- key: help_s_percel -->
Spostamento advettivo massimo per passo, in larghezze di cella. TVD richiede ≤ 1.

<!-- key: help_s_mxpart -->
MOC/HMOC: capacità totale di particelle mobili, non per cella.

<!-- key: help_s_itrack -->
MOC/MMOC/HMOC: 1 = Eulero, 2 = Runge–Kutta del quarto ordine, 3 = tracciamento ibrido.

<!-- key: help_s_wd -->
Metodi delle caratteristiche: peso della concentrazione nella separazione degli operatori; 0,5–1.

<!-- key: help_s_dceps -->
MOC/HMOC: soglia del gradiente relativo che distingue NPL e NPH.

<!-- key: help_s_nplane -->
MOC/HMOC: 0 = disposizione casuale; positivo = piani orizzontali per cella.

<!-- key: help_s_npl -->
MOC/HMOC: particelle iniziali per cella con gradiente ≤ DCEPS; zero ammesso.

<!-- key: help_s_nph -->
MOC/HMOC: particelle iniziali per cella ad alto gradiente. Gli schemi fissi possono arrotondare il numero.

<!-- key: help_s_npmin -->
MOC/HMOC: inserisce particelle sotto questo minimo per cella.

<!-- key: help_s_npmax -->
MOC/HMOC: superato il limite, sostituisce le particelle della cella con NPH particelle.

<!-- key: help_s_interp -->
MMOC/HMOC: interpolazione della concentrazione; solo 1 (lineare) disponibile.

<!-- key: help_s_nlsink -->
Celle pozzo MMOC/HMOC: 0 = casuale; positivo = piani di particelle.

<!-- key: help_s_npsink -->
MMOC/HMOC: particelle rappresentative di ogni cella pozzo.

<!-- key: help_s_dchmoc -->
HMOC: MOC sopra questa soglia relativa, MMOC sotto.

<!-- key: help_s_mxiter -->
Limite delle iterazioni esterne GCG. Una basta per questo trasporto conservativo lineare.

<!-- key: help_s_iter1 -->
Limite di iterazioni interne GCG per le equazioni di trasporto.

<!-- key: help_s_isolve -->
Precondizionatore GCG: 1 = Jacobi, 2 = SSOR, 3 = Cholesky incompleto modificato (MIC).

<!-- key: help_s_ncrs -->
Termini incrociati: 0 = approssimazione al secondo membro; 1 = tensore completo nella matrice.

<!-- key: help_s_accl -->
Fattore di rilassamento, solo per SSOR (ISOLVE = 2).

<!-- key: help_s_cclose -->
Tolleranza relativa sulla variazione di concentrazione GCG. Valori minori sono più restrittivi.

<!-- key: help_s_iprgcg -->
Stampa variazioni ogni N iterazioni GCG; 0 a fine periodo.

<!-- key: help_s_dt0 -->
Passo iniziale in giorni; 0 lascia scegliere MT3D.

<!-- key: help_s_ttsmult -->
Moltiplicatore dei passi FD impliciti; ignorato da TVD e caratteristiche.

<!-- key: help_s_ttsmax -->
Passo massimo in giorni se TTSMULT > 1; 0 usa il limite automatico.

<!-- key: help_s_mxstrn -->
Massimo numero di passi di trasporto per passo di flusso; il limite può arrestare il calcolo.

<!-- key: help_s_timeout -->
Tempo massimo per eseguibile. Più particelle possono richiedere più tempo.

<!-- key: help_s_hclose -->
Tolleranza PCG sulla variazione di carico, in metri.

<!-- key: help_s_rclose -->
Tolleranza del residuo di portata PCG, in m³/giorno.

<!-- key: help_s_flow_mxiter -->
Iterazioni esterne massime del solutore di flusso MODFLOW PCG.

<!-- key: help_s_flow_iter1 -->
Iterazioni interne PCG massime per iterazione esterna.

<!-- key: help_particle_count_mode -->
Scegliere per cella sorgente o un totale esatto sull’intera sorgente per rilascio.

<!-- key: help_particles_per_cell -->
Particelle distribuite uniformemente in ogni cella sorgente a ogni rilascio. Solo MODPATH, non MOC.

<!-- key: help_total_source_particles -->
Totale esatto per rilascio su tutte le celle sorgente; almeno una per cella. Differenza massima di una particella; pesi secondo volume dei pori.

<!-- key: help_release_groups -->
Rilasci ai punti medi di intervalli uguali approssimano impulso o apporto continuo. Più gruppi affinano i tempi; Dirac rilascia a t = 0.

<!-- key: help_run_label -->
Lasciare vuoto per il nome suggerito. Il testo sostituisce metodo/segnale; numero e suffisso eterogeneo restano automatici.

<!-- key: help_expert -->
Mostra strati e tutti i parametri dei solutori. I valori nascosti sono mantenuti.

<!-- key: help_sliders -->
Passa tra campi numerici e cursori senza cambiare i valori.

<!-- key: help_extent -->
Estensione fisica in metri. Modificarla avvia una nuova serie.

<!-- key: help_thickness -->
Spessore confinato; base a 0 m e tetto a questo valore. Strati di uguale spessore.

<!-- key: help_grid_mode -->
Definire numero o larghezza massima delle celle. Il numero si arrotonda in eccesso mantenendo il dominio.

<!-- key: help_grid_count -->
Numero di celle uniformi in questa direzione. L’infittimento conserva i calcoli precedenti.

<!-- key: help_cell_width -->
Larghezza massima richiesta in metri. L’anteprima mostra quella effettiva.

<!-- key: help_nlay -->
Uno strato dà un modello in pianta; più strati uguali consentono trasporto verticale e viste 3D.

<!-- key: help_k -->
Conducibilità idraulica orizzontale di fondo. Inserire m/s; conversione in m/giorno.

<!-- key: help_porosity -->
Frazione porosa mobile; controlla velocità interstiziale e accumulo del soluto.

<!-- key: help_ss -->
Acqua rilasciata per volume e calo unitario di carico (1/m). Qui il flusso stazionario non attiva accumulo.

<!-- key: help_kv_ratio -->
Conducibilità verticale divisa per l’orizzontale, in ogni strato.

<!-- key: help_zones_preset -->
Scegliere proprietà omogenee, campo casuale ripetibile o lente/canale/barriera.

<!-- key: help_zone_seed -->
Seme casuale. Stesso seme e impostazioni riproducono il campo fisico.

<!-- key: help_random_unit -->
Dimensione fisica dei blocchi casuali in questa direzione, indipendente dalla griglia.

<!-- key: help_random_k -->
Limiti della conducibilità casuale, campionamento uniforme nello spazio logaritmico (m/s).

<!-- key: help_random_ss -->
Limiti dell’immagazzinamento specifico log-uniforme (1/m). Salvato, inattivo nel flusso stazionario.

<!-- key: help_random_por -->
Limiti della porosità efficace uniforme, tra zero e uno.

<!-- key: help_head -->
Carico imposto sulla colonna esterna. Sinistra maggiore della destra; entrambi almeno al tetto.

<!-- key: help_duration -->
Durata simulata del trasporto in giorni, indipendente dalla velocità dell’animazione.

<!-- key: help_dispersion -->
Include dispersione meccanica proporzionale alla velocità interstiziale. Disattivata restano advezione e diffusione numerica.

<!-- key: help_al -->
Dispersività longitudinale in metri; coefficiente associato = αL × velocità.

<!-- key: help_trpt -->
Dispersività trasversale orizzontale divisa per longitudinale: αTH/αL.

<!-- key: help_trpv -->
Dispersività trasversale verticale divisa per longitudinale: αTV/αL. Rilevante con più strati.

<!-- key: help_source_kind -->
Dirac: massa iniziale a t = 0. Impulso: carico costante fino alla fine. Continuo: carico costante per tutto il calcolo.

<!-- key: help_source_mass -->
Massa disciolta iniziale totale nel volume poroso sorgente (grammi).

<!-- key: help_mass_rate -->
Carico totale (g/giorno), distribuito per volume poroso sorgente. Nessuna iniezione d’acqua.

<!-- key: help_pulse_duration -->
Il carico termina dopo questo tempo (giorni), inferiore alla durata totale.

<!-- key: help_source_position -->
Coordinata assoluta del centro sorgente in metri, assegnata a una cella. Evitare colonne a carico imposto.

<!-- key: help_source_cells -->
Celle sorgente in questa direzione. Verificare l’impronta; cambiare geometria avvia una nuova serie.

<!-- key: help_source_all_layers -->
Distribuire la sorgente su tutti gli strati, altrimenti solo su quello scelto.

<!-- key: help_src_layer -->
Strato che riceve la sorgente; 1 è quello superiore.

<!-- key: help_method -->
Scegliere advezione MT3D: FD up/centrale, TVD, MOC avanti, MMOC indietro o HMOC ibrido. Indipendente da MODPATH.

<!-- key: help_track_particles -->
Esegue MODPATH 7 nel campo calcolato. Solo advezione; MODPATH non calcola dispersione né concentrazioni.

<!-- key: help_observation -->
Coordinata assoluta di osservazione in metri. Concentrazione della cella contenente il punto, senza interpolazione.

<!-- key: help_nobs -->
Confrontare concentrazioni in uno-cinque punti usando i calcoli salvati.

<!-- key: help_outputs -->
Tempi salvati, incluso t = 0; anche fine impulso. Più uscite affinano animazione e curve, non i passi del solutore.

<!-- key: help_length -->
Estensione fisica in metri. Modificarla avvia una nuova serie.

<!-- key: help_width -->
Estensione fisica in metri. Modificarla avvia una nuova serie.

<!-- key: help_ncol -->
Numero di celle uniformi in questa direzione. L’infittimento conserva i calcoli precedenti.

<!-- key: help_nrow -->
Numero di celle uniformi in questa direzione. L’infittimento conserva i calcoli precedenti.

<!-- key: help_cell_x -->
Larghezza massima richiesta in metri. L’anteprima mostra quella effettiva.

<!-- key: help_cell_y -->
Larghezza massima richiesta in metri. L’anteprima mostra quella effettiva.

<!-- key: help_random_unit_x -->
Dimensione fisica dei blocchi casuali in questa direzione, indipendente dalla griglia.

<!-- key: help_random_unit_y -->
Dimensione fisica dei blocchi casuali in questa direzione, indipendente dalla griglia.

<!-- key: help_zone_k_min -->
Limiti della conducibilità casuale, campionamento uniforme nello spazio logaritmico (m/s).

<!-- key: help_zone_k_max -->
Limiti della conducibilità casuale, campionamento uniforme nello spazio logaritmico (m/s).

<!-- key: help_zone_ss_min -->
Limiti dell’immagazzinamento specifico log-uniforme (1/m). Salvato, inattivo nel flusso stazionario.

<!-- key: help_zone_ss_max -->
Limiti dell’immagazzinamento specifico log-uniforme (1/m). Salvato, inattivo nel flusso stazionario.

<!-- key: help_zone_por_min -->
Limiti della porosità efficace uniforme, tra zero e uno.

<!-- key: help_zone_por_max -->
Limiti della porosità efficace uniforme, tra zero e uno.

<!-- key: help_head_left -->
Carico imposto sulla colonna esterna. Sinistra maggiore della destra; entrambi almeno al tetto.

<!-- key: help_head_right -->
Carico imposto sulla colonna esterna. Sinistra maggiore della destra; entrambi almeno al tetto.

<!-- key: help_src_x -->
Coordinata assoluta del centro sorgente in metri, assegnata a una cella. Evitare colonne a carico imposto.

<!-- key: help_src_y -->
Coordinata assoluta del centro sorgente in metri, assegnata a una cella. Evitare colonne a carico imposto.

<!-- key: help_src_ncol -->
Celle sorgente in questa direzione. Verificare l’impronta; cambiare geometria avvia una nuova serie.

<!-- key: help_src_nrow -->
Celle sorgente in questa direzione. Verificare l’impronta; cambiare geometria avvia una nuova serie.

<!-- key: help_animation_mode -->
2D anima pianta e sezioni. 3D mostra concentrazioni nei centri con vista fissa; richiede più strati.

<!-- key: help_animation_frames -->
Fino a 80 stati salvati, inclusi primo e ultimo. Nessuna interpolazione temporale della concentrazione.

<!-- key: help_animation_fps -->
Fotogrammi per secondo reale. Ogni immagine indica il tempo simulato; non cambia il modello.

<!-- key: help_animation_exaggeration -->
Scala l’altezza visiva 3D. Quote e calcoli restano invariati.

<!-- key: help_generate_animation -->
Elabora risultati salvati su richiesta. Rigenerare dopo modifiche; senza rieseguire il modello.

<!-- key: help_view_time -->
Scegliere un tempo salvato, senza ricalcolo.

<!-- key: help_view_layer -->
Strato in pianta; 1 è in alto.

<!-- key: help_section -->
Posizione assoluta in metri, nella riga/colonna corrispondente. Assi relativi non spostano la sezione.

<!-- key: help_fill -->
Colora le celle secondo la concentrazione; zero rimane bianco.

<!-- key: help_lines -->
Disegna isolinee di concentrazione sui colori.

<!-- key: help_show_heads -->
Sovrappone sottili isolinee del carico calcolato, in metri.

<!-- key: help_log -->
Colori logaritmici per concentrazioni positive. Valori non positivi nascosti solo nella vista.

<!-- key: help_particle_paths -->
Mostra posizioni e percorsi MODPATH fino al tempo scelto. Massimo 120 traiettorie visibili; esportazione completa.

<!-- key: help_opacity -->
Opacità: 1 è opaco; valori minori rivelano gli elementi sotto.

<!-- key: help_focus_plume -->
Inquadra pennacchio positivo e traiettorie con margine. L’animazione usa una finestra fissa sui tempi scelti.

<!-- key: help_focus_threshold -->
Zoom statico: percentuale del picco. In animazione 3D: percentuale del massimo assoluto della scala fissa per mostrare celle.

<!-- key: help_analytical -->
Confronta con riferimento analitico omogeneo stazionario. Flusso eterogeneo o transitorio fuori dalle ipotesi.

<!-- key: help_compare -->
Confronta calcoli al tempo disponibile più vicino nelle sezioni di quello visualizzato.

<!-- key: help_analytic_on -->
Confronta con riferimento analitico omogeneo stazionario. Flusso eterogeneo o transitorio fuori dalle ipotesi.

<!-- key: help_btc_analytical -->
Confronta con riferimento analitico omogeneo stazionario. Flusso eterogeneo o transitorio fuori dalle ipotesi.

<!-- key: help_compare_sections -->
Confronta calcoli al tempo disponibile più vicino nelle sezioni di quello visualizzato.

<!-- key: help_overlay_runs -->
Confronta calcoli al tempo disponibile più vicino nelle sezioni di quello visualizzato.

<!-- key: help_compare_top -->
Confronta calcoli al tempo disponibile più vicino nelle sezioni di quello visualizzato.

<!-- key: help_btc_runs -->
Confrontare concentrazioni in uno-cinque punti usando i calcoli salvati.

<!-- key: Animation settings -->
Impostazioni dell’animazione

<!-- key: Animation colour scale -->
Scala cromatica dell’animazione

<!-- key: animation_colour_enhanced -->
Basse concentrazioni evidenziate (scala fissa)

<!-- key: animation_colour_linear -->
Lineare (scala fissa)

<!-- key: animation_colour_log -->
Logaritmica (scala fissa)

<!-- key: help_animation_colour -->
Il miglioramento usa una trasformazione di potenza (esponente 0,35) per rendere visibili le basse concentrazioni. Tutti i fotogrammi mantengono gli stessi limiti fisici di concentrazione; lo zero resta bianco. Le scale lineare e potenziata mostrano i valori numerici negativi; quella logaritmica nasconde i valori non positivi. I dati calcolati non cambiano.

<!-- key: Zoom animation to plume -->
Ingrandisci il pennacchio nell’animazione

<!-- key: help_animation_focus -->
Una finestra fissa comprende il pennacchio positivo e le traiettorie MODPATH visualizzate a tutti i tempi selezionati, con un margine del 20 %. Indipendente dallo zoom statico. Disattivare per mostrare tutto il dominio. Disponibile in 2D e 3D.

<!-- key: Plume threshold (% of peak) -->
Soglia del pennacchio (% del massimo)

<!-- key: help_animation_threshold -->
Lo zoom include concentrazioni superiori a questa percentuale del massimo positivo di ogni fotogramma. In 3D, questa soglia determina anche le celle visibili rispetto alla concentrazione assoluta massima della scala fissa. Valore iniziale: 0,1 %. Influenza solo la visualizzazione.

<!-- key: animation_progress -->
Generazione dell’animazione… {percent} %

<!-- key: MODPATH settings -->
Impostazioni MODPATH

<!-- key: expert_transport_location_hint -->
I parametri avanzati di MT3D si trovano nel pannello espandibile separato **Impostazioni esperte del solutore di trasporto**, subito sotto. Seguono le impostazioni MODPATH.
