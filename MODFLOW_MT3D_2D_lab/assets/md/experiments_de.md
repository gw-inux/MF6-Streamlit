### 1. Einen endlichen Stoffpuls verfolgen

1. Beginnen Sie mit dem homogenen Einschichtmodell und TVD. Schätzen Sie vor der Berechnung den Transportweg vt und die Gesamtmasse $\dot M\tau$.
2. Berechnen Sie das Modell. Verfolgen Sie die Vorder- und Rückseite der Stofffahne über die gespeicherten Zeiten.
3. Vergleichen Sie x-/y-Profile und Durchbruchskurve. Warum dauert das Signal am Beobachtungspunkt länger als der Quellpuls?
4. Aktivieren Sie die analytische Referenz im rechten farbigen Feld. Garantiert eine gute Massenbilanz auch eine gute Stofffahnenform?

### 2. Physische und numerische Verbreiterung trennen

1. Schalten Sie unter **Transport und Quelle** die Dispersion aus und vergleichen Sie FD up, FD cen und TVD bei gleicher Quelle und gleichem Gitter.
2. Aktivieren Sie **Schnittprofile vergleichen** und wählen Sie die Läufe aus. Beachten Sie negative Konzentrationen und verbleibende Frontverbreiterung.
3. Aktivieren Sie Dispersion erneut. Welcher Anteil der Verbreiterung tritt auch in der analytischen Lösung auf?
4. Verfeinern Sie das Gitter über Zellanzahl oder Zellweite. Die Läufe bleiben in derselben Reihe. Prüfen Sie die tatsächliche Quellgröße: Eine feste Zahl von Quellzellen verändert bei Verfeinerung das physische Quellvolumen.

### 3. Charakteristikenverfahren untersuchen

1. Vergleichen Sie MOC, MMOC und HMOC mit TVD im Pulsexperiment.
2. Erhöhen Sie unter den Experteneinstellungen die zum Verfahren gehörenden Partikeldichten.
3. Vergleichen Sie Rechenzeit und Massenabweichung mit Fahnenform und Durchbruchskurve. Ist der teuerste Lauf auch der genaueste?
4. Verringern Sie PERCEL. Warum kann eine stabil laufende Berechnung trotzdem vom Transportzeitschritt abhängen?

### 4. Dirac-Zugabe und endlichen Puls vergleichen

1. Wählen Sie Dirac und verfolgen Sie das endliche anfängliche Quellvolumen.
2. Exportieren Sie das Ergebnis. Wechseln Sie anschließend zu einem kurzen Puls mit derselben Gesamtmasse $M=\dot M\tau$. Der Signalwechsel beginnt bewusst eine neue Vergleichsreihe.
3. Vergleichen Sie frühe und späte Fahnenformen anhand der exportierten Resultate. Warum unterscheiden sie sich trotz gleicher Masse nahe der Quelle?
4. Ergänzen Sie unter **Auswertung und Beobachtungen** weitere Beobachtungen, auch seitlich versetzt. Ordnen Sie Laufzeit und Spitzenkonzentration der longitudinalen bzw. transversalen Ausbreitung zu.

### 5. Hydrogeologie und Zufallsmuster

1. Wählen Sie unter **Strömung und Modellgebiet** die niedrig leitende Linse. Vergleichen Sie Stofffahne und MODPATH-Bahnen.
2. Untersuchen Sie hoch leitende Rinne und teilweise Barriere. Verschieben Sie die Schnittpositionen durch und neben die Struktur.
3. Wählen Sie zufällige stochastische Parameter. Variieren Sie die K-Spannweite und die physische Einheitengröße. Halten Sie den Zufallsstartwert zunächst fest.
4. Verfeinern Sie das Gitter bei unveränderten Einheitengrößen: Die geologische Realisierung bleibt erhalten. Ändern Sie anschließend den Startwert, um eine andere Realisierung zu untersuchen.
5. Begründen Sie, warum die homogene analytische Referenz hier nicht als Genauigkeitsmaß verwendet wird.

### 6. Das stationäre Strömungsfeld lesen

1. Vergleichen Sie die berechneten Potentiallinien für homogenes Material, eine Linse mit geringem K und ein Zufallsmuster. Erklären Sie Änderungen von Gradienten und Partikelbahnen.
2. Ändern Sie die Differenz der vorgegebenen Potentialhöhen. Vergleichen Sie Stofftransport und MODPATH bei unverändertem Signal und unveränderter Quellgeometrie.
3. Ändern Sie Ss bei sonst gleichen Einstellungen. Warum bleiben Strömung und Transport bei diesem stationären Experiment unverändert?
4. Verfeinern Sie das numerische Gitter bei festen physischen Zufallseinheiten. Welche Strukturen kann das grobe Gitter auflösen?

### 7. Auf 3D erweitern

1. Aktivieren Sie Experteneinstellungen und mindestens drei Schichten. Begrenzen Sie die Quelle anschließend auf eine Schicht; diese Quellenänderung startet eine neue Reihe.
2. Betrachten Sie x–z- und y–z-Schnitte. Erhöhen Sie das vertikale transversale Dispersivitätsverhältnis und vergleichen Sie die Läufe über **Schnittprofile vergleichen**.
3. Wählen Sie das Zufallsmuster und vergleichen Sie Partikelbahnen und Konzentrationsschnitte. Dasselbe horizontale Materialmuster gilt in allen Schichten. Vertikale Stoffausbreitung entsteht durch die begrenzte Quelle und vertikale Dispersion.
4. Wiederholen Sie das Experiment mit einer über alle Schichten gleichmäßigen Quelle und homogenem Material. Warum wird die Lösung vertikal gleichmäßig, obwohl das Gitter dreidimensional bleibt?

Formulieren Sie jeweils zuerst eine Erwartung, vergleichen Sie diese mit dem Ergebnis und begründen Sie Ihre Erklärung anhand der numerischen Diagnose.
