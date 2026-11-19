## introduction

Esplorate il trasporto di un soluto conservativo lungo un percorso di flusso sotterraneo con un semplice modello monodimensionale. Confrontate MT3DMS con le soluzioni analitiche per osservare come la discretizzazione e i metodi numerici influenzano il segnale trasportato.

## concept_explanation

Immaginate un tubo di flusso stretto che segue il percorso dell’acqua sotterranea in un acquifero omogeneo e saturo. L’acqua scorre in condizioni stazionarie. Un soluto conservativo entra a monte e viene trasportato per advezione. La dispersione può allargare il segnale lungo il percorso.

Questo modello unidimensionale idealizzato permette di studiare l’effetto del metodo numerico, della dimensione delle celle e del passo temporale. Confrontate MT3DMS con la soluzione analitica per esaminare allargamento del fronte, oscillazioni, tempo di transito e bilancio di massa. Scegliete prima il segnale e i processi, poi confrontate fino a dieci varianti numeriche dello stesso scenario.

## concept_caption

Tubo di flusso schematico con moto monodimensionale stazionario e un punto di osservazione a 250 m. Non vi è scambio di acqua o soluto attraverso i confini laterali; le dimensioni trasversali non sono in scala.

## concept_response_caption

Risposte analitiche illustrative a un ingresso rettangolare di 400 d con C/Cref = 1 e v = 0,24 m/d. Verde: sola advezione; blu: dispersività longitudinale di 10 m, D = 2,4 m²/d e diffusione molecolare nulla. Questi esempi fissi sono indipendenti dalle impostazioni attuali del modello.

## front_task

1. Selezionate ingresso continuo, 21 celle, differenze finite upwind e dispersione disattivata. Prevedete la posizione del fronte al giorno 2000 dalla velocità interstiziale.
2. Eseguite il modello e osservate le concentrazioni sui due lati del fronte analitico.
3. Ripetete con TVD e poi con 101 celle. Confrontate larghezza del fronte, errore del profilo e bilancio di massa.

## spreading_task

1. Usate ingresso continuo, dispersività di 10 m, diffusione nulla e TVD con 21 celle. Osservate il profilo analitico.
2. Ripetete con 101 celle e poi con differenze upwind. Quale parte dell’allargamento compare anche nella soluzione analitica?
3. Esaminate le curve a 250 m. Disattivate la dispersione per iniziare un confronto con sola advezione. Le modifiche in « Ingresso e trasporto » cancellano le varianti salvate.

## impulse_task

1. Scegliete un impulso rettangolare di 400 d e seguite i suoi fronti nel profilo e a 250 m.
2. Iniziate uno scenario Dirac con area di 50 d, durata numerica di 50 d, 101 celle e dispersività di 10 m. Annotate i RMSE per l’impulso applicato e quello ideale.
3. Riducete la durata a 10 d mantenendo l’area. Calcolate il nuovo scenario e confrontate gli errori annotati. Raffinate poi la sua griglia e controllate il bilancio di massa.

## theory

L’acquifero confinato è spesso 1 m e largo 1 m. I carichi imposti di circa 6,944 m e 0 m agiscono nei centri delle celle estreme, distanti 1000 m. Con $K=10^{-4}$ m/s e $n_e=0.25$, il flusso di Darcy è 0,06 m/d e la velocità interstiziale $v$ è 0,24 m/d. L’interno è inizialmente privo di soluto. L’acqua esce alla concentrazione locale. Il riferimento è $C_{\mathrm{ref}}=1$ g/m³, equivalente a 1 mg/L.

L’equazione è $\partial C/\partial t=D\partial^2 C/\partial x^2-v\partial C/\partial x$, con $D=\alpha_Lv+D_e$. Senza dispersione il segnale percorre $vt$. Per $D>0$, la risposta a un gradino unitario di concentrazione imposta in una colonna semi-infinita è

$$
S(x,t)=\tfrac12\left[\operatorname{erfc}\!\left(\frac{x-vt}{2\sqrt{Dt}}\right)
+e^{vx/D}\operatorname{erfc}\!\left(\frac{x+vt}{2\sqrt{Dt}}\right)\right],\quad t>0.
$$

Un ingresso continuo di altezza $H$ dà $HS(x,t)$. Un rettangolo di durata $\tau$ dà $H[S(x,t)-S(x,t-\tau)]$, con il secondo termine nullo prima dell’interruzione. Per un Dirac in ingresso con area $A=\int(C_{\mathrm{in}}/C_{\mathrm{ref}})dt$, la risposta interna è

$$
A\frac{\partial S}{\partial t}
=A\,\frac{x}{\sqrt{4\pi D t^3}}\exp\!\left[-\frac{(x-vt)^2}{4Dt}\right].
$$

MT3DMS applica un rettangolo di durata $\varepsilon$ e altezza $A/\varepsilon$, conservando l’area della storia di concentrazione all’ingresso. Il bilancio effettivo include anche il flusso dispersivo al contorno. Con $D=0$, il Dirac viaggia a $v$ e non ha un picco puntuale finito.

## profile_hint

I profili numerici usano le concentrazioni nei centri delle celle. I tempi intermedi sono interpolati linearmente tra passi salvati. Il giorno 2000 usa l’ultimo risultato del solutore.

## breakthrough_hint

Ogni passo di trasporto viene salvato. La concentrazione è interpolata tra centri di cella alla distanza scelta. Il tempo di transito per advezione è {t:.1f} d.

## balance_hint

Lo scarto cumulato con segno proviene da TOTAL IN–OUT nel file MAS ed è una percentuale della media delle masse assolute in ingresso e in uscita, incluso l’immagazzinamento. Un errore piccolo può coesistere con un fronte allargato.

## dirac_reading

La linea tratteggiata segue il rettangolo applicato. Quella punteggiata indica il Dirac ideale. Senza dispersione la linea verticale indica la sua posizione o il suo arrivo. L’altezza non rappresenta una concentrazione.

## outlet_hint

Per {ids}, il gradino analitico a 1000 m raggiunge almeno l’1 % al giorno 2000. L’uscita della colonna finita può influenzare il tratto a valle. Il controllo comprende anche gli impulsi, la cui concentrazione in uscita può essere inferiore.

## table_hint

Tutte le varianti sono valutate sugli stessi 90 intervalli di 10 m fra 50 e 950 m. RMSE e MAE confrontano il profilo finale con la soluzione analitica del segnale applicato, in C/Cref.

## mass_warning

{ids} supera l’1 % di errore assoluto di massa al giorno 2000. Esaminate bilancio e profilo. Un metodo a particelle può perdere un impulso breve su una griglia grossolana.

## metrics_notes

La concentrazione numerica è costante nella cella e viene mediata su ciascun intervallo di 10 m in proporzione alla sovrapposizione. La concentrazione analitica viene integrata sullo stesso intervallo. Le celle di contorno sono escluse anche sulla griglia più grossolana. RMSE è la radice della media dei residui al quadrato. MAE è la media dei residui assoluti.

Per Dirac, il RMSE aggiuntivo usa l’impulso ideale. Senza dispersione il suo peso spaziale è $vA$. Un impulso su un bordo condiviso contribuisce per metà a ciascun lato. Mantenete segnale e intensità costanti quando confrontate metodi.

Il tempo di calcolo comprende i due eseguibili, escludendo preparazione, lettura e grafici. Il bilancio idrico è l’ultimo scarto MODFLOW. Il numero di Péclet è $v\Delta x/D$, infinito per sola advezione. Le differenze centrate possono produrre concentrazioni fuori dall’intervallo di ingresso, visibili nei grafici.

## references

- `TRANS_1D_MT3D.ipynb`, MWW01.
- Zheng & Wang (1999), *MT3DMS*, 1. [MODFLOW benchmark](https://modflow6-examples.readthedocs.io/en/latest/_examples/ex-gwt-mt3dms-p01.html)
- Wexler (1992), *Analytical Solutions for One-, Two-, and Three-Dimensional Solute Transport in Ground-Water Systems with Uniform Flow*. [USGS TWRI 3-B7](https://pubs.usgs.gov/twri/twri3-b7/pdf/twri_3-B7_a.pdf)
- Pérez Guerrero et al. (2013), *Analytical solutions of the one-dimensional advection–dispersion solute transport equation subject to time-dependent boundary conditions*. [DOI](https://doi.org/10.1016/j.cej.2013.01.095)
- FloPy [MT3DMS ADV](https://flopy.readthedocs.io/en/latest/source/flopy.mt3d.mtadv.html), [MT3DMS SSM](https://flopy.readthedocs.io/en/latest/source/flopy.mt3d.mtssm.html).

## method_upwind

La concentrazione a monte determina il flusso advettivo sulla faccia. Osservate l’allargamento del fronte con dispersione fisica disattivata.

## method_central

Il flusso usa le concentrazioni sui due lati della faccia. Griglie grossolane dominate dall’advezione possono mostrare oscillazioni vicino a un fronte netto.

## method_tvd

ULTIMATE TVD del terzo ordine limita i flussi vicino a forti gradienti. Confrontate la larghezza del fronte con il metodo upwind.

## method_moc

Il metodo delle caratteristiche segue le particelle in avanti. Qui MT3DMS colloca inizialmente quattro particelle nelle celle con un gradiente di concentrazione sufficiente.

## method_mmoc

Il metodo delle caratteristiche modificato segue le traiettorie a ritroso per stimare la concentrazione che entra in una cella.

## method_hmoc

Il metodo ibrido alterna MOC e MMOC secondo il gradiente locale di concentrazione.

