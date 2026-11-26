<!-- key: title -->
MT3D – Laboratorio de transporte 2D/3D

<!-- key: intro_caption -->
Ilustración introductoria: ejemplo de pluma y curva de llegada, independiente de los parámetros actuales del modelo.

<!-- key: Model & run -->
1 · Modelo y ejecución

<!-- key: Results & method comparison -->
2 · Resultados y comparación de métodos

<!-- key: series_reset -->
Cambió la señal o la geometría del dominio/fuente: comienza una serie nueva. Se borraron las ejecuciones anteriores.

<!-- key: grid_summary -->
Malla: {nx} × {ny} × {nz} celdas. Tamaño real: Δx = {dx:.3f} m; Δy = {dy:.3f} m; Δz = {dz:.3f} m.

<!-- key: velocity_summary -->
Velocidad intersticial homogénea de referencia: {velocity:.4f} m/día.

<!-- key: source_bounds -->
x = {x0:.2f}–{x1:.2f} m; y = {y0:.2f}–{y1:.2f} m; z = {z0:.2f}–{z1:.2f} m.

<!-- key: source_snap_hint -->
La fuente ocupa las celdas seleccionadas. La resolución puede cambiar sus dimensiones efectivas. Introducir el tamaño de celda conserva la extensión total e indica el espaciado uniforme real.

<!-- key: input_error -->
Corrija los parámetros indicados antes de ejecutar.

<!-- key: missing_executables -->
Faltan programas: {names}. Coloque ejecutables compatibles en `bin/` de la aplicación o del repositorio. En local: `python setup_executables.py`.

<!-- key: label_placeholder -->
Automático: 01 TVD / Pulse (heterogéneo: / het.)

<!-- key: history_full -->
Hay diez ejecuciones guardadas. Elimine una o vacíe la serie para continuar.

<!-- key: running -->
Ejecutando MODFLOW, MT3D y, opcionalmente, MODPATH…

<!-- key: run_success -->
Ejecución completada. Se muestra el resultado más reciente.

<!-- key: run_failed -->
Esta ejecución no se completó y no se añadió a la comparación.

<!-- key: changed_source_footprint -->
El refinamiento cambió la extensión real de la fuente. Revise sus dimensiones en la tabla ampliada.

<!-- key: nearest_time -->
{name}: tiempo guardado más cercano {time:.3f} días (ejecución mostrada: {target:.3f} días).

<!-- key: no_comparison_time -->
{name}: sin salida a {time:.3f} días; omitido.

<!-- key: evaluating_reference -->
Evaluando la referencia analítica…

<!-- key: export_hint -->
El archivo incluye entradas, registros, concentraciones, cargas, balances y partículas, incluidos sus tiempos de llegada.

<!-- key: no_runs -->
Ejecute el pulso inicial para ver la pluma, perfiles, curvas de llegada y comparación de métodos.

<!-- key: footer -->
MT3D 2D/3D · v0.5.1 · Versión de trabajo para docencia en directo

<!-- key: transient_hint -->
El flujo inicial se equilibra; la carga derecha cambia en t = 0.

<!-- key: expert_flow_hint -->
Active el modo experto para modificar tolerancias e iteraciones del solucionador de flujo.

<!-- key: stochastic_hint -->
Semilla fija: zonas reproducibles. K y Ss son uniformes en escala logarítmica; la porosidad es uniforme. El refinamiento conserva la realización.

<!-- key: zones_hint -->
Los rectángulos seleccionan centros de celda; las filas posteriores prevalecen. Las capas empiezan en 1.

<!-- key: observation_hint -->
Las observaciones usan la celda que contiene el punto. Puede moverlos sin recalcular los modelos guardados.

<!-- key: output_hint -->
Incluye t = 0 y el tiempo final. Controla la salida de concentraciones para gráficos y exportación.

<!-- key: preset_homogeneous -->
Homogéneo

<!-- key: preset_lens -->
Lente de K baja

<!-- key: preset_channel -->
Canal de K alta

<!-- key: preset_barrier -->
Barrera parcial de K baja

<!-- key: preset_stochastic -->
Zonificación estocástica

<!-- key: preset_custom -->
Rectángulos personalizados

<!-- key: preset_hint_lens -->
Lente central: K = 0,01 × K de fondo; toda la profundidad.

<!-- key: preset_hint_channel -->
Canal longitudinal: K = 10 × K de fondo; toda la profundidad.

<!-- key: preset_hint_barrier -->
Barrera transversal parcial: K = 0,01 × K de fondo; permite rodearla.

<!-- key: signal_pulse -->
Pulso / entrada rectangular

<!-- key: signal_continuous -->
Entrada continua

<!-- key: signal_dirac -->
Dirac / aporte instantáneo

<!-- key: signal_short_pulse -->
Pulso

<!-- key: signal_short_continuous -->
Cont.

<!-- key: signal_short_dirac -->
Dirac

<!-- key: Concept, assumptions and equations -->
Concepto, hipótesis y ecuaciones

<!-- key: Guided experiments -->
Experimentos guiados

<!-- key: Expert settings -->
Ajustes expertos

<!-- key: Use sliders for main parameters -->
Deslizadores para parámetros principales

<!-- key: Flow & domain -->
Flujo y dominio

<!-- key: Transport & source -->
Transporte y fuente

<!-- key: Post-processing & observations -->
Posprocesado y observaciones

<!-- key: Hydraulic properties -->
Propiedades hidráulicas

<!-- key: Hydraulic conductivity K (m/s) -->
Conductividad hidráulica K (m/s)

<!-- key: Effective porosity (-) -->
Porosidad efectiva (-)

<!-- key: Specific storage Ss (1/m) -->
Almacenamiento específico Ss (1/m)

<!-- key: Vertical / horizontal K -->
K vertical / horizontal

<!-- key: Boundary conditions -->
Condiciones de contorno

<!-- key: Specified head left (m) -->
Carga especificada izquierda (m)

<!-- key: Specified head right (m) -->
Carga especificada derecha (m)

<!-- key: Transient flow experiment -->
Flujo transitorio

<!-- key: Right head after t = 0 (m) -->
Carga derecha después de t = 0 (m)

<!-- key: Model extent and spatial discretization -->
Extensión y discretización espacial

<!-- key: Model length in x-direction (m) -->
Longitud en x (m)

<!-- key: Model width in y-direction (m) -->
Anchura en y (m)

<!-- key: Aquifer thickness / top elevation (m) -->
Espesor / cota superior (m)

<!-- key: Define the grid by -->
Definir malla mediante

<!-- key: Number of cells -->
Número de celdas

<!-- key: Cell width -->
Tamaño de celda

<!-- key: Cells x -->
Celdas x

<!-- key: Cells y -->
Celdas y

<!-- key: Cell width x (m) -->
Tamaño de celda x (m)

<!-- key: Cell width y (m) -->
Tamaño de celda y (m)

<!-- key: Number of layers -->
Número de capas

<!-- key: Numerical solution for flow -->
Solución numérica del flujo

<!-- key: Head tolerance (m) -->
Tolerancia de carga (m)

<!-- key: Flow residual tolerance (m³/day) -->
Tolerancia del residuo (m³/día)

<!-- key: PCG outer iterations -->
Iteraciones externas PCG

<!-- key: PCG inner iterations -->
Iteraciones internas PCG

<!-- key: Flow time steps (approximately total) -->
Pasos de flujo (total aproximado)

<!-- key: Hydrogeology and zonation -->
Hidrogeología y heterogeneidad

<!-- key: Hydrogeology preset -->
Caso hidrogeológico

<!-- key: Number of zones -->
Número de zonas

<!-- key: Random seed -->
Semilla aleatoria

<!-- key: K range (m/s) -->
Rango K (m/s)

<!-- key: Ss range (1/m) -->
Rango Ss (1/m)

<!-- key: Porosity range (-) -->
Rango de porosidad (-)

<!-- key: Minimum -->
Mínimo

<!-- key: Maximum -->
Máximo

<!-- key: Edit hydrogeological zones -->
Editar zonas

<!-- key: Zone name -->
Nombre de zona

<!-- key: First layer -->
Primera capa

<!-- key: Last layer -->
Última capa

<!-- key: Porosity -->
Porosidad

<!-- key: Boundary conditions and source -->
Contornos y fuente

<!-- key: Input signal -->
Señal de entrada

<!-- key: Released mass (g) -->
Masa liberada (g)

<!-- key: Mass input rate (g/day) -->
Tasa de entrada de masa (g/día)

<!-- key: Pulse duration (days) -->
Duración del pulso (días)

<!-- key: Source x (m) -->
Fuente x (m)

<!-- key: Source y (m) -->
Fuente y (m)

<!-- key: Source cells x -->
Celdas fuente x

<!-- key: Source cells y -->
Celdas fuente y

<!-- key: Source spans all layers -->
Fuente en todas las capas

<!-- key: Source layer (1 = top) -->
Capa fuente (1 = superior)

<!-- key: Transport parameters -->
Parámetros de transporte

<!-- key: Dispersion -->
Dispersión

<!-- key: Longitudinal dispersivity (m) -->
Dispersividad longitudinal (m)

<!-- key: Horizontal transverse / longitudinal -->
Transversal horizontal / longitudinal

<!-- key: Vertical transverse / longitudinal -->
Transversal vertical / longitudinal

<!-- key: Temporal discretization -->
Discretización temporal

<!-- key: Transport duration (days) -->
Duración del transporte (días)

<!-- key: DT0 · initial step (days; 0 = automatic) -->
DT0 · paso inicial (días; 0 = auto)

<!-- key: TTSMAX · maximum step (days; 0 = automatic) -->
TTSMAX · paso máximo (días; 0 = auto)

<!-- key: TTSMULT · step multiplier -->
TTSMULT · multiplicador de paso

<!-- key: MXSTRN · maximum transport steps -->
MXSTRN · máximo de pasos de transporte

<!-- key: Numerical solution for transport -->
Solución numérica del transporte

<!-- key: MT3D advection method -->
Método de advección MT3D

<!-- key: MODPATH particle comparison -->
Comparación de partículas MODPATH

<!-- key: PERCEL · Courant number -->
PERCEL · número de Courant

<!-- key: CCLOSE · concentration tolerance -->
CCLOSE · tolerancia de concentración

<!-- key: Timeout per executable (seconds) -->
Tiempo límite por programa (s)

<!-- key: Expert transport solver settings -->
Ajustes expertos del transporte

<!-- key: MXPART · maximum particles -->
MXPART · máximo de partículas

<!-- key: ITRACK · tracking algorithm -->
ITRACK · algoritmo de seguimiento

<!-- key: WD · concentration weighting -->
WD · ponderación de concentración

<!-- key: DCEPS · gradient threshold -->
DCEPS · umbral de gradiente

<!-- key: NPLANE · particle planes -->
NPLANE · planos de partículas

<!-- key: NPL · low-gradient particles -->
NPL · partículas con gradiente bajo

<!-- key: NPH · high-gradient particles -->
NPH · partículas con gradiente alto

<!-- key: NPMIN · minimum particles/cell -->
NPMIN · partículas mín./celda

<!-- key: NPMAX · maximum particles/cell -->
NPMAX · partículas máx./celda

<!-- key: INTERP · interpolation -->
INTERP · interpolación

<!-- key: NLSINK · sink planes -->
NLSINK · planos de sumideros

<!-- key: NPSINK · sink particles -->
NPSINK · partículas de sumideros

<!-- key: DCHMOC · HMOC threshold -->
DCHMOC · umbral HMOC

<!-- key: MXITER · GCG outer iterations -->
MXITER · iteraciones externas GCG

<!-- key: ITER1 · GCG inner iterations -->
ITER1 · iteraciones internas GCG

<!-- key: ISOLVE · preconditioner -->
ISOLVE · precondicionador

<!-- key: NCRS · cross-dispersion -->
NCRS · dispersión cruzada

<!-- key: ACCL · relaxation -->
ACCL · relajación

<!-- key: IPRGCG · print interval -->
IPRGCG · intervalo de impresión

<!-- key: MODPATH release settings -->
Liberación de partículas MODPATH

<!-- key: Particles per source cell -->
Partículas por celda fuente

<!-- key: Release batches (pulse / continuous) -->
Lotes de liberación (pulso / continuo)

<!-- key: Observation points -->
Puntos de observación

<!-- key: Number of observation points -->
Número de puntos de observación

<!-- key: Output settings -->
Opciones de salida

<!-- key: Saved transport times -->
Tiempos de transporte guardados

<!-- key: Actual source footprint -->
Extensión real de la fuente

<!-- key: Optional run label -->
Nombre opcional de ejecución

<!-- key: Run model -->
Ejecutar modelo

<!-- key: Run diagnostic -->
Diagnóstico de ejecución

<!-- key: More comparison metrics -->
Más métricas de comparación

<!-- key: Displayed run -->
Ejecución mostrada

<!-- key: Run to remove -->
Ejecución a eliminar

<!-- key: Remove -->
Eliminar

<!-- key: Clear comparison runs -->
Borrar ejecuciones comparadas

<!-- key: Plume & sections -->
Pluma y secciones

<!-- key: Observation curves -->
Curvas de observación

<!-- key: Mass & diagnostics -->
Masa y diagnósticos

<!-- key: Export -->
Exportar

<!-- key: Time (days) -->
Tiempo (días)

<!-- key: Top-view layer -->
Capa de vista superior

<!-- key: Layer {number} -->
Capa {number}

<!-- key: Analytical reference -->
Referencia analítica

<!-- key: Plot settings and section positions -->
Gráficos y posiciones de secciones

<!-- key: x-direction section · y (m) -->
Sección en x · y (m)

<!-- key: y-direction section · x (m) -->
Sección en y · x (m)

<!-- key: Colour fill -->
Relleno de color

<!-- key: Contour lines -->
Isolíneas

<!-- key: Log colours -->
Colores logarítmicos

<!-- key: Particle paths -->
Trayectorias de partículas

<!-- key: Opacity -->
Opacidad

<!-- key: Compare runs in x / y sections -->
Comparar ejecuciones en secciones x / y

<!-- key: Compare section profiles -->
Comparar perfiles

<!-- key: Runs for section comparison -->
Ejecuciones para comparar secciones

<!-- key: Also overlay top-view contours -->
Superponer también isolíneas en planta

<!-- key: Download plume figure (PNG) -->
Descargar figura de pluma (PNG)

<!-- key: Runs in breakthrough comparison -->
Ejecuciones para comparar curvas de llegada

<!-- key: Observation cells used by each run -->
Celdas de observación por ejecución

<!-- key: Download breakthrough curves (CSV) -->
Descargar curvas de llegada (CSV)

<!-- key: Detailed mass-budget data -->
Datos detallados del balance de masa

<!-- key: Stored run configuration -->
Configuración guardada

<!-- key: Download comparison table (CSV) -->
Descargar tabla comparativa (CSV)

<!-- key: Download run configuration (JSON) -->
Descargar configuración (JSON)

<!-- key: Prepare complete displayed-run archive -->
Preparar archivo completo de la ejecución mostrada

<!-- key: Preparing archive… -->
Preparando archivo…

<!-- key: Download run archive (ZIP) -->
Descargar archivo (ZIP)

<!-- key: Run -->
Ejecución

<!-- key: Method -->
Método

<!-- key: Signal -->
Señal

<!-- key: Grid -->
Malla

<!-- key: K zones -->
Zonas K

<!-- key: Flow -->
Flujo

<!-- key: MB disc. (%) -->
Error masa (%)

<!-- key: Flow disc. (%) -->
Error flujo (%)

<!-- key: MT3D (s) -->
MT3D (s)

<!-- key: MP7 (s) -->
MP7 (s)

<!-- key: Flow (s) -->
Flujo (s)

<!-- key: Total (s) -->
Total (s)

<!-- key: Ref. L1 (%) -->
Ref. L1 (%)

<!-- key: Mass (g) -->
Masa (g)

<!-- key: Input (g) -->
Entrada (g)

<!-- key: Min. C (g/m³) -->
C mín. (g/m³)

<!-- key: Neg. mass (g) -->
Masa neg. (g)

<!-- key: Centroid x (m) -->
Centroide x (m)

<!-- key: Steps -->
Pasos

<!-- key: Source box (m) -->
Dimensiones fuente (m)

<!-- key: End (d) -->
Fin (d)

<!-- key: Scenario -->
Escenario

<!-- key: Point -->
Punto

<!-- key: Requested x -->
x solicitado

<!-- key: Requested y -->
y solicitado

<!-- key: Requested z -->
z solicitado

<!-- key: Cell centre x -->
Centro celda x

<!-- key: Cell centre y -->
Centro celda y

<!-- key: Cell centre z -->
Centro celda z

<!-- key: Layer -->
Capa

<!-- key: Row -->
Fila

<!-- key: Column -->
Columna

<!-- key: Cumulative in (g) -->
Entrada acumulada (g)

<!-- key: Cumulative out (g) -->
Salida acumulada (g)

<!-- key: Sources (g) -->
Fuentes (g)

<!-- key: Sinks (g) -->
Sumideros (g)

<!-- key: Fluid storage (g) -->
Almacenamiento fluido (g)

<!-- key: Native resident mass (g) -->
Masa residente nativa (g)

<!-- key: Alternative disc. (%) -->
Error alternativo (%)

<!-- key: Analytical reference requires homogeneous steady flow. -->
La referencia analítica requiere flujo estacionario homogéneo.

<!-- key: Source cells -->
Celdas fuente

<!-- key: Specified head -->
Carga especificada

<!-- key: Section locations -->
Posiciones de secciones

<!-- key: Background flow -->
Flujo de fondo

<!-- key: Model preview: grid, boundaries and source -->
Vista previa: malla, contornos y fuente

<!-- key: Computed head contours -->
Isopiezas calculadas

<!-- key: Homogeneous steady head contours -->
Isopiezas estacionarias homogéneas

<!-- key: Time (d) -->
Tiempo (d)

<!-- key: Mass rate (g/d) -->
Tasa de masa (g/d)

<!-- key: Instantaneous mass (g) -->
Masa instantánea (g)

<!-- key: Dirac input (initial cell mass) -->
Entrada Dirac (masa inicial en celdas)

<!-- key: Finite pulse input -->
Entrada de pulso finito

<!-- key: Continuous input -->
Entrada continua

<!-- key: Concentration (g/m³) -->
Concentración (g/m³)

<!-- key: Elevation z (m) -->
Cota z (m)

<!-- key: MODPATH advection (slice) -->
Advección MODPATH (corte)

<!-- key: Analytical -->
Analítica

<!-- key: Analytical (active run) -->
Analítica (ejecución activa)

<!-- key: Mass output unavailable -->
Salida de masa no disponible

<!-- key: MT3D discrepancy (%) -->
Error MT3D (%)

<!-- key: Initial + injected mass (first run) -->
Masa inicial + aportada (primera ejecución)

<!-- key: Resident mass: grid sum and MT3D budget -->
Masa residente: suma en malla y balance MT3D

<!-- key: Reported mass-balance closure -->
Cierre del balance de masa informado

<!-- key: Example: pulse plume after 600 days -->
Ejemplo: pluma a los 600 días

<!-- key: Example: observation P1 -->
Ejemplo: observación P1

<!-- key: P1 · x (m) -->
P1 · x (m)

<!-- key: P1 · y (m) -->
P1 · y (m)

<!-- key: P1 · elevation z (m) -->
P1 · Cota z (m)

<!-- key: P2 · x (m) -->
P2 · x (m)

<!-- key: P2 · y (m) -->
P2 · y (m)

<!-- key: P2 · elevation z (m) -->
P2 · Cota z (m)

<!-- key: P3 · x (m) -->
P3 · x (m)

<!-- key: P3 · y (m) -->
P3 · y (m)

<!-- key: P3 · elevation z (m) -->
P3 · Cota z (m)

<!-- key: P4 · x (m) -->
P4 · x (m)

<!-- key: P4 · y (m) -->
P4 · y (m)

<!-- key: P4 · elevation z (m) -->
P4 · Cota z (m)

<!-- key: P5 · x (m) -->
P5 · x (m)

<!-- key: P5 · y (m) -->
P5 · y (m)

<!-- key: P5 · elevation z (m) -->
P5 · Cota z (m)

<!-- key: fig_head -->
Carga especificada: {head:g} m

<!-- key: fig_layers -->
{layers} capa(s); escala vertical exagerada

<!-- key: fig_total -->
Total: {mass:g} g

<!-- key: fig_initial -->
{mass:g} g en t = 0

<!-- key: fig_xprofile -->
Perfil x en y = {y:.3g} m

<!-- key: fig_yprofile -->
Perfil y en x = {x:.3g} m

<!-- key: fig_section -->
Sección {axis}–z en {other} = {value:.3g} m

<!-- key: fig_title -->
{method} · t = {time:g} d · capa {layer} (z = {z:.3g} m)

<!-- key: fig_gridmass -->
{label}: suma en malla

<!-- key: fig_nativemass -->
{label}: balance MT3D

<!-- key: fig_nodata -->
{label}: fuera del dominio — sin datos

<!-- key: table_help_MB disc. (%) -->
Error final del balance de masa informado por MT3D.

<!-- key: table_help_Flow disc. (%) -->
Error final del balance hídrico MODFLOW.

<!-- key: table_help_MT3D (s) -->
Tiempo real del programa de transporte.

<!-- key: table_help_MP7 (s) -->
Tiempo MODPATH; las partículas representan solo advección.

<!-- key: table_help_Ref. L1 (%) -->
Error absoluto de concentración ponderado por volumen de poros, dividido por la masa de referencia.

<!-- key: table_help_Mass (g) -->
Masa disuelta final integrada en la malla de concentración.

<!-- key: MT3DMS final mass discrepancy exceeds 1%; inspect method and transport time step settings. -->
El error final de masa MT3DMS supera el 1 %; revise método y paso de transporte.

<!-- key: At least one MODFLOW water-budget discrepancy exceeds 0.1%. -->
Al menos un error del balance hídrico MODFLOW supera el 0,1 %.

<!-- key: Negative concentrations occurred. They are retained in diagnostics and exports; central FD and particle methods can oscillate. -->
Hay concentraciones negativas, conservadas en diagnósticos y exportaciones. FD central y métodos de partículas pueden oscilar.

<!-- key: Source coordinates must lie inside the domain. -->
Las coordenadas de la fuente deben estar dentro del dominio.

<!-- key: This confined lab requires heads at or above aquifer top. -->
Este modelo confinado requiere cargas iguales o superiores al techo del acuífero.

<!-- key: Pulse duration must be between zero and model duration. -->
La duración del pulso debe estar entre cero y la duración del modelo.

<!-- key: Observation point is outside the model. -->
El punto de observación está fuera del modelo.

<!-- key: TVD requires PERCEL no greater than 1. -->
TVD requiere PERCEL ≤ 1.

<!-- key: language_fallback -->
Si falta una traducción se utiliza el texto inglés.

<!-- key: preset_random -->
Parámetros aleatorios estocásticos

<!-- key: Random unit x (m) -->
Unidad aleatoria x (m)

<!-- key: Random unit y (m) -->
Unidad aleatoria y (m)

<!-- key: random_hint -->
Unidades pequeñas: patrón fino; grandes: manchas mayores. Mantenga semilla y tamaños físicos al refinar para conservar la realización.

<!-- key: Active cells -->
Celdas activas

<!-- key: table_help_Active cells -->
Todas las celdas no inactivas, incluidas las de carga especificada.

<!-- key: Random field -->
Campo aleatorio

<!-- key: Comparison runs -->
Ejecuciones comparadas

<!-- key: discard_tags_hint -->
Quite una etiqueta con × para eliminar la ejecución. Quitarlas todas inicia una comparación nueva. Exporte antes lo que desee conservar.

<!-- key: Head contours -->
Isopiezas

<!-- key: Computed head contours (m) -->
Isopiezas calculadas (m)

<!-- key: Head contours appear after running the model -->
Las isopiezas aparecen tras ejecutar el modelo

<!-- key: fig_background_k -->
K de fondo = {k:.2e} m/s

<!-- key: fig_low_lens_k -->
Lente de K baja: K = {k:.2e} m/s

<!-- key: fig_high_channel_k -->
Canal de K alta: K = {k:.2e} m/s

<!-- key: fig_low_barrier_k -->
Barrera de K baja: K = {k:.2e} m/s

<!-- key: Focus on plume -->
Enfocar la pluma

<!-- key: Focus threshold (% of peak) -->
Umbral (% del máximo)

<!-- key: focus_hint -->
El enfoque usa el máximo positivo actual de cada pluma mostrada, con un margen del 20 % por lado. Incluye las trayectorias MODPATH visibles. Sin pluma ni trayectorias se muestra todo el dominio. Solo cambia la vista superior.

<!-- key: Download plume figure (SVG) -->
Descargar figura de pluma (SVG)

<!-- key: steady -->
estacionario

<!-- key: transient -->
transitorio

<!-- key: fig_minimum -->
Mínimo numérico: {minimum:.3g} g/m³

<!-- key: fig_minimum_log -->
Mínimo numérico: {minimum:.3g} g/m³ (valores no positivos ocultos en escala logarítmica)

<!-- key: The plume reaches an x specified-head boundary; enlarge the domain before treating the infinite-x analytical solution as a benchmark. -->
La pluma llega a un borde x de carga especificada; amplíe el dominio antes de usar la solución infinita como referencia.

<!-- key: fig_reference_boundary -->
Error analítico desactivado: interacción con bordes x superior al umbral de {tolerance_percent:.2g}%.

<!-- key: Low K lens -->
Lente de K baja

<!-- key: High K channel -->
Canal de K alta

<!-- key: Low K barrier -->
Barrera parcial de K baja

<!-- key: Page width -->
Ancho de página

<!-- key: width_1 -->
Estrecho

<!-- key: width_2 -->
Compacto

<!-- key: width_3 -->
Estándar

<!-- key: width_4 -->
Amplio

<!-- key: width_5 -->
Ancho completo

<!-- key: page_width_hint -->
Cinco anchos, de estrecho a completo. Estándar conserva el ancho anterior. La página se adapta a pantallas pequeñas.

<!-- key: Show model grid -->
Mostrar malla

<!-- key: grid_hint -->
Bordes discretos de las celdas de la ejecución mostrada. Los perfiles de una capa muestran guías verticales en los bordes.

<!-- key: Plume-centered x/y -->
x/y centrados en la pluma

<!-- key: relative_hint -->
El cero es el centroide de masa disuelta positiva en la capa mostrada. Las superposiciones comparten el origen. Las coordenadas de entrada y cotas siguen siendo absolutas.

<!-- key: relative_mass_origin -->
Origen relativo: x = {x:.2f} m; y = {y:.2f} m (centro de masa de la pluma).

<!-- key: relative_source_origin -->
Sin masa positiva en esta capa: origen en el centro de la fuente ajustada a la malla, x = {x:.2f} m; y = {y:.2f} m.

<!-- key: fig_relative_xprofile -->
Perfil x en y′ = {y:.3g} m

<!-- key: fig_relative_yprofile -->
Perfil y en x′ = {x:.3g} m

<!-- key: fig_relative_section -->
Sección {axis}–z en {other}′ = {value:.3g} m
