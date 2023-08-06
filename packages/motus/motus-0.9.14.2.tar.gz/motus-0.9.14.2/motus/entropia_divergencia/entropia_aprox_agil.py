import numpy as np
from motus.entropia_divergencia.entropia_aprox import phi


def calcular_probabilidad_vector_unico(datos, vector, umbral):
    probabilidad_actual = 0
    tamanio_vector = len(vector)
    for i in range(0, len(datos) - tamanio_vector + 1):
        print("-------------------------------")
        print("Vector", i)
        print(vector)
        print("[" + str(datos[i]) + ",", str(datos[i + 1]) + "]")
        abs_1 = np.abs(datos[i] - vector[0])
        abs_2 = np.abs(datos[i + 1] - vector[1])
        dist = max(abs_1, abs_2)
        print("Dist:", dist)
        if dist <= umbral:
            probabilidad_actual += 1
    probabilidad_actual /= (len(datos) - tamanio_vector + 1)
    return probabilidad_actual


def calcular_probabilidad_vector(datos, vector, umbral):
    probabilidad_actual = 0
    probabilidad_actual_extra = 0
    tamanio_vector = len(vector)
    for i in range(0, len(datos) - tamanio_vector + 1):
        print("-------------------------------")
        print("Vector", i)
        print(vector)
        print("["+str(datos[i])+",", str(datos[i+1])+",", str(datos[i+2])+"]")
        abs_1 = np.abs(datos[i] - vector[0])
        abs_2 = np.abs(datos[i+1] - vector[1])
        abs_3 = np.abs(datos[i+2] - vector[2])
        dist = max(abs_1, abs_2)
        dist_extra = max(dist, abs_3)
        print("Dist:", dist)
        print("Dist extra:", dist_extra)
        if dist <= umbral:
            probabilidad_actual += 1
        if dist_extra <= umbral:
            probabilidad_actual_extra += 1
    print("Vector",tamanio_vector)
    print(vector[0:2])
    print(datos[-2:])
    abs_1 = np.abs(datos[-2] - vector[0])
    abs_2 = np.abs(datos[-1] - vector[1])
    dist = max(abs_1, abs_2)
    if dist <= umbral:
        probabilidad_actual += 1
    probabilidad_actual /= len(datos) - tamanio_vector + 2
    probabilidad_actual_extra /= len(datos) - tamanio_vector + 1
    return probabilidad_actual, probabilidad_actual_extra


def calcular_probabilidades_agil_corregido(datos, umbral):
    probabilidades_m = []
    probabilidades_m_extra = []
    for i in range(0, len(datos) - 3 + 1):
        vector_actual = datos[i:i+3]
        probabilidad_actual, probabilidad_extra = calcular_probabilidad_vector(datos, vector_actual, umbral)
        probabilidades_m.append(probabilidad_actual)
        probabilidades_m_extra.append(probabilidad_extra)
    ultimo_vector = datos[-2:]
    ultima_probabilidad = calcular_probabilidad_vector_unico(datos, ultimo_vector, umbral)
    probabilidades_m.append(ultima_probabilidad)
    return probabilidades_m, probabilidades_m_extra


def calcula_entropia_aprox_agil(datos, umbral=3):
    c1, c2 = calcular_probabilidades_agil_corregido(datos=datos, umbral=umbral)
    print("Probabilidad 1:", c1)
    print("Probabilidad 2:", c2)
    return phi(c1) - phi(c2)
