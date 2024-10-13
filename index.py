# Código para Compressão de Imagem usando Transformada Discreta do Cosseno (DCT) e Transformada Wavelet (DWT)

import cv2
import numpy as np
import matplotlib.pyplot as plt
import pywt
import os

# Função para aplicar a Transformada Discreta do Cosseno (DCT)
def apply_dct(image):
    height, width = image.shape
    dct_image = np.zeros((height, width))
    block_size = 8
    
    # Aplicar DCT em blocos de 8x8
    for i in range(0, height, block_size):
        for j in range(0, width, block_size):
            block = image[i:i+block_size, j:j+block_size]
            if block.shape == (block_size, block_size):  # Garantir que o bloco é 8x8
                dct_block = cv2.dct(np.float32(block))
                dct_image[i:i+block_size, j:j+block_size] = dct_block
    
    return dct_image

# Função para aplicar a quantização nos coeficientes DCT
def apply_quantization(dct_image, block_size=8, quantization_value=20):
    height, width = dct_image.shape
    quantized_dct = np.zeros((height, width))
    quantization_matrix = np.ones((block_size, block_size)) * quantization_value
    
    # Aplicar a quantização em blocos de 8x8
    for i in range(0, height, block_size):
        for j in range(0, width, block_size):
            block = dct_image[i:i+block_size, j:j+block_size]
            if block.shape == (block_size, block_size):  # Garantir que o bloco é 8x8
                quantized_block = np.round(block / quantization_matrix) * quantization_matrix
                quantized_dct[i:i+block_size, j:j+block_size] = quantized_block
    
    return quantized_dct

# Função para aplicar a inversa da DCT e reconstruir a imagem
def apply_idct(quantized_dct, block_size=8):
    height, width = quantized_dct.shape
    reconstructed_image = np.zeros((height, width), dtype=np.float32)
    
    # Aplicar a Inversa da DCT em blocos de 8x8
    for i in range(0, height, block_size):
        for j in range(0, width, block_size):
            block = quantized_dct[i:i+block_size, j:j+block_size]
            if block.shape == (block_size, block_size):  # Garantir que o bloco é 8x8
                idct_block = cv2.idct(block)
                reconstructed_image[i:i+block_size, j:j+block_size] = idct_block
    
    return np.uint8(np.clip(reconstructed_image, 0, 255))

# Função para aplicar a Transformada Discreta Wavelet (DWT)
def apply_dwt(image, wavelet='haar', level=1):
    coeffs = pywt.wavedec2(image, wavelet=wavelet, level=level)
    return coeffs

# Função para aplicar o thresholding nos coeficientes DWT
def apply_thresholding(coeffs, threshold=20):
    thresholded_coeffs = []
    for coeff in coeffs:
        if isinstance(coeff, tuple):
            thresholded_coeffs.append(tuple(np.where(np.abs(c) > threshold, c, 0) for c in coeff))
        else:
            thresholded_coeffs.append(np.where(np.abs(coeff) > threshold, coeff, 0))
    return thresholded_coeffs

# Função para reconstruir a imagem a partir dos coeficientes DWT
def apply_idwt(coeffs, wavelet='haar'):
    reconstructed_image = pywt.waverec2(coeffs, wavelet=wavelet)
    return np.uint8(np.clip(reconstructed_image, 0, 255))

# Função para calcular o erro quadrático médio (MSE)
def calculate_mse(original, reconstructed):
    return np.mean((original - reconstructed) ** 2)

# Função para calcular o pico da razão sinal-ruído (PSNR)
def calculate_psnr(original, reconstructed):
    mse = calculate_mse(original, reconstructed)
    if mse == 0:
        return float('inf')
    max_pixel = 255.0
    psnr = 20 * np.log10(max_pixel / np.sqrt(mse))
    return psnr

# Carregar a imagem em escala de cinza
image = cv2.imread('imagem_exemplo.jpg', cv2.IMREAD_GRAYSCALE)

# Salvar a imagem original com compressão JPEG
cv2.imwrite('imagem_original.jpg', image, [cv2.IMWRITE_JPEG_QUALITY, 95])

# Aplicar DCT, quantização e IDCT
print("Processando compressão usando DCT...")
dct_image = apply_dct(image)
quantized_dct = apply_quantization(dct_image)
reconstructed_image_dct = apply_idct(quantized_dct)

# Salvar a imagem reconstruída usando DCT com compressão JPEG
cv2.imwrite('imagem_reconstruida_dct.jpg', reconstructed_image_dct, [cv2.IMWRITE_JPEG_QUALITY, 70])

# Aplicar DWT, thresholding e IDWT
print("Processando compressão usando DWT...")
dwt_coeffs = apply_dwt(image, wavelet='haar', level=2)
thresholded_coeffs = apply_thresholding(dwt_coeffs)
reconstructed_image_dwt = apply_idwt(thresholded_coeffs, wavelet='haar')

# Salvar a imagem reconstruída usando DWT com compressão JPEG
cv2.imwrite('imagem_reconstruida_dwt.jpg', reconstructed_image_dwt, [cv2.IMWRITE_JPEG_QUALITY, 70])

# Mostrar as imagens originais e reconstruídas
plt.figure(figsize=(12, 6))
plt.subplot(1, 3, 1)
plt.title('Imagem Original')
plt.imshow(image, cmap='gray')

plt.subplot(1, 3, 2)
plt.title('Imagem Reconstruída (DCT)')
plt.imshow(reconstructed_image_dct, cmap='gray')

plt.subplot(1, 3, 3)
plt.title('Imagem Reconstruída (DWT)')
plt.imshow(reconstructed_image_dwt, cmap='gray')

plt.show()

# Comparação entre DCT e DWT
print("Comparando as técnicas DCT e DWT...")

# Calcular MSE e PSNR para DCT e DWT
mse_dct = calculate_mse(image, reconstructed_image_dct)
psnr_dct = calculate_psnr(image, reconstructed_image_dct)

mse_dwt = calculate_mse(image, reconstructed_image_dwt)
psnr_dwt = calculate_psnr(image, reconstructed_image_dwt)

# Calcular o tamanho dos arquivos
original_size = os.path.getsize('imagem_original.jpg')
dct_size = os.path.getsize('imagem_reconstruida_dct.jpg')
dwt_size = os.path.getsize('imagem_reconstruida_dwt.jpg')

# Exibir os resultados de comparação
print("\nResultados de Comparação:")
print(f"MSE (DCT): {mse_dct:.2f} - Erro Quadrático Médio da técnica DCT indica a diferença média ao quadrado entre a imagem original e a imagem reconstruída. Quanto menor o valor, melhor a qualidade da reconstrução.")
print(f"PSNR (DCT): {psnr_dct:.2f} dB - Pico da Razão Sinal-Ruído da técnica DCT mede a relação entre a intensidade máxima do sinal e o ruído. Quanto maior o valor, melhor a qualidade da imagem reconstruída.")
print(f"MSE (DWT): {mse_dwt:.2f} - Erro Quadrático Médio da técnica DWT indica a diferença média ao quadrado entre a imagem original e a imagem reconstruída. Quanto menor o valor, melhor a qualidade da reconstrução.")
print(f"PSNR (DWT): {psnr_dwt:.2f} dB - Pico da Razão Sinal-Ruído da técnica DWT mede a relação entre a intensidade máxima do sinal e o ruído. Quanto maior o valor, melhor a qualidade da imagem reconstruída.")

# Exibir tamanhos dos arquivos
print("\nTamanhos dos Arquivos:")
print(f"Tamanho da Imagem Original: {original_size / 1024:.2f} KB")
print(f"Tamanho da Imagem Reconstruída (DCT): {dct_size / 1024:.2f} KB")
print(f"Tamanho da Imagem Reconstruída (DWT): {dwt_size / 1024:.2f} KB")
print(f"Diferença de Tamanho (Original vs DCT): {((original_size - dct_size) / original_size) * 100:.2f}% de redução")
print(f"Diferença de Tamanho (Original vs DWT): {((original_size - dwt_size) / original_size) * 100:.2f}% de redução")