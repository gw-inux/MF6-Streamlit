### Konzept

Das Labor verfolgt einen konservativen Stoff in einem vollständig gesättigten, gespannten Aquifer. Vorgegebene Potentialhöhen in der ersten und letzten Spalte erzeugen die Hintergrundströmung. Die übrigen Außenflächen sind für Grundwasserströmung und dispersiven Stofffluss geschlossen. Einströmendes Wasser an den Potentialrändern ist unbelastet; ausströmendes Wasser führt die lokale Konzentration mit. Reaktionen, Sorption, Dichteeffekte, Neubildung und Brunnen werden nicht berücksichtigt.

Das Grundexperiment besteht aus einer Schicht und beschreibt horizontalen 2D-Transport. Zusätzliche Schichten ermöglichen vertikale Konzentrationsgradienten und vertikale Ausbreitung. Eine homogene, über alle Schichten gleichmäßige Quelle bleibt vertikal gleichmäßig: Zusätzliche Schichten allein erzeugen keine vertikale Strömung. Materialzonen und eine Quelle in nur einer Schicht ermöglichen echte 3D-Untersuchungen.

Längen werden in Metern, Zeiten in Tagen, Massen in Gramm und Konzentrationen in g/m³ Wasser angegeben. Zahlenmäßig gilt 1 g/m³ = 1 mg/L. Die interne K-Einheit ist m/Tag; $10^{-4}$ m/s entsprechen 8,64 m/Tag.

### Strömung und Speicherung

Bei homogener stationärer Strömung beträgt die Abstandsgeschwindigkeit

$$v_x=\frac{K}{n_e}\frac{h_L-h_R}{L-\Delta x}.$$

Der Nenner ist der Abstand zwischen den Mittelpunkten der Randzellen mit vorgegebener Potentialhöhe, nicht der Abstand zwischen den äußeren Modellflächen. Bei Heterogenität berechnet MODFLOW das ungleichmäßige Strömungsfeld aus den Zellleitfähigkeiten. Vertikales K ist das lokale horizontale K, multipliziert mit dem gewählten Verhältnis.

Das interaktive Labor verwendet stationäre Strömung. Der spezifische Speicherkoeffizient $S_s$ wird als Materialeigenschaft gespeichert, beeinflusst jedoch weder stationäre Potentialhöhen noch Geschwindigkeiten. Der Aquifer ist gespannt; alle vorgegebenen Potentialhöhen müssen mindestens auf Höhe der Aquiferoberkante liegen. Die spezifische Ergiebigkeit wird nicht verwendet.

### Eingangssignale

| Signal | Numerische Darstellung | Vorgegebene Größe |
|---|---|---|
| Dirac / momentane Stoffzugabe | Gleichmäßige Anfangskonzentration in den Quellzellen bei t = 0 | Anfangsmasse $M$ |
| Endlicher Puls / Block | Massenrate $\dot M$ bis zum Abschaltzeitpunkt $\tau$ | Gesamtmasse $\dot M\tau$ |
| Kontinuierliche Eingabe | Massenrate $\dot M$ während der gesamten Modellzeit | Masse bis t: $\dot M t$ |

Die Quellen fügen Stoffmasse ohne zusätzliches Wasser hinzu und verändern daher die Hintergrundströmung nicht. Ein Puls wird exakt an einer Belastungsperiodengrenze abgeschaltet. Die numerische Dirac-Quelle ist zeitlich momentan, räumlich jedoch auf die ausgewählten Zellen verteilt. Bei homogener Porosität ist die Anfangskonzentration $M/(n_e V_s)$. Unterschiedliche Quellporositäten werden über das Porenvolumen gewichtet.

Quellposition und -größe werden auf Zellen abgebildet. Bei gleicher Anzahl von Quellzellen verändert eine Gitterverfeinerung die physische Quellgröße. Die Vorschau und die erweiterte Vergleichstabelle zeigen die tatsächlich verwendeten Abmessungen.

### Advektion und Dispersion

Für homogene stationäre Strömung in x-Richtung gilt

$$\frac{\partial C}{\partial t}=D_x\frac{\partial^2 C}{\partial x^2}+D_y\frac{\partial^2 C}{\partial y^2}+D_z\frac{\partial^2 C}{\partial z^2}-v_x\frac{\partial C}{\partial x}+\frac{s}{n_e}.$$

Dabei ist s der Stoffeintrag je Gesamtvolumen und Zeit. In diesem Lehrmodell wird molekulare Diffusion nicht eingestellt; sie ist null. Für gleichmäßige Strömung gilt $D_x=\alpha_L|v_x|$, $D_y=\alpha_{TH}|v_x|$ und $D_z=\alpha_{TV}|v_x|$. Transversale Dispersivitäten werden als Verhältnis zu $\alpha_L$ eingegeben. In heterogenen Strömungsfeldern verwendet MT3D den lokalen Geschwindigkeitstensor.

Bei genau einer Modellschicht gibt es keinen Konzentrationsgradienten zwischen vertikalen Zellen und keinen Stoffaustausch über Ober- oder Unterkante. Die vertikale transversale Dispersivität beeinflusst dieses 2D-Modell daher nicht und wird erst bei mehreren Schichten angezeigt. Mit ausgeschalteter Dispersion verbleibt ausschließlich Advektion einschließlich numerischer Fehler.

| Verfahren | MT3D-Option | Untersuchungsziel |
|---|---|---|
| FD up | MIXELM = 0, NADVFD = 0 | Numerische Verbreiterung der Front |
| FD cen | MIXELM = 0, NADVFD = 2 | Oszillationen und negative Konzentrationen bei grobem Gitter |
| TVD | MIXELM = −1 | Scharfe Fronten mit begrenzten Oszillationen |
| MOC | MIXELM = 1 | Vorwärts-Charakteristiken; Einfluss der Partikeldichte |
| MMOC | MIXELM = 2 | Rückwärts-Charakteristiken; Einfluss auf die Massenbilanz |
| HMOC | MIXELM = 3 | Lokaler Wechsel zwischen MOC und MMOC |

FD cen ist ein zentrales Verfahren, kein Downwind-Verfahren. Die Experteneinstellungen enthalten ADV-, GCG- und Transportzeitschrittparameter sowie MODFLOW-Toleranzen. Einige Parameter wirken nur bei bestimmten Verfahren. PERCEL begrenzt die advektive Bewegung je Transportzeitschritt; bei TVD darf es höchstens 1 sein. Erfolgreiche Programmbeendigung ist kein Genauigkeitsnachweis.

### Analytische Referenz

Die Referenz verwendet konstante Geschwindigkeit, Porosität und Dispersion. Sie integriert die Greensche Funktion sowohl über die tatsächliche Quelle als auch über jede empfangende Zelle. y- und z-Ränder reflektieren Stoff; x wird als unendlich angenommen. Die einschichtige Lösung reduziert sich damit korrekt auf den mächtigkeitsbezogenen 2D-Fall. Puls- und Dauereinträge ergeben sich durch zeitliche Faltung desselben Kerns.

Für eine momentane Punktquelle im unendlichen 3D-Raum gilt

$$C=\frac{M}{n_e(4\pi t)^{3/2}\sqrt{D_xD_yD_z}}\exp\left[-\frac{(x-x_s-v_xt)^2}{4D_xt}-\frac{(y-y_s)^2}{4D_yt}-\frac{(z-z_s)^2}{4D_zt}\right].$$

Im horizontalen 2D-Fall wird der Nenner durch $4\pi n_e b t\sqrt{D_xD_y}$ ersetzt und der z-Term entfällt. Diese Punktquellenformeln erklären die Form; der numerische Vergleich integriert die endlichen Zellvolumina.

Für zonierte oder instationäre Strömung ist diese homogene Referenz nicht exakt und wird daher nicht als Genauigkeitsmaß verwendet. Ein kumulatives Grenzübertrittskriterium prüft die Nähe zu den x-Rändern. Überschreitet der geschätzte Einfluss 0,5 %, entfällt der Genauigkeitsvergleich. Eine Sensitivitätsprüfung der Gebietsgröße bleibt sinnvoll.

### MODPATH und Ergebnisvergleich

MODPATH 7 verwendet das MODFLOW-Strömungsfeld und dieselbe effektive Porosität. Es berechnet advektive Bahnen und Laufzeiten, aber keine Dispersion oder gelöste Konzentration. Partikelwolken dürfen deshalb nicht als dispersive Stofffahnen gelesen werden. MOC-Partikel in MT3D und MODPATH-Partikel haben unterschiedliche Aufgaben.

Vergleichen Sie Stofffahne, x-/y-Profile und Durchbruchskurven zusammen mit Bilanz und Rechenzeit. Kleine Bilanzabweichungen schließen starke numerische Verbreiterung oder Oszillationen nicht aus. Negative Konzentrationen bleiben in Daten und Diagnose erhalten; eine logarithmische Darstellung kann sie nicht anzeigen.

Beobachtungen und Schnitte verwenden die jeweilige Modellzelle; ihre tatsächliche Lage wird ausgewiesen. Neue Läufe werden unmittelbar angezeigt. Änderungen des Eingangssignals oder der physischen Modell-/Quellgeometrie leeren die Vergleichsreihe. Änderungen von Zellanzahl und Zellweite bleiben Varianten. Ein Laufarchiv bewahrt Eingaben und Resultate für spätere Auswertung.

### Quellen

- [MT3D-Advektionsparameter — FloPy](https://flopy.readthedocs.io/en/latest/source/flopy.mt3d.mtadv.html)
- [MT3D-Dispersion — FloPy](https://flopy.readthedocs.io/en/3.4.2/source/flopy.mt3d.mtdsp.html)
- [MT3D-Masseneintragsquellen — FloPy](https://flopy.readthedocs.io/en/latest/source/flopy.mt3d.mtssm.html)
- [Pollock (2016), MODPATH 7 — USGS](https://pubs.usgs.gov/publication/ofr20161086)
- [Wexler (1992), analytische Transportlösungen — USGS](https://pubs.usgs.gov/twri/twri3-b7/)

### Heterogenität und Vergleichsreihen

Zur Auswahl stehen homogen, zufällige stochastische Parameter, eine Linse mit geringem K, ein Kanal mit hohem K und eine partielle Barriere mit geringem K. Die Übersicht zeigt das Hintergrundmaterial weiß und abweichende K-Werte farbig; die Legende nennt K in m/s. Zufallsparameter werden auf einem physischen Raster vergeben. Kleine Einheiten erzeugen ein feines zellweises Muster, größere Einheiten größere Bereiche. K und Ss werden gleichverteilt im logarithmischen Raum gezogen, die Porosität gleichverteilt. Dasselbe horizontale Muster gilt in allen Schichten. Es handelt sich um ein didaktisches Zufallsmuster und nicht um ein geostatistisches Feld mit vorgegebener Kovarianz.

Bei unverändertem Seed und unveränderten physischen Einheitengrößen bleibt die Realisierung bei Netzverfeinerung erhalten. Eine numerische Zelle übernimmt die Parameter der Einheit an ihrem Mittelpunkt. Ein grobes Netz kann kleine Strukturen übergehen. Die alten Eingabeformate für Rechteckzonen und instationäre Strömung bleiben zur Reproduktion älterer exportierter Konfigurationen außerhalb der Oberfläche lesbar.

Der neueste abgeschlossene Lauf wird automatisch angezeigt. Änderungen am Signal oder an der physischen Modell- bzw. Quellengeometrie beginnen eine neue Vergleichsreihe. Zellzahlen, Zellweiten und Lösungsparameter bleiben Varianten. Die Quelle wird auf Zellen abgebildet; ihre tatsächlichen Abmessungen sind nach einer Verfeinerung zu prüfen. FD cen bezeichnet zentrale finite Differenzen.

Markierungen der Vergleichsläufe können mit × entfernt werden. Der angezeigte Lauf ist separat wählbar. Die Draufsicht der Ergebnisse enthält standardmäßig berechnete Potentiallinien (h in Metern). Bei einer Schicht zeigen die x/y-Diagramme Konzentrationsprofile. Bei mehreren Schichten zeigen die x–z- und y–z-Schnitte die Konzentration durch Farben und beschriftete Konturen über der Höhe; die Konzentrationseinheit entspricht der Draufsicht.

### Fahnenzoom und Laufnamen

Heterogene Läufe erhalten den Zusatz **het.**; die Namen bleiben beim Sprachwechsel unverändert. Der Fahnenzoom nutzt standardmäßig 0,1 % des aktuellen positiven Maximums jeder dargestellten Fahne in der Draufsicht. Die Schwelle ist einstellbar. Um die betreffenden Zellränder kommen auf jeder Seite 20 % Rand hinzu; sichtbare, auf den Anzeigezeitpunkt begrenzte MODPATH-Bahnen bleiben enthalten. Ohne Fahne und Bahnen bleibt die Gesamtansicht erhalten. Nur die Achsengrenzen der Draufsicht ändern sich, nicht Konzentrationen, Schnitte oder Farbnormierung.
