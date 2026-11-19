## title

Laboratorio di trasporto 1D

## experiments

Esperimenti guidati

## experiment_front

Fronte di advezione

## experiment_spreading

Dispersione fisica

## experiment_impulse

Impulso rettangolare e Dirac

## theory_title

Flusso e soluzioni analitiche

## setup

Configurazione del modello

## inlet_processes

Ingresso e trasporto

## grid_time

Griglia e tempo

## solver

Metodo MT3DMS

## signal

Segnale in ingresso

## continuous

Ingresso continuo

## block

Impulso rettangolare

## dirac

Impulso di Dirac

## amplitude

Concentrazione in ingresso C/Cref [–]

## block_days

Durata dell’impulso [d]

## impulse_area

Area dell’impulso A [d]

## impulse_days

Durata numerica ε [d]

## rectangle

Altezza in ingresso MT3DMS = {height:.4g} C/Cref.

## dispersion

Attivare la dispersione

## dispersivity

Dispersività longitudinale αL [m]

## diffusion

Diffusione efficace Dₑ [m²/d]

## grid_by

Definire la griglia con

## cells

Numero di celle

## spacing

Passo spaziale

## cell_count

Celle

## target_spacing

Larghezza desiderata [m]

## grid_summary

{n} celle · Δx effettivo = {dx:.3g} m

## courant

Limite di Courant

## time_hint

Tutte le varianti terminano al giorno 2000. Un impulso finito usa almeno otto passi di trasporto durante l’immissione.

## scheme

Schema di advezione

## upwind

DF · upwind

## central

DF · centrato

## tvd

TVD · ULTIMATE

## moc

MOC

## mmoc

MMOC

## hmoc

HMOC

## solver_hint

MODFLOW-2005 fornisce il flusso stazionario. MT3DMS risolve le equazioni implicite con GCG.

## preview

Anteprima del modello

## preview_summary

{signal} · {scheme} · {n} celle · Δx = {dx:.3g} m · D = {D:.4g} m²/d

## distance

Distanza dall’ingresso [m]

## time

Tempo [d]

## inlet_axis

Ingresso C/Cref [–]

## optional_name

Nome della variante (facoltativo)

## name_example

ad es. Griglia fine con TVD

## limit

Sono memorizzate dieci varianti. Eliminarne una in « Gestisci varianti » per eseguire un altro calcolo.

## missing

Eseguibile richiesto assente o incompatibile — {names}. Usare la cartella condivisa bin o impostare TRANSPORT_LAB_BIN.

## run

Esegui modello

## running

Esecuzione di MODFLOW-2005 e MT3DMS…

## failed

Il calcolo non è stato completato. Le varianti salvate sono disponibili sotto.

## diagnostic

Dettagli del calcolo

## results

Risultati del trasporto

## visible

Varianti nei grafici

## cells_unit

celle

## show_analytical

Soluzione analitica

## show_markers

Punti numerici

## profile

Profilo di concentrazione

## breakthrough

Curva di arrivo

## budget

Bilancio di massa del soluto

## profile_time

Tempo del profilo [d]

## observation

Distanza di osservazione [m]

## applied_curve

Analitica · ingresso applicato

## ideal_curve

Dirac ideale

## mass_axis

Errore di massa [%]

## no_selection

Selezionare una variante per visualizzarne le curve.

## comparison

Confronto finale · giorno 2000

## variant

Variante

## rmse

RMSE

## mae

MAE

## ideal_rmse

RMSE · Dirac ideale

## mass_error

Errore di massa [%]

## seconds

Tempo di calcolo [s]

## run_name

Nome

## dx_col

Δx [m]

## height_col

Ingresso C/Cref

## duration_col

Durata ingresso [d]

## area_col

Dirac A [d]

## alpha_col

αL [m]

## dm_col

Dₑ [m²/d]

## d_col

D [m²/d]

## pe_col

Péclet della griglia

## co_col

Limite di Courant

## count_col

Passi di trasporto

## flow_s

MODFLOW [s]

## mt_s

MT3DMS [s]

## flow_error

Bilancio idrico [%]

## min_c

Min. finale C/Cref

## max_c

Max. finale C/Cref

## detail_heading

Impostazioni e definizione degli indicatori

## download

Scarica confronto (CSV)

## manage

Gestisci varianti

## remove_choice

Variante da eliminare

## remove

Elimina variante selezionata

## references_title

Riferimenti

## saved

V{number} salvata per il confronto.

## applied_color_key

Analitica · colore della variante

## ideal_color_key

Dirac ideale · colore della variante

## pulse_cells

Lunghezza dell’impulso [celle]

## pulse_resolution

Durante l’immissione, l’advezione trasporta l’impulso per {length:.3g} m, pari a {cells:.3g} celle.

## specified_head

Carico imposto · {head:.4g} m

## hydraulic_summary

Conducibilità idraulica K = {k:.0e} m/s

## scenario_reset_hint

Le modifiche qui cancellano le varianti salvate.

## comparison_cleared

Sono cambiate le impostazioni di ingresso o trasporto. Il confronto è stato svuotato per il nuovo scenario.

## concept_title

Modello concettuale e risposte tipiche

## concept_inlet

Ingresso

## concept_outlet

Uscita

## concept_observation

Osservazione

## concept_profile

Profilo a t = {time:g} d

## concept_breakthrough

Arrivo a x = {distance:g} m

## concept_advection

Solo advezione

## concept_dispersion

Advezione + dispersione
