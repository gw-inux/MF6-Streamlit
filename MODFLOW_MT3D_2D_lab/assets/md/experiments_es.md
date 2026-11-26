Los controles están en **Flujo y dominio**, **Transporte y fuente** y **Posprocesado y observaciones**. Compare perfiles superponiendo ejecuciones; el control analítico está a la derecha.

### 1. Seguir un pulso
Prediga $vt$ y $\dot M\tau$ en el caso homogéneo TVD. Ejecute y recorra los tiempos, identificando frente y cola. Compare perfiles, llegada y referencia. ¿Por qué la señal observada dura más que el pulso? ¿Un buen balance garantiza una buena forma?

### 2. Separar dispersión física y numérica
Sin dispersión, compare FD up, FD cen y TVD a fuente/malla fijas. Anote tiempo, concentración mínima, balance y error analítico. Active dispersión y repita; después refine. Compruebe el volumen real de la fuente.

### 3. Métodos de características
Compare MOC, MMOC y HMOC con TVD. Aumente la densidad de partículas correspondiente en modo experto. Compare coste, balance, pluma y llegada. Reduzca PERCEL: ¿por qué una solución estable depende aún del paso?

### 4. Dirac frente a pulso
Siga una masa inicial Dirac y expórtela. Cambie a un pulso corto con $M=\dot M\tau$; la señal nueva inicia otra serie. Compare los archivos a tiempos tempranos y tardíos. Añada puntos desplazados en y y explique sus máximos.

### 5. Contrastes de K
Introduzca una lente de K baja entre fuente y observación. Compare con MODPATH y explique desvíos y tiempos. Pruebe canal, barrera y patrones aleatorios finos/gruesos. Al refinar, mantenga semilla y unidades físicas. ¿Por qué no hay error analítico homogéneo?

### 6. Leer el flujo estacionario
Compare isopiezas homogéneas, lente y heterogeneidad aleatoria. Cambie la diferencia de carga manteniendo la fuente. Cambie solo Ss: ¿por qué no cambia el resultado? ¿Qué estructuras no resuelve la malla gruesa?

### 7. Extender a 3D
Use al menos tres capas y una fuente en una sola. Examine x–z/y–z y aumente dispersividad vertical. El patrón aleatorio horizontal se repite en todas las capas. Repita homogéneo con fuente en todo el espesor y explique la uniformidad vertical.

Prediga antes de cada ejecución y justifique la interpretación con diagnósticos. Enfocar la pluma permite ver detalles sin cambiar resultados.
