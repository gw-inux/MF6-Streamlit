## introduction

Explore el transporte de un soluto conservativo a lo largo de una trayectoria de flujo subterráneo mediante un modelo unidimensional sencillo. Compare MT3DMS con soluciones analíticas para observar cómo la discretización y los métodos numéricos afectan a la señal transportada.

## concept_explanation

Imagine un tubo de corriente estrecho que sigue una trayectoria del agua subterránea en un acuífero homogéneo y saturado. El agua circula en régimen estacionario. Un soluto conservativo entra por el extremo aguas arriba y avanza por advección. La dispersión puede ensanchar la señal a lo largo de la trayectoria.

Este modelo unidimensional idealizado permite estudiar cómo influyen el método numérico, el tamaño de celda y el paso de tiempo. Compare MT3DMS con la solución analítica para examinar el ensanchamiento del frente, las oscilaciones, el tiempo de viaje y el balance de masa. Elija primero la señal y los procesos, y compare hasta diez variantes numéricas del mismo escenario.

## concept_caption

Tubo de corriente esquemático con flujo unidimensional estacionario y un punto de observación a 250 m. No hay intercambio de agua ni de soluto a través de los límites laterales; las dimensiones transversales no están a escala.

## concept_response_caption

Respuestas analíticas ilustrativas a una entrada rectangular de 400 d con C/Cref = 1 y v = 0,24 m/d. Verde: solo advección; azul: dispersividad longitudinal de 10 m, D = 2,4 m²/d y difusión molecular nula. Estos ejemplos fijos son independientes de los parámetros actuales del modelo.

## front_task

1. Elija entrada continua, 21 celdas, diferencias finitas aguas arriba y dispersión desactivada. Prediga la posición del frente en el día 2000 a partir de la velocidad intersticial.
2. Ejecute el modelo y examine las concentraciones a ambos lados del frente analítico.
3. Repita con TVD y luego con 101 celdas. Compare la anchura del frente, el error del perfil y el balance de masa.

## spreading_task

1. Use entrada continua, dispersividad de 10 m, difusión nula y TVD con 21 celdas. Examine el perfil analítico.
2. Repita con 101 celdas y luego con diferencias aguas arriba. ¿Qué parte del ensanchamiento aparece también en la solución analítica?
3. Examine las curvas a 250 m. Desactive la dispersión para comenzar otra comparación con advección pura. Los cambios en « Entrada y transporte » borran las variantes guardadas.

## impulse_task

1. Elija un pulso rectangular de 400 d y siga sus bordes delantero y trasero en el perfil y a 250 m.
2. Inicie un escenario Dirac con área de 50 d, anchura de 50 d, 101 celdas y dispersividad de 10 m. Anote los RMSE del pulso aplicado y del impulso ideal.
3. Reduzca la anchura a 10 d manteniendo el área. Calcule el nuevo escenario y compare los errores anotados. Refine después su malla y compruebe el balance de masa.

## theory

El acuífero confinado tiene 1 m de espesor y 1 m de anchura. Las cargas prescritas de aproximadamente 6,944 m y 0 m actúan en los centros de las celdas extremas, separados 1000 m. Con $K=10^{-4}$ m/s y $n_e=0.25$, el flujo de Darcy es 0,06 m/d y la velocidad intersticial $v$ es 0,24 m/d. El interior comienza sin soluto. El agua sale con la concentración local. Se usa $C_{\mathrm{ref}}=1$ g/m³, equivalente a 1 mg/L.

La ecuación es $\partial C/\partial t=D\partial^2 C/\partial x^2-v\partial C/\partial x$, con $D=\alpha_Lv+D_e$. Sin dispersión, la señal recorre $vt$. Para $D>0$, la respuesta a un escalón unitario de concentración prescrita en una columna semiinfinita es

$$
S(x,t)=\tfrac12\left[\operatorname{erfc}\!\left(\frac{x-vt}{2\sqrt{Dt}}\right)
+e^{vx/D}\operatorname{erfc}\!\left(\frac{x+vt}{2\sqrt{Dt}}\right)\right],\quad t>0.
$$

La entrada continua de altura $H$ produce $HS(x,t)$. Un pulso de duración $\tau$ produce $H[S(x,t)-S(x,t-\tau)]$, con el segundo término nulo antes del apagado. Para un impulso Dirac en la entrada de área $A=\int(C_{\mathrm{in}}/C_{\mathrm{ref}})dt$, la respuesta interior es

$$
A\frac{\partial S}{\partial t}
=A\,\frac{x}{\sqrt{4\pi D t^3}}\exp\!\left[-\frac{(x-vt)^2}{4Dt}\right].
$$

MT3DMS aplica un rectángulo de anchura $\varepsilon$ y altura $A/\varepsilon$, conservando el área del historial de concentración de entrada. El balance real también incluye el flujo dispersivo en este límite. Con $D=0$, el impulso ideal viaja a $v$ y carece de un máximo puntual finito.

## profile_hint

Los perfiles numéricos usan concentraciones en los centros de celda. Los tiempos intermedios se interpolan linealmente entre pasos guardados. El día 2000 utiliza la salida final del modelo.

## breakthrough_hint

Se guarda cada paso de transporte. La concentración se interpola entre centros de celda en la distancia elegida. El tiempo de viaje advectivo es {t:.1f} d.

## balance_hint

La discrepancia acumulada con signo procede de TOTAL IN–OUT en el archivo MAS. Se expresa como porcentaje de la media de las masas absolutas entrante y saliente, incluido el almacenamiento. Un balance pequeño puede coexistir con un frente ensanchado.

## dirac_reading

La línea discontinua corresponde al pulso aplicado. La línea de puntos representa el Dirac ideal. Sin dispersión, la línea vertical indica su posición o llegada. Su altura no representa una concentración.

## outlet_hint

Para {ids}, el escalón analítico en 1000 m alcanza al menos el 1 % en el día 2000. La salida de la columna finita puede influir en el extremo aguas abajo. Esta comprobación también cubre pulsos, cuya concentración de salida puede ser menor.

## table_hint

Todas las variantes se evalúan en los mismos 90 intervalos de 10 m entre 50 y 950 m. RMSE y MAE comparan el perfil final con la solución analítica de la señal aplicada, en C/Cref.

## mass_warning

{ids} supera el 1 % de discrepancia absoluta de masa en el día 2000. Examine el balance y el perfil. Un método de partículas puede omitir un pulso corto en una malla gruesa.

## metrics_notes

La concentración numérica es constante dentro de cada celda y se promedia sobre cada intervalo de 10 m según su solapamiento. La concentración analítica se integra en el mismo intervalo. Se excluyen las celdas de contorno incluso en la malla más gruesa. RMSE es la raíz de la media de los residuos al cuadrado. MAE es la media de sus valores absolutos.

Para Dirac, el RMSE adicional usa el impulso ideal. Sin dispersión su peso espacial es $vA$. Si está en un borde compartido, aporta la mitad a cada lado. Mantenga la señal y su intensidad al comparar métodos.

El tiempo de cálculo cubre los dos ejecutables, excluyendo preparación, lectura y gráficos. El balance hídrico es la última discrepancia de MODFLOW. El número de Péclet es $v\Delta x/D$, infinito en advección pura. Las diferencias centradas pueden producir concentraciones fuera del rango de entrada, visibles en los gráficos.

## references

- `TRANS_1D_MT3D.ipynb`, MWW01.
- Zheng & Wang (1999), *MT3DMS*, 1. [MODFLOW benchmark](https://modflow6-examples.readthedocs.io/en/latest/_examples/ex-gwt-mt3dms-p01.html)
- Wexler (1992), *Analytical Solutions for One-, Two-, and Three-Dimensional Solute Transport in Ground-Water Systems with Uniform Flow*. [USGS TWRI 3-B7](https://pubs.usgs.gov/twri/twri3-b7/pdf/twri_3-B7_a.pdf)
- Pérez Guerrero et al. (2013), *Analytical solutions of the one-dimensional advection–dispersion solute transport equation subject to time-dependent boundary conditions*. [DOI](https://doi.org/10.1016/j.cej.2013.01.095)
- FloPy [MT3DMS ADV](https://flopy.readthedocs.io/en/latest/source/flopy.mt3d.mtadv.html), [MT3DMS SSM](https://flopy.readthedocs.io/en/latest/source/flopy.mt3d.mtssm.html).

## method_upwind

La concentración aguas arriba define el flujo advectivo por cada cara. Observe si el frente se ensancha al desactivar la dispersión física.

## method_central

El flujo utiliza concentraciones a ambos lados de la cara. En mallas gruesas dominadas por advección pueden aparecer oscilaciones junto a frentes abruptos.

## method_tvd

ULTIMATE TVD de tercer orden limita los flujos cerca de gradientes fuertes. Compare su anchura de frente con la de diferencias aguas arriba.

## method_moc

El método de características sigue partículas hacia adelante. Aquí MT3DMS coloca inicialmente cuatro partículas en celdas con gradiente de concentración suficiente.

## method_mmoc

El método de características modificado sigue las trayectorias hacia atrás para estimar la concentración transportada a una celda.

## method_hmoc

El método híbrido alterna entre MOC y MMOC según el gradiente local de concentración.

