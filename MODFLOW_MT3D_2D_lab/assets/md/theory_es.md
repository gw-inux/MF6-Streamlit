### Modelo conceptual
El laboratorio sigue un soluto conservativo en un acuífero confinado y saturado. Las cargas especificadas en la primera y última columna generan el flujo de fondo. Las demás caras impiden el flujo de agua y el flujo dispersivo. El agua entrante tiene concentración cero; la saliente transporta la concentración residente. No hay reacciones, sorción, efectos de densidad, recarga ni bombeo.

Una capa representa transporte horizontal 2D. Varias capas permiten gradientes y dispersión verticales. Una fuente uniforme en todo el espesor de un medio homogéneo permanece uniforme verticalmente: añadir capas no crea flujo vertical. Una fuente en una sola capa permite investigar el transporte 3D.

Unidades: m, días, g y g/m³ de agua; 1 g/m³ = 1 mg/L. Internamente, K se expresa en m/d: $10^{-4}$ m/s = 8,64 m/d.

### Flujo y almacenamiento
La velocidad intersticial homogénea estacionaria es:
$$
v_x=\frac{K}{n_e}\frac{h_L-h_R}{L-\Delta x}.
$$
El denominador mide la distancia entre los **centros de las celdas** de carga especificada, no entre caras exteriores. MODFLOW calcula el flujo heterogéneo con las conductividades locales. K vertical es K horizontal local multiplicada por la relación seleccionada.

La interfaz usa flujo estacionario. Ss se guarda como propiedad, pero no cambia las cargas ni velocidades estacionarias. Las cargas deben estar a la altura del techo del acuífero o por encima. No se utiliza el rendimiento específico.

### Señales de entrada
| Señal | Representación | Cantidad conservada |
|---|---|---|
| Dirac | Concentración inicial uniforme en las celdas fuente | Masa inicial $M$ |
| Pulso rectangular | Tasa de masa prescrita hasta $\tau$ | Masa total $\dot M\tau$ |
| Continua | Tasa de masa prescrita durante toda la simulación | Masa aplicada hasta $t$: $\dot M t$ |

Son fuentes internas de masa que no añaden agua ni alteran el flujo. El pulso se apaga en un límite de periodo de esfuerzo y después se prescribe tasa cero. Dirac es instantáneo en el tiempo, pero ocupa un volumen finito. La concentración inicial homogénea es $M/(n_eV_s)$; con porosidades diferentes se pondera por volumen de poros para obtener la misma concentración inicial.

La fuente se ajusta a las celdas. Compruebe sus dimensiones y posición tras cambiar la malla: mantener el número de celdas fuente también cambia su volumen físico.

### Advección y dispersión
Para flujo homogéneo estacionario en x:
$$
\frac{\partial C}{\partial t}
=D_x\frac{\partial^2 C}{\partial x^2}
+D_y\frac{\partial^2 C}{\partial y^2}
+D_z\frac{\partial^2 C}{\partial z^2}
-v_x\frac{\partial C}{\partial x}+\frac{s}{n_e}.
$$
$s$ es la entrada de soluto por volumen total y tiempo. $D_x=\alpha_L|v_x|+D_e$, $D_y=\alpha_{TH}|v_x|+D_e$ y $D_z=\alpha_{TV}|v_x|+D_e$. Las dispersividades transversales se introducen como fracciones de $\alpha_L$. En flujo heterogéneo, MT3D construye el tensor con velocidades locales. La difusión molecular es cero. Desactivar dispersión elimina el ensanchamiento mecánico. Con una capa y techo/base cerrados, la dispersividad vertical no tiene efecto; solo aparece en modelos multicapa.

| Método | Opción MT3D | Qué estudiar |
|---|---|---|
| FD up | MIXELM = 0, NADVFD = 0 | Suavizado por dispersión numérica |
| FD cen | MIXELM = 0, NADVFD = 2 | Oscilaciones y concentraciones negativas en mallas gruesas dominadas por advección |
| TVD | MIXELM = −1 | Frentes abruptos con limitación de flujo |
| MOC | MIXELM = 1 | Características hacia delante; densidad de partículas |
| MMOC | MIXELM = 2 | Características hacia atrás; balance de masa |
| HMOC | MIXELM = 3 | Cambio local entre MOC y MMOC |

El modo experto permite modificar advección, solucionador GCG, pasos de transporte y tolerancias MODFLOW. Algunas opciones solo se aplican a ciertos métodos: MXPART limita partículas móviles MOC/HMOC. PERCEL controla el desplazamiento por paso; TVD exige PERCEL ≤ 1. Terminar correctamente no demuestra exactitud.

### Comparación analítica
La referencia supone velocidad, porosidad y dispersión constantes. Integra la función de Green en el **volumen fuente real** y cada celda receptora. Los bordes y/z reflejan soluto y x se considera infinito. Una fuente de una capa en todo el espesor da la solución 2D normalizada por espesor. Pulso y continuo usan convolución temporal.

La función de Green puntual instantánea 3D no acotada es:
$$
C=\frac{M}{n_e(4\pi t)^{3/2}\sqrt{D_xD_yD_z}}
\exp\!\left[-\frac{(x-x_s-v_xt)^2}{4D_xt}
-\frac{(y-y_s)^2}{4D_yt}-\frac{(z-z_s)^2}{4D_zt}\right].
$$
En 2D horizontal, el denominador es $4\pi n_e b t\sqrt{D_xD_y}$ y se omite el término z. Estas fórmulas explican la forma; la comparación usa volúmenes finitos para mantener la dilución coherente con MT3D.

La referencia homogénea no es exacta para medios zonificados o flujo transitorio: se suprimen sus métricas de error. Los bordes x deben quedar lejos de la pluma. La retención de masa indica proximidad a los bordes, pero no demuestra equivalencia entre dominios finito e infinito. Aumente el dominio y compruebe sensibilidad si la pluma se aproxima a ellos.

### MODPATH y resultados
MODPATH 7 usa el flujo MODFLOW y la misma porosidad para seguir trayectorias advectivas. No calcula dispersión ni concentración. El ancho de la nube de partículas no es una pluma dispersiva. Su masa representada es un peso de cuadratura de la liberación, no un balance de soluto MODPATH. Las partículas MOC cumplen otra función.

Compare forma, curvas de llegada y tabla: un error pequeño de balance puede coexistir con ensanchamiento u oscilaciones. Mantenga fuente, propiedades y malla al comparar métodos. El tiempo real depende de la carga del equipo; repita en la misma máquina. Observaciones y secciones usan celdas del modelo. Se conservan concentraciones con signo; la escala logarítmica oculta valores no positivos. Use también escala lineal y concentración mínima.

### Heterogeneidad, series y enfoque
Los casos son homogéneo, aleatorio, lente de K baja, canal de K alta y barrera parcial. El fondo homogéneo es blanco; los contrastes tienen color y leyenda K en m/s. Las unidades aleatorias forman una retícula física: pequeñas dan patrones finos, grandes dan manchas. K y Ss se muestrean uniformemente en escala logarítmica; porosidad, en escala lineal. El patrón horizontal atraviesa todas las capas. No es un campo geoestadístico de covarianza prescrita.

Semilla y tamaños físicos fijos preservan la realización al refinar. Cada celda toma la unidad que contiene su centro; una malla gruesa puede omitir estructuras pequeñas. Los formatos antiguos de rectángulos y flujo transitorio siguen siendo reproducibles fuera de la interfaz.

Se muestra automáticamente la ejecución más reciente. Cambiar señal o geometría física inicia nueva serie; discretización y ajustes numéricos permanecen como variantes. **het.** identifica casos heterogéneos. Quite etiquetas × para eliminar ejecuciones. Las isopiezas calculadas aparecen por defecto. Una capa muestra perfiles de concentración x/y; varias muestran concentración por colores e isolíneas en x–z/y–z.

**Enfocar la pluma** usa por defecto **0,1 % del máximo positivo actual** de cada pluma mostrada y **20 % de margen por lado**, incluyendo trayectorias MODPATH visibles. El umbral es ajustable. Sin pluma ni trayectorias se mantiene todo el dominio. Solo cambia el alcance de la vista superior; concentraciones, secciones y escala de colores no cambian.

### Referencias
Las cuatro aplicaciones analíticas facilitadas inspiraron los ejemplos. Sus fórmulas puntuales o de concentración impuesta no sustituyen directamente la referencia de fuente de masa de volumen finito utilizada aquí.


- [FloPy — MT3DMS ADV](https://flopy.readthedocs.io/en/3.12.0/source/flopy.mt3d.mtadv.html)
- [FloPy — MT3DMS SSM](https://flopy.readthedocs.io/en/3.12.0/source/flopy.mt3d.mtssm.html)
- [FloPy — MT3DMS GCG](https://flopy.readthedocs.io/en/3.12.0/source/flopy.mt3d.mtgcg.html)
- [Pollock (2016) — MODPATH 7, USGS](https://pubs.usgs.gov/publication/ofr20161086)
- [Wexler (1992) — USGS](https://pubs.usgs.gov/twri/twri3-b7/)
- [MODFLOW-ORG](https://github.com/MODFLOW-ORG/executables)
