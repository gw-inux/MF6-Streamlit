## introduction

Untersuchen Sie den konservativen Stofftransport entlang eines Grundwasserfließwegs mit einem einfachen eindimensionalen Modell. Vergleichen Sie MT3DMS mit analytischen Lösungen, um den Einfluss der Diskretisierung und der numerischen Verfahren auf das Transportsignal zu erkennen.

## concept_explanation

Stellen Sie sich eine schmale Stromröhre entlang eines Grundwasserfließwegs in einem homogenen, vollständig gesättigten Grundwasserleiter vor. Das Wasser strömt stationär entlang dieses Wegs. Am oberstromigen Ende tritt ein konservativer Stoff ein. Advektion transportiert ihn, und Dispersion kann das Signal entlang des Fließwegs verbreitern.

Mit diesem idealisierten eindimensionalen Modell lässt sich gezielt untersuchen, wie das numerische Transportverfahren, die Zellgröße und der Zeitschritt das berechnete Signal beeinflussen. Vergleichen Sie MT3DMS mit der analytischen Lösung und betrachten Sie Frontaufweitung, Oszillationen, Fließzeit und Massenbilanz. Legen Sie zuerst Eingangssignal und Transportprozesse fest und vergleichen Sie anschließend bis zu zehn numerische Varianten dieses Szenarios.

## concept_caption

Schematische Stromröhre mit stationärer eindimensionaler Strömung und einem Beobachtungspunkt bei 250 m. Über die seitlichen Grenzen treten weder Wasser noch Stoff aus; die Querabmessungen sind nicht maßstabsgetreu.

## concept_response_caption

Beispielhafte analytische Antworten auf einen 400 d langen Blockeintrag mit C/Cref = 1 und v = 0,24 m/d. Grün: reine Advektion; blau: longitudinale Dispersivität 10 m, D = 2,4 m²/d und keine molekulare Diffusion. Diese festen Beispiele sind unabhängig von den aktuellen Modelleinstellungen.

## front_task

1. Wählen Sie eine kontinuierliche Eingabe, 21 Zellen und das Upwind-Verfahren. Lassen Sie die Dispersion ausgeschaltet. Wie weit sollte sich die Front mit der gegebenen Abstandsgeschwindigkeit bis Tag 2000 bewegen?
2. Starten Sie das Modell. Bestimmen Sie die Lage der analytischen Front und betrachten Sie die numerischen Konzentrationen auf beiden Seiten.
3. Wiederholen Sie den Versuch mit TVD und anschließend mit 101 Zellen. Welche Änderung führt zu einer schärferen Front? Vergleichen Sie den Profilfehler mit dem Fehler der Stoffmassenbilanz.

## spreading_task

1. Wählen Sie eine kontinuierliche Eingabe, aktivieren Sie die Dispersion und stellen Sie die longitudinale Dispersivität auf 10 m. Belassen Sie die effektive Diffusion bei null. Rechnen Sie mit TVD und 21 Zellen und betrachten Sie das analytische Profil.
2. Wiederholen Sie den Lauf mit 101 Zellen und anschließend mit dem Upwind-Verfahren. Welcher Anteil der Aufweitung ist auch in der analytischen Lösung zu erkennen?
3. Betrachten Sie die Durchbruchskurven bei 250 m. Für einen Versuch mit reiner Advektion schalten Sie die Dispersion aus und beginnen einen neuen Vergleich. Änderungen unter „Einlass und Transport“ löschen die gespeicherten Varianten.

## impulse_task

1. Wählen Sie einen Rechteckpuls mit einer Dauer von 400 d. Verfolgen Sie seine Vorder- und Hinterkante im Profil und an der Beobachtungsstelle bei 250 m.
2. Beginnen Sie ein neues Szenario mit einem Dirac-Impuls der Fläche 50 d und einer numerischen Pulsbreite von 50 d. Verwenden Sie 101 Zellen und eine Dispersivität von 10 m. Notieren Sie die RMSE-Werte für den angelegten Puls und den idealen Impuls.
3. Verringern Sie bei gleicher Fläche die Pulsbreite auf 10 d und berechnen Sie das neue Szenario. Vergleichen Sie die notierten Fehler. Verfeinern Sie anschließend innerhalb dieses Szenarios das Gitter und prüfen Sie erneut die Stoffmassenbilanz.

## theory

Der gespannte Grundwasserleiter ist 1 m mächtig und 1 m breit. Die vorgegebenen hydraulischen Höhen von rund 6,944 m und 0 m liegen in den Mittelpunkten der ersten und letzten Zelle, die 1000 m voneinander entfernt sind. Bei $K=10^{-4}$ m/s und einer effektiven Porosität von $n_e=0{,}25$ ergeben sich eine Filtergeschwindigkeit von 0,06 m/d und eine Abstandsgeschwindigkeit $v$ von 0,24 m/d. Der Modellinnenraum ist anfangs stofffrei. Am Auslass tritt Wasser mit der dort berechneten Konzentration aus. Bezugsgröße für die Konzentrationen ist $C_{\mathrm{ref}}=1$ g/m³, entsprechend 1 mg/L.

Mit der longitudinalen Dispersivität $\alpha_L$ und der effektiven molekularen Diffusion $D_e$ lautet die Transportgleichung $\partial C/\partial t=D\,\partial^2 C/\partial x^2-v\,\partial C/\partial x$ mit $D=\alpha_L v+D_e$. Bei ausgeschalteter Dispersion legt das Signal in der Zeit $t$ die Strecke $vt$ zurück.

Für $D>0$ beschreibt die folgende Sprungantwort eine auf eins festgesetzte Einlasskonzentration in einer halbunendlichen Säule.

$$
S(x,t)=\tfrac12\left[\operatorname{erfc}\!\left(\frac{x-vt}{2\sqrt{Dt}}\right)
+e^{vx/D}\operatorname{erfc}\!\left(\frac{x+vt}{2\sqrt{Dt}}\right)\right],\quad t>0.
$$

Eine kontinuierliche Eingabe der Höhe $H$ liefert $HS(x,t)$. Ein Rechteckpuls der Dauer $\tau$ liefert $H[S(x,t)-S(x,t-\tau)]$. Bis zum Abschalten ist der zeitlich versetzte Term null.

Für einen idealen Dirac-Impuls am Einlass mit der Konzentrations-Zeit-Fläche $A=\int(C_{\mathrm{in}}/C_{\mathrm{ref}})\,dt$ gilt im Inneren

$$
A\frac{\partial S}{\partial t}
=A\,\frac{x}{\sqrt{4\pi D t^3}}\exp\!\left[-\frac{(x-vt)^2}{4Dt}\right].
$$

MT3DMS setzt einen Rechteckpuls der Breite $\varepsilon$ und Höhe $A/\varepsilon$ an. Dadurch bleibt die Fläche unter dem zeitlichen Verlauf der **Einlasskonzentration** erhalten. In die tatsächliche Stoffmassenbilanz geht auch der dispersive Fluss an diesem Rand ein. Bei $D=0$ bewegt sich der ideale Impuls mit $v$ und besitzt keinen endlichen Konzentrationshöchstwert.

## profile_hint

Die numerischen Profile zeigen die Konzentrationen in den Zellmittelpunkten. Für Zeitpunkte zwischen zwei gespeicherten Transportschritten wird linear interpoliert. Für Tag 2000 wird die letzte berechnete Lösung verwendet.

## breakthrough_hint

MT3DMS speichert jeden Transportschritt. Für die gewählte Beobachtungsentfernung wird die Konzentration zwischen benachbarten Zellmittelpunkten interpoliert. Die advektive Fließzeit bis zu diesem Ort beträgt {t:.1f} d.

## balance_hint

MT3DMS gibt die vorzeichenbehaftete kumulierte Stoffmassenabweichung in Prozent des Mittelwerts der absoluten Zu- und Abgänge einschließlich Speicheränderung an. Die Darstellung verwendet die Spalte TOTAL IN–OUT der MAS-Datei. Auch bei kleinem Bilanzfehler kann eine Front numerisch stark verbreitert sein.

## dirac_reading

Die gestrichelte Linie gehört zum endlichen MT3DMS-Eingangspuls. Die gepunktete Linie zeigt die Antwort auf den idealen Dirac-Impuls. Bei reiner Advektion markiert die gepunktete senkrechte Linie die Lage oder Ankunftszeit des Impulses. Ihre Höhe hat keine physikalische Bedeutung.

## outlet_hint

Für {ids} erreicht die analytische Antwort auf einen Einheitssprung bei 1000 m bis Tag 2000 mindestens 1 %. In der endlichen MT3DMS-Säule kann der Auslass den randnahen Profilabschnitt beeinflussen. Die Prüfung gilt auch für Pulse, deren Konzentration am Auslass geringer ausfallen kann.

## table_hint

Alle gespeicherten Varianten werden auf denselben 90 Intervallen von je 10 m zwischen 50 und 950 m ausgewertet. RMSE und MAE vergleichen das Endprofil mit der analytischen Lösung für das angelegte Eingangssignal. Beide Fehler sind in C/Cref angegeben.

## mass_warning

Für {ids} beträgt der absolute Stoffmassenbilanzfehler an Tag 2000 mehr als 1 %. Prüfen Sie neben dem Konzentrationsprofil auch den zeitlichen Verlauf der Bilanz. Auf einem groben Gitter kann ein Partikelverfahren einen kurzen Eingangspuls verfehlen.

## metrics_notes

Für den Vergleich gilt die numerische Konzentration innerhalb jeder Modellzelle als konstant. Ihr Beitrag zu jedem 10-m-Intervall wird nach der Länge der Überdeckung gewichtet. Die analytische Lösung wird über dasselbe Intervall integriert. Der gemeinsame Auswertebereich lässt selbst beim gröbsten Gitter beide Randzellen aus. RMSE ist die Wurzel des mittleren quadratischen Fehlers. MAE ist der mittlere absolute Fehler.

Bei einem Dirac-Eingang bezieht sich der zusätzliche RMSE auf den idealen Impuls in denselben Intervallen. Bei reiner Advektion beträgt dessen räumliches Gewicht $vA$. Liegt der Impuls auf der Grenze zweier Intervalle, wird jeder Seite die Hälfte zugerechnet. Die Fehler hängen von der Eingangsamplitude ab. Halten Sie beim Verfahrensvergleich Signalform und Stärke konstant.

Die Rechenzeit umfasst die Laufzeit der beiden ausführbaren Programme. Das Schreiben und Lesen der Dateien, die Diagrammerstellung und die Fehlerberechnung liegen außerhalb der Zeitmessung. Für die Wasserbilanz wird die letzte Bilanzabweichung im MODFLOW-Listing verwendet. Die Gitter-Péclet-Zahl beträgt $v\Delta x/D$ und ist bei reiner Advektion unendlich. Zentrierte Differenzen können Konzentrationen außerhalb des vorgegebenen Bereichs ergeben. Die Diagramme zeigen diese Werte.

## references

- Kursnotebook `TRANS_1D_MT3D.ipynb`, konservative Fälle 1 und 2. Die Voreinstellung mit 21 Zellen entspricht der Kursfassung des Vergleichsmodells.
- Zheng und Wang (1999), *MT3DMS*, Beispiel 1. [Beschreibung des Vergleichsmodells](https://modflow6-examples.readthedocs.io/en/latest/_examples/ex-gwt-mt3dms-p01.html)
- Wexler (1992), *Analytical Solutions for One-, Two-, and Three-Dimensional Solute Transport in Ground-Water Systems with Uniform Flow*, Beispiele mit vorgegebener Einlasskonzentration. [USGS TWRI 3-B7](https://pubs.usgs.gov/twri/twri3-b7/pdf/twri_3-B7_a.pdf)
- Pérez Guerrero und Koautoren (2013), *Analytical solutions of the one-dimensional advection–dispersion solute transport equation subject to time-dependent boundary conditions*. [DOI](https://doi.org/10.1016/j.cej.2013.01.095)
- FloPy-Dokumentation zum [Advektionspaket](https://flopy.readthedocs.io/en/latest/source/flopy.mt3d.mtadv.html) und zur [Vorgabe der Einlasskonzentration](https://flopy.readthedocs.io/en/latest/source/flopy.mt3d.mtssm.html).

## method_upwind

Die Konzentration in der oberstromigen Zelle bestimmt den advektiven Fluss über die Zellgrenze. Achten Sie bei ausgeschalteter Dispersion auf die Breite der Front.

## method_central

Der Fluss über eine Zellgrenze berücksichtigt die Konzentrationen auf beiden Seiten. Bei advektionsdominiertem Transport können auf groben Gittern Oszillationen an einer scharfen Front entstehen.

## method_tvd

Das ULTIMATE-TVD-Verfahren dritter Ordnung begrenzt die advektiven Flüsse bei starken Gradienten. Vergleichen Sie die Frontbreite mit dem Upwind-Verfahren.

## method_moc

Die Charakteristikenmethode verfolgt Partikel vorwärts. In Zellen mit hinreichend starkem Konzentrationsgradienten platziert MT3DMS hier anfangs vier Partikel.

## method_mmoc

Die modifizierte Charakteristikenmethode verfolgt Bahnen rückwärts und schätzt so die in eine Zelle transportierte Konzentration.

## method_hmoc

Die hybride Methode wechselt abhängig vom lokalen Konzentrationsgradienten zwischen der vorwärts gerichteten MOC und der rückwärts gerichteten MMOC.
