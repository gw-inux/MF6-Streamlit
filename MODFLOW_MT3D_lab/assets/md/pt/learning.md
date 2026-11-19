## introduction

Explore o transporte de um soluto conservativo ao longo de uma trajetória de escoamento subterrâneo com um modelo unidimensional simples. Compare o MT3DMS com soluções analíticas para observar como a discretização e os métodos numéricos afetam o sinal transportado.

## concept_explanation

Imagine um tubo de corrente estreito ao longo de um percurso de água subterrânea num aquífero homogéneo e saturado. A água escoa em regime estacionário. Um soluto conservativo entra a montante e é transportado por advecção. A dispersão pode alargar o sinal ao longo do percurso.

Este modelo unidimensional idealizado permite estudar a influência do método numérico, da dimensão das células e do passo de tempo. Compare o MT3DMS com a solução analítica para examinar o alargamento da frente, as oscilações, o tempo de percurso e o balanço de massa. Escolha primeiro o sinal e os processos e compare até dez variantes numéricas do mesmo cenário.

## concept_caption

Tubo de corrente esquemático com escoamento unidimensional permanente e um ponto de observação a 250 m. Não há troca de água ou soluto através dos limites laterais; as dimensões transversais não estão à escala.

## concept_response_caption

Respostas analíticas ilustrativas a uma entrada retangular de 400 d com C/Cref = 1 e v = 0,24 m/d. Verde: apenas advecção; azul: dispersividade longitudinal de 10 m, D = 2,4 m²/d e difusão molecular nula. Estes exemplos fixos são independentes dos parâmetros atuais do modelo.

## front_task

1. Escolha entrada contínua, 21 células, diferenças finitas a montante e dispersão desativada. Preveja a posição da frente no dia 2000 a partir da velocidade intersticial.
2. Execute o modelo e examine as concentrações dos dois lados da frente analítica.
3. Repita com TVD e depois com 101 células. Compare a largura da frente, o erro do perfil e o balanço de massa.

## spreading_task

1. Use entrada contínua, dispersividade de 10 m, difusão nula e TVD com 21 células. Examine o perfil analítico.
2. Repita com 101 células e depois com diferenças a montante. Que parte do alargamento aparece também na solução analítica?
3. Examine as curvas a 250 m. Desative a dispersão para iniciar uma comparação com advecção pura. As alterações em « Entrada e transporte » apagam as variantes guardadas.

## impulse_task

1. Escolha um pulso retangular de 400 d e siga as suas frentes no perfil e a 250 m.
2. Inicie um cenário Dirac com área de 50 d, largura de 50 d, 101 células e dispersividade de 10 m. Registe os RMSE do pulso aplicado e do impulso ideal.
3. Reduza a largura para 10 d mantendo a área. Calcule o novo cenário e compare os erros registados. Refine depois a malha desse cenário e verifique o balanço de massa.

## theory

O aquífero confinado tem 1 m de espessura e 1 m de largura. As cargas prescritas, aproximadamente 6,944 m e 0 m, atuam nos centros das células extremas, separados por 1000 m. Com $K=10^{-4}$ m/s e $n_e=0.25$, o fluxo de Darcy é 0,06 m/d e a velocidade intersticial $v$ é 0,24 m/d. O interior começa sem soluto. A água sai com a concentração local. A referência é $C_{\mathrm{ref}}=1$ g/m³, equivalente a 1 mg/L.

A equação é $\partial C/\partial t=D\partial^2 C/\partial x^2-v\partial C/\partial x$, com $D=\alpha_Lv+D_e$. Sem dispersão, o sinal percorre $vt$. Para $D>0$, a resposta a um degrau unitário de concentração prescrita numa coluna semi-infinita é

$$
S(x,t)=\tfrac12\left[\operatorname{erfc}\!\left(\frac{x-vt}{2\sqrt{Dt}}\right)
+e^{vx/D}\operatorname{erfc}\!\left(\frac{x+vt}{2\sqrt{Dt}}\right)\right],\quad t>0.
$$

Uma entrada contínua de altura $H$ produz $HS(x,t)$. Um retângulo de duração $\tau$ produz $H[S(x,t)-S(x,t-\tau)]$, sendo o segundo termo nulo antes do corte. Para um impulso Dirac na entrada de área $A=\int(C_{\mathrm{in}}/C_{\mathrm{ref}})dt$, a resposta interior é

$$
A\frac{\partial S}{\partial t}
=A\,\frac{x}{\sqrt{4\pi D t^3}}\exp\!\left[-\frac{(x-vt)^2}{4Dt}\right].
$$

O MT3DMS aplica um retângulo de largura $\varepsilon$ e altura $A/\varepsilon$, conservando a área do histórico da concentração de entrada. O balanço real também inclui o fluxo dispersivo nessa fronteira. Para $D=0$, o impulso ideal viaja a $v$ e não tem um pico pontual finito.

## profile_hint

Os perfis numéricos usam concentrações nos centros das células. Os instantes intermédios são interpolados linearmente entre passos guardados. O dia 2000 usa o resultado final do modelo.

## breakthrough_hint

Cada passo de transporte é guardado. A concentração é interpolada entre centros de células na distância escolhida. O tempo de percurso advectivo é {t:.1f} d.

## balance_hint

O desvio acumulado com sinal provém de TOTAL IN–OUT no ficheiro MAS. É expresso em percentagem da média das massas absolutas de entrada e saída, incluindo armazenamento. Um pequeno desvio pode coexistir com uma frente alargada.

## dirac_reading

A linha tracejada corresponde ao pulso aplicado. A linha pontilhada representa o Dirac ideal. Sem dispersão, a linha vertical indica a posição ou chegada do impulso. A sua altura não representa concentração.

## outlet_hint

Para {ids}, o degrau analítico a 1000 m atinge pelo menos 1 % no dia 2000. A saída da coluna finita pode influenciar o trecho a jusante. Esta verificação inclui pulsos, cuja concentração na saída pode ser menor.

## table_hint

Todas as variantes são avaliadas nos mesmos 90 intervalos de 10 m entre 50 e 950 m. RMSE e MAE comparam o perfil final com a solução analítica do sinal aplicado, em C/Cref.

## mass_warning

{ids} ultrapassa 1 % de desvio absoluto de massa no dia 2000. Examine o balanço e o perfil. Um método de partículas pode falhar um pulso curto numa malha grosseira.

## metrics_notes

A concentração numérica é constante em cada célula e é ponderada pela sobreposição com cada intervalo de 10 m. A solução analítica é integrada no mesmo intervalo. As células de fronteira são excluídas mesmo na malha mais grosseira. RMSE é a raiz da média dos resíduos ao quadrado. MAE é a média dos resíduos absolutos.

Para Dirac, o RMSE adicional usa o impulso ideal. Sem dispersão, o seu peso espacial é $vA$. Um impulso numa fronteira partilhada contribui com metade para cada lado. Mantenha o sinal e a sua intensidade ao comparar métodos.

O tempo de cálculo inclui os dois executáveis e exclui preparação, leitura e gráficos. O balanço hídrico é o último desvio MODFLOW. O número de Péclet é $v\Delta x/D$, infinito em advecção pura. As diferenças centradas podem produzir concentrações fora do intervalo de entrada, visíveis nos gráficos.

## references

- `TRANS_1D_MT3D.ipynb`, MWW01.
- Zheng & Wang (1999), *MT3DMS*, 1. [MODFLOW benchmark](https://modflow6-examples.readthedocs.io/en/latest/_examples/ex-gwt-mt3dms-p01.html)
- Wexler (1992), *Analytical Solutions for One-, Two-, and Three-Dimensional Solute Transport in Ground-Water Systems with Uniform Flow*. [USGS TWRI 3-B7](https://pubs.usgs.gov/twri/twri3-b7/pdf/twri_3-B7_a.pdf)
- Pérez Guerrero et al. (2013), *Analytical solutions of the one-dimensional advection–dispersion solute transport equation subject to time-dependent boundary conditions*. [DOI](https://doi.org/10.1016/j.cej.2013.01.095)
- FloPy [MT3DMS ADV](https://flopy.readthedocs.io/en/latest/source/flopy.mt3d.mtadv.html), [MT3DMS SSM](https://flopy.readthedocs.io/en/latest/source/flopy.mt3d.mtssm.html).

## method_upwind

A concentração a montante determina o fluxo advectivo em cada face. Observe o alargamento da frente quando a dispersão física está desativada.

## method_central

O fluxo usa as concentrações dos dois lados da face. Em malhas grosseiras dominadas pela advecção podem surgir oscilações junto de frentes abruptas.

## method_tvd

O ULTIMATE TVD de terceira ordem limita fluxos junto de gradientes fortes. Compare a largura da frente com a obtida por diferenças a montante.

## method_moc

O método das características segue partículas para a frente. Aqui o MT3DMS coloca inicialmente quatro partículas em células com gradiente de concentração suficiente.

## method_mmoc

O método das características modificado segue trajetórias para trás para estimar a concentração transportada para uma célula.

## method_hmoc

O método híbrido alterna MOC e MMOC segundo o gradiente local de concentração.

