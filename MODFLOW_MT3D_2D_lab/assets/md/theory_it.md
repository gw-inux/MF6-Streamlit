### Modello concettuale
Il laboratorio segue un soluto conservativo in un acquifero confinato e saturo. I carichi imposti nella prima e nell'ultima colonna generano il flusso di fondo. Le altre facce sono chiuse al flusso idrico e dispersivo. L'acqua entrante ha concentrazione nulla; l'uscita trasporta la concentrazione residente. Non sono inclusi reazioni, adsorbimento, effetti di densità, ricarica o pompaggio.

Uno strato rappresenta il trasporto orizzontale 2D. Più strati consentono gradienti e dispersione verticali. Una sorgente uniforme sull'intero spessore in materiale omogeneo rimane uniforme verticalmente: aggiungere strati non genera flusso verticale. Una sorgente in un solo strato consente esperimenti 3D.

Unità: m, giorni, g e g/m³ d'acqua; 1 g/m³ = 1 mg/L. Internamente K è in m/giorno: $10^{-4}$ m/s = 8,64 m/giorno.

### Flusso e immagazzinamento
Per flusso omogeneo stazionario la velocità interstiziale è:
$$
v_x=\frac{K}{n_e}\frac{h_L-h_R}{L-\Delta x}.
$$
Il denominatore è la distanza fra i **centri delle celle** a carico imposto, non fra le facce esterne. MODFLOW calcola il campo eterogeneo dai K locali. La conducibilità verticale è quella orizzontale locale moltiplicata per il rapporto selezionato.

L'interfaccia usa flusso stazionario. Ss è salvato come proprietà del materiale, ma non modifica carichi e velocità stazionari. I carichi devono essere almeno pari alla quota del tetto. Il rendimento specifico non è usato.

### Segnali di ingresso
| Segnale | Rappresentazione | Quantità conservata |
|---|---|---|
| Dirac | Concentrazione iniziale uniforme nelle celle sorgente | Massa iniziale $M$ |
| Impulso rettangolare | Portata massica prescritta fino a $\tau$ | Massa totale $\dot M\tau$ |
| Continuo | Portata massica per l'intera durata | Massa immessa fino a $t$: $\dot M t$ |

Le sorgenti interne aggiungono soluto senza acqua e senza alterare il flusso. L'impulso termina al confine di un periodo di sollecitazione, poi la portata massica è esplicitamente nulla. Dirac è istantaneo nel tempo, ma occupa un volume finito. La concentrazione iniziale omogenea è $M/(n_eV_s)$; con porosità diverse i pesi dei volumi dei pori producono la stessa concentrazione iniziale.

La sorgente coincide con le celle selezionate. Verificarne dimensioni e posizione dopo il raffinamento: mantenere il numero di celle sorgente ne modifica il volume fisico.

### Advezione e dispersione
Per flusso omogeneo stazionario lungo x:
$$
\frac{\partial C}{\partial t}
=D_x\frac{\partial^2 C}{\partial x^2}
+D_y\frac{\partial^2 C}{\partial y^2}
+D_z\frac{\partial^2 C}{\partial z^2}
-v_x\frac{\partial C}{\partial x}+\frac{s}{n_e}.
$$
$s$ è l'apporto di soluto per volume totale e tempo. $D_x=\alpha_L|v_x|+D_e$, $D_y=\alpha_{TH}|v_x|+D_e$ e $D_z=\alpha_{TV}|v_x|+D_e$. Le dispersività trasversali sono rapporti rispetto a $\alpha_L$. MT3D costruisce il tensore dalle velocità locali nel flusso eterogeneo. La diffusione molecolare è zero; disattivare la dispersione elimina l'allargamento meccanico. Con uno strato e tetto/base chiusi, la dispersività verticale non ha effetto e il relativo controllo appare solo con più strati.

| Metodo | Opzione MT3D | Cosa investigare |
|---|---|---|
| FD up | MIXELM = 0, NADVFD = 0 | Smussamento numerico dei fronti |
| FD cen | MIXELM = 0, NADVFD = 2 | Oscillazioni e concentrazioni negative su griglie grossolane dominate dall'advezione |
| TVD | MIXELM = −1 | Fronti netti con limitazione del flusso |
| MOC | MIXELM = 1 | Caratteristiche in avanti; densità delle particelle |
| MMOC | MIXELM = 2 | Caratteristiche all'indietro; bilancio di massa |
| HMOC | MIXELM = 3 | Commutazione locale MOC/MMOC |

Le opzioni esperte includono advezione, GCG, passi di trasporto e tolleranze MODFLOW. Alcune valgono solo per determinati metodi: MXPART limita le particelle mobili MOC/HMOC. PERCEL controlla lo spostamento per passo; TVD richiede PERCEL ≤ 1. La normale terminazione non prova l'accuratezza.

### Riferimento analitico
Il riferimento assume velocità, porosità e dispersione costanti. Integra la funzione di Green sul **volume sorgente effettivo** e su ogni cella ricevente. I bordi y/z riflettono il soluto; x è infinito. Una sorgente a uno strato sull'intero spessore dà la soluzione 2D normalizzata per spessore. Impulso e continuo usano convoluzione temporale.

La funzione di Green puntuale istantanea 3D illimitata è:
$$
C=\frac{M}{n_e(4\pi t)^{3/2}\sqrt{D_xD_yD_z}}
\exp\!\left[-\frac{(x-x_s-v_xt)^2}{4D_xt}
-\frac{(y-y_s)^2}{4D_yt}-\frac{(z-z_s)^2}{4D_zt}\right].
$$
In 2D orizzontale il denominatore diventa $4\pi n_e b t\sqrt{D_xD_y}$ e si omette il termine z. Queste formule spiegano la forma; il confronto usa volumi finiti per una diluizione coerente con MT3D.

Il riferimento omogeneo non è esatto per materiali zonati o flusso transitorio: le metriche d'errore vengono soppresse. I bordi x devono restare lontani dal pennacchio. Il controllo della massa trattenuta segnala vicinanza ai bordi, ma non dimostra equivalenza tra domini finito e infinito. Ampliare il dominio e verificarne la sensibilità quando il pennacchio si avvicina ai bordi.

### MODPATH e lettura dei risultati
MODPATH 7 usa flusso MODFLOW e identica porosità per traiettorie advettive. Non calcola dispersione o concentrazioni. La larghezza della nuvola di particelle non rappresenta un pennacchio dispersivo. La massa associata è un peso di quadratura della distribuzione del rilascio, non un bilancio di soluto MODPATH. Le particelle MOC hanno un altro scopo.

Confrontare forme, curve di arrivo e tabella. Un piccolo scarto di bilancio può accompagnare dispersione numerica o oscillazioni. Mantenere sorgente, proprietà e griglia fisse nel confronto fra metodi. Il tempo dipende dal carico della macchina: ripetere sulla stessa macchina. Le osservazioni usano le celle contenenti i punti; le sezioni seguono la griglia. Si conservano i valori negativi, nascosti nella vista logaritmica: esaminare anche scala lineare e minimo.

### Eterogeneità, serie e ingrandimento
Scenari: omogeneo, casuale, lente a K bassa, canale a K elevata e barriera parziale. Il materiale di riferimento è bianco; i contrasti sono colorati con legenda K in m/s. Le unità casuali formano un reticolo fisico: piccole per trame fini, grandi per zone più ampie. K e Ss sono uniformi nello spazio logaritmico; la porosità in quello lineare. Il motivo orizzontale attraversa tutti gli strati. Non è un campo geostatistico a covarianza prescritta.

Seme e dimensioni fisiche fissi preservano la realizzazione durante il raffinamento. Ogni cella campiona l'unità che contiene il suo centro; griglie grossolane possono perdere piccoli dettagli. I vecchi formati rettangolari e transitori restano riproducibili fuori dall'interfaccia.

L'ultima esecuzione appare automaticamente. Segnale e geometria fisica modificati avviano una nuova serie; discretizzazione e impostazioni numeriche restano varianti. **het.** identifica i casi eterogenei. Le etichette × eliminano esecuzioni. Le isopieze calcolate compaiono per impostazione predefinita. Uno strato: profili di concentrazione x/y; più strati: mappe x–z/y–z con quota e concentrazione.

L'ingrandimento usa **0,1% del picco positivo attuale** di ciascun pennacchio mostrato e **20% di margine per lato**, includendo le traiettorie MODPATH visibili. La soglia è modificabile. Se mancano pennacchio e traiettorie resta l'intero dominio. Cambiano solo i limiti della vista in pianta, non concentrazioni, sezioni o scala cromatica.

### Riferimenti
Le quattro applicazioni analitiche fornite hanno ispirato gli esempi. Le loro formule puntuali o a concentrazione imposta non sostituiscono direttamente il benchmark a sorgente massica di volume finito usato qui.


- [FloPy — MT3DMS ADV](https://flopy.readthedocs.io/en/3.12.0/source/flopy.mt3d.mtadv.html)
- [FloPy — MT3DMS SSM](https://flopy.readthedocs.io/en/3.12.0/source/flopy.mt3d.mtssm.html)
- [FloPy — MT3DMS GCG](https://flopy.readthedocs.io/en/3.12.0/source/flopy.mt3d.mtgcg.html)
- [Pollock (2016) — MODPATH 7, USGS](https://pubs.usgs.gov/publication/ofr20161086)
- [Wexler (1992) — USGS](https://pubs.usgs.gov/twri/twri3-b7/)
- [MODFLOW-ORG](https://github.com/MODFLOW-ORG/executables)

### Griglia, coordinate relative e larghezza

La griglia aggiunge bordi grigi discreti in pianta e nelle sezioni dell’esecuzione visualizzata; nei profili a uno strato mostra guide verticali ai bordi delle celle. Le coordinate x′/y′ usano il baricentro della massa disciolta positiva nello strato mostrato, considerando la porosità locale. Senza massa positiva si usa il centro della sorgente sulla griglia. Confronti, riferimento e particelle condividono l’origine; quote, input ed esportazioni numeriche restano assoluti. Il controllo è indipendente dallo zoom. Sono disponibili cinque larghezze; Standard mantiene quella precedente. Il campo del nome giallo diventa verde dopo aver confermato un testo non vuoto con Invio o uscendo dal campo.
