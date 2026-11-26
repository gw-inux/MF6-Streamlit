<!-- key: title -->
MT3D – Laboratório de transporte 2D/3D

<!-- key: intro_caption -->
Ilustração introdutória: exemplo de pluma e curva de chegada, independente dos parâmetros atuais do modelo.

<!-- key: Model & run -->
1 · Modelo e execução

<!-- key: Results & method comparison -->
2 · Resultados e comparação de métodos

<!-- key: series_reset -->
O sinal ou a geometria do domínio/fonte mudou: começa uma nova série. As execuções anteriores foram apagadas.

<!-- key: grid_summary -->
Malha: {nx} × {ny} × {nz} células. Dimensão real: Δx = {dx:.3f} m; Δy = {dy:.3f} m; Δz = {dz:.3f} m.

<!-- key: velocity_summary -->
Velocidade intersticial homogénea de referência: {velocity:.4f} m/dia.

<!-- key: source_bounds -->
x = {x0:.2f}–{x1:.2f} m; y = {y0:.2f}–{y1:.2f} m; z = {z0:.2f}–{z1:.2f} m.

<!-- key: source_snap_hint -->
A fonte ocupa as células selecionadas. A resolução pode alterar as dimensões efetivas. A entrada por dimensão da célula mantém a extensão total e indica o espaçamento uniforme real.

<!-- key: input_error -->
Corrija os parâmetros indicados antes de executar.

<!-- key: missing_executables -->
Programas em falta: {names}. Coloque executáveis compatíveis em `bin/` da aplicação ou do repositório. Localmente: `python setup_executables.py`.

<!-- key: label_placeholder -->
Automático: 01 TVD / Pulse (heterogéneo: / het.)

<!-- key: history_full -->
Estão guardadas dez execuções. Elimine uma ou limpe a série para continuar.

<!-- key: running -->
A executar MODFLOW, MT3D e MODPATH opcional…

<!-- key: run_success -->
Execução concluída. É apresentado o resultado mais recente.

<!-- key: run_failed -->
Esta execução não foi concluída nem adicionada à comparação.

<!-- key: changed_source_footprint -->
O refinamento alterou a extensão real da fonte. Verifique as dimensões na tabela alargada.

<!-- key: nearest_time -->
{name}: tempo guardado mais próximo {time:.3f} dias (execução apresentada: {target:.3f} dias).

<!-- key: no_comparison_time -->
{name}: sem saída a {time:.3f} dias; omitido.

<!-- key: evaluating_reference -->
A calcular a referência analítica…

<!-- key: export_hint -->
O arquivo contém entradas, registos, concentrações, cargas, balanços e partículas, incluindo as chegadas.

<!-- key: no_runs -->
Execute a experiência inicial de pulso para ver a pluma, perfis, curvas de chegada e comparação de métodos.

<!-- key: footer -->
MT3D 2D/3D · v0.4.0 · Versão de trabalho para aulas ao vivo

<!-- key: transient_hint -->
O campo inicial equilibra-se; a carga direita muda em t = 0.

<!-- key: expert_flow_hint -->
Ative as opções avançadas para alterar tolerâncias e iterações do solucionador de fluxo.

<!-- key: stochastic_hint -->
Semente fixa: zonas reprodutíveis. K e Ss são uniformes em escala logarítmica; a porosidade é uniforme. O refinamento mantém a realização.

<!-- key: zones_hint -->
Os retângulos selecionam centros de células; as linhas seguintes prevalecem. As camadas começam em 1.

<!-- key: observation_hint -->
As observações usam a célula que contém o ponto. As posições podem mudar sem recalcular os modelos guardados.

<!-- key: output_hint -->
Inclui t = 0 e o tempo final. Controla as concentrações guardadas para gráficos e exportação.

<!-- key: preset_homogeneous -->
Homogéneo

<!-- key: preset_lens -->
Lente de K baixa

<!-- key: preset_channel -->
Canal de K elevada

<!-- key: preset_barrier -->
Barreira parcial de K baixa

<!-- key: preset_stochastic -->
Zonamento estocástico

<!-- key: preset_custom -->
Retângulos personalizados

<!-- key: preset_hint_lens -->
Lente central: K = 0,01 × K de fundo; toda a espessura.

<!-- key: preset_hint_channel -->
Canal longitudinal: K = 10 × K de fundo; toda a espessura.

<!-- key: preset_hint_barrier -->
Barreira transversal parcial: K = 0,01 × K de fundo; mantém passagem lateral.

<!-- key: signal_pulse -->
Pulso / entrada retangular

<!-- key: signal_continuous -->
Entrada contínua

<!-- key: signal_dirac -->
Dirac / libertação instantânea

<!-- key: signal_short_pulse -->
Pulso

<!-- key: signal_short_continuous -->
Cont.

<!-- key: signal_short_dirac -->
Dirac

<!-- key: Concept, assumptions and equations -->
Conceito, hipóteses e equações

<!-- key: Guided experiments -->
Experiências guiadas

<!-- key: Expert settings -->
Opções avançadas

<!-- key: Use sliders for main parameters -->
Cursores para parâmetros principais

<!-- key: Flow & domain -->
Fluxo e domínio

<!-- key: Transport & source -->
Transporte e fonte

<!-- key: Post-processing & observations -->
Pós-processamento e observações

<!-- key: Hydraulic properties -->
Propriedades hidráulicas

<!-- key: Hydraulic conductivity K (m/s) -->
Condutividade hidráulica K (m/s)

<!-- key: Effective porosity (-) -->
Porosidade eficaz (-)

<!-- key: Specific storage Ss (1/m) -->
Armazenamento específico Ss (1/m)

<!-- key: Vertical / horizontal K -->
K vertical / horizontal

<!-- key: Boundary conditions -->
Condições de fronteira

<!-- key: Specified head left (m) -->
Carga especificada à esquerda (m)

<!-- key: Specified head right (m) -->
Carga especificada à direita (m)

<!-- key: Transient flow experiment -->
Fluxo transitório

<!-- key: Right head after t = 0 (m) -->
Carga direita após t = 0 (m)

<!-- key: Model extent and spatial discretization -->
Extensão e discretização espacial

<!-- key: Model length in x-direction (m) -->
Comprimento em x (m)

<!-- key: Model width in y-direction (m) -->
Largura em y (m)

<!-- key: Aquifer thickness / top elevation (m) -->
Espessura / cota do topo (m)

<!-- key: Define the grid by -->
Definir a malha por

<!-- key: Number of cells -->
Número de células

<!-- key: Cell width -->
Dimensão da célula

<!-- key: Cells x -->
Células x

<!-- key: Cells y -->
Células y

<!-- key: Cell width x (m) -->
Dimensão x (m)

<!-- key: Cell width y (m) -->
Dimensão y (m)

<!-- key: Number of layers -->
Número de camadas

<!-- key: Numerical solution for flow -->
Solução numérica do fluxo

<!-- key: Head tolerance (m) -->
Tolerância da carga (m)

<!-- key: Flow residual tolerance (m³/day) -->
Tolerância do resíduo (m³/dia)

<!-- key: PCG outer iterations -->
Iterações externas PCG

<!-- key: PCG inner iterations -->
Iterações internas PCG

<!-- key: Flow time steps (approximately total) -->
Passos de fluxo (total aproximado)

<!-- key: Hydrogeology and zonation -->
Hidrogeologia e heterogeneidade

<!-- key: Hydrogeology preset -->
Cenário hidrogeológico

<!-- key: Number of zones -->
Número de zonas

<!-- key: Random seed -->
Semente aleatória

<!-- key: K range (m/s) -->
Intervalo K (m/s)

<!-- key: Ss range (1/m) -->
Intervalo Ss (1/m)

<!-- key: Porosity range (-) -->
Intervalo de porosidade (-)

<!-- key: Minimum -->
Mínimo

<!-- key: Maximum -->
Máximo

<!-- key: Edit hydrogeological zones -->
Editar zonas

<!-- key: Zone name -->
Nome da zona

<!-- key: First layer -->
Primeira camada

<!-- key: Last layer -->
Última camada

<!-- key: Porosity -->
Porosidade

<!-- key: Boundary conditions and source -->
Fronteiras e fonte

<!-- key: Input signal -->
Sinal de entrada

<!-- key: Released mass (g) -->
Massa libertada (g)

<!-- key: Mass input rate (g/day) -->
Taxa de entrada de massa (g/dia)

<!-- key: Pulse duration (days) -->
Duração do pulso (dias)

<!-- key: Source x (m) -->
Fonte x (m)

<!-- key: Source y (m) -->
Fonte y (m)

<!-- key: Source cells x -->
Células fonte x

<!-- key: Source cells y -->
Células fonte y

<!-- key: Source spans all layers -->
Fonte em todas as camadas

<!-- key: Source layer (1 = top) -->
Camada fonte (1 = superior)

<!-- key: Transport parameters -->
Parâmetros de transporte

<!-- key: Dispersion -->
Dispersão

<!-- key: Longitudinal dispersivity (m) -->
Dispersividade longitudinal (m)

<!-- key: Horizontal transverse / longitudinal -->
Transversal horizontal / longitudinal

<!-- key: Vertical transverse / longitudinal -->
Transversal vertical / longitudinal

<!-- key: Temporal discretization -->
Discretização temporal

<!-- key: Transport duration (days) -->
Duração do transporte (dias)

<!-- key: DT0 · initial step (days; 0 = automatic) -->
DT0 · passo inicial (dias; 0 = auto)

<!-- key: TTSMAX · maximum step (days; 0 = automatic) -->
TTSMAX · passo máximo (dias; 0 = auto)

<!-- key: TTSMULT · step multiplier -->
TTSMULT · multiplicador do passo

<!-- key: MXSTRN · maximum transport steps -->
MXSTRN · máximo de passos de transporte

<!-- key: Numerical solution for transport -->
Solução numérica do transporte

<!-- key: MT3D advection method -->
Método de advecção MT3D

<!-- key: MODPATH particle comparison -->
Comparação de partículas MODPATH

<!-- key: PERCEL · Courant number -->
PERCEL · número de Courant

<!-- key: CCLOSE · concentration tolerance -->
CCLOSE · tolerância de concentração

<!-- key: Timeout per executable (seconds) -->
Tempo limite por programa (s)

<!-- key: Expert transport solver settings -->
Opções avançadas do solucionador de transporte

<!-- key: MXPART · maximum particles -->
MXPART · máximo de partículas

<!-- key: ITRACK · tracking algorithm -->
ITRACK · algoritmo de seguimento

<!-- key: WD · concentration weighting -->
WD · ponderação da concentração

<!-- key: DCEPS · gradient threshold -->
DCEPS · limiar do gradiente

<!-- key: NPLANE · particle planes -->
NPLANE · planos de partículas

<!-- key: NPL · low-gradient particles -->
NPL · partículas de baixo gradiente

<!-- key: NPH · high-gradient particles -->
NPH · partículas de alto gradiente

<!-- key: NPMIN · minimum particles/cell -->
NPMIN · partículas mín./célula

<!-- key: NPMAX · maximum particles/cell -->
NPMAX · partículas máx./célula

<!-- key: INTERP · interpolation -->
INTERP · interpolação

<!-- key: NLSINK · sink planes -->
NLSINK · planos de sumidouros

<!-- key: NPSINK · sink particles -->
NPSINK · partículas de sumidouros

<!-- key: DCHMOC · HMOC threshold -->
DCHMOC · limiar HMOC

<!-- key: MXITER · GCG outer iterations -->
MXITER · iterações externas GCG

<!-- key: ITER1 · GCG inner iterations -->
ITER1 · iterações internas GCG

<!-- key: ISOLVE · preconditioner -->
ISOLVE · pré-condicionador

<!-- key: NCRS · cross-dispersion -->
NCRS · dispersão cruzada

<!-- key: ACCL · relaxation -->
ACCL · relaxação

<!-- key: IPRGCG · print interval -->
IPRGCG · intervalo de impressão

<!-- key: MODPATH release settings -->
Libertação de partículas MODPATH

<!-- key: Particles per source cell -->
Partículas por célula fonte

<!-- key: Release batches (pulse / continuous) -->
Lotes de libertação (pulso / contínuo)

<!-- key: Observation points -->
Pontos de observação

<!-- key: Number of observation points -->
Número de pontos de observação

<!-- key: Output settings -->
Opções de saída

<!-- key: Saved transport times -->
Tempos de transporte guardados

<!-- key: Actual source footprint -->
Extensão real da fonte

<!-- key: Optional run label -->
Nome opcional da execução

<!-- key: Run model -->
Executar modelo

<!-- key: Run diagnostic -->
Diagnóstico da execução

<!-- key: More comparison metrics -->
Mais métricas de comparação

<!-- key: Displayed run -->
Execução apresentada

<!-- key: Run to remove -->
Execução a eliminar

<!-- key: Remove -->
Eliminar

<!-- key: Clear comparison runs -->
Limpar execuções comparadas

<!-- key: Plume & sections -->
Pluma e secções

<!-- key: Observation curves -->
Curvas de observação

<!-- key: Mass & diagnostics -->
Massa e diagnósticos

<!-- key: Export -->
Exportar

<!-- key: Time (days) -->
Tempo (dias)

<!-- key: Top-view layer -->
Camada em planta

<!-- key: Layer {number} -->
Camada {number}

<!-- key: Analytical reference -->
Referência analítica

<!-- key: Plot settings and section positions -->
Gráficos e posições das secções

<!-- key: x-direction section · y (m) -->
Secção em x · y (m)

<!-- key: y-direction section · x (m) -->
Secção em y · x (m)

<!-- key: Colour fill -->
Preenchimento de cor

<!-- key: Contour lines -->
Isolinhas

<!-- key: Log colours -->
Cores logarítmicas

<!-- key: Particle paths -->
Trajetórias de partículas

<!-- key: Opacity -->
Opacidade

<!-- key: Compare runs in x / y sections -->
Comparar execuções em secções x / y

<!-- key: Compare section profiles -->
Comparar perfis

<!-- key: Runs for section comparison -->
Execuções para comparar secções

<!-- key: Also overlay top-view contours -->
Sobrepor também isolinhas em planta

<!-- key: Download plume figure (PNG) -->
Descarregar figura da pluma (PNG)

<!-- key: Runs in breakthrough comparison -->
Execuções para comparar curvas de chegada

<!-- key: Observation cells used by each run -->
Células de observação por execução

<!-- key: Download breakthrough curves (CSV) -->
Descarregar curvas de chegada (CSV)

<!-- key: Detailed mass-budget data -->
Dados detalhados do balanço de massa

<!-- key: Stored run configuration -->
Configuração guardada

<!-- key: Download comparison table (CSV) -->
Descarregar tabela comparativa (CSV)

<!-- key: Download run configuration (JSON) -->
Descarregar configuração (JSON)

<!-- key: Prepare complete displayed-run archive -->
Preparar arquivo completo da execução apresentada

<!-- key: Preparing archive… -->
A preparar arquivo…

<!-- key: Download run archive (ZIP) -->
Descarregar arquivo (ZIP)

<!-- key: Run -->
Execução

<!-- key: Method -->
Método

<!-- key: Signal -->
Sinal

<!-- key: Grid -->
Malha

<!-- key: K zones -->
Zonas K

<!-- key: Flow -->
Fluxo

<!-- key: MB disc. (%) -->
Desvio massa (%)

<!-- key: Flow disc. (%) -->
Desvio fluxo (%)

<!-- key: MT3D (s) -->
MT3D (s)

<!-- key: MP7 (s) -->
MP7 (s)

<!-- key: Flow (s) -->
Fluxo (s)

<!-- key: Total (s) -->
Total (s)

<!-- key: Ref. L1 (%) -->
Ref. L1 (%)

<!-- key: Mass (g) -->
Massa (g)

<!-- key: Input (g) -->
Entrada (g)

<!-- key: Min. C (g/m³) -->
C mín. (g/m³)

<!-- key: Neg. mass (g) -->
Massa neg. (g)

<!-- key: Centroid x (m) -->
Centroide x (m)

<!-- key: Steps -->
Passos

<!-- key: Source box (m) -->
Dimensões fonte (m)

<!-- key: End (d) -->
Fim (d)

<!-- key: Scenario -->
Cenário

<!-- key: Point -->
Ponto

<!-- key: Requested x -->
x pedido

<!-- key: Requested y -->
y pedido

<!-- key: Requested z -->
z pedido

<!-- key: Cell centre x -->
Centro célula x

<!-- key: Cell centre y -->
Centro célula y

<!-- key: Cell centre z -->
Centro célula z

<!-- key: Layer -->
Camada

<!-- key: Row -->
Linha

<!-- key: Column -->
Coluna

<!-- key: Cumulative in (g) -->
Entrada acumulada (g)

<!-- key: Cumulative out (g) -->
Saída acumulada (g)

<!-- key: Sources (g) -->
Fontes (g)

<!-- key: Sinks (g) -->
Sumidouros (g)

<!-- key: Fluid storage (g) -->
Armazenamento fluido (g)

<!-- key: Native resident mass (g) -->
Massa residente nativa (g)

<!-- key: Alternative disc. (%) -->
Desvio alternativo (%)

<!-- key: Analytical reference requires homogeneous steady flow. -->
A referência analítica requer fluxo permanente homogéneo.

<!-- key: Source cells -->
Células fonte

<!-- key: Specified head -->
Carga especificada

<!-- key: Section locations -->
Posições das secções

<!-- key: Background flow -->
Fluxo de fundo

<!-- key: Model preview: grid, boundaries and source -->
Pré-visualização: malha, fronteiras e fonte

<!-- key: Computed head contours -->
Isopiezas calculadas

<!-- key: Homogeneous steady head contours -->
Isopiezas permanentes homogéneas

<!-- key: Time (d) -->
Tempo (d)

<!-- key: Mass rate (g/d) -->
Taxa de massa (g/d)

<!-- key: Instantaneous mass (g) -->
Massa instantânea (g)

<!-- key: Dirac input (initial cell mass) -->
Entrada Dirac (massa inicial nas células)

<!-- key: Finite pulse input -->
Entrada de pulso finito

<!-- key: Continuous input -->
Entrada contínua

<!-- key: Concentration (g/m³) -->
Concentração (g/m³)

<!-- key: Elevation z (m) -->
Cota z (m)

<!-- key: MODPATH advection (slice) -->
Advecção MODPATH (corte)

<!-- key: Analytical -->
Analítica

<!-- key: Analytical (active run) -->
Analítica (execução ativa)

<!-- key: Mass output unavailable -->
Saída de massa indisponível

<!-- key: MT3D discrepancy (%) -->
Desvio MT3D (%)

<!-- key: Initial + injected mass (first run) -->
Massa inicial + introduzida (primeira execução)

<!-- key: Resident mass: grid sum and MT3D budget -->
Massa residente: soma da malha e balanço MT3D

<!-- key: Reported mass-balance closure -->
Fecho do balanço de massa reportado

<!-- key: Example: pulse plume after 600 days -->
Exemplo: pluma após 600 dias

<!-- key: Example: observation P1 -->
Exemplo: observação P1

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
{layers} camada(s); escala vertical exagerada

<!-- key: fig_total -->
Total: {mass:g} g

<!-- key: fig_initial -->
{mass:g} g em t = 0

<!-- key: fig_xprofile -->
Perfil x em y = {y:.3g} m

<!-- key: fig_yprofile -->
Perfil y em x = {x:.3g} m

<!-- key: fig_section -->
Secção {axis}–z em {other} = {value:.3g} m

<!-- key: fig_title -->
{method} · t = {time:g} d · camada {layer} (z = {z:.3g} m)

<!-- key: fig_gridmass -->
{label}: soma da malha

<!-- key: fig_nativemass -->
{label}: balanço MT3D

<!-- key: fig_nodata -->
{label}: fora do domínio — sem dados

<!-- key: table_help_MB disc. (%) -->
Desvio final do balanço de massa reportado pelo MT3D.

<!-- key: table_help_Flow disc. (%) -->
Desvio final do balanço hídrico MODFLOW.

<!-- key: table_help_MT3D (s) -->
Tempo real do programa de transporte.

<!-- key: table_help_MP7 (s) -->
Tempo MODPATH; as partículas descrevem apenas advecção.

<!-- key: table_help_Ref. L1 (%) -->
Erro absoluto de concentração ponderado pelo volume poroso, dividido pela massa de referência.

<!-- key: table_help_Mass (g) -->
Massa dissolvida final integrada na malha de concentração.

<!-- key: MT3DMS final mass discrepancy exceeds 1%; inspect method and transport time step settings. -->
O desvio final de massa MT3DMS excede 1%; verifique método e passo de transporte.

<!-- key: At least one MODFLOW water-budget discrepancy exceeds 0.1%. -->
Pelo menos um desvio do balanço hídrico MODFLOW excede 0,1%.

<!-- key: Negative concentrations occurred. They are retained in diagnostics and exports; central FD and particle methods can oscillate. -->
Existem concentrações negativas, mantidas nos diagnósticos e exportações. FD central e métodos de partículas podem oscilar.

<!-- key: Source coordinates must lie inside the domain. -->
As coordenadas da fonte devem estar no domínio.

<!-- key: This confined lab requires heads at or above aquifer top. -->
Este modelo confinado requer cargas iguais ou superiores ao topo do aquífero.

<!-- key: Pulse duration must be between zero and model duration. -->
A duração do pulso deve estar entre zero e a duração do modelo.

<!-- key: Observation point is outside the model. -->
O ponto de observação está fora do modelo.

<!-- key: TVD requires PERCEL no greater than 1. -->
TVD requer PERCEL ≤ 1.

<!-- key: language_fallback -->
Uma tradução em falta utiliza o texto inglês.

<!-- key: preset_random -->
Parâmetros aleatórios estocásticos

<!-- key: Random unit x (m) -->
Unidade aleatória x (m)

<!-- key: Random unit y (m) -->
Unidade aleatória y (m)

<!-- key: random_hint -->
Unidades pequenas: padrão fino; grandes: manchas maiores. Mantenha semente e dimensões físicas no refinamento para preservar a realização.

<!-- key: Active cells -->
Células ativas

<!-- key: table_help_Active cells -->
Todas as células não inativas, incluindo as de carga especificada.

<!-- key: Random field -->
Campo aleatório

<!-- key: Comparison runs -->
Execuções comparadas

<!-- key: discard_tags_hint -->
Remova uma etiqueta com × para eliminar a execução. Remover todas inicia nova comparação. Exporte antes o que deseja guardar.

<!-- key: Head contours -->
Isopiezas

<!-- key: Computed head contours (m) -->
Isopiezas calculadas (m)

<!-- key: Head contours appear after running the model -->
As isopiezas aparecem após a execução

<!-- key: fig_background_k -->
K de fundo = {k:.2e} m/s

<!-- key: fig_low_lens_k -->
Lente de K baixa: K = {k:.2e} m/s

<!-- key: fig_high_channel_k -->
Canal de K elevada: K = {k:.2e} m/s

<!-- key: fig_low_barrier_k -->
Barreira de K baixa: K = {k:.2e} m/s

<!-- key: Focus on plume -->
Focar a pluma

<!-- key: Focus threshold (% of peak) -->
Limiar (% do pico)

<!-- key: focus_hint -->
O foco usa o pico positivo atual de cada pluma apresentada, com margem de 20% por lado. Inclui as trajetórias MODPATH visíveis. Sem pluma ou trajetórias mostra todo o domínio. Só muda a vista em planta.

<!-- key: Download plume figure (SVG) -->
Descarregar figura da pluma (SVG)

<!-- key: steady -->
permanente

<!-- key: transient -->
transitório

<!-- key: fig_minimum -->
Mínimo numérico: {minimum:.3g} g/m³

<!-- key: fig_minimum_log -->
Mínimo numérico: {minimum:.3g} g/m³ (valores não positivos ocultos na escala logarítmica)

<!-- key: The plume reaches an x specified-head boundary; enlarge the domain before treating the infinite-x analytical solution as a benchmark. -->
A pluma atinge uma fronteira x de carga especificada; amplie o domínio antes de usar a referência infinita.

<!-- key: fig_reference_boundary -->
Erro analítico desativado: interação com fronteiras x excede o limiar de {tolerance_percent:.2g}%.

<!-- key: Low K lens -->
Lente de K baixa

<!-- key: High K channel -->
Canal de K elevada

<!-- key: Low K barrier -->
Barreira parcial de K baixa
