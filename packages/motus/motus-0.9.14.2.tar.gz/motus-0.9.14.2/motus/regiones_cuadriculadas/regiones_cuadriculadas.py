import numpy as np


def calcula_regiones_cuadriculadas(tiempos,
                                   serie_posiciones_x, serie_posiciones_y,
                                   cantidad_filas, cantidad_columnas,
                                   dimension_caja):
    print("Calculando regiones en la caja...")

    posiciones_x = serie_posiciones_x
    posiciones_y = serie_posiciones_y

    cantidad_tiempos = len(tiempos)

    matriz_cuadriculada = np.zeros((cantidad_filas, cantidad_columnas))

    tamanio_horizontal = dimension_caja[0] / cantidad_columnas
    tamanio_vertical = dimension_caja[1] / cantidad_filas

    print("Tamanio de los cuadros: ", tamanio_horizontal, "x", tamanio_vertical)

    arreglo_region_cuadriculada = np.zeros(cantidad_tiempos)

    for k in range(cantidad_tiempos):
        # print("Posicion de k:", k)

        if not (np.isnan(posiciones_x.iloc[k])) or not (np.isnan(posiciones_y.iloc[k])):

            posicion_x = posiciones_x.iloc[k]
            posicion_y = posiciones_y.iloc[k]
            # print("Indice:", k)
            if posicion_x == dimension_caja[0]:
                # print(cantidad_columnas)
                j = cantidad_columnas - 1
                # print("Entro en opcion 1-x")
            else:
                # print("Entro en opcion 2-x")
                j = int(posiciones_x.iloc[k] // tamanio_horizontal)
            if posicion_y == dimension_caja[1]:
                # print(cantidad_filas)
                i = cantidad_filas - 1
                # print("Entro en opcion 1-y")
            else:
                i = int(posiciones_y.iloc[k] // tamanio_vertical)
                # print("Entro en opcion 2-y")
            # print("i: ", i)
            # print("j: ", j)
            matriz_cuadriculada[i][j] = matriz_cuadriculada[i][j] + 1
            arreglo_region_cuadriculada[k] = cantidad_columnas * i + j

        matriz_cuadriculada = np.flipud(matriz_cuadriculada)

    return arreglo_region_cuadriculada, matriz_cuadriculada


def obtener_indice_regiones_objeto(dimension_caja,
                                   cantidad_filas, cantidad_columnas,
                                   lista_objetos_relevantes):

    indice_region_objeto_1 = None
    indice_region_objeto_2 = None
    indice_region_objeto_3 = None
    indice_region_objeto_4 = None

    tamanio_horizontal = dimension_caja[0] / cantidad_columnas
    tamanio_vertical = dimension_caja[1] / cantidad_filas

    for objeto in lista_objetos_relevantes:

        posicion_x = objeto[0]
        posicion_y = objeto[1]

        if posicion_x == dimension_caja[0]:
            j = cantidad_columnas - 1
        else:
            j = posicion_x // tamanio_horizontal
        if posicion_y == dimension_caja[1]:
            i = cantidad_filas - 1
        else:
            i = posicion_y // tamanio_vertical

        if indice_region_objeto_1 is None:
            indice_region_objeto_1 = cantidad_columnas * i + j
        elif indice_region_objeto_2 is None:
            indice_region_objeto_2 = cantidad_columnas * i + j
        elif indice_region_objeto_3 is None:
            indice_region_objeto_3 = cantidad_columnas * i + j
        elif indice_region_objeto_4 is None:
            indice_region_objeto_4 = cantidad_columnas * i + j

    return indice_region_objeto_1, indice_region_objeto_2, indice_region_objeto_3, indice_region_objeto_4