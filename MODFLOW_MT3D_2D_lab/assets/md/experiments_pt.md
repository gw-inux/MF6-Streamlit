Os controlos estão em **Fluxo e domínio**, **Transporte e fonte** e **Pós-processamento e observações**. Compare perfis sobrepondo execuções; o controlo analítico está à direita.

### 1. Seguir um pulso
Preveja $vt$ e $\dot M\tau$ no caso homogéneo TVD. Execute e percorra os tempos, localizando frente e cauda. Compare perfis, chegadas e referência. Porque dura a chegada mais do que o pulso? Um bom balanço garante uma boa forma?

### 2. Separar alargamento físico e numérico
Sem dispersão, compare FD up, FD cen e TVD com fonte/malha fixas. Registe tempo, mínimo, balanço e erro analítico. Ative dispersão, repita e refine. Verifique o volume real da fonte.

### 3. Métodos de características
Compare MOC, MMOC, HMOC e TVD. Aumente a densidade de partículas apropriada nas opções avançadas. Compare custo, balanço, pluma e chegadas. Reduza PERCEL: porque depende uma solução estável ainda do passo?

### 4. Dirac e pulso
Siga e exporte uma massa inicial Dirac. Escolha um pulso curto de igual massa $M=\dot M\tau$; o novo sinal inicia outra série. Compare os arquivos cedo e tarde. Adicione pontos deslocados em y e explique os picos.

### 5. Contrastes de K
Insira uma lente de K baixa entre fonte e observação. Compare pluma/MODPATH e explique desvios e tempos. Experimente canal, barreira e padrões aleatórios finos/grosseiros. Mantenha semente e unidades físicas ao refinar. Porque não está disponível o erro analítico homogéneo?

### 6. Ler o fluxo permanente
Compare isopiezas homogéneas, lente e aleatório. Altere a diferença de carga com fonte fixa. Altere apenas Ss: porque não muda o resultado? Que estruturas se perdem numa malha grosseira?

### 7. Estender a 3D
Use pelo menos três camadas e fonte numa única camada. Examine x–z/y–z e aumente a dispersividade vertical. O padrão aleatório horizontal atravessa todas as camadas. Repita homogéneo com fonte em toda a espessura e explique a uniformidade vertical.

Preveja antes de executar e fundamente a interpretação com diagnósticos. O foco na pluma mostra detalhes sem alterar resultados.
