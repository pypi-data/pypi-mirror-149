import matplotlib.pyplot as plt


def calcula_histograma_de_serie(serie):
    valores_histograma_velocidad, bins, bars = plt.hist(serie)
    return valores_histograma_velocidad


def agrega_categoria_histograma(diccionario_histograma, categoria, serie):
    if categoria not in diccionario_histograma:
        diccionario_histograma[categoria] = calcula_histograma_de_serie(serie)