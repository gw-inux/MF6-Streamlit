Utilisez **Écoulement et domaine**, **Transport et source**, puis **Post-traitement et observations**. La comparaison des profils superpose les calculs ; la référence analytique est à droite.

### 1. Suivre un créneau
Prédisez $vt$ et $\dot M\tau$ dans le cas homogène TVD. Calculez, parcourez les temps, repérez fronts et traîne. Comparez profils, restitution et référence. Pourquoi la restitution dure-t-elle plus longtemps que l'apport ? Un bon bilan garantit-il une bonne forme ?

### 2. Séparer étalements physique et numérique
Sans dispersion, comparez FD up, FD cen et TVD à source/maillage fixes. Relevez temps, minimum, écart de masse et erreur analytique. Rétablissez la dispersion puis raffinez. Vérifiez l'emprise source : son nombre de cellules fixe ne conserve pas son volume.

### 3. Méthodes caractéristiques
Comparez MOC, MMOC, HMOC et TVD. Augmentez la densité particulaire adaptée à chaque méthode en mode expert. Comparez coût, bilan, panache et restitution. Réduisez PERCEL : pourquoi une solution stable dépend-elle encore du pas ?

### 4. Dirac et créneau
Suivez une masse initiale Dirac, exportez-la, puis utilisez un créneau court de même masse $M=\dot M\tau$. Le changement de signal ouvre une nouvelle série. Comparez les exports aux temps précoces/tardifs ; ajoutez des observations décalées selon y et expliquez les pics.

### 5. Contrastes de K
Insérez une lentille faible K et comparez panache/trajectoires MODPATH. Expliquez contournement et temps de trajet. Essayez chenal, barrière et motifs aléatoires fins/grossiers ; gardez graine et taille d'unité fixes au raffinement. Pourquoi l'erreur analytique homogène n'est-elle pas disponible ?

### 6. Lire l'écoulement permanent
Comparez isopièzes homogènes, lentille et aléatoire. Changez la différence de charge et observez les trajets, à source fixe. Changez uniquement Ss : pourquoi le résultat reste-t-il identique ? Quelles petites structures un maillage grossier manque-t-il ?

### 7. Passer en 3D
Activez au moins trois couches et une source dans une seule couche. Comparez les coupes x–z/y–z en augmentant la dispersivité verticale. Le motif aléatoire horizontal traverse les couches. Répétez en milieu homogène avec source sur toute l'épaisseur : pourquoi la solution devient-elle uniforme verticalement ?

Prédisez avant chaque calcul, confrontez les résultats aux prédictions et appuyez votre explication sur les diagnostics. Le zoom sur le panache aide à lire les détails ; il ne change aucun résultat.
