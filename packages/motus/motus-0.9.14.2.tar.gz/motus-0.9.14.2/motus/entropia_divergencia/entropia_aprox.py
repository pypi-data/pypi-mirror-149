import numpy as np


def formar_sucesiones_vectoriales(datos, tamanio_sucesiones_vectoriales):
    lista_sucesiones_vectoriales = []
    tamanio_datos = len(datos)
    print("Tamanio datos:", tamanio_datos)
    total_vectores = tamanio_datos - tamanio_sucesiones_vectoriales + 1
    print("Total vectores:", total_vectores)
    for i in range(0, total_vectores):
        vector = [dato for dato in datos[i:i+tamanio_sucesiones_vectoriales]]
        print("Vector", i)
        print(vector)
        lista_sucesiones_vectoriales.append(vector)
    return lista_sucesiones_vectoriales


def distancia_vectores_max_dif(vector_1, vector_2):
    if len(vector_1) == len(vector_2):
        print("Realizo la distancia vectorial")
        longitud_vectores = len(vector_1)
        distancias_totales = []
        for i in range(0, longitud_vectores):
            pos_v1 = vector_1[i]
            pos_v2 = vector_2[i]
            distancia_actual = abs(pos_v1 - pos_v2)
            distancias_totales.append(distancia_actual)
        return max(distancias_totales)
    else:
        print("No se puede realizar la distancia vectorial.")
        return None


def compara_val_dist_con_umbral(distancia, umbral):
    if distancia < umbral:
        return 1
    else:
        return 0


def obtener_coeficiente_c_i(lista_vectores, posicion, umbral):
    vector_a_comparar = lista_vectores[posicion]
    cantidad_vectores = len(lista_vectores)
    cantidad_vectores_mayores_umbral = 0
    for vector in lista_vectores:
        distancia_resultante = distancia_vectores_max_dif(vector_a_comparar, vector)
        cantidad_vectores_mayores_umbral += compara_val_dist_con_umbral(distancia=distancia_resultante,
                                                                        umbral=umbral)
    print("Cantidad vectores mayores a umbral: ", cantidad_vectores_mayores_umbral)
    print("longitud_vectores")
    resultado = cantidad_vectores_mayores_umbral/cantidad_vectores
    return resultado


def obtener_todos_coeficientes_c(lista_vectores, umbral):
    lista_coeficientes_c = []
    for i in range(0, len(lista_vectores)):
        c_actual = obtener_coeficiente_c_i(lista_vectores=lista_vectores,
                                           posicion=i,
                                           umbral=umbral)
        lista_coeficientes_c.append(c_actual)
    return lista_coeficientes_c


def phi(coeficientes_c):
    return sum(np.log(coeficientes_c))/len(coeficientes_c)


def entropia_aprox(lista_datos, tamanio_vectorial, umbral):
    lista_vectores = formar_sucesiones_vectoriales(datos=lista_datos,
                                                   tamanio_sucesiones_vectoriales=tamanio_vectorial)
    coef_c_i_m = obtener_todos_coeficientes_c(lista_vectores, umbral)
    print("Coeficientes_m", coef_c_i_m)
    phi_m = phi(coeficientes_c=coef_c_i_m)
    lista_vectores = formar_sucesiones_vectoriales(datos=lista_datos,
                                                   tamanio_sucesiones_vectoriales=tamanio_vectorial+1)
    coef_c_i_m = obtener_todos_coeficientes_c(lista_vectores, umbral)
    print("Coeficientes_m_1", coef_c_i_m)
    phi_m_1 = phi(coeficientes_c=coef_c_i_m)
    resultado_entropia_aprox = phi_m - phi_m_1
    return resultado_entropia_aprox




