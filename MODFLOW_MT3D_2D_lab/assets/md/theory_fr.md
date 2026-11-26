### Modèle conceptuel
Un soluté conservatif traverse un aquifère captif entièrement saturé. Des charges imposées dans les première et dernière colonnes créent l'écoulement de fond. Les autres faces sont imperméables à l'eau et au flux dispersif. L'eau entrante aux limites a une concentration nulle ; l'eau sortante emporte la concentration résidente. Réactions, sorption, effets de densité, recharge et pompage sont absents.

Une couche représente le transport horizontal 2D. Plusieurs couches permettent des gradients et une dispersion verticaux. Une source uniforme sur toute l'épaisseur en milieu homogène reste uniforme verticalement : ajouter des couches ne crée pas d'écoulement vertical. Une source localisée dans une couche permet d'étudier le transport 3D.

Unités : m, j, g et g/m³ d'eau ; 1 g/m³ = 1 mg/L. Le code utilise K en m/j : $10^{-4}$ m/s = 8,64 m/j.

### Écoulement et stockage
En régime permanent homogène, la vitesse interstitielle vaut :
$$
v_x=\frac{K}{n_e}\frac{h_L-h_R}{L-\Delta x}.
$$
La distance est celle entre les **centres des cellules** à charge imposée, $L-\Delta x$. MODFLOW calcule le champ non uniforme à partir des K locaux en milieu hétérogène. K vertical est K horizontal local multiplié par le rapport choisi.

L'interface utilise un écoulement permanent. L'emmagasinement spécifique $S_s$ est conservé comme propriété, mais n'influence ni charges ni vitesses permanentes. Toutes les charges imposées doivent rester au moins à la cote du toit ; le coefficient d'emmagasinement libre n'est pas utilisé.

### Signaux d'entrée
| Signal | Représentation | Quantité conservée |
|---|---|---|
| Dirac | Concentration initiale uniforme dans les cellules source | Masse initiale $M$ |
| Créneau | Débit massique prescrit jusqu'à l'arrêt à $\tau$ | Masse $\dot M\tau$ |
| Continu | Débit massique prescrit sur toute la durée | Masse apportée à $t$ : $\dot M t$ |

Ces sources internes apportent du soluté sans eau et ne perturbent pas l'écoulement. Le créneau est arrêté à une limite de période de contrainte, puis son débit massique est explicitement nul. Dirac est instantané dans le temps, mais occupe un volume fini. Sa concentration initiale est $M/(n_eV_s)$ en milieu homogène ; des porosités différentes sont pondérées par le volume poreux pour obtenir la même concentration initiale.

La source suit les cellules sélectionnées. Vérifiez position et dimensions réalisées après raffinement : conserver le nombre de cellules source change aussi son volume physique.

### Advection et dispersion
Pour un écoulement homogène permanent selon x :
$$
\frac{\partial C}{\partial t}
=D_x\frac{\partial^2 C}{\partial x^2}
+D_y\frac{\partial^2 C}{\partial y^2}
+D_z\frac{\partial^2 C}{\partial z^2}
-v_x\frac{\partial C}{\partial x}+\frac{s}{n_e}.
$$
$s$ est l'apport de soluté par unité de volume total et de temps. $D_x=\alpha_L|v_x|+D_e$, $D_y=\alpha_{TH}|v_x|+D_e$ et $D_z=\alpha_{TV}|v_x|+D_e$. Les dispersivités transversales sont saisies comme rapports à $\alpha_L$. En milieu hétérogène, MT3D utilise les vitesses locales pour construire le tenseur. La diffusion moléculaire est fixée à zéro ; désactiver la dispersion supprime l'étalement mécanique. Avec une couche et des faces supérieure/inférieure fermées, la dispersivité verticale n'a aucun effet : son réglage n'apparaît qu'avec plusieurs couches.

| Méthode | Option MT3D | À examiner |
|---|---|---|
| FD up | MIXELM = 0, NADVFD = 0 | Étalement numérique des fronts |
| FD cen | MIXELM = 0, NADVFD = 2 | Oscillations et valeurs négatives sur maillage grossier dominé par l'advection |
| TVD | MIXELM = −1 | Fronts nets et limitation des flux |
| MOC | MIXELM = 1 | Caractéristiques vers l'avant ; densité particulaire |
| MMOC | MIXELM = 2 | Caractéristiques vers l'arrière ; bilan massique |
| HMOC | MIXELM = 3 | Commutation locale MOC/MMOC |

Le mode expert donne accès aux contrôles d'advection, au solveur GCG, aux pas de transport et aux tolérances MODFLOW. Certains réglages ne concernent que certaines méthodes : MXPART limite les particules mobiles de MOC/HMOC. PERCEL limite leur déplacement par pas ; TVD exige PERCEL ≤ 1. Une terminaison normale ne démontre pas l'exactitude.

### Référence analytique
La référence suppose vitesse, porosité et dispersion constantes. Elle intègre la fonction de Green sur le **volume source réel** et sur chaque cellule réceptrice. Les limites y/z réfléchissent le soluté ; x est infini. Une source sur toute l'épaisseur à une couche donne la solution 2D normalisée par l'épaisseur. Les apports créneau/continu utilisent une convolution temporelle.

La solution ponctuelle instantanée 3D non bornée est :
$$
C=\frac{M}{n_e(4\pi t)^{3/2}\sqrt{D_xD_yD_z}}
\exp\!\left[-\frac{(x-x_s-v_xt)^2}{4D_xt}
-\frac{(y-y_s)^2}{4D_yt}-\frac{(z-z_s)^2}{4D_zt}\right].
$$
En 2D horizontale, le dénominateur devient $4\pi n_e b t\sqrt{D_xD_y}$ et le terme z disparaît. Ces équations expliquent la forme ; la comparaison utilise des volumes finis pour respecter la dilution de MT3D.

La référence homogène n'est pas exacte en milieu zoné ou en régime transitoire : les erreurs analytiques y sont désactivées. Les limites x doivent rester éloignées du panache. Le contrôle de rétention de masse signale leur proximité, sans prouver l'identité des domaines fini et infini. Agrandissez le domaine pour vérifier la sensibilité près des limites.

### MODPATH et lecture des résultats
MODPATH 7 suit l'advection dans le champ MODFLOW avec la même porosité. Il ne calcule ni dispersion ni concentration. La largeur du nuage particulaire n'est donc pas celle d'un panache dispersif. La masse associée aux particules est un poids de quadrature de la libération, pas un bilan de soluté MODPATH. Les particules MOC ont une autre fonction.

Comparez formes, restitutions et tableau. Un faible écart de bilan peut masquer étalement ou oscillations. Gardez source, propriétés et maillage fixes pour comparer les méthodes. Les temps réels dépendent de la charge de la machine ; répétez les calculs sur la même machine. Les observations utilisent la cellule contenant le point ; les coupes suivent les sections du maillage. Les concentrations signées sont conservées. Une échelle logarithmique masque les valeurs non positives : examinez aussi la vue linéaire et le minimum.

### Hétérogénéité, séries et zoom
Préréglages : homogène, paramètres aléatoires, lentille faible K, chenal K élevé, barrière partielle faible K. Le fond de référence est blanc ; les contrastes sont colorés et la légende indique K en m/s. Les unités aléatoires forment un réseau physique : petites unités, motif fin ; grandes unités, grandes plages. K et Ss sont uniformes en espace logarithmique, la porosité en espace linéaire. Le motif horizontal traverse toutes les couches. Il ne s'agit pas d'un champ géostatistique à covariance prescrite.

Graine et tailles physiques fixes préservent la réalisation pendant le raffinement. Chaque cellule échantillonne l'unité contenant son centre ; un maillage grossier peut manquer de petites structures. Les anciens formats rectangulaires/transitoires restent reproductibles hors interface.

Le dernier calcul est affiché automatiquement. Signal et géométrie physique changés ouvrent une nouvelle série ; discrétisation et paramètres numériques restent des variantes. Le suffixe **het.** distingue les modèles hétérogènes. Les étiquettes × suppriment les calculs. Les isopièzes calculées sont affichées par défaut. Une couche : profils de concentration x/y ; plusieurs couches : cartes de concentration x–z/y–z avec altitude.

Le zoom utilise par défaut **0,1 % du maximum positif actuel** de chaque panache affiché, avec **20 % de marge par côté**, et inclut les trajectoires MODPATH visibles. Le seuil est modifiable ; sans panache ni trajectoire, le domaine complet reste visible. Seules les limites de la vue de dessus changent, pas les concentrations, les coupes ou la normalisation des couleurs.

### Références
Les quatre applications analytiques fournies ont inspiré les exemples. Leurs formules ponctuelles ou à concentration imposée ne remplacent pas directement le benchmark à source massique de volume fini utilisé ici.


- [FloPy — MT3DMS ADV](https://flopy.readthedocs.io/en/3.12.0/source/flopy.mt3d.mtadv.html)
- [FloPy — MT3DMS SSM](https://flopy.readthedocs.io/en/3.12.0/source/flopy.mt3d.mtssm.html)
- [FloPy — MT3DMS GCG](https://flopy.readthedocs.io/en/3.12.0/source/flopy.mt3d.mtgcg.html)
- [Pollock (2016) — MODPATH 7, USGS](https://pubs.usgs.gov/publication/ofr20161086)
- [Wexler (1992) — USGS](https://pubs.usgs.gov/twri/twri3-b7/)
- [MODFLOW-ORG](https://github.com/MODFLOW-ORG/executables)

### Maillage, coordonnées relatives et largeur

Le maillage ajoute de fines limites grises aux cellules du calcul affiché, en plan et en coupe ; les profils monocouches ont des repères verticaux aux bords des cellules. Les coordonnées x′/y′ prennent pour origine le barycentre de masse dissoute positive de la couche affichée, avec sa porosité locale. Sans masse positive, le centre de la source maillée sert d’origine. Comparaisons, référence et particules partagent cette origine ; cotes, entrées et exports numériques restent absolus. Ce réglage est indépendant du zoom. Cinq largeurs sont disponibles en haut ; Standard conserve l’ancienne largeur. Le champ de nom jaune devient vert après validation d’un texte non vide par Entrée ou en quittant le champ.
