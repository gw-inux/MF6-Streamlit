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
MT3D 2D/3D · v{version} · Versão de trabalho para aulas ao vivo · Desenvolvido por Thomas Reimann · TU Dresden · The Groundwater Project

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

<!-- key: Page width -->
Largura da página

<!-- key: width_1 -->
Estreita

<!-- key: width_2 -->
Compacta

<!-- key: width_3 -->
Padrão

<!-- key: width_4 -->
Ampla

<!-- key: width_5 -->
Largura total

<!-- key: page_width_hint -->
Cinco larguras, de estreita a total. Padrão mantém a largura anterior. A página adapta-se a ecrãs pequenos.

<!-- key: Show model grid -->
Mostrar malha

<!-- key: grid_hint -->
Limites discretos das células da execução apresentada. Perfis de uma camada mostram guias verticais nos bordos das células.

<!-- key: Plume-centered x/y -->
x/y centrados na pluma

<!-- key: relative_hint -->
O zero é o centroide da massa dissolvida positiva na camada apresentada. As sobreposições partilham esta origem. As coordenadas de entrada e cotas mantêm-se absolutas.

<!-- key: relative_mass_origin -->
Origem relativa: x = {x:.2f} m; y = {y:.2f} m (centro de massa da pluma).

<!-- key: relative_source_origin -->
Sem massa positiva nesta camada: origem no centro da fonte ajustada à malha, x = {x:.2f} m; y = {y:.2f} m.

<!-- key: fig_relative_xprofile -->
Perfil x em y′ = {y:.3g} m

<!-- key: fig_relative_yprofile -->
Perfil y em x′ = {x:.3g} m

<!-- key: fig_relative_section -->
Secção {axis}–z em {other}′ = {value:.3g} m

<!-- key: MODPATH particle count -->
Número de partículas MODPATH

<!-- key: particle_count_cell -->
Por célula fonte

<!-- key: particle_count_total -->
Fonte inteira por libertação

<!-- key: Particles in the whole source per release -->
Partículas em toda a fonte por libertação

<!-- key: particle_count_summary -->
{count} partículas em {cells} células fonte × {groups} libertações = {total} partículas.

<!-- key: expert_transport_hint -->
São apresentados todos os controlos do transporte. NPL / NPH e NPMIN / NPMAX controlam as partículas MOC / HMOC; MXPART limita o total. As ajudas indicam os métodos aplicáveis. MODPATH usa partículas independentes.

<!-- key: Plume animation -->
Animação da pluma

<!-- key: Animation view -->
Vista da animação

<!-- key: animation_2d -->
Vista superior e secções

<!-- key: animation_3d -->
Concentrações 3D nos centros das células

<!-- key: Animation frames -->
Fotogramas

<!-- key: Playback speed (frames/s) -->
Velocidade (fotogramas/s)

<!-- key: Vertical exaggeration -->
Exagero vertical

<!-- key: Generate / refresh animation -->
Gerar / atualizar animação

<!-- key: Generating animation… -->
A gerar animação…

<!-- key: Download animation (HTML) -->
Descarregar animação (HTML)

<!-- key: Play -->
Reproduzir

<!-- key: Pause -->
Pausa

<!-- key: Animation frame -->
Fotograma

<!-- key: animation_layers_hint -->
Adicione camadas nas definições avançadas para a vista 3D.

<!-- key: animation_hint -->
Usa os tempos salvos da simulação exibida. Escolha cores e zoom independentes para a animação; a escala permanece fixa no tempo. As outras configurações 2D são mantidas. Comparações e referências analíticas permanecem nos gráficos estáticos. O reprodutor aparece abaixo das configurações; o HTML baixado funciona offline.

<!-- key: animation_3d_hint -->
A vista 3D mostra concentrações nos centros das células acima do limiar, com câmara fixa. Mostra até {maximum} células amostradas uniformemente; cálculos e exportações mantêm todas. As partículas comparam a advecção. O exagero é apenas visual.

<!-- key: animation_refresh_hint -->
As definições mudaram. Gere novamente para atualizar.

<!-- key: animation_failed -->
Não foi possível gerar a animação. Os resultados mantêm-se.

<!-- key: animation_size_limit -->
A animação excede 45 MiB. Reduza os fotogramas.

<!-- key: help_s_percel -->
Deslocamento advectivo máximo por passo, em larguras de célula. TVD exige ≤ 1.

<!-- key: help_s_mxpart -->
MOC/HMOC: capacidade total de partículas móveis, não por célula.

<!-- key: help_s_itrack -->
MOC/MMOC/HMOC: 1 = Euler, 2 = Runge–Kutta de quarta ordem, 3 = seguimento híbrido.

<!-- key: help_s_wd -->
Métodos das características: ponderação da concentração na separação dos operadores; 0,5–1.

<!-- key: help_s_dceps -->
MOC/HMOC: limiar do gradiente relativo que separa NPL e NPH.

<!-- key: help_s_nplane -->
MOC/HMOC: 0 = distribuição aleatória; positivo = planos horizontais por célula.

<!-- key: help_s_npl -->
MOC/HMOC: partículas iniciais por célula com gradiente ≤ DCEPS; zero permitido.

<!-- key: help_s_nph -->
MOC/HMOC: partículas iniciais por célula de gradiente elevado. Padrões fixos podem arredondar o número.

<!-- key: help_s_npmin -->
MOC/HMOC: insere partículas quando o número por célula fica abaixo do mínimo.

<!-- key: help_s_npmax -->
MOC/HMOC: ultrapassar o limite substitui as partículas da célula por NPH partículas.

<!-- key: help_s_interp -->
MMOC/HMOC: interpolação da concentração; apenas 1 (linear) disponível.

<!-- key: help_s_nlsink -->
Células sumidouro MMOC/HMOC: 0 = aleatório; positivo = planos de partículas.

<!-- key: help_s_npsink -->
MMOC/HMOC: partículas que representam cada célula sumidouro.

<!-- key: help_s_dchmoc -->
HMOC: MOC acima deste limiar relativo, MMOC abaixo.

<!-- key: help_s_mxiter -->
Limite de iterações externas GCG. Uma basta para este transporte conservativo linear.

<!-- key: help_s_iter1 -->
Limite de iterações internas GCG para resolver o transporte.

<!-- key: help_s_isolve -->
Pré-condicionador GCG: 1 = Jacobi, 2 = SSOR, 3 = Cholesky incompleto modificado (MIC).

<!-- key: help_s_ncrs -->
Termos cruzados: 0 = aproximação no segundo membro; 1 = tensor completo na matriz.

<!-- key: help_s_accl -->
Fator de relaxação, apenas para SSOR (ISOLVE = 2).

<!-- key: help_s_cclose -->
Tolerância relativa da variação de concentração GCG. Valores menores são mais exigentes.

<!-- key: help_s_iprgcg -->
Imprime variações a cada N iterações GCG; 0 no fim de cada período.

<!-- key: help_s_dt0 -->
Passo inicial em dias; 0 deixa MT3D escolher.

<!-- key: help_s_ttsmult -->
Multiplicador dos passos FD implícitos; ignorado por TVD e características.

<!-- key: help_s_ttsmax -->
Passo máximo em dias se TTSMULT > 1; 0 usa o limite automático.

<!-- key: help_s_mxstrn -->
Máximo de passos de transporte por passo de escoamento; atingir o limite pode parar o cálculo.

<!-- key: help_s_timeout -->
Tempo máximo por executável. Mais partículas podem exigir mais tempo.

<!-- key: help_s_hclose -->
Tolerância PCG de variação da carga, em metros.

<!-- key: help_s_rclose -->
Tolerância do resíduo de caudal PCG, em m³/dia.

<!-- key: help_s_flow_mxiter -->
Máximo de iterações externas do solver de fluxo MODFLOW PCG.

<!-- key: help_s_flow_iter1 -->
Máximo de iterações internas PCG por iteração externa.

<!-- key: help_particle_count_mode -->
Escolha por célula fonte ou um total exato em toda a fonte por libertação.

<!-- key: help_particles_per_cell -->
Distribuição uniforme em cada célula fonte por libertação. Apenas MODPATH, não MOC.

<!-- key: help_total_source_particles -->
Total exato por libertação em todas as células fonte; pelo menos uma por célula. Diferença máxima de uma partícula; pesos pelo volume poroso.

<!-- key: help_release_groups -->
Libertações a meio de intervalos iguais aproximam pulso ou entrada contínua. Mais grupos refinam os tempos; Dirac liberta em t = 0.

<!-- key: help_run_label -->
Deixe vazio para o nome sugerido. O texto substitui método/sinal; número e sufixo heterogéneo continuam automáticos.

<!-- key: help_expert -->
Mostra camadas e todos os parâmetros dos solvers. Mantém os valores ocultos.

<!-- key: help_sliders -->
Alterne entre campos numéricos e deslizadores sem alterar valores.

<!-- key: help_extent -->
Extensão física em metros. Alterá-la inicia uma nova série.

<!-- key: help_thickness -->
Espessura confinada; base a 0 m e topo neste valor. Camadas de igual espessura.

<!-- key: help_grid_mode -->
Defina número ou largura máxima das células. O número arredonda para cima, mantendo o domínio.

<!-- key: help_grid_count -->
Número de células uniformes nesta direção. O refinamento mantém cálculos anteriores.

<!-- key: help_cell_width -->
Largura máxima pedida em metros. A pré-visualização indica a real.

<!-- key: help_nlay -->
Uma camada dá um modelo em planta; várias iguais permitem transporte vertical e vistas 3D.

<!-- key: help_k -->
Condutividade hidráulica horizontal de fundo. Introduza m/s; conversão para m/dia.

<!-- key: help_porosity -->
Fração porosa móvel; controla velocidade intersticial e armazenamento de soluto.

<!-- key: help_ss -->
Água libertada por volume e descida unitária de carga (1/m). Aqui o escoamento estacionário não ativa armazenamento.

<!-- key: help_kv_ratio -->
Condutividade vertical dividida pela horizontal, em cada camada.

<!-- key: help_zones_preset -->
Escolha propriedades homogéneas, campo aleatório repetível ou lente/canal/barreira.

<!-- key: help_zone_seed -->
Semente aleatória. Mesma semente e definições reproduzem o padrão.

<!-- key: help_random_unit -->
Dimensão física dos blocos aleatórios nesta direção, independente da malha.

<!-- key: help_random_k -->
Limites da condutividade aleatória, amostragem uniforme no espaço logarítmico (m/s).

<!-- key: help_random_ss -->
Limites do armazenamento específico log-uniforme (1/m). Guardado, inativo em regime estacionário.

<!-- key: help_random_por -->
Limites da porosidade eficaz uniforme, entre zero e um.

<!-- key: help_head -->
Carga imposta nesta coluna exterior. Esquerda maior que direita; ambas pelo menos ao topo.

<!-- key: help_duration -->
Tempo total simulado em dias, independente da velocidade da animação.

<!-- key: help_dispersion -->
Inclui dispersão mecânica proporcional à velocidade intersticial. Desligada restam advecção e dispersão numérica.

<!-- key: help_al -->
Dispersividade longitudinal em metros; coeficiente associado = αL × velocidade.

<!-- key: help_trpt -->
Dispersividade transversal horizontal dividida pela longitudinal: αTH/αL.

<!-- key: help_trpv -->
Dispersividade transversal vertical dividida pela longitudinal: αTV/αL. Relevante em multicamada.

<!-- key: help_source_kind -->
Dirac: massa inicial em t = 0. Pulso: carga constante até ao fim. Contínuo: carga constante durante todo o cálculo.

<!-- key: help_source_mass -->
Massa dissolvida inicial total no volume poroso fonte (gramas).

<!-- key: help_mass_rate -->
Carga total (g/dia), distribuída pelo volume poroso fonte. Sem injeção de água.

<!-- key: help_pulse_duration -->
A carga termina após este tempo (dias), menor que a duração total.

<!-- key: help_source_position -->
Coordenada absoluta do centro fonte em metros, ajustada a uma célula. Evite colunas de carga imposta.

<!-- key: help_source_cells -->
Células fonte nesta direção. Verifique a extensão; mudar geometria inicia nova série.

<!-- key: help_source_all_layers -->
Distribua a fonte por todas as camadas; caso contrário apenas na escolhida.

<!-- key: help_src_layer -->
Camada que recebe a fonte; 1 é a superior.

<!-- key: help_method -->
Escolha advecção MT3D: FD montante/central, TVD, MOC direto, MMOC inverso ou HMOC híbrido. Independente de MODPATH.

<!-- key: help_track_particles -->
Executa MODPATH 7 no campo calculado. Só advecção; MODPATH não calcula dispersão nem concentrações.

<!-- key: help_observation -->
Coordenada absoluta de observação em metros. Concentração da célula que contém o ponto, sem interpolação.

<!-- key: help_nobs -->
Compare concentrações em um a cinco pontos com cálculos guardados.

<!-- key: help_outputs -->
Tempos guardados, incluindo t = 0 e fim do pulso. Mais saídas refinam animação e curvas, não os passos do solver.

<!-- key: help_length -->
Extensão física em metros. Alterá-la inicia uma nova série.

<!-- key: help_width -->
Extensão física em metros. Alterá-la inicia uma nova série.

<!-- key: help_ncol -->
Número de células uniformes nesta direção. O refinamento mantém cálculos anteriores.

<!-- key: help_nrow -->
Número de células uniformes nesta direção. O refinamento mantém cálculos anteriores.

<!-- key: help_cell_x -->
Largura máxima pedida em metros. A pré-visualização indica a real.

<!-- key: help_cell_y -->
Largura máxima pedida em metros. A pré-visualização indica a real.

<!-- key: help_random_unit_x -->
Dimensão física dos blocos aleatórios nesta direção, independente da malha.

<!-- key: help_random_unit_y -->
Dimensão física dos blocos aleatórios nesta direção, independente da malha.

<!-- key: help_zone_k_min -->
Limites da condutividade aleatória, amostragem uniforme no espaço logarítmico (m/s).

<!-- key: help_zone_k_max -->
Limites da condutividade aleatória, amostragem uniforme no espaço logarítmico (m/s).

<!-- key: help_zone_ss_min -->
Limites do armazenamento específico log-uniforme (1/m). Guardado, inativo em regime estacionário.

<!-- key: help_zone_ss_max -->
Limites do armazenamento específico log-uniforme (1/m). Guardado, inativo em regime estacionário.

<!-- key: help_zone_por_min -->
Limites da porosidade eficaz uniforme, entre zero e um.

<!-- key: help_zone_por_max -->
Limites da porosidade eficaz uniforme, entre zero e um.

<!-- key: help_head_left -->
Carga imposta nesta coluna exterior. Esquerda maior que direita; ambas pelo menos ao topo.

<!-- key: help_head_right -->
Carga imposta nesta coluna exterior. Esquerda maior que direita; ambas pelo menos ao topo.

<!-- key: help_src_x -->
Coordenada absoluta do centro fonte em metros, ajustada a uma célula. Evite colunas de carga imposta.

<!-- key: help_src_y -->
Coordenada absoluta do centro fonte em metros, ajustada a uma célula. Evite colunas de carga imposta.

<!-- key: help_src_ncol -->
Células fonte nesta direção. Verifique a extensão; mudar geometria inicia nova série.

<!-- key: help_src_nrow -->
Células fonte nesta direção. Verifique a extensão; mudar geometria inicia nova série.

<!-- key: help_animation_mode -->
2D anima planta e secções. 3D mostra concentrações nos centros com vista fixa; requer várias camadas.

<!-- key: help_animation_frames -->
Até 80 estados guardados, incluindo primeiro e último. Sem interpolação temporal da concentração.

<!-- key: help_animation_fps -->
Fotogramas por segundo real. Cada imagem indica o tempo simulado; não muda o modelo.

<!-- key: help_animation_exaggeration -->
Altere a altura visual 3D. Cotas e cálculos mantêm-se.

<!-- key: help_generate_animation -->
Renderiza resultados guardados a pedido. Regenere após alterar definições; sem recalcular o modelo.

<!-- key: help_view_time -->
Escolha um tempo guardado, sem recalcular.

<!-- key: help_view_layer -->
Camada em planta; 1 é a superior.

<!-- key: help_section -->
Posição absoluta em metros, na linha/coluna correspondente. Eixos relativos não movem a secção.

<!-- key: help_fill -->
Colore células pela concentração; zero fica branco.

<!-- key: help_lines -->
Desenha isolinhas de concentração sobre as cores.

<!-- key: help_show_heads -->
Sobrepõe isolinhas finas de carga calculada, em metros.

<!-- key: help_log -->
Cores logarítmicas para concentrações positivas. Valores não positivos ocultos só na vista.

<!-- key: help_particle_paths -->
Mostra posições e trajetórias MODPATH até ao tempo escolhido. Máximo 120 trajetórias visíveis; exportação completa.

<!-- key: help_opacity -->
Opacidade: 1 é opaco; valores menores revelam elementos abaixo.

<!-- key: help_focus_plume -->
Aproxima pluma positiva e trajetórias com margem. A animação usa uma janela fixa para os tempos escolhidos.

<!-- key: help_focus_threshold -->
Foco estático: percentagem do pico. Em animação 3D: percentagem do máximo absoluto da escala fixa para mostrar células.

<!-- key: help_analytical -->
Compare com referência analítica homogénea estacionária. Fluxo heterogéneo ou transitório fora das hipóteses.

<!-- key: help_compare -->
Compare cálculos no tempo disponível mais próximo nas secções do apresentado.

<!-- key: help_analytic_on -->
Compare com referência analítica homogénea estacionária. Fluxo heterogéneo ou transitório fora das hipóteses.

<!-- key: help_btc_analytical -->
Compare com referência analítica homogénea estacionária. Fluxo heterogéneo ou transitório fora das hipóteses.

<!-- key: help_compare_sections -->
Compare cálculos no tempo disponível mais próximo nas secções do apresentado.

<!-- key: help_overlay_runs -->
Compare cálculos no tempo disponível mais próximo nas secções do apresentado.

<!-- key: help_compare_top -->
Compare cálculos no tempo disponível mais próximo nas secções do apresentado.

<!-- key: help_btc_runs -->
Compare concentrações em um a cinco pontos com cálculos guardados.

<!-- key: Animation settings -->
Configurações da animação

<!-- key: Animation colour scale -->
Escala de cores da animação

<!-- key: animation_colour_enhanced -->
Concentrações baixas realçadas (escala fixa)

<!-- key: animation_colour_linear -->
Linear (escala fixa)

<!-- key: animation_colour_log -->
Logarítmica (escala fixa)

<!-- key: help_animation_colour -->
O realce usa uma transformação de potência (expoente 0,35) para revelar concentrações pequenas. Todos os quadros mantêm os mesmos limites físicos de concentração; zero permanece branco. As escalas linear e realçada conservam valores numéricos negativos; a logarítmica oculta valores não positivos. Os dados calculados não são alterados.

<!-- key: Zoom animation to plume -->
Ampliar a pluma na animação

<!-- key: help_animation_focus -->
Uma janela fixa abrange a pluma positiva e as trajetórias MODPATH exibidas em todos os tempos selecionados, com margem de 20 %. Independente do zoom estático. Desative para mostrar todo o domínio. Disponível em 2D e 3D.

<!-- key: Plume threshold (% of peak) -->
Limiar da pluma (% do máximo)

<!-- key: help_animation_threshold -->
O zoom inclui concentrações acima desta percentagem do máximo positivo de cada quadro. Em 3D, também define o limiar das células visíveis em relação à concentração absoluta máxima da escala fixa. Padrão: 0,1 %. Afeta apenas a visualização.

<!-- key: animation_progress -->
Gerando animação… {percent} %

<!-- key: MODPATH settings -->
Configurações do MODPATH

<!-- key: expert_transport_location_hint -->
Os parâmetros avançados do MT3D estão no painel expansível separado **Opções avançadas do solucionador de transporte**, logo abaixo. As configurações do MODPATH aparecem em seguida.
