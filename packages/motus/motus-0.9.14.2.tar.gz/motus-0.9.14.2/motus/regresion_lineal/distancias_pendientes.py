import numpy as np


def calcula_distancias_para_lista_pendientes(lista_pendientes_signo):
    print("-------------------------------------------------------------")
    print("Inicia procesamiento para lista de pendientes: ")
    print("-------------------------------------------------------------")
    distancias_calculadas = []
    for i in range(0, len(lista_pendientes_signo)-1):
        a = lista_pendientes_signo[i]
        print("a: ", a)
        b = lista_pendientes_signo[i+1]
        print("b: ", b)
        resultado = distancia_arreglos_pendientes(a, b)
        distancias_calculadas.append(resultado)
    print("Distancias calculadas:", distancias_calculadas)
    return distancias_calculadas


def procesa_lista_pendientes_funcion_signo(lista_pendientes, epsilon):
    lista_pendientes_funcion_signo = []
    for pendiente in lista_pendientes:
        pendiente_signo = genera_pendiente_con_funcion_signo(pendiente, epsilon)
        lista_pendientes_funcion_signo.append(pendiente_signo)
    return lista_pendientes_funcion_signo


def distancia_arreglos_pendientes(arreglo_pendiente_1, arreglo_pendiente_2):
    print("---------------------------------------------------------")
    print("Calcular distancia entre arreglos:")
    print("---------------------------------------------------------")
    print("Arreglo pendiente 1:", arreglo_pendiente_1)
    print("Arreglo pendiente 2:", arreglo_pendiente_2)
    print("---------------------------------------------------------")
    numerador = np.dot(arreglo_pendiente_1, arreglo_pendiente_2)
    print("Numerador:", numerador)
    val_abs_arreglo_pendiente_1 = np.abs(arreglo_pendiente_1)
    val_abs_arreglo_pendiente_2 = np.abs(arreglo_pendiente_2)
    denominador = np.dot(val_abs_arreglo_pendiente_1, val_abs_arreglo_pendiente_2)
    print("Denominador: ", denominador)
    resultado = (1/2)*(1 - numerador/denominador)
    print("Resultado:", resultado)
    return resultado


def genera_pendiente_con_funcion_signo(arreglo_pendiente, epsilon):
    arreglo_resultado = []
    for valor in arreglo_pendiente:
        signo = funcion_signo(valor, epsilon)
        arreglo_resultado.append(signo)
    return arreglo_resultado


def funcion_signo(valor, epsilon):
    if valor > epsilon:
        return 1
    elif -epsilon <= valor <= epsilon:
        return 0
    elif valor < -epsilon:
        return -1

