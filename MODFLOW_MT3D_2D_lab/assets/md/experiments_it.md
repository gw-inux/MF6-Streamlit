I controlli sono in **Flusso e dominio**, **Trasporto e sorgente** e **Post-elaborazione e osservazioni**. Il confronto dei profili sovrappone le esecuzioni; il riferimento analitico è a destra.

### 1. Seguire un impulso
Prevedi $vt$ e $\dot M\tau$ nel caso omogeneo TVD. Esegui e scorri i tempi, individuando fronte e coda. Confronta profili, arrivi e riferimento. Perché l'arrivo dura più dell'impulso? Un buon bilancio garantisce la forma corretta?

### 2. Separare allargamento fisico e numerico
Senza dispersione, confronta FD up, FD cen e TVD a sorgente/griglia fisse. Annota tempo, minimo, scarto di massa ed errore analitico. Ripristina dispersione e ripeti, poi raffina. Controlla il volume effettivo della sorgente.

### 3. Metodi delle caratteristiche
Confronta MOC, MMOC, HMOC e TVD. Aumenta la densità delle particelle pertinente in modalità esperta. Confronta costo, bilancio, pennacchio e arrivi. Riduci PERCEL: perché una soluzione stabile dipende ancora dal passo?

### 4. Dirac e impulso
Segui ed esporta un rilascio Dirac, poi scegli un impulso breve di uguale massa $M=\dot M\tau$. Il cambio di segnale apre una nuova serie. Confronta gli archivi a tempi precoci e tardivi. Aggiungi osservazioni spostate lungo y e spiega i picchi.

### 5. Contrasti di K
Aggiungi una lente a K bassa fra sorgente e osservazione. Confronta pennacchio e MODPATH, spiegando deviazioni e tempi. Prova canale, barriera e trame casuali fini/grossolane. Nel raffinamento mantieni seme e unità fisiche. Perché l'errore analitico omogeneo non è disponibile?

### 6. Leggere il flusso stazionario
Confronta isopieze omogenee, lente e casuale. Cambia differenza di carico a sorgente fissa. Cambia solo Ss: perché il risultato resta identico? Quali strutture sfuggono alla griglia grossolana?

### 7. Estendere al 3D
Usa almeno tre strati e una sorgente in uno solo. Esamina x–z/y–z aumentando la dispersività verticale. La trama casuale orizzontale attraversa ogni strato. Ripeti con materiale omogeneo e sorgente sull'intero spessore: perché la soluzione è uniforme verticalmente?

Formula previsioni prima di ogni esecuzione e sostieni le interpretazioni con i diagnostici. L'ingrandimento mostra dettagli senza modificare risultati.
