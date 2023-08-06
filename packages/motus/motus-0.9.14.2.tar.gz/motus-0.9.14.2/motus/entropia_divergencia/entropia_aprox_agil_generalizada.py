import numpy as np
from motus.entropia_divergencia.entropia_aprox import phi


def generar_vectores_a_analizar(datos, tamanio_vector=2, brinco_datos=1, superposicion=True):
    lista_vectores = []
    if superposicion is True:
        brinco_generar_vectores = brinco_datos
    else:
        brinco_generar_vectores = brinco_datos + tamanio_vector + 1
    for i in range(0, len(datos) - tamanio_vector, brinco_generar_vectores):
        vector = datos[i: i+tamanio_vector+1]
        lista_vectores.append(vector)
    return lista_vectores


def calcular_probabilidad_vector(lista_vectores, vector_a_comparar, umbral=3):
    #print("-------------calcula_probabilidad_vector--------------------------")
    probabilidad_actual = 0
    probabilidad_actual_extra = 0
    vector_a_comparar = np.array(vector_a_comparar)
    for vector in lista_vectores:
        #print("Vector a comparar:", vector_a_comparar)
        nuevo_vector = np.array(vector)
        #print("Nuevo vector:", nuevo_vector)
        lista_val_abs = np.abs(nuevo_vector - vector_a_comparar)
        #print("Valores absolutos:", lista_val_abs)
        distancia = max(lista_val_abs[:-1])
        distancia_extra = max(lista_val_abs)
        #print("Distancia, dist extra:", distancia, distancia_extra)
        if distancia <= umbral:
            probabilidad_actual += 1
        if distancia_extra <= umbral:
            probabilidad_actual_extra += 1
        #print("------------------------------------------------------")
    vector_a_comparar = vector_a_comparar[:-1]
    #print("Vector a comparar:", vector_a_comparar)
    vector_final = np.array(lista_vectores[-1])[1:]
    #print("Vector final:", vector_final)
    lista_val_abs = np.abs(vector_final - vector_a_comparar)
    #print("Lista val abs:", lista_val_abs)
    distancia = max(lista_val_abs)
    #print("Distancia:", distancia)
    if distancia <= umbral:
        probabilidad_actual += 1
    #print("-------------------------------")
    #print("Prob, prob_extra:", probabilidad_actual, probabilidad_actual_extra)
    probabilidad_actual /= len(lista_vectores) + 1
    probabilidad_actual_extra /= len(lista_vectores)
    return probabilidad_actual, probabilidad_actual_extra


def calcular_probabilidad_vector_final(lista_vectores, vector_a_comparar, umbral=3):
    #print("-------------Vector final------------------------")
    probabilidad_actual = 0
    vector_a_comparar = np.array(vector_a_comparar[1:])
    for vector in lista_vectores:
        #print("Vector a comparar:", vector_a_comparar)
        #print("Vector:", vector)
        nuevo_vector = np.array(vector[:-1])
        #print("Nuevo vector:", nuevo_vector)
        lista_val_abs = np.abs(nuevo_vector - vector_a_comparar)
        #print("Lista_val_abs:", lista_val_abs)
        distancia = max(lista_val_abs)
        #print("Distancia:", distancia)
        if distancia <= umbral:
            probabilidad_actual += 1
        #print("-----------------------------")
    probabilidad_actual += 1
    probabilidad_actual /= len(lista_vectores) + 1
    return probabilidad_actual


def calcular_probabilidades(datos, tamanio_vector=2, brinco_datos=1, sobreposicion=True, umbral=3):
    probabilidades_m = []
    probabilidades_m_extra = []
    lista_vectores = generar_vectores_a_analizar(datos, tamanio_vector, brinco_datos, sobreposicion)
    #print("Lista vectores:", lista_vectores)
    for vector in lista_vectores:
        probabilidad_actual, probabilidad_extra = calcular_probabilidad_vector(lista_vectores,
                                                                               vector, umbral)
        probabilidades_m.append(probabilidad_actual)
        probabilidades_m_extra.append(probabilidad_extra)
    ultimo_vector = lista_vectores[-1]
    ultima_probabilidad = calcular_probabilidad_vector_final(lista_vectores, ultimo_vector, umbral)
    probabilidades_m.append(ultima_probabilidad)
    return probabilidades_m, probabilidades_m_extra


def calcula_entropia_aprox_agil_general(datos, tamanio_vector=2, umbral=3, sobreposicion=True):
    #print("----------------------------------------------------------")
    #print("-------------------Inicio---------------------------------")
    c1, c2 = calcular_probabilidades(datos=datos,
                                     tamanio_vector=tamanio_vector,
                                     umbral=umbral,
                                     sobreposicion=sobreposicion)
    #print("Probabilidad 1:", c1)
    #print("Probabilidad 2:", c2)
    return phi(c1) - phi(c2)
