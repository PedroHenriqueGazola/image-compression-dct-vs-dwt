# Comparação de Técnicas de Compressão de Imagem: Transformada Discreta do Cosseno (DCT) vs Transformada Wavelet (DWT)

Este repositório contém um código Python que implementa e compara duas técnicas de compressão de imagem: a Transformada Discreta do Cosseno (DCT) e a Transformada Wavelet (DWT). Ambas as técnicas são amplamente utilizadas em compressão de imagem e o código foi desenvolvido para avaliar a eficácia de cada uma delas em termos de qualidade da reconstrução da imagem e tamanho do arquivo comprimido.

## Conteúdo do Código

### Bibliotecas Utilizadas

- `cv2`: Para manipulação de imagens, carregamento e aplicação da Transformada Discreta do Cosseno (DCT).
- `numpy`: Para operações matemáticas e manipulação de matrizes.
- `matplotlib.pyplot`: Para visualização gráfica das imagens originais e reconstruídas.
- `pywt`: Para aplicação da Transformada Wavelet Discreta (DWT).
- `os`: Para manipulação de arquivos e cálculo dos tamanhos dos arquivos.

### Estrutura do Código

O código está dividido em várias funções para modularizar o processo de compressão, reconstrução e análise de imagem. Abaixo está uma explicação detalhada de cada função.

#### Funções de Transformada Discreta do Cosseno (DCT)

1. **`apply_dct(image)`**

   - **Descrição**: Aplica a Transformada Discreta do Cosseno (DCT) em blocos de 8x8 da imagem. A DCT é uma técnica de transformação que converte a imagem para o domínio de frequência, permitindo a compressão através da eliminação de frequências menos significativas.
   - **Entrada**: Imagem em escala de cinza.
   - **Saída**: Imagem transformada com coeficientes DCT.

2. **`apply_quantization(dct_image, block_size=8, quantization_value=20)`**

   - **Descrição**: Aplica uma quantização nos coeficientes DCT, reduzindo a precisão das frequências de alta frequência, o que permite a compressão da imagem.
   - **Entrada**: Imagem com coeficientes DCT, tamanho do bloco e valor de quantização.
   - **Saída**: Imagem com coeficientes DCT quantizados.

3. **`apply_idct(quantized_dct, block_size=8)`**
   - **Descrição**: Aplica a Inversa da DCT em blocos de 8x8 para reconstruir a imagem a partir dos coeficientes quantizados.
   - **Entrada**: Imagem com coeficientes DCT quantizados.
   - **Saída**: Imagem reconstruída no domínio espacial.

#### Funções de Transformada Wavelet (DWT)

1. **`apply_dwt(image, wavelet='haar', level=1)`**

   - **Descrição**: Aplica a Transformada Discreta Wavelet (DWT) à imagem, decompõe a imagem em sub-bandas de diferentes frequências (aproximação e detalhes).
   - **Entrada**: Imagem em escala de cinza, tipo de wavelet e nível de decomposição.
   - **Saída**: Coeficientes wavelet da imagem.

2. **`apply_thresholding(coeffs, threshold=20)`**

   - **Descrição**: Aplica um threshold (limiar) aos coeficientes wavelet para eliminar valores insignificantes, o que ajuda a reduzir o tamanho da imagem ao remover detalhes de baixa importância.
   - **Entrada**: Coeficientes wavelet da imagem e valor do threshold.
   - **Saída**: Coeficientes wavelet após a aplicação do threshold.

3. **`apply_idwt(coeffs, wavelet='haar')`**
   - **Descrição**: Reconstroi a imagem a partir dos coeficientes wavelet modificados usando a Inversa da Transformada Wavelet.
   - **Entrada**: Coeficientes wavelet modificados.
   - **Saída**: Imagem reconstruída no domínio espacial.

#### Funções de Avaliação de Qualidade

1. **`calculate_mse(original, reconstructed)`**

   - **Descrição**: Calcula o Erro Quadrático Médio (MSE) entre a imagem original e a imagem reconstruída. O MSE indica a diferença média ao quadrado entre os pixels correspondentes das duas imagens.
   - **Entrada**: Imagem original e imagem reconstruída.
   - **Saída**: Valor do MSE.

2. **`calculate_psnr(original, reconstructed)`**
   - **Descrição**: Calcula o Pico da Razão Sinal-Ruído (PSNR) entre a imagem original e a imagem reconstruída. O PSNR mede a qualidade da reconstrução, sendo que valores mais altos indicam melhor qualidade.
   - **Entrada**: Imagem original e imagem reconstruída.
   - **Saída**: Valor do PSNR (em dB).

### Fluxo do Código Principal

1. **Carregar a Imagem**: A imagem de entrada é carregada em escala de cinza usando a função `cv2.imread()`.

2. **Salvar a Imagem Original**: A imagem original é salva com compressão JPEG de alta qualidade (95%) para fins de comparação.

3. **Compressão Usando DCT**:

   - Aplica-se a DCT na imagem.
   - A quantização é realizada para reduzir a precisão dos coeficientes de alta frequência.
   - A imagem é reconstruída aplicando a inversa da DCT.
   - A imagem reconstruída é salva com compressão JPEG de qualidade 70%.

4. **Compressão Usando DWT**:

   - A DWT é aplicada na imagem usando a wavelet 'haar'.
   - Thresholding é aplicado para reduzir os detalhes de baixa importância.
   - A imagem é reconstruída aplicando a inversa da DWT.
   - A imagem reconstruída é salva com compressão JPEG de qualidade 70%.

5. **Mostrar Imagens**: As imagens original, reconstruída usando DCT e reconstruída usando DWT são exibidas lado a lado usando `matplotlib`.

6. **Comparação de Qualidade**:
   - O MSE e o PSNR são calculados para ambas as técnicas (DCT e DWT) em relação à imagem original.
   - Os tamanhos dos arquivos das imagens original, DCT e DWT são obtidos usando `os.path.getsize()`.
   - Os resultados são exibidos no console, incluindo a diferença percentual de tamanho em relação à imagem original.

### Resultados de Comparação

- **Erro Quadrático Médio (MSE)**: Quanto menor o MSE, maior a similaridade entre a imagem original e a reconstruída.
- **Pico da Razão Sinal-Ruído (PSNR)**: Um valor de PSNR mais alto indica uma melhor qualidade da reconstrução.
- **Tamanhos dos Arquivos**: O objetivo é reduzir o tamanho do arquivo mantendo uma qualidade visual aceitável.

Os resultados da comparação mostraram que a Transformada Discreta do Cosseno (DCT) teve um desempenho melhor em termos de qualidade de reconstrução, com menor MSE e maior PSNR, além de uma boa redução no tamanho do arquivo. A Transformada Wavelet (DWT) apresentou uma redução de tamanho similar, mas a qualidade da reconstrução foi inferior à obtida com a DCT.

### Executando o Código

Para executar o código, siga os seguintes passos:

1. Certifique-se de que todas as bibliotecas necessárias estejam instaladas. Você pode instalar as dependências usando o seguinte comando:

   ```sh
   pip install numpy opencv-python matplotlib PyWavelets
   ```

2. Execute o script Python no terminal:
   ```sh
   python nome_do_arquivo.py
   ```

### Conclusão

Este projeto implementa duas técnicas populares de compressão de imagem e as compara em termos de qualidade e eficiência de compressão. A DCT mostrou-se mais vantajosa neste experimento, mantendo uma melhor qualidade visual da imagem reconstruída e oferecendo uma redução significativa no tamanho do arquivo. A DWT, apesar de também ser eficiente na redução de tamanho, apresentou uma qualidade inferior na reconstrução.
