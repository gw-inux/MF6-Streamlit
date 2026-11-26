### Modelo conceptual
O laboratório segue um soluto conservativo num aquífero confinado e saturado. As cargas especificadas na primeira e última coluna geram o fluxo de fundo. As restantes faces são fechadas ao fluxo de água e ao fluxo dispersivo. A água que entra tem concentração nula; a que sai transporta a concentração residente. Não se incluem reações, sorção, efeitos de densidade, recarga ou bombagem.

Uma camada representa transporte horizontal 2D. Várias camadas permitem gradientes e dispersão verticais. Uma fonte uniforme em toda a espessura de um meio homogéneo mantém uniformidade vertical: acrescentar camadas não cria fluxo vertical. Uma fonte numa única camada permite experiências 3D.

Unidades: m, dias, g e g/m³ de água; 1 g/m³ = 1 mg/L. Internamente, K usa m/d: $10^{-4}$ m/s = 8,64 m/d.

### Fluxo e armazenamento
A velocidade intersticial homogénea permanente é:
$$
v_x=\frac{K}{n_e}\frac{h_L-h_R}{L-\Delta x}.
$$
O denominador é a distância entre os **centros das células** de carga especificada, não entre faces externas. MODFLOW calcula o fluxo heterogéneo com K locais. A condutividade vertical é a horizontal local multiplicada pela razão selecionada.

A interface utiliza fluxo permanente. Ss é guardado como propriedade, mas não altera cargas ou velocidades permanentes. Todas as cargas devem estar no topo do aquífero ou acima dele. O rendimento específico não é utilizado.

### Sinais de entrada
| Sinal | Representação | Quantidade conservada |
|---|---|---|
| Dirac | Concentração inicial uniforme nas células fonte | Massa inicial $M$ |
| Pulso retangular | Taxa de massa prescrita até $\tau$ | Massa total $\dot M\tau$ |
| Contínuo | Taxa de massa durante toda a simulação | Massa aplicada até $t$: $\dot M t$ |

São fontes internas de massa: não adicionam água nem perturbam o fluxo. O pulso termina num limite de período de solicitação, seguido de taxa explicitamente nula. Dirac é instantâneo no tempo, mas tem volume finito. A concentração inicial homogénea é $M/(n_eV_s)$; porosidades diferentes são ponderadas pelo volume poroso para obter concentração inicial igual.

A fonte acompanha as células selecionadas. Verifique as dimensões e a posição após refinar: manter o número de células fonte altera também o seu volume físico.

### Advecção e dispersão
Para fluxo homogéneo permanente em x:
$$
\frac{\partial C}{\partial t}
=D_x\frac{\partial^2 C}{\partial x^2}
+D_y\frac{\partial^2 C}{\partial y^2}
+D_z\frac{\partial^2 C}{\partial z^2}
-v_x\frac{\partial C}{\partial x}+\frac{s}{n_e}.
$$
$s$ é a entrada de soluto por volume total e tempo. $D_x=\alpha_L|v_x|+D_e$, $D_y=\alpha_{TH}|v_x|+D_e$ e $D_z=\alpha_{TV}|v_x|+D_e$. As dispersividades transversais são razões de $\alpha_L$. No fluxo heterogéneo, MT3D constrói o tensor com as velocidades locais. A difusão molecular é zero. Desligar a dispersão remove o alargamento mecânico. Com uma camada e topo/base fechados, a dispersividade vertical não tem efeito e só é apresentada para várias camadas.

| Método | Opção MT3D | O que investigar |
|---|---|---|
| FD up | MIXELM = 0, NADVFD = 0 | Suavização por dispersão numérica |
| FD cen | MIXELM = 0, NADVFD = 2 | Oscilações e concentrações negativas em malhas grosseiras dominadas pela advecção |
| TVD | MIXELM = −1 | Frentes nítidas com limitação de fluxo |
| MOC | MIXELM = 1 | Características para a frente; densidade de partículas |
| MMOC | MIXELM = 2 | Características para trás; balanço de massa |
| HMOC | MIXELM = 3 | Alternância local MOC/MMOC |

As opções avançadas abrangem advecção, GCG, passos de transporte e tolerâncias MODFLOW. Alguns parâmetros só se aplicam a certos métodos: MXPART limita partículas móveis MOC/HMOC. PERCEL controla o deslocamento por passo; TVD exige PERCEL ≤ 1. Terminar normalmente não demonstra exatidão.

### Referência analítica
A referência pressupõe velocidade, porosidade e dispersão constantes. Integra a função de Green no **volume real da fonte** e em cada célula recetora. As fronteiras y/z refletem soluto; x é infinito. Uma fonte em toda a espessura de uma camada dá a solução 2D normalizada pela espessura. Pulso e contínuo usam convolução temporal.

A função de Green pontual instantânea 3D ilimitada é:
$$
C=\frac{M}{n_e(4\pi t)^{3/2}\sqrt{D_xD_yD_z}}
\exp\!\left[-\frac{(x-x_s-v_xt)^2}{4D_xt}
-\frac{(y-y_s)^2}{4D_yt}-\frac{(z-z_s)^2}{4D_zt}\right].
$$
Em 2D horizontal o denominador torna-se $4\pi n_e b t\sqrt{D_xD_y}$ e omite-se o termo z. Estas fórmulas explicam a forma; a comparação usa volumes finitos para manter a diluição coerente com MT3D.

A referência homogénea não é exata para meios zonados ou fluxo transitório: as métricas de erro são suprimidas. As fronteiras x devem estar longe da pluma. O teste de retenção de massa sinaliza proximidade às fronteiras, mas não prova equivalência entre domínios finito e infinito. Amplie o domínio e teste a sensibilidade perto das fronteiras.

### MODPATH e resultados
MODPATH 7 segue trajetórias advectivas usando o fluxo MODFLOW e a mesma porosidade. Não calcula dispersão nem concentrações. A largura da nuvem de partículas não representa uma pluma dispersiva. A massa associada é um peso de quadratura da libertação, não um balanço de soluto MODPATH. As partículas MOC têm outra função.

Compare forma, curvas de chegada e tabela. Um desvio pequeno de balanço pode coexistir com alargamento ou oscilações. Mantenha fonte, propriedades e malha ao comparar métodos. O tempo depende da carga da máquina: repita na mesma máquina. Observações usam a célula que contém o ponto; secções seguem a malha. Conservam-se concentrações com sinal; a escala logarítmica oculta valores não positivos. Examine também a escala linear e o mínimo.

### Heterogeneidade, séries e foco
Cenários: homogéneo, aleatório, lente de K baixa, canal de K elevada e barreira parcial. O fundo de referência é branco; os contrastes têm cor e legenda K em m/s. As unidades aleatórias formam uma grelha física: pequenas para padrão fino, grandes para manchas maiores. K e Ss são uniformes em espaço logarítmico; porosidade, em espaço linear. O padrão horizontal atravessa todas as camadas. Não é um campo geoestatístico com covariância prescrita.

Semente e dimensões físicas fixas preservam a realização ao refinar. Cada célula amostra a unidade que contém o seu centro; malhas grosseiras podem perder pequenas estruturas. Os formatos antigos de retângulos e fluxo transitório continuam reproduzíveis fora da interface.

A execução mais recente é apresentada automaticamente. Sinal ou geometria física novos iniciam outra série; discretização e ajustes numéricos são variantes. **het.** identifica heterogeneidade. Remover etiquetas × elimina execuções. As isopiezas calculadas aparecem por predefinição. Uma camada: perfis de concentração x/y; várias: mapas x–z/y–z de concentração em função da cota.

O foco usa **0,1% do pico positivo atual** de cada pluma apresentada e **20% de margem por lado**, incluindo trajetórias MODPATH visíveis. O limiar é ajustável. Sem pluma nem trajetórias, mantém-se o domínio completo. Só mudam os limites da vista em planta; concentrações, secções e escala de cores não mudam.

### Referências
As quatro aplicações analíticas fornecidas inspiraram os exemplos. As suas fórmulas pontuais ou de concentração imposta não substituem diretamente o teste de fonte de massa de volume finito usado aqui.


- [FloPy — MT3DMS ADV](https://flopy.readthedocs.io/en/3.12.0/source/flopy.mt3d.mtadv.html)
- [FloPy — MT3DMS SSM](https://flopy.readthedocs.io/en/3.12.0/source/flopy.mt3d.mtssm.html)
- [FloPy — MT3DMS GCG](https://flopy.readthedocs.io/en/3.12.0/source/flopy.mt3d.mtgcg.html)
- [Pollock (2016) — MODPATH 7, USGS](https://pubs.usgs.gov/publication/ofr20161086)
- [Wexler (1992) — USGS](https://pubs.usgs.gov/twri/twri3-b7/)
- [MODFLOW-ORG](https://github.com/MODFLOW-ORG/executables)

### Malha, coordenadas relativas e largura

A malha acrescenta bordos cinzentos discretos em planta e nas secções da execução apresentada; os perfis de uma camada mostram guias verticais nos bordos das células. A origem x′/y′ é o centroide da massa dissolvida positiva da camada apresentada, incluindo a porosidade local. Sem massa positiva usa-se o centro da fonte ajustada à malha. Comparações, referência e partículas partilham a origem; cotas, entradas e exportações numéricas continuam absolutas. É independente do foco da pluma. Há cinco larguras no topo; Padrão mantém a anterior. O campo do nome vazio é amarelo e torna-se verde ao confirmar texto não vazio com Enter ou ao sair do campo.
