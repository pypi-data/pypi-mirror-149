import numpy as np


def calcula_distancias_a_objetos(posiciones_x, posiciones_y, lista_objetos):

    objeto_1_x = lista_objetos[0][0]
    objeto_1_y = lista_objetos[0][1]

    objeto_2_x = lista_objetos[1][0]
    objeto_2_y = lista_objetos[1][1]

    objeto_3_x = lista_objetos[2][0]
    objeto_3_y = lista_objetos[2][1]

    objeto_4_x = lista_objetos[3][0]
    objeto_4_y = lista_objetos[3][1]

    dist_objeto_1 = ((objeto_1_x - posiciones_x) ** 2 + (objeto_1_y - posiciones_y) ** 2) ** 0.5
    dist_objeto_2 = ((objeto_2_x - posiciones_x) ** 2 + (objeto_2_y - posiciones_y) ** 2) ** 0.5
    dist_objeto_3 = ((objeto_3_x - posiciones_x) ** 2 + (objeto_3_y - posiciones_y) ** 2) ** 0.5
    dist_objeto_4 = ((objeto_4_x - posiciones_x) ** 2 + (objeto_4_y - posiciones_y) ** 2) ** 0.5

    return dist_objeto_1, dist_objeto_2, dist_objeto_3, dist_objeto_4


def resultados_distancias(posiciones_x, posiciones_y, lista_distancias):

    dist_1 = lista_distancias[0]
    dist_2 = lista_distancias[1]
    dist_3 = lista_distancias[2]
    dist_4 = lista_distancias[3]

    distancia_minima_objetos_2_3_4 = np.minimum(dist_2,
                                                np.minimum(dist_3, dist_4))
    distancia_minima_todos_objetos = np.minimum(dist_1, distancia_minima_objetos_2_3_4)

    longitud_distancias = len(dist_1)

    nuevas_posiciones_x = posiciones_x.fillna(0)
    nuevas_posiciones_y = posiciones_y.fillna(0)

    distancia_total_recorrida = 0

    for i in range(1, longitud_distancias):
        distancia_x = (nuevas_posiciones_x.iloc[i] - nuevas_posiciones_x.iloc[i - 1]) ** 2
        distancia_y = (nuevas_posiciones_y.iloc[i] - nuevas_posiciones_y.iloc[i - 1]) ** 2
        distancia_total_recorrida += (distancia_x + distancia_y)**(1/2)

    return distancia_minima_objetos_2_3_4, distancia_minima_todos_objetos, distancia_total_recorrida


def obtener_arreglo_con_valores_promediados_para_distancia_a_objeto(arreglo, tamanio_intervalo):
    arreglo_con_promedio = []
    for i in range(len(arreglo)):
        valor_promediado = obtener_valor_promediado_para_distancia_a_objeto(arreglo, i, tamanio_intervalo)
        arreglo_con_promedio.append(valor_promediado)
    return arreglo_con_promedio


def obtener_valor_promediado_para_distancia_a_objeto(arreglo, indice, tamanio_intervalo):
    if indice - tamanio_intervalo < 0:
        left = arreglo[0:indice]
    else:
        left = arreglo[(indice - tamanio_intervalo):indice]
    if indice + tamanio_intervalo > len(arreglo):
        right = arreglo[(indice + 1):len(arreglo)]
    else:
        right = arreglo[indice + 1:(indice + tamanio_intervalo) + 1]
    arreglo_final = left + [arreglo[indice]] + right
    promedio = sum(arreglo_final) / len(arreglo_final)
    return promedio


