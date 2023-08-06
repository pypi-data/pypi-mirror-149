from motus.regiones_cuadriculadas import regiones_cuadriculadas as m_reg_c
import numpy as np

def calcula_matrices_de_recurrencia(arreglo_regiones,
                                    region_importante=None):

    longitud_matriz_recurrencia = len(arreglo_regiones)

    matriz_recurrencia = np.zeros((longitud_matriz_recurrencia, longitud_matriz_recurrencia))

    if region_importante is None:

        for i in range(len(arreglo_regiones)):
            valor = arreglo_regiones[i]
            for j in range(len(arreglo_regiones)):
                if valor == arreglo_regiones[j]:
                    matriz_recurrencia[i][j] = 1

    elif type(region_importante) is int:
        for i in range(len(arreglo_regiones)):
            valor = arreglo_regiones[i]
            for j in range(len(arreglo_regiones)):
                if valor == arreglo_regiones[j]:
                    if valor == region_importante:
                        matriz_recurrencia[i][j] = 1

    elif type(region_importante) is list:

        indice_region_objeto_1 = region_importante[0]
        indice_region_objeto_2 = region_importante[1]
        indice_region_objeto_3 = region_importante[2]
        indice_region_objeto_4 = region_importante[3]

        for i in range(len(arreglo_regiones)):
            valor = arreglo_regiones[i]
            for j in range(len(arreglo_regiones)):
                if valor == arreglo_regiones[j]:
                    if valor == indice_region_objeto_1:
                        matriz_recurrencia[i][j] = 1
                    if valor == indice_region_objeto_2:
                        matriz_recurrencia[i][j] = 2
                    if valor == indice_region_objeto_3:
                        matriz_recurrencia[i][j] = 3
                    if valor == indice_region_objeto_4:
                        matriz_recurrencia[i][j] = 4

    return matriz_recurrencia