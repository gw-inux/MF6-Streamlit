## title

Laboratorio de transporte 1D

## experiments

Experimentos guiados

## experiment_front

Frente de advección

## experiment_spreading

Dispersión física

## experiment_impulse

Pulso e impulso

## theory_title

Flujo y soluciones analíticas

## setup

Configuración del modelo

## inlet_processes

Entrada y transporte

## grid_time

Malla y tiempo

## solver

Método MT3DMS

## signal

Señal de entrada

## continuous

Entrada continua

## block

Pulso rectangular

## dirac

Impulso de Dirac

## amplitude

Concentración de entrada C/Cref [–]

## block_days

Duración del pulso [d]

## impulse_area

Área del impulso A [d]

## impulse_days

Anchura numérica ε [d]

## rectangle

Altura de entrada MT3DMS = {height:.4g} C/Cref.

## dispersion

Activar dispersión

## dispersivity

Dispersividad longitudinal αL [m]

## diffusion

Difusión efectiva Dₑ [m²/d]

## grid_by

Definir malla mediante

## cells

Número de celdas

## spacing

Tamaño

## cell_count

Celdas

## target_spacing

Anchura deseada [m]

## grid_summary

{n} celdas · Δx real = {dx:.3g} m

## courant

Límite de Courant

## time_hint

Todas las variantes terminan en el día 2000. Un pulso finito utiliza al menos ocho pasos de transporte durante su aplicación.

## scheme

Esquema de advección

## upwind

DF · aguas arriba

## central

DF · centrado

## tvd

TVD · ULTIMATE

## moc

MOC

## mmoc

MMOC

## hmoc

HMOC

## solver_hint

MODFLOW-2005 proporciona el flujo estacionario. MT3DMS resuelve sus ecuaciones implícitas con GCG.

## preview

Vista previa del modelo

## preview_summary

{signal} · {scheme} · {n} celdas · Δx = {dx:.3g} m · D = {D:.4g} m²/d

## distance

Distancia desde la entrada [m]

## time

Tiempo [d]

## inlet_axis

Entrada C/Cref [–]

## optional_name

Nombre de la variante (opcional)

## name_example

p. ej. Malla fina con TVD

## limit

Hay diez variantes guardadas. Elimine una en « Gestionar variantes » para ejecutar otra.

## missing

Ejecutable necesario ausente o incompatible — {names}. Use la carpeta compartida bin o defina TRANSPORT_LAB_BIN.

## run

Ejecutar modelo

## running

Ejecutando MODFLOW-2005 y MT3DMS…

## failed

El cálculo no pudo completarse. Las variantes guardadas están disponibles abajo.

## diagnostic

Detalles del cálculo

## results

Resultados del transporte

## visible

Variantes en los gráficos

## cells_unit

celdas

## show_analytical

Solución analítica

## show_markers

Puntos numéricos

## profile

Perfil de concentración

## breakthrough

Curva de llegada

## budget

Balance de masa del soluto

## profile_time

Tiempo del perfil [d]

## observation

Distancia de observación [m]

## applied_curve

Analítica · entrada aplicada

## ideal_curve

Dirac ideal

## mass_axis

Error de masa [%]

## no_selection

Seleccione una variante para mostrar sus curvas.

## comparison

Comparación final · día 2000

## variant

Variante

## rmse

RMSE

## mae

MAE

## ideal_rmse

RMSE · Dirac ideal

## mass_error

Error de masa [%]

## seconds

Tiempo de cálculo [s]

## run_name

Nombre

## dx_col

Δx [m]

## height_col

Entrada C/Cref

## duration_col

Duración de entrada [d]

## area_col

Dirac A [d]

## alpha_col

αL [m]

## dm_col

Dₑ [m²/d]

## d_col

D [m²/d]

## pe_col

Péclet de celda

## co_col

Límite de Courant

## count_col

Pasos de transporte

## flow_s

MODFLOW [s]

## mt_s

MT3DMS [s]

## flow_error

Balance hídrico [%]

## min_c

Mín. final C/Cref

## max_c

Máx. final C/Cref

## detail_heading

Configuración y definición de métricas

## download

Descargar comparación (CSV)

## manage

Gestionar variantes

## remove_choice

Variante que eliminar

## remove

Eliminar variante seleccionada

## references_title

Referencias

## saved

V{number} guardada para comparar.

## applied_color_key

Analítica · color de la variante

## ideal_color_key

Dirac ideal · color de la variante

## pulse_cells

Longitud del pulso [celdas]

## pulse_resolution

Durante la entrada, la advección transporta el pulso {length:.3g} m, equivalentes a {cells:.3g} celdas.

## specified_head

Carga prescrita · {head:.4g} m

## hydraulic_summary

Conductividad hidráulica K = {k:.0e} m/s

## scenario_reset_hint

Los cambios aquí borran las variantes guardadas.

## comparison_cleared

La entrada o el transporte ha cambiado. Se ha vaciado la comparación para el nuevo escenario.

## concept_title

Modelo conceptual y respuestas típicas

## concept_inlet

Entrada

## concept_outlet

Salida

## concept_observation

Observación

## concept_profile

Perfil en t = {time:g} d

## concept_breakthrough

Llegada en x = {distance:g} m

## concept_advection

Solo advección

## concept_dispersion

Advección + dispersión
