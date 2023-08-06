import numpy as np


def determinar_regiones_importantes_cadena_texto(cadena_texto):
    listas_numeros = cadena_texto.split(",")
    print("Listas de numeros: ", listas_numeros)
    resultado = []
    for lista in listas_numeros:
        if lista.find("-") == -1:
            print("No hay -")
            resultado.append(int(lista))
            print(resultado)
        else:
            print("Hay -")
            limites = lista.split("-")
            print("Limites: ", limites)
            lista_numeros = list(range(int(limites[0]), int(limites[1])+1))
            for numero in lista_numeros:
                resultado.append(int(numero))
        print("Resultado final: ", resultado)
    return resultado


def obtener_complemento_de_sublista(lista, sublista):
    complemento = lista.copy()
    for elemento in sublista:
        complemento.remove(elemento)
    return complemento


def obtener_submatriz_indices_dados(matriz, lista_indices):
    print("inicio proceso para obtener valores en subindices dados para la matriz: ", matriz)
    copia_matriz_plana = matriz.copy().flatten()
    print("Submatriz plana: ", copia_matriz_plana)
    print("Lista de indices dados:", lista_indices)
    matriz_posiciones_interes = copia_matriz_plana[lista_indices]

    arreglo_valores_resultantes = np.zeros(len(copia_matriz_plana))
    arreglo_valores_resultantes[lista_indices] = matriz_posiciones_interes

    total_filas = matriz.shape[0]
    total_columnas = matriz.shape[1]

    matriz_resultante = np.reshape(arreglo_valores_resultantes, (total_filas, total_columnas))

    print("Matriz resultante: ")

    return matriz_resultante

