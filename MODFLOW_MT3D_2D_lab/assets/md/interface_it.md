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
MT3D 2D/3D · v0.5.1 · Versione di lavoro per lezioni dal vivo

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
