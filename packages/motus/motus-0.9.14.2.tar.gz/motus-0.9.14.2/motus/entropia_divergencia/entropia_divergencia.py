import numpy as np
import scipy.stats as st
import motus.entropia_divergencia.entropia_aprox_agil as m_eaa
import motus.entropia_divergencia.entropia_aprox_agil_generalizada as m_eaag


def agrega_categoria_entropia(diccionario_entropia, categoria, datos):
    print("Agrego categoria de entropia: ")
    print("--------------------------------------------------------------")
    print("Diccionario:", diccionario_entropia)
    print("Categoria", categoria)
    print("Datos:", datos)
    nuevos_datos = np.array(datos)
    if categoria not in diccionario_entropia:
        diccionario_entropia[categoria] = st.entropy(nuevos_datos)
    print("Nuevo diccionario: ", diccionario_entropia)


def agrega_categoria_entropia_aproximada(diccionario_entropia,
                                         categoria,
                                         datos,
                                         tamanio_vectorial,
                                         umbral,
                                         sobreposicion):
    print("Agrego categoria de entropia aproximada: ")
    print("--------------------------------------------------------------")
    print("Diccionario:", diccionario_entropia)
    print("Categoria", categoria)
    print("Datos:", datos)
    nuevos_datos = np.array(datos)
    if categoria not in diccionario_entropia:
        print("Procesando informacion")
        diccionario_entropia[categoria] = \
            m_eaag.calcula_entropia_aprox_agil_general(datos=nuevos_datos,
                                                       tamanio_vector=tamanio_vectorial,
                                                       umbral=umbral,
                                                       sobreposicion=sobreposicion)
    print("Nuevo diccionario: ", diccionario_entropia)


def modificar_arreglo_para_evitar_divergencia_infinita(datos):
    nuevos_datos = np.copy(datos)
    indices_con_valores_0 = np.argwhere(nuevos_datos == 0)

    for indice in indices_con_valores_0:
        nuevos_datos[indice] = 1

    return nuevos_datos


def calcula_divergencia_de_2_arreglos(pk, qk):
    nuevo_qk = modificar_arreglo_para_evitar_divergencia_infinita(qk)
    divergencia = st.entropy(pk, nuevo_qk)
    return divergencia


def calcula_divergencias_de_lista_arreglos(lista_arreglos):

    resultados_divergencia = []

    for i in range(0, len(lista_arreglos) - 1):
        pk = lista_arreglos[i]
        qk = lista_arreglos[i+1]

        divergencia_pk_qk = calcula_divergencia_de_2_arreglos(pk, qk)

        resultados_divergencia.append(divergencia_pk_qk)

    return resultados_divergencia
