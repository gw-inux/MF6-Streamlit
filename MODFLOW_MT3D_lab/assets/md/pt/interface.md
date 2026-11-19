## title

Laboratório de transporte 1D

## experiments

Experiências orientadas

## experiment_front

Frente de advecção

## experiment_spreading

Dispersão física

## experiment_impulse

Pulso e impulso

## theory_title

Escoamento e soluções analíticas

## setup

Configuração do modelo

## inlet_processes

Entrada e transporte

## grid_time

Malha e tempo

## solver

Método MT3DMS

## signal

Sinal de entrada

## continuous

Entrada contínua

## block

Pulso retangular

## dirac

Impulso de Dirac

## amplitude

Concentração de entrada C/Cref [–]

## block_days

Duração do pulso [d]

## impulse_area

Área do impulso A [d]

## impulse_days

Largura numérica ε [d]

## rectangle

Altura de entrada MT3DMS = {height:.4g} C/Cref.

## dispersion

Ativar dispersão

## dispersivity

Dispersividade longitudinal αL [m]

## diffusion

Difusão efetiva Dₑ [m²/d]

## grid_by

Definir a malha por

## cells

Número de células

## spacing

Espaçamento

## cell_count

Células

## target_spacing

Largura pretendida [m]

## grid_summary

{n} células · Δx efetivo = {dx:.3g} m

## courant

Limite de Courant

## time_hint

Todas as variantes terminam no dia 2000. Um pulso finito usa pelo menos oito passos de transporte durante a aplicação.

## scheme

Esquema de advecção

## upwind

DF · montante

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

O MODFLOW-2005 fornece o escoamento estacionário. O MT3DMS resolve as equações implícitas com GCG.

## preview

Pré-visualização do modelo

## preview_summary

{signal} · {scheme} · {n} células · Δx = {dx:.3g} m · D = {D:.4g} m²/d

## distance

Distância desde a entrada [m]

## time

Tempo [d]

## inlet_axis

Entrada C/Cref [–]

## optional_name

Nome da variante (opcional)

## name_example

p. ex. Malha fina com TVD

## limit

Estão guardadas dez variantes. Elimine uma em « Gerir variantes » para executar outra.

## missing

Executável necessário ausente ou incompatível — {names}. Use a pasta partilhada bin ou defina TRANSPORT_LAB_BIN.

## run

Executar modelo

## running

A executar MODFLOW-2005 e MT3DMS…

## failed

O cálculo não foi concluído. As variantes guardadas estão disponíveis abaixo.

## diagnostic

Detalhes do cálculo

## results

Resultados do transporte

## visible

Variantes nos gráficos

## cells_unit

células

## show_analytical

Solução analítica

## show_markers

Pontos numéricos

## profile

Perfil de concentração

## breakthrough

Curva de chegada

## budget

Balanço de massa do soluto

## profile_time

Instante do perfil [d]

## observation

Distância de observação [m]

## applied_curve

Analítica · entrada aplicada

## ideal_curve

Dirac ideal

## mass_axis

Erro de massa [%]

## no_selection

Selecione uma variante para mostrar as suas curvas.

## comparison

Comparação final · dia 2000

## variant

Variante

## rmse

RMSE

## mae

MAE

## ideal_rmse

RMSE · Dirac ideal

## mass_error

Erro de massa [%]

## seconds

Tempo de cálculo [s]

## run_name

Nome

## dx_col

Δx [m]

## height_col

Entrada C/Cref

## duration_col

Duração da entrada [d]

## area_col

Dirac A [d]

## alpha_col

αL [m]

## dm_col

Dₑ [m²/d]

## d_col

D [m²/d]

## pe_col

Péclet da malha

## co_col

Limite de Courant

## count_col

Passos de transporte

## flow_s

MODFLOW [s]

## mt_s

MT3DMS [s]

## flow_error

Balanço hídrico [%]

## min_c

Mín. final C/Cref

## max_c

Máx. final C/Cref

## detail_heading

Definições e indicadores

## download

Descarregar comparação (CSV)

## manage

Gerir variantes

## remove_choice

Variante a eliminar

## remove

Eliminar variante selecionada

## references_title

Referências

## saved

V{number} guardada para comparação.

## applied_color_key

Analítica · cor da variante

## ideal_color_key

Dirac ideal · cor da variante

## pulse_cells

Comprimento do pulso [células]

## pulse_resolution

Durante a entrada, a advecção transporta o pulso {length:.3g} m, equivalentes a {cells:.3g} células.

## specified_head

Carga prescrita · {head:.4g} m

## hydraulic_summary

Condutividade hidráulica K = {k:.0e} m/s

## scenario_reset_hint

As alterações aqui apagam as variantes guardadas.

## comparison_cleared

A entrada ou o transporte foi alterado. A comparação foi limpa para o novo cenário.

## concept_title

Modelo conceptual e respostas típicas

## concept_inlet

Entrada

## concept_outlet

Saída

## concept_observation

Observação

## concept_profile

Perfil em t = {time:g} d

## concept_breakthrough

Passagem em x = {distance:g} m

## concept_advection

Apenas advecção

## concept_dispersion

Advecção + dispersão
