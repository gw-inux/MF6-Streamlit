## introduction

Étudiez le transport d’un soluté conservatif le long d’un trajet d’écoulement souterrain à l’aide d’un modèle unidimensionnel simple. Comparez MT3DMS aux solutions analytiques pour observer l’influence de la discrétisation et des méthodes numériques sur le signal transporté.

## concept_explanation

Imaginez un tube de courant étroit suivant un trajet d’écoulement dans un aquifère homogène et saturé. L’eau y circule en régime permanent. Un soluté conservatif entre à l’amont et est transporté par advection. La dispersion peut étaler le signal le long du trajet.

Ce modèle unidimensionnel idéalisé permet d’étudier l’effet de la méthode numérique, de la taille des cellules et du pas de temps. Comparez MT3DMS à la solution analytique pour examiner l’étalement du front, les oscillations, le temps de parcours et le bilan de masse. Définissez d’abord le signal d’entrée et les processus, puis comparez jusqu’à dix variantes numériques de ce scénario.

## concept_caption

Tube de courant schématique avec un écoulement permanent unidimensionnel et un point d’observation à 250 m. Aucun échange d’eau ou de soluté ne traverse les limites latérales ; les dimensions transversales ne sont pas à l’échelle.

## concept_response_caption

Réponses analytiques illustratives à un apport en créneau de 400 d avec C/Cref = 1 et v = 0,24 m/d. Vert : advection seule ; bleu : dispersivité longitudinale de 10 m, D = 2,4 m²/d et diffusion moléculaire nulle. Ces exemples fixes sont indépendants des paramètres actuels du modèle.

## front_task

1. Choisissez une entrée continue, 21 cellules, les différences finies amont et une dispersion nulle. Prévoyez la position du front au jour 2000 à partir de la vitesse interstitielle.
2. Lancez le calcul et comparez les concentrations numériques de part et d’autre du front analytique.
3. Recommencez avec TVD, puis 101 cellules. Comparez la largeur du front, l’erreur du profil et le bilan de masse.

## spreading_task

1. Utilisez une entrée continue, une dispersivité de 10 m, une diffusion nulle et TVD avec 21 cellules. Examinez le profil analytique.
2. Recommencez avec 101 cellules, puis les différences amont. Quelle part de l’étalement apparaît dans la solution analytique ?
3. Examinez la courbe à 250 m. Désactivez la dispersion pour commencer une comparaison en advection pure. Toute modification sous « Entrée et transport » efface les variantes enregistrées.

## impulse_task

1. Choisissez un créneau de 400 j et suivez ses fronts avant et arrière dans le profil et à 250 m.
2. Commencez un scénario Dirac avec une aire de 50 j, une largeur de 50 j, 101 cellules et une dispersivité de 10 m. Notez les RMSE du créneau appliqué et du Dirac idéal.
3. Réduisez la largeur à 10 j en conservant l’aire. Calculez ce nouveau scénario et comparez les erreurs notées. Affinez ensuite son maillage et vérifiez le bilan de masse.

## theory

L’aquifère captif mesure 1 m d’épaisseur et 1 m de largeur. Les charges imposées, environ 6,944 m et 0 m, agissent aux centres des cellules extrêmes distantes de 1000 m. Avec $K=10^{-4}$ m/s et $n_e=0.25$, le flux de Darcy vaut 0,06 m/j et la vitesse interstitielle $v$ vaut 0,24 m/j. L’intérieur est initialement sans soluté. L’eau sort avec la concentration locale. La référence est $C_{\mathrm{ref}}=1$ g/m³, soit 1 mg/L.

Le modèle résout $\partial C/\partial t=D\partial^2 C/\partial x^2-v\partial C/\partial x$ avec $D=\alpha_Lv+D_e$. À dispersion nulle, le signal se déplace de $vt$. Pour $D>0$, la réponse à un échelon unitaire de concentration imposée dans une colonne semi-infinie est

$$
S(x,t)=\tfrac12\left[\operatorname{erfc}\!\left(\frac{x-vt}{2\sqrt{Dt}}\right)
+e^{vx/D}\operatorname{erfc}\!\left(\frac{x+vt}{2\sqrt{Dt}}\right)\right],\quad t>0.
$$

Une entrée continue de hauteur $H$ donne $HS(x,t)$. Un créneau de durée $\tau$ donne $H[S(x,t)-S(x,t-\tau)]$, le second terme étant nul avant l’arrêt. Pour un Dirac à l’entrée d’aire $A=\int(C_{\mathrm{in}}/C_{\mathrm{ref}})dt$, la réponse intérieure est

$$
A\frac{\partial S}{\partial t}
=A\,\frac{x}{\sqrt{4\pi D t^3}}\exp\!\left[-\frac{(x-vt)^2}{4Dt}\right].
$$

MT3DMS applique un créneau de largeur $\varepsilon$ et de hauteur $A/\varepsilon$. L’aire de l’historique de concentration à l’entrée est ainsi conservée. Le bilan réel inclut aussi le flux dispersif à cette limite. À $D=0$, le Dirac se déplace à $v$ et son pic ponctuel n’est pas fini.

## profile_hint

Les profils numériques utilisent les concentrations aux centres des cellules. Les temps intermédiaires sont interpolés linéairement entre les pas enregistrés. Le jour 2000 utilise la sortie finale du solveur.

## breakthrough_hint

Chaque pas de transport est enregistré. À la distance choisie, la concentration est interpolée entre les centres des cellules. Le temps de parcours advectif est {t:.1f} j.

## balance_hint

L’écart cumulé signé provient de la colonne TOTAL IN–OUT du fichier MAS. Il est rapporté à la moyenne des masses absolues entrante et sortante, stockage inclus. Un faible écart de bilan peut accompagner un front étalé.

## dirac_reading

Le trait discontinu représente la réponse au créneau appliqué. Les pointillés représentent le Dirac idéal. À dispersion nulle, la ligne verticale indique sa position ou son arrivée. Sa hauteur ne représente aucune concentration.

## outlet_hint

Pour {ids}, l’échelon analytique à 1000 m atteint au moins 1 % au jour 2000. La sortie de la colonne finie peut influencer la partie aval du profil. Ce contrôle couvre aussi les impulsions, dont la concentration de sortie peut être plus faible.

## table_hint

Les variantes sont évaluées sur les mêmes 90 intervalles de 10 m entre 50 et 950 m. RMSE et MAE comparent le profil final à la solution analytique du signal appliqué, en C/Cref.

## mass_warning

{ids} dépasse 1 % d’écart absolu de masse au jour 2000. Examinez le bilan et le profil. Une méthode particulaire peut manquer une impulsion courte sur un maillage grossier.

## metrics_notes

La concentration numérique est considérée constante dans chaque cellule et moyennée sur chaque intervalle de 10 m selon les recouvrements. L’analytique est intégrée sur le même intervalle. Les cellules limites sont exclues même avec le maillage le plus grossier. RMSE est la racine de la moyenne des résidus au carré. MAE est la moyenne de leurs valeurs absolues.

Pour Dirac, le RMSE supplémentaire utilise l’impulsion idéale. À dispersion nulle, son poids spatial est $vA$. Une impulsion sur une limite d’intervalle contribue pour moitié de chaque côté. Gardez le même signal et la même intensité pour comparer les méthodes.

La durée couvre les deux exécutables, en excluant la préparation, la lecture et les graphiques. Le bilan d’eau vient du dernier écart MODFLOW. Le nombre de Péclet vaut $v\Delta x/D$, infini en advection pure. Les différences centrées peuvent produire des dépassements de concentration visibles sur les graphiques.

## references

- `TRANS_1D_MT3D.ipynb`, MWW01.
- Zheng & Wang (1999), *MT3DMS*, 1. [MODFLOW benchmark](https://modflow6-examples.readthedocs.io/en/latest/_examples/ex-gwt-mt3dms-p01.html)
- Wexler (1992), *Analytical Solutions for One-, Two-, and Three-Dimensional Solute Transport in Ground-Water Systems with Uniform Flow*. [USGS TWRI 3-B7](https://pubs.usgs.gov/twri/twri3-b7/pdf/twri_3-B7_a.pdf)
- Pérez Guerrero et al. (2013), *Analytical solutions of the one-dimensional advection–dispersion solute transport equation subject to time-dependent boundary conditions*. [DOI](https://doi.org/10.1016/j.cej.2013.01.095)
- FloPy [MT3DMS ADV](https://flopy.readthedocs.io/en/latest/source/flopy.mt3d.mtadv.html), [MT3DMS SSM](https://flopy.readthedocs.io/en/latest/source/flopy.mt3d.mtssm.html).

## method_upwind

La concentration amont définit le flux advectif à chaque face. Observez l’élargissement du front lorsque la dispersion physique est désactivée.

## method_central

Le flux utilise les concentrations des deux côtés de la face. Une maille grossière dominée par l’advection peut produire des oscillations près d’un front abrupt.

## method_tvd

Le schéma ULTIMATE TVD du troisième ordre limite les flux près des forts gradients. Comparez sa largeur de front à celle du schéma amont.

## method_moc

La méthode des caractéristiques suit les particules vers l’aval. MT3DMS place ici initialement quatre particules dans les cellules à gradient de concentration suffisant.

## method_mmoc

La méthode des caractéristiques modifiée remonte les trajectoires pour estimer la concentration qui entre dans une cellule.

## method_hmoc

La méthode hybride choisit MOC ou MMOC selon le gradient local de concentration.

