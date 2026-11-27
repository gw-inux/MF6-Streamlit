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
MT3D 2D/3D · v{version} · Versión de trabajo para docencia en directo · Desarrollado por Thomas Reimann · TU Dresden · The Groundwater Project

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

<!-- key: MODPATH particle count -->
Número de partículas MODPATH

<!-- key: particle_count_cell -->
Por celda fuente

<!-- key: particle_count_total -->
Fuente completa por liberación

<!-- key: Particles in the whole source per release -->
Partículas en toda la fuente por liberación

<!-- key: particle_count_summary -->
{count} partículas en {cells} celdas fuente × {groups} liberaciones = {total} partículas.

<!-- key: expert_transport_hint -->
Se muestran todos los ajustes del transporte. NPL / NPH y NPMIN / NPMAX controlan las partículas MOC / HMOC; MXPART limita su total. Las ayudas indican los métodos aplicables. MODPATH usa partículas independientes.

<!-- key: Plume animation -->
Animación de la pluma

<!-- key: Animation view -->
Vista de animación

<!-- key: animation_2d -->
Vista superior y secciones

<!-- key: animation_3d -->
Concentraciones 3D en centros de celda

<!-- key: Animation frames -->
Fotogramas

<!-- key: Playback speed (frames/s) -->
Velocidad (fotogramas/s)

<!-- key: Vertical exaggeration -->
Exageración vertical

<!-- key: Generate / refresh animation -->
Generar / actualizar animación

<!-- key: Generating animation… -->
Generando animación…

<!-- key: Download animation (HTML) -->
Descargar animación (HTML)

<!-- key: Play -->
Reproducir

<!-- key: Pause -->
Pausa

<!-- key: Animation frame -->
Fotograma

<!-- key: animation_layers_hint -->
Añada capas en ajustes expertos para la vista 3D.

<!-- key: animation_hint -->
Usa los tiempos guardados de la simulación mostrada. Elija colores y zoom independientes para la animación; la escala permanece fija en el tiempo. Se conservan los otros ajustes 2D. Comparaciones y referencias analíticas permanecen en las figuras estáticas. El reproductor aparece debajo de los ajustes; el HTML descargado funciona sin conexión.

<!-- key: animation_3d_hint -->
La vista 3D muestra concentraciones en centros de celda sobre el umbral, con cámara fija. Se muestran hasta {maximum} celdas muestreadas regularmente; cálculos y exportaciones conservan todas. Las partículas comparan la advección. La exageración solo afecta la vista.

<!-- key: animation_refresh_hint -->
Los ajustes cambiaron. Genere de nuevo para actualizar.

<!-- key: animation_failed -->
No se pudo generar la animación. Se conservan los resultados.

<!-- key: animation_size_limit -->
La animación supera 45 MiB. Reduzca los fotogramas.

<!-- key: help_s_percel -->
Desplazamiento advectivo máximo por paso, en anchos de celda. TVD requiere ≤ 1.

<!-- key: help_s_mxpart -->
MOC/HMOC: capacidad total de partículas móviles, no por celda.

<!-- key: help_s_itrack -->
MOC/MMOC/HMOC: 1 = Euler, 2 = Runge–Kutta de orden 4, 3 = seguimiento híbrido.

<!-- key: help_s_wd -->
Métodos de características: ponderación de concentración en separación de operadores; 0,5–1.

<!-- key: help_s_dceps -->
MOC/HMOC: umbral del gradiente relativo que separa NPL y NPH.

<!-- key: help_s_nplane -->
MOC/HMOC: 0 = distribución aleatoria; positivo = planos horizontales por celda.

<!-- key: help_s_npl -->
MOC/HMOC: partículas iniciales por celda con gradiente ≤ DCEPS; admite cero.

<!-- key: help_s_nph -->
MOC/HMOC: partículas iniciales por celda de alto gradiente. Los patrones fijos pueden redondear la cifra.

<!-- key: help_s_npmin -->
MOC/HMOC: se añaden partículas si la celda queda por debajo del mínimo.

<!-- key: help_s_npmax -->
MOC/HMOC: al superarse, se sustituye el conjunto de la celda por NPH partículas.

<!-- key: help_s_interp -->
MMOC/HMOC: interpolación de concentración; solo 1 (lineal) disponible.

<!-- key: help_s_nlsink -->
Celdas sumidero MMOC/HMOC: 0 = aleatorio; positivo = planos de partículas.

<!-- key: help_s_npsink -->
MMOC/HMOC: partículas que representan cada celda sumidero.

<!-- key: help_s_dchmoc -->
HMOC: MOC por encima de este umbral relativo, MMOC por debajo.

<!-- key: help_s_mxiter -->
Límite de iteraciones externas GCG. Una basta para este transporte conservativo lineal.

<!-- key: help_s_iter1 -->
Límite de iteraciones internas GCG para resolver el transporte.

<!-- key: help_s_isolve -->
Precondicionador GCG: 1 = Jacobi, 2 = SSOR, 3 = Cholesky incompleto modificado (MIC).

<!-- key: help_s_ncrs -->
Términos cruzados de dispersión: 0 = aproximación en lado derecho; 1 = tensor completo en matriz.

<!-- key: help_s_accl -->
Factor de relajación, solo para SSOR (ISOLVE = 2).

<!-- key: help_s_cclose -->
Tolerancia relativa de cambio de concentración GCG. Menor valor exige mayor convergencia.

<!-- key: help_s_iprgcg -->
Imprime cambios cada N iteraciones GCG; 0 al final de cada periodo.

<!-- key: help_s_dt0 -->
Paso inicial en días; 0 permite elección automática de MT3D.

<!-- key: help_s_ttsmult -->
Multiplicador de pasos para FD implícito; TVD y características lo ignoran.

<!-- key: help_s_ttsmax -->
Paso máximo en días si TTSMULT > 1; 0 usa el límite automático.

<!-- key: help_s_mxstrn -->
Máximo de pasos de transporte por paso de flujo; alcanzar el límite puede detener el cálculo.

<!-- key: help_s_timeout -->
Tiempo máximo por ejecutable. Más partículas pueden requerir más tiempo.

<!-- key: help_s_hclose -->
Tolerancia PCG de cambio de carga, en metros.

<!-- key: help_s_rclose -->
Tolerancia del residuo de caudal PCG, en m³/día.

<!-- key: help_s_flow_mxiter -->
Máximo de iteraciones externas del solver de flujo MODFLOW PCG.

<!-- key: help_s_flow_iter1 -->
Máximo de iteraciones internas PCG por iteración externa.

<!-- key: help_particle_count_mode -->
Elija por celda fuente o un total exacto en toda la fuente por liberación.

<!-- key: help_particles_per_cell -->
Partículas distribuidas uniformemente en cada celda fuente y liberación. Solo MODPATH, no MOC.

<!-- key: help_total_source_particles -->
Total exacto por liberación en todas las celdas fuente; al menos una por celda. Diferencia máxima de una partícula entre celdas; pesos según volumen de poros.

<!-- key: help_release_groups -->
Liberaciones en puntos medios de intervalos iguales aproximan pulso o aporte continuo. Más grupos refinan el tiempo; Dirac libera en t = 0.

<!-- key: help_run_label -->
Deje vacío para el nombre sugerido. La etiqueta sustituye método/señal; número y sufijo heterogéneo son automáticos.

<!-- key: help_expert -->
Muestra capas y todos los parámetros de los solvers. Se conservan los valores ocultos.

<!-- key: help_sliders -->
Cambie entre campos numéricos y deslizadores sin alterar valores.

<!-- key: help_extent -->
Extensión física en metros. Cambiarla inicia una nueva serie comparativa.

<!-- key: help_thickness -->
Espesor confinado; base a 0 m y techo a este valor. Capas de igual espesor.

<!-- key: help_grid_mode -->
Defina número o ancho máximo de celdas. El número se redondea hacia arriba conservando el dominio.

<!-- key: help_grid_count -->
Número de celdas uniformes en esta dirección. Refinar conserva cálculos previos.

<!-- key: help_cell_width -->
Ancho máximo solicitado en metros. La vista previa muestra el real.

<!-- key: help_nlay -->
Una capa da un modelo en planta; varias capas iguales permiten transporte vertical y vistas 3D.

<!-- key: help_k -->
Conductividad hidráulica horizontal de fondo. Introduzca m/s; se convierte a m/día.

<!-- key: help_porosity -->
Fracción de poros móviles; controla velocidad intersticial y almacenamiento de soluto.

<!-- key: help_ss -->
Agua liberada por volumen y descenso unitario de carga (1/m). Aquí el flujo estacionario no activa almacenamiento.

<!-- key: help_kv_ratio -->
Conductividad vertical dividida por horizontal, aplicada en cada capa.

<!-- key: help_zones_preset -->
Elija propiedades homogéneas, campo aleatorio reproducible o lente/canal/barrera.

<!-- key: help_zone_seed -->
Semilla aleatoria. Misma semilla y ajustes reproducen el patrón físico.

<!-- key: help_random_unit -->
Tamaño físico de bloques aleatorios en esta dirección, independiente del refinamiento.

<!-- key: help_random_k -->
Límites de conductividad aleatoria, muestreo uniforme en espacio logarítmico (m/s).

<!-- key: help_random_ss -->
Límites del almacenamiento específico log-uniforme (1/m). Se guarda; inactivo en flujo estacionario.

<!-- key: help_random_por -->
Límites de porosidad eficaz uniforme, entre cero y uno.

<!-- key: help_head -->
Carga especificada en esta columna externa. Izquierda mayor que derecha; ambas al menos al techo.

<!-- key: help_duration -->
Tiempo total simulado en días, independiente de la velocidad de animación.

<!-- key: help_dispersion -->
Incluye dispersión mecánica proporcional a velocidad intersticial. Al apagarla quedan advección y dispersión numérica.

<!-- key: help_al -->
Dispersividad longitudinal en metros; coeficiente asociado = αL × velocidad.

<!-- key: help_trpt -->
Dispersividad transversal horizontal dividida por longitudinal: αTH/αL.

<!-- key: help_trpv -->
Dispersividad transversal vertical dividida por longitudinal: αTV/αL. Relevante con varias capas.

<!-- key: help_source_kind -->
Dirac: masa inicial en t = 0. Pulso: carga constante hasta su fin. Continuo: carga constante todo el cálculo.

<!-- key: help_source_mass -->
Masa disuelta inicial total en el volumen de poros fuente (gramos).

<!-- key: help_mass_rate -->
Carga total (g/día), distribuida por volumen de poros fuente. Sin inyección de agua.

<!-- key: help_pulse_duration -->
La carga cesa tras este tiempo (días), menor que la duración total.

<!-- key: help_source_position -->
Coordenada absoluta del centro fuente en metros, ajustada a una celda. Evite columnas de carga fija.

<!-- key: help_source_cells -->
Celdas fuente en esta dirección. Revise la huella; cambiar geometría inicia nueva serie.

<!-- key: help_source_all_layers -->
Distribuya la fuente en todas las capas; si no, solo en la elegida.

<!-- key: help_src_layer -->
Capa que recibe la fuente; 1 es la superior.

<!-- key: help_method -->
Elija advección MT3D: FD aguas arriba/central, TVD, MOC adelante, MMOC atrás o HMOC híbrido. Independiente de MODPATH.

<!-- key: help_track_particles -->
Ejecuta MODPATH 7 en el flujo calculado. Solo advección; MODPATH no calcula dispersión ni concentraciones.

<!-- key: help_observation -->
Coordenada absoluta de observación en metros. Concentración de la celda que contiene el punto, sin interpolación.

<!-- key: help_nobs -->
Compare concentraciones en uno a cinco puntos con cálculos guardados.

<!-- key: help_outputs -->
Tiempos guardados, incluido t = 0; también se guarda el fin del pulso. Más salidas mejoran animación y curvas, no los pasos del solver.

<!-- key: help_length -->
Extensión física en metros. Cambiarla inicia una nueva serie comparativa.

<!-- key: help_width -->
Extensión física en metros. Cambiarla inicia una nueva serie comparativa.

<!-- key: help_ncol -->
Número de celdas uniformes en esta dirección. Refinar conserva cálculos previos.

<!-- key: help_nrow -->
Número de celdas uniformes en esta dirección. Refinar conserva cálculos previos.

<!-- key: help_cell_x -->
Ancho máximo solicitado en metros. La vista previa muestra el real.

<!-- key: help_cell_y -->
Ancho máximo solicitado en metros. La vista previa muestra el real.

<!-- key: help_random_unit_x -->
Tamaño físico de bloques aleatorios en esta dirección, independiente del refinamiento.

<!-- key: help_random_unit_y -->
Tamaño físico de bloques aleatorios en esta dirección, independiente del refinamiento.

<!-- key: help_zone_k_min -->
Límites de conductividad aleatoria, muestreo uniforme en espacio logarítmico (m/s).

<!-- key: help_zone_k_max -->
Límites de conductividad aleatoria, muestreo uniforme en espacio logarítmico (m/s).

<!-- key: help_zone_ss_min -->
Límites del almacenamiento específico log-uniforme (1/m). Se guarda; inactivo en flujo estacionario.

<!-- key: help_zone_ss_max -->
Límites del almacenamiento específico log-uniforme (1/m). Se guarda; inactivo en flujo estacionario.

<!-- key: help_zone_por_min -->
Límites de porosidad eficaz uniforme, entre cero y uno.

<!-- key: help_zone_por_max -->
Límites de porosidad eficaz uniforme, entre cero y uno.

<!-- key: help_head_left -->
Carga especificada en esta columna externa. Izquierda mayor que derecha; ambas al menos al techo.

<!-- key: help_head_right -->
Carga especificada en esta columna externa. Izquierda mayor que derecha; ambas al menos al techo.

<!-- key: help_src_x -->
Coordenada absoluta del centro fuente en metros, ajustada a una celda. Evite columnas de carga fija.

<!-- key: help_src_y -->
Coordenada absoluta del centro fuente en metros, ajustada a una celda. Evite columnas de carga fija.

<!-- key: help_src_ncol -->
Celdas fuente en esta dirección. Revise la huella; cambiar geometría inicia nueva serie.

<!-- key: help_src_nrow -->
Celdas fuente en esta dirección. Revise la huella; cambiar geometría inicia nueva serie.

<!-- key: help_animation_mode -->
2D anima planta y secciones. 3D muestra concentraciones calculadas en centros, con vista fija; requiere varias capas.

<!-- key: help_animation_frames -->
Hasta 80 estados guardados, incluidos primero y último. Sin interpolación temporal de concentración.

<!-- key: help_animation_fps -->
Fotogramas por segundo real. Cada uno indica el tiempo simulado; no cambia el modelo.

<!-- key: help_animation_exaggeration -->
Escale la altura visual 3D. Elevaciones y cálculos no cambian.

<!-- key: help_generate_animation -->
Renderiza resultados guardados bajo demanda. Regenere tras cambiar ajustes; no recalcula el modelo.

<!-- key: help_view_time -->
Elija un tiempo guardado, sin recalcular.

<!-- key: help_view_layer -->
Capa en planta; 1 es la superior.

<!-- key: help_section -->
Posición absoluta en metros, en la fila/columna correspondiente. Ejes relativos no mueven la sección.

<!-- key: help_fill -->
Coloree celdas según concentración; cero queda blanco.

<!-- key: help_lines -->
Dibuja isolíneas de concentración sobre el color.

<!-- key: help_show_heads -->
Superpone contornos finos de carga calculada, en metros.

<!-- key: help_log -->
Colores logarítmicos para concentración positiva. Valores no positivos ocultos solo en la vista.

<!-- key: help_particle_paths -->
Muestra posiciones y trayectorias MODPATH hasta el tiempo elegido. Máximo 120 trayectorias visibles; exportación completa.

<!-- key: help_opacity -->
Opacidad: 1 es opaco; valores menores revelan elementos inferiores.

<!-- key: help_focus_plume -->
Amplía la pluma positiva y trayectorias con margen. La animación usa una ventana fija para todos sus tiempos.

<!-- key: help_focus_threshold -->
Foco estático: porcentaje del pico de cada pluma. En animación 3D: porcentaje del máximo absoluto de escala fija para mostrar celdas.

<!-- key: help_analytical -->
Compare con referencia analítica homogénea estacionaria. Flujo heterogéneo o transitorio fuera de sus supuestos.

<!-- key: help_compare -->
Compare cálculos al tiempo disponible más cercano en las secciones del mostrado.

<!-- key: help_analytic_on -->
Compare con referencia analítica homogénea estacionaria. Flujo heterogéneo o transitorio fuera de sus supuestos.

<!-- key: help_btc_analytical -->
Compare con referencia analítica homogénea estacionaria. Flujo heterogéneo o transitorio fuera de sus supuestos.

<!-- key: help_compare_sections -->
Compare cálculos al tiempo disponible más cercano en las secciones del mostrado.

<!-- key: help_overlay_runs -->
Compare cálculos al tiempo disponible más cercano en las secciones del mostrado.

<!-- key: help_compare_top -->
Compare cálculos al tiempo disponible más cercano en las secciones del mostrado.

<!-- key: help_btc_runs -->
Compare concentraciones en uno a cinco puntos con cálculos guardados.

<!-- key: Animation settings -->
Ajustes de la animación

<!-- key: Animation colour scale -->
Escala de colores de la animación

<!-- key: animation_colour_enhanced -->
Concentraciones bajas realzadas (escala fija)

<!-- key: animation_colour_linear -->
Lineal (escala fija)

<!-- key: animation_colour_log -->
Logarítmica (escala fija)

<!-- key: help_animation_colour -->
El realce utiliza una transformación de potencia (exponente 0,35) para mostrar concentraciones pequeñas. Todos los fotogramas comparten los mismos límites físicos de concentración; el cero permanece blanco. Las escalas lineal y realzada conservan los valores numéricos negativos; la logarítmica oculta los valores no positivos. Los datos calculados no cambian.

<!-- key: Zoom animation to plume -->
Ampliar la pluma en la animación

<!-- key: help_animation_focus -->
Usa una ventana fija que abarca la pluma positiva y las trayectorias MODPATH mostradas en todos los tiempos seleccionados, con un margen del 20 %. Independiente del zoom estático. Desactive para ver todo el dominio. Disponible en 2D y 3D.

<!-- key: Plume threshold (% of peak) -->
Umbral de la pluma (% del máximo)

<!-- key: help_animation_threshold -->
El zoom incluye concentraciones superiores a este porcentaje del máximo positivo de cada fotograma. En 3D, también fija el umbral de las celdas visibles respecto a la concentración absoluta máxima de la escala fija. Valor inicial: 0,1 %. Solo afecta a la visualización.

<!-- key: animation_progress -->
Generando animación… {percent} %

<!-- key: MODPATH settings -->
Ajustes de MODPATH

<!-- key: expert_transport_location_hint -->
Los parámetros expertos de MT3D están en el panel desplegable independiente **Ajustes expertos del transporte**, justo debajo. Los ajustes de MODPATH aparecen después.
