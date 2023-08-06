import pandas as pd
import numpy as np
import matplotlib
import random
import os
import sys
from matplotlib.figure import Figure
import matplotlib.colors as colors
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pathlib
import warnings
from decimal import Decimal
from motus import funciones_auxiliares as fa
from motus.fisica_estadistica import histogramas as m_hist, velocidad_aceleracion as m_vel
from motus.regresion_lineal import analisis_regresion_lineal as m_arl
from motus.entropia_divergencia import entropia_divergencia as m_ed
from motus.rutas_distancias import distancias as m_dist, rutas_vectoriales as m_rv
from motus.graficador import cilindros as m_ci
from motus.regiones_cuadriculadas import regiones_cuadriculadas as m_reg_cuad, \
    regiones_preferidas as m_reg_pref, matrices_recurrencia as m_recurr
from motus.regresion_lineal import analisis_regresion_lineal as m_arl
import motus.graficador.config_graficas as m_cg

warnings.filterwarnings("error")

matplotlib.use('TkAgg')


class Experimento:

    def __init__(self, nombre_archivo,
                 dimension_caja=[100, 100],
                 cantidad_filas=10, cantidad_columnas=10,
                 procesar_tiempo_archivo_irregular=False,
                 puntos_importantes=None):
        self.nombre_archivo = nombre_archivo
        print("NOMBRE_ARCHIVO:", self.nombre_archivo, "\n TIPO_ARCHIVO:", type(self.nombre_archivo))
        self.dimension_caja = dimension_caja
        self.cantidad_filas = cantidad_filas
        self.cantidad_columnas = cantidad_columnas

        self.lista_de_indices_para_subsucesiones = None
        self.lista_ordenada_de_indices_mas_altos = None
        self.archivo_consecuencias = False

        self.velocidades_promediadas = dict()
        self.aceleraciones_promediadas = dict()
        self.entropias = dict()
        self.histogramas = dict()
        self.regresiones_lineales = dict()

        nombre_recortado = pathlib.Path(self.nombre_archivo)
        try:
            dataframe_a_recortar = pd.DataFrame(pd.read_csv(self.nombre_archivo,
                                                            header=None,
                                                            sep=',',
                                                            na_values='-',
                                                            usecols=[0],
                                                            engine='python',
                                                            encoding='latin1',
                                                            ))
        except:
            try:
                dataframe_a_recortar = pd.DataFrame(pd.read_csv(self.nombre_archivo,
                                                                header=None,
                                                                sep=';',
                                                                na_values='-',
                                                                usecols=[0],
                                                                engine='python',
                                                                encoding='latin1',
                                                                ))
            except:
                raise Exception('El archivo ', self.nombre_archivo,
                                'no es un archivo separado por comas o puntos y comas.')
        print("Obteniendo datos de csv...")
        df = dataframe_a_recortar
        try:
            inicio_datos = df.index[df[0] == 'Sample no.'].tolist()
            print("Los datos empiezan en la fila", inicio_datos)
            inicio_datos = inicio_datos[0]
            lista_filas = list(range(0, inicio_datos))
            print("Lista de filas:", lista_filas)
            self.datos = pd.DataFrame(pd.read_csv(self.nombre_archivo,
                                                  header=0,
                                                  na_values='-',
                                                  skiprows=lista_filas,
                                                  index_col=False,
                                                  encoding='latin1'))
            print("Datos procesados.")
        except:
            raise Exception('El archivo ', nombre_recortado.stem, 'no es compatible con motus.')

        longitud_datos = len(self.datos)
        try:
            arreglo_samples = pd.to_numeric(self.datos['Sample no.'].tail(longitud_datos))
            arreglo_tiempo = pd.to_numeric(self.datos['Time'].tail(longitud_datos))
            arreglo_posicion_x = pd.to_numeric(self.datos['X'].tail(longitud_datos))
            arreglo_posicion_y = pd.to_numeric(self.datos['Y'].tail(longitud_datos))
            if 'Consecuences' in self.datos:
                self.archivo_consecuencias = True
                arreglo_consecuencias = pd.to_numeric(self.datos['Consecuences'].tail(longitud_datos))
        except:
            raise Exception('Alguno de los nombres de las columnas del CSV no es correcto. Esto podria ser por un'
                            ' espacio en blanco al principio del nombre.')

        print("--------------------------------------")

        print("Tiempo:", arreglo_tiempo)
        print("Pos. eje x", arreglo_posicion_x)
        print("Pos eje y", arreglo_posicion_y)

        if puntos_importantes is None:

            self.objeto_relevante_1 = [50, 0]
            self.objeto_relevante_2 = [0, 50]
            self.objeto_relevante_3 = [50, 100]
            self.objeto_relevante_4 = [100, 50]

        else:

            self.objeto_relevante_1 = puntos_importantes[0]
            self.objeto_relevante_2 = puntos_importantes[1]
            self.objeto_relevante_3 = puntos_importantes[2]
            self.objeto_relevante_4 = puntos_importantes[3]

        self.lista_objetos_relevantes = [self.objeto_relevante_1,
                                         self.objeto_relevante_2,
                                         self.objeto_relevante_3,
                                         self.objeto_relevante_4]

        self.cantidad_posiciones_volumenes = None
        self.radios_volumenes = None

        self.distancia_a_objeto_promediado = None

        self.indice_region_objeto_1 = None
        self.indice_region_objeto_2 = None
        self.indice_region_objeto_3 = None
        self.indice_region_objeto_4 = None

        print("Objeto relevante 1:", self.objeto_relevante_1)
        print("Objeto relevante 2:", self.objeto_relevante_2)
        print("Objeto relevante 3:", self.objeto_relevante_3)
        print("Objeto relevante 4:", self.objeto_relevante_4)

        self.posiciones_x = arreglo_posicion_x
        self.posiciones_y = arreglo_posicion_y

        self.config_graficas = m_cg.ConfigGrafica()
        self.procesador_regresion_lineal = m_arl.ProcesamientoRegresionLineal()
        self.rutas_vectoriales = m_rv.InformacionRutasVectoriales(posiciones_eje_x=self.posiciones_x,
                                                                  posiciones_eje_y=self.posiciones_y)

        self.tiempo = arreglo_tiempo
        self.samples = arreglo_samples

        self.consecuencias = None

        print("Se encuentra la columna consecuences: ", self.archivo_consecuencias)
        if self.archivo_consecuencias is True:
            self.consecuencias = arreglo_consecuencias

            print("self.consecuencias: ", self.consecuencias)
            print(np.where(self.consecuencias == 1)[0])

            self.config_graficas.columna_consecuencia_disponible = True
            self.config_graficas.lista_consecuencias = np.where(self.consecuencias == 1)[0]
        else:
            self.config_graficas.columna_consecuencia_disponible = False

        self.valor_intervalos_tiempo = arreglo_tiempo.iloc[1] - arreglo_tiempo.iloc[0]

        print("Procesar tiempo irregular: ", procesar_tiempo_archivo_irregular)

        if procesar_tiempo_archivo_irregular is False:
            if self.verifica_intervalo_tiempo() is False:
                raise Warning("Los intervalos entre frames del archivo son irregulares. Si desea continuar con el "
                              "procesamiento del archivo, active la casilla  \"Procesamiento tiempo irregular\". "
                              "Tenga presente que el procesamiento de datos estara basado en el valor medio del "
                              "total de frames. Le sugerimos explicitar que el procesamiento de datos se realizo "
                              "ajustando el valor de los intervalos entre frames a un valor medio, con base en el "
                              "siguiente calculo: Intervalo = (Tiempo final - tiempo inicial)/total de registros")
        else:
            print("Se empieza la generacion de tiempos regulares: ")
            self.genera_tiempos_regulares()

        self.distancia_total_recorrida = 0

        self.dist_objeto_1 = None
        self.dist_objeto_2 = None
        self.dist_objeto_3 = None
        self.dist_objeto_4 = None

        self.distancia_minima_objetos_2_3_4 = None
        self.distancia_minima_todos_objetos = None

        self.serie_velocidad = None
        self.velocidad_maxima = None

        self.serie_aceleracion = None
        self.aceleracion_maxima = None

        self.arreglo_region_cuadriculada = None
        self.lista_matrices_recurrencia_regiones_importantes = []
        self.matriz_recurrencia_region_cuadriculada = None
        self.matriz_recurrencia_combinada = None

        self.matriz_cuadriculada = None
        self.matriz_cuadriculada_regiones_preferidas = None
        self.matriz_cuadriculada_solo_regiones_preferidas = None
        self.matriz_cuadriculada_solo_regiones_no_preferidas = None

        self.regiones_preferidas = None
        self.regiones_no_preferidas = None
        self.visitas_regiones_preferidas = None
        self.visitas_regiones_no_preferidas = None

        self.cantidad_posiciones_volumen_1 = None
        self.cantidad_posiciones_volumen_2 = None
        self.cantidad_posiciones_volumen_3 = None
        self.cantidad_posiciones_volumen_4 = None
        self.radios_volumenes = None

        print("Construccion de series de tiempo y de posicion.")

        if self.posiciones_x.max() > dimension_caja[0]:
            raise Exception('Hay un dato en el eje X que es mayor que la dimension de la caja. Valor: ',
                            self.posiciones_x.max())
        if self.posiciones_y.max() > dimension_caja[1]:
            raise Exception('Hay un dato en el eje Y que es mayor que la dimension de la caja. Valor: ',
                            self.posiciones_y.max())

    def regresa_tipo_arreglo(self, nombre_arreglo):
        arreglos = {
            "Velocidad": self.serie_velocidad,
            "Aceleracion": self.serie_aceleracion
        }
        return arreglos[nombre_arreglo]

    def verifica_intervalo_tiempo(self):
        arreglo_tiempo = self.tiempo
        valor = True
        nuevo_valor = 0
        print("Tiempo: ", arreglo_tiempo)
        for i in range(len(arreglo_tiempo)):
            print("Nuevo valor:", nuevo_valor)
            print("Valor a comparar:", arreglo_tiempo[i])
            if not nuevo_valor == arreglo_tiempo[i]:
                valor = False
                break
            nuevo_valor = round(nuevo_valor + self.valor_intervalos_tiempo, 3)
        print(valor)
        return valor

    def genera_tiempos_regulares(self):
        tiempo_a_utilizar = self.tiempo.values
        tiempo_total = len(tiempo_a_utilizar)
        tiempo_inicial = tiempo_a_utilizar[0]
        tiempo_final = tiempo_a_utilizar[-1]
        nuevos_tiempos = pd.Series(np.linspace(tiempo_inicial, tiempo_final, tiempo_total), name='Time')
        print("Tiempo original:", self.tiempo)
        print("Tiempos nuevos:", nuevos_tiempos)
        self.tiempo = nuevos_tiempos

    def calcula_distancias(self):

        print("Calculo de distancias...")

        self.dist_objeto_1, self.dist_objeto_2, self.dist_objeto_3, self.dist_objeto_4 = \
            m_dist.calcula_distancias_a_objetos(self.posiciones_x, self.posiciones_y, self.lista_objetos_relevantes)

        m_hist.agrega_categoria_histograma(diccionario_histograma=self.histogramas,
                                           categoria="dist_objeto_1",
                                           serie=self.dist_objeto_1)

        m_hist.agrega_categoria_histograma(diccionario_histograma=self.histogramas,
                                           categoria="dist_objeto_2",
                                           serie=self.dist_objeto_2)

        m_hist.agrega_categoria_histograma(diccionario_histograma=self.histogramas,
                                           categoria="dist_objeto_3",
                                           serie=self.dist_objeto_3)

        m_hist.agrega_categoria_histograma(diccionario_histograma=self.histogramas,
                                           categoria="dist_objeto_4",
                                           serie=self.dist_objeto_4)

        print("Distancias calculadas.")

        lista_dist_objetos = [self.dist_objeto_1, self.dist_objeto_2, self.dist_objeto_3, self.dist_objeto_4]

        self.distancia_minima_objetos_2_3_4, self.distancia_minima_todos_objetos, self.distancia_total_recorrida = \
            m_dist.resultados_distancias(self.posiciones_x, self.posiciones_y, lista_dist_objetos)

        print("Distancia total calculada")

    def calcula_distancia_promediada_con_objeto(self, objeto, intervalo):
        arreglo_elegido = []
        if objeto is 1:
            arreglo_elegido = self.dist_objeto_1.tolist()
        elif objeto is 2:
            arreglo_elegido = self.dist_objeto_2.tolist()
        elif objeto is 3:
            arreglo_elegido = self.dist_objeto_3.tolist()
        elif objeto is 4:
            arreglo_elegido = self.dist_objeto_4.tolist()
        self.distancia_a_objeto_promediado = \
            m_dist.obtener_arreglo_con_valores_promediados_para_distancia_a_objeto(arreglo_elegido, intervalo)

    def calcula_velocidades(self):

        self.serie_velocidad = m_vel.calcula_serie_velocidad(self.tiempo,
                                                             self.posiciones_x,
                                                             self.posiciones_y)
        self.velocidad_maxima = round(self.serie_velocidad.max(), 3)

        m_hist.agrega_categoria_histograma(diccionario_histograma=self.histogramas,
                                           categoria="velocidad",
                                           serie=self.serie_velocidad)

        self.serie_aceleracion = m_vel.calcula_serie_aceleracion(arreglo_tiempo=self.tiempo,
                                                                 serie_velocidad=self.serie_velocidad)

        self.aceleracion_maxima = round(self.serie_aceleracion.max(), 3)

        m_hist.agrega_categoria_histograma(diccionario_histograma=self.histogramas,
                                           categoria="aceleracion",
                                           serie=self.serie_aceleracion)

    def calcula_entropias(self, tamanio_vectores, umbral, sobreposicion):

        m_ed.agrega_categoria_entropia(diccionario_entropia=self.entropias,
                                       categoria="histograma_velocidad",
                                       datos=self.histogramas["velocidad"])

        m_ed.agrega_categoria_entropia_aproximada(diccionario_entropia=self.entropias,
                                                  categoria="aproximada_velocidad",
                                                  datos=self.serie_velocidad.to_numpy(),
                                                  tamanio_vectorial=tamanio_vectores,
                                                  umbral=umbral,
                                                  sobreposicion=sobreposicion)

        m_ed.agrega_categoria_entropia(diccionario_entropia=self.entropias,
                                       categoria="histograma_aceleracion",
                                       datos=self.histogramas["aceleracion"])

        m_ed.agrega_categoria_entropia_aproximada(diccionario_entropia=self.entropias,
                                                  categoria="aproximada_aceleracion",
                                                  datos=self.serie_aceleracion.to_numpy(),
                                                  tamanio_vectorial=tamanio_vectores,
                                                  umbral=umbral)

    def calcula_velocidades_promediadas(self, cantidad_datos_promedio):
        print("-------------------------------------------------------------")
        print("Entro a calcular velocidades promediadas\n")
        print("Serie de velocidad: ", self.serie_velocidad)

        serie_velocidad_promediada = m_vel.obtener_arreglo_promediado(self.serie_velocidad,
                                                                      cantidad_datos_promedio)

        m_vel.agrega_categoria_velocidad_aceleracion_promediados(diccionario_vel_acel_prom=
                                                                 self.velocidades_promediadas,
                                                                 datos=serie_velocidad_promediada,
                                                                 promedio=cantidad_datos_promedio)

        m_hist.agrega_categoria_histograma(diccionario_histograma=self.histogramas,
                                           categoria="velocidad_promediada_" + str(cantidad_datos_promedio),
                                           serie=serie_velocidad_promediada)

        m_ed.agrega_categoria_entropia(diccionario_entropia=self.entropias,
                                       categoria="histograma_velocidad_promediada_" + str(cantidad_datos_promedio),
                                       datos=self.histogramas["velocidad_promediada_" + str(cantidad_datos_promedio)])

        print("-------------------------------------------------------------")
        print("Entro a calcular aceleracion promediada\n")
        print("Serie de aceleracion: ", self.serie_aceleracion)

        serie_aceleracion_promediada = m_vel.obtener_arreglo_promediado(self.serie_aceleracion,
                                                                        cantidad_datos_promedio)

        m_vel.agrega_categoria_velocidad_aceleracion_promediados(diccionario_vel_acel_prom=
                                                                 self.aceleraciones_promediadas,
                                                                 datos=serie_aceleracion_promediada,
                                                                 promedio=cantidad_datos_promedio)

        m_hist.agrega_categoria_histograma(diccionario_histograma=self.histogramas,
                                           categoria="aceleracion_promediada_" + str(cantidad_datos_promedio),
                                           serie=serie_aceleracion_promediada)

        m_ed.agrega_categoria_entropia(diccionario_entropia=self.entropias,
                                       categoria="histograma_aceleracion_promediada_" + str(cantidad_datos_promedio),
                                       datos=self.histogramas["aceleracion_promediada_" + str(cantidad_datos_promedio)])

    def calcula_regiones_cuadriculadas(self):

        self.arreglo_region_cuadriculada, self.matriz_cuadriculada = \
            m_reg_cuad.calcula_regiones_cuadriculadas(tiempos=self.tiempo,
                                                      serie_posiciones_x=self.posiciones_x,
                                                      serie_posiciones_y=self.posiciones_y,
                                                      cantidad_filas=self.cantidad_filas,
                                                      cantidad_columnas=self.cantidad_columnas,
                                                      dimension_caja=self.dimension_caja)

        m_ed.agrega_categoria_entropia(diccionario_entropia=self.entropias,
                                       categoria="visitas_regiones",
                                       datos=self.matriz_cuadriculada.flatten())

        m_ed.agrega_categoria_entropia_aproximada(diccionario_entropia=self.entropias,
                                                  categoria="visitas_regiones_aprox",
                                                  datos=self.matriz_cuadriculada.flatten(),
                                                  tamanio_vectorial=2,
                                                  umbral=3)

        print(self.matriz_cuadriculada)

    def calcula_matrices_de_recurrencia(self):
        self.matriz_recurrencia_region_cuadriculada = \
            m_recurr.calcula_matrices_de_recurrencia(self.arreglo_region_cuadriculada)

        lista_indices = [self.indice_region_objeto_1,
                         self.indice_region_objeto_2,
                         self.indice_region_objeto_3,
                         self.indice_region_objeto_4]

        self.lista_matrices_recurrencia_regiones_importantes = []

        for indice in lista_indices:
            matriz = m_recurr.calcula_matrices_de_recurrencia(self.arreglo_region_cuadriculada,
                                                              region_importante=indice)
            self.lista_matrices_recurrencia_regiones_importantes.append(matriz)

        self.matriz_recurrencia_combinada = \
            m_recurr.calcula_matrices_de_recurrencia(self.arreglo_region_cuadriculada,
                                                     region_importante=lista_indices)

    def calcula_matrices_solo_regiones_preferidas(self, regiones_preferidas):

        print("Se inicia el procesamiento de las matrices con regiones preferidas")

        self.regiones_preferidas = regiones_preferidas
        total_regiones = list(range(0, self.cantidad_columnas * self.cantidad_filas))
        self.regiones_no_preferidas = m_reg_pref.obtener_complemento_de_sublista(lista=total_regiones,
                                                                                 sublista=regiones_preferidas)

        print("Regiones preferidas: ", self.regiones_preferidas)
        print("Regiones no preferidas: ", self.regiones_no_preferidas)

        print("--------------------------------------------------------------------------------")

        matriz_cuadriculada = np.flipud(self.matriz_cuadriculada)
        print("Se toma matriz cuadriculada", matriz_cuadriculada)

        self.matriz_cuadriculada_solo_regiones_preferidas = \
            m_reg_pref.obtener_submatriz_indices_dados(matriz_cuadriculada, self.regiones_preferidas)
        self.matriz_cuadriculada_solo_regiones_preferidas = \
            np.flipud(self.matriz_cuadriculada_solo_regiones_preferidas)

        m_ed.agrega_categoria_entropia(diccionario_entropia=self.entropias,
                                       categoria="visitas_regiones_preferidas",
                                       datos=self.matriz_cuadriculada_solo_regiones_preferidas.flatten())

        self.matriz_cuadriculada_solo_regiones_no_preferidas = \
            m_reg_pref.obtener_submatriz_indices_dados(matriz_cuadriculada, self.regiones_no_preferidas)
        self.matriz_cuadriculada_solo_regiones_no_preferidas = \
            np.flipud(self.matriz_cuadriculada_solo_regiones_no_preferidas)

        m_ed.agrega_categoria_entropia(diccionario_entropia=self.entropias,
                                       categoria="visitas_regiones_no_preferidas",
                                       datos=self.matriz_cuadriculada_solo_regiones_no_preferidas.flatten())

    def calcula_arreglos_rutas_vectoriales(self,
                                           tamanio_vectorial,
                                           brinco_temporal,
                                           indice_consecuencia):
        self.rutas_vectoriales.tamanio_vectorial = tamanio_vectorial
        self.rutas_vectoriales.brinco_temporal = brinco_temporal
        self.rutas_vectoriales.indice_consecuencia = indice_consecuencia

        self.rutas_vectoriales.obtener_posiciones_vectores()
        self.rutas_vectoriales.obtener_direcciones_vectores()

    def genera_modulo_para_reducir_sesiones(self):

        cantidad_filas = self.cantidad_filas
        cantidad_columnas = self.cantidad_columnas

        tamanio_horizontal = self.dimension_caja[0] / cantidad_columnas

        print("Tamaño horizontal:", tamanio_horizontal)

        velocidad_promedio = self.serie_velocidad.mean()

        print("Velocidad promedio", velocidad_promedio)

        nominador = tamanio_horizontal / velocidad_promedio

        print("Nominador:", nominador)

        modulo = nominador / 0.2

        print("Modulo:", modulo)

        return int(modulo)

    def obtener_coeficientes_de_regiones_mas_visitadas(self, cantidad_indices_a_obtener):
        matriz_regiones_aplastada = np.flipud(self.matriz_cuadriculada).flatten()
        regiones_mas_visitadas = np.argpartition(matriz_regiones_aplastada, -cantidad_indices_a_obtener)
        regiones_mas_visitadas = regiones_mas_visitadas[-(cantidad_indices_a_obtener + 1):]
        valores_mas_altos = matriz_regiones_aplastada[regiones_mas_visitadas]
        lista_ordenada_de_indices_mas_altos = [x for y, x in sorted(zip(valores_mas_altos, regiones_mas_visitadas))]
        print("Lista ordenada de indices mas altos",
              lista_ordenada_de_indices_mas_altos[(cantidad_indices_a_obtener + 1):0:-1])
        return lista_ordenada_de_indices_mas_altos[(cantidad_indices_a_obtener + 1):0:-1]

    def crea_sucesiones_a_evaluar(self, arreglo_de_subsucesiones, tamanio_de_subsucesiones):
        copia_sucesion_original = arreglo_de_subsucesiones.copy()
        lista_resultado_final = []
        lista_indices_final = []
        for i in range(0, len(copia_sucesion_original) - tamanio_de_subsucesiones):
            lista_resultado_final.append(copia_sucesion_original[i:(i + tamanio_de_subsucesiones)])
            lista_indices_final.append(
                list(range(self.modulo * i, self.modulo * (i + tamanio_de_subsucesiones), self.modulo)))
        print("Subsucesiones formadas: ", lista_resultado_final)
        print("indices_correspondientes", lista_indices_final)
        return lista_resultado_final, lista_indices_final

    def obtener_indices_subsucesiones_iniciales_para_distancias(self, cantidad_indices_a_obtener):
        lista_de_indices_de_subsucesiones_iniciales = []
        print("Obteniendo indices mas altos...")
        if self.lista_ordenada_de_indices_mas_altos is None:
            print("Calculando nueva lista de indices mas altos.")
            self.lista_ordenada_de_indices_mas_altos = self.obtener_coeficientes_de_regiones_mas_visitadas(
                cantidad_indices_a_obtener)
        print("Lista ordenada de indices mas altos: ", self.lista_ordenada_de_indices_mas_altos)
        for indice in self.lista_ordenada_de_indices_mas_altos:
            for i in range(len(self.lista_con_subsucesiones)):
                subsucesion = self.lista_con_subsucesiones[i]
                if subsucesion[0] == indice:
                    lista_de_indices_de_subsucesiones_iniciales.append(i)
                    break
        self.lista_de_indices_para_subsucesiones = lista_de_indices_de_subsucesiones_iniciales

    def reduce_elementos_sesion_con_modulo(self,
                                           tamanio,
                                           epsilon,
                                           subsucesiones_iniciales,
                                           subsucesiones_aleatorias,
                                           multiples_sesiones=False):
        self.modulo = self.genera_modulo_para_reducir_sesiones()
        self.tamanio = tamanio
        self.serie_a_utilizar = pd.Series(self.arreglo_region_cuadriculada)
        self.serie_a_utilizar = self.serie_a_utilizar[self.serie_a_utilizar.index % self.modulo == 0]
        print(self.serie_a_utilizar)
        arreglo_a_utilizar = self.serie_a_utilizar.to_numpy()
        self.calcula_distancias_entre_subsucesiones_aleatorias(tamanio_de_subsucesiones=tamanio,
                                                               epsilon=epsilon,
                                                               cantidad_subgrupos_sucesiones=subsucesiones_iniciales,
                                                               subsucesiones_aleatorias=subsucesiones_aleatorias,
                                                               arreglo_reducido_con_modulo=arreglo_a_utilizar)
        if multiples_sesiones is False:
            self.grafica_subsucesiones_parecidas(modulo=self.modulo, tamanio=self.tamanio)

    def grafica_subsucesiones_parecidas(self, modulo, tamanio):
        lista_colores = ["blue", "red", "green", "orange", "purple", "cyan", "magenta", "brown", "pink", "gray"]
        print(self.lista_indices_subsucesiones_parecidas)
        plt.clf()
        for i in range(len(self.lista_indices_subsucesiones_parecidas)):
            sublista_indice = self.lista_indices_subsucesiones_parecidas[i]
            print(sublista_indice)
            color = lista_colores[i]
            for j in range(len(sublista_indice)):
                indice_de_subsucesion = sublista_indice[j]
                valores = list(range(modulo * indice_de_subsucesion, modulo * indice_de_subsucesion + modulo * tamanio))
                plt.plot(self.posiciones_x[valores], self.posiciones_y[valores], color=color)
        plt.xlim(0, self.dimension_caja[0])
        plt.ylim(0, self.dimension_caja[1])
        plt.grid(True)
        plt.show()

    def calcula_distancias_entre_subsucesiones_aleatorias(self, tamanio_de_subsucesiones, epsilon,
                                                          cantidad_subgrupos_sucesiones,
                                                          subsucesiones_aleatorias,
                                                          arreglo_reducido_con_modulo=None):

        print(arreglo_reducido_con_modulo)

        if arreglo_reducido_con_modulo is None:
            arreglo_reducido_con_modulo = self.arreglo_region_cuadriculada

        self.lista_con_subsucesiones, self.lista_con_trazo_de_subsucesiones = self.crea_sucesiones_a_evaluar(
            arreglo_reducido_con_modulo,
            tamanio_de_subsucesiones)

        lista_de_indices_de_subsucesiones = list(range(0, len(self.lista_con_subsucesiones)))

        if subsucesiones_aleatorias == True:
            self.lista_de_indices_para_subsucesiones = random.sample(lista_de_indices_de_subsucesiones,
                                                                     cantidad_subgrupos_sucesiones)
        else:
            self.obtener_indices_subsucesiones_iniciales_para_distancias(cantidad_subgrupos_sucesiones)

        print("Subsucesiones iniciales elegidas: ", self.lista_de_indices_para_subsucesiones)

        lista_con_subsucesiones_aleatorias = []
        self.lista_indices_subsucesiones_parecidas = []

        print(self.lista_de_indices_para_subsucesiones)

        for i in self.lista_de_indices_para_subsucesiones:
            lista_con_subsucesiones_aleatorias.append(self.lista_con_subsucesiones[i])
            self.lista_indices_subsucesiones_parecidas.append([i])

        self.lista_dataframes_subsucesiones_parecidas = []

        print("Lista con subsucesiobes aleatorias: ", lista_con_subsucesiones_aleatorias)

        for i in range(len(self.lista_de_indices_para_subsucesiones)):
            self.lista_dataframes_subsucesiones_parecidas.append(pd.DataFrame())
            sucesion_a_comparar = lista_con_subsucesiones_aleatorias[i]
            dataframe_de_sucesion_a_comparar = self.lista_dataframes_subsucesiones_parecidas[i]
            dataframe_de_sucesion_a_comparar[0] = sucesion_a_comparar

            for j in range(len(self.lista_con_subsucesiones)):
                if j != self.lista_de_indices_para_subsucesiones[i]:
                    sucesion_nueva = self.lista_con_subsucesiones[j]
                    se_encontro_epsilon = self.distancia_entre_sucesiones(sucesion_a_comparar, sucesion_nueva, epsilon)
                    if se_encontro_epsilon:
                        dataframe_de_sucesion_a_comparar[len(dataframe_de_sucesion_a_comparar.columns)] = \
                            sucesion_nueva
                        self.lista_indices_subsucesiones_parecidas[i].append(j)

    def calcula_distancias_entre_sucesiones(self, brinco, epsilon=1):
        print("---------------------------------------------------------------")
        copia_sucesion_original = self.arreglo_region_cuadriculada.copy()
        for i in range(0, len(copia_sucesion_original), brinco):
            copia_segunda_sucesion = copia_sucesion_original.copy()
            for j in range(0, len(copia_segunda_sucesion), brinco):
                self.funcion_sigma_sucesion_2(copia_segunda_sucesion, j)
                se_encontro_epsilon = self.distancia_entre_sucesiones(copia_sucesion_original,
                                                                      copia_segunda_sucesion,
                                                                      epsilon)
                if se_encontro_epsilon:
                    break
            if se_encontro_epsilon:
                break
            else:
                copia_sucesion_original = self.funcion_sigma_sucesion_1(copia_sucesion_original, brinco)
        print("Las sucesiones similares son: ")
        print(copia_sucesion_original)
        print(copia_segunda_sucesion)

    def funcion_sigma_sucesion_1(self, sucesion, brinco):
        copia_sucesion = sucesion.copy()
        if (len(copia_sucesion) >= brinco):
            for i in range(0, brinco):
                copia_sucesion = np.delete(copia_sucesion, 0)
        else:
            return []
        return copia_sucesion

    def funcion_sigma_sucesion_2(self, sucesion, indice):
        sucesion[indice] = 0

    def distancia_entre_sucesiones(self, sucesion_1, sucesion_2, epsilon):
        operacion = 0
        total_de_regiones_en_sucesion = len(set(sucesion_1))
        for n in range(len(sucesion_1)):
            operacion += abs(Decimal(sucesion_1[n]) - Decimal(sucesion_2[n])) / (Decimal(2 ** n))
        if (operacion < epsilon):
            return True
        else:
            return False

    def genera_dataframe_de_datos(self):
        diccionario_csv = {'Sample no.': self.samples,
                           'Time': self.tiempo,
                           'X': self.posiciones_x,
                           'Y': self.posiciones_y,
                           'Obj_Dist_1': self.dist_objeto_1,
                           'Obj_Dist_Prom_1': self.distancia_a_objeto_promediado,
                           'Obj_Dist_2': self.dist_objeto_2,
                           'Obj_Dist_3': self.dist_objeto_3,
                           'Obj_Dist_4': self.dist_objeto_4,
                           'Obj_Dist_Min_2_3_4': self.distancia_minima_objetos_2_3_4,
                           'Velocity': self.serie_velocidad,
                           'Acceleration': self.serie_aceleracion}
        tabla_csv = pd.DataFrame(diccionario_csv)
        print(diccionario_csv)
        return tabla_csv

    def exporta_csv(self, nombre):

        tabla_csv = self.genera_dataframe_de_datos()

        print(tabla_csv)

        tabla_csv.to_csv(nombre, index=False)

    def exporta_estadisticas(self, nombre):
        data = {'1': ['Max_Vel', 'Max_Accel', 'Total_Dist', 'Recurrence Matrix'],
                '2': [round(self.velocidad_maxima, 3), round(self.aceleracion_maxima, 3),
                      round(self.distancia_total_recorrida, 3),
                      '']}
        data = pd.DataFrame(data)
        datos_a_exportar = data.append(pd.DataFrame(np.flipud(self.matriz_recurrencia_region_cuadriculada)))
        print(datos_a_exportar)
        print('Aqui voy bien')
        data_para_matriz_tiempos = {'1': ['Time_in_Region_Matrix']}
        data_para_matriz_tiempos = pd.DataFrame(data_para_matriz_tiempos)
        data_para_matriz_tiempos = data_para_matriz_tiempos.append(pd.DataFrame(self.matriz_cuadriculada))
        print("------------------------------------------------------------------------")
        print(data_para_matriz_tiempos)
        datos_a_exportar = datos_a_exportar.append(data_para_matriz_tiempos)
        print("------------------------------------------------------------------------")
        print(datos_a_exportar)
        pd.DataFrame(datos_a_exportar).to_csv(nombre, header=None, index=False)

    def exporta_estadisticas_2(self, nombre):
        data = {'1': ['Max_Vel',
                      'Max_Accel',
                      'Total_Dist',
                      'Recurrence_Matrix',
                      '',
                      'Time_in_region_Matrix'],
                '2': [round(self.velocidad_maxima, 3),
                      round(self.aceleracion_maxima, 3),
                      round(self.distancia_total_recorrida, 3),
                      pd.DataFrame(np.flipud(self.matriz_recurrencia_region_cuadriculada), columns=None, index=None),
                      '',
                      pd.DataFrame(self.matriz_cuadriculada, columns=None, index=None)
                      ]}
        data = pd.DataFrame(data)
        data.to_csv(nombre, header=None, index=False)

    def exporta_matriz_tiempo_regiones(self, nombre):
        data = pd.DataFrame(self.matriz_cuadriculada, columns=None, index=None)
        data.to_csv(nombre, header=None, index=False)

    def exporta_regiones_circulares(self, nombre):
        data = {'1': ['Objeto_1',
                      'Objeto_2',
                      'Objeto_3',
                      'Objeto_4', ],
                '2': [self.cantidad_posiciones_volumen_1,
                      self.cantidad_posiciones_volumen_2,
                      self.cantidad_posiciones_volumen_3,
                      self.cantidad_posiciones_volumen_4,
                      ]}
        data = pd.DataFrame(data)
        data.to_csv(nombre, header=None, index=False)

    def graficar_figura(self, nombre_grafica, config_grafica):
        print("-----------------------------------------------------------")
        print("Tipo de grafica", nombre_grafica)

        limites_x, limites_y = config_grafica.regresa_config_grafica_general()
        lim_inf_x = limites_x[0]
        lim_sup_x = limites_x[1]
        lim_inf_y = limites_y[0]
        lim_sup_y = limites_y[1]

        objetos_seleccionados, objeto_a_promediar, tamanio_intervalo_para_promedio = \
            config_grafica.regresa_config_grafica_distancias()

        print("Objetos a graficar: ", objetos_seleccionados)

        objeto_1_seleccionado = objetos_seleccionados[0]
        objeto_2_seleccionado = objetos_seleccionados[1]
        objeto_3_seleccionado = objetos_seleccionados[2]
        objeto_4_seleccionado = objetos_seleccionados[3]

        fig = Figure(figsize=(6, 6))
        plt = fig.add_subplot(111)
        plt.grid(True)

        if nombre_grafica is not 'region_cuadricula_3d':
            if limites_x[0] is not None and limites_x[1] is not None:
                plt.set_xlim(limites_x[0], limites_x[1])
            if limites_y[0] is not None and limites_y[1] is not None:
                plt.set_ylim(limites_y[0], limites_y[1])

        if nombre_grafica == 'ruta':
            print("Entro a ruta")

            plt.plot(self.posiciones_x, self.posiciones_y, color='blue')
            if objeto_1_seleccionado is True:
                plt.plot(self.objeto_relevante_1[0], self.objeto_relevante_1[1], '*', color='blue')
            if objeto_2_seleccionado is True:
                plt.plot(self.objeto_relevante_2[0], self.objeto_relevante_2[1], 'o', color='green')
            if objeto_3_seleccionado is True:
                plt.plot(self.objeto_relevante_3[0], self.objeto_relevante_3[1], 'o', color='red')
            if objeto_4_seleccionado is True:
                plt.plot(self.objeto_relevante_4[0], self.objeto_relevante_4[1], 'o', color='orange')

        elif nombre_grafica == 'ruta_vectoriales_consecuencia':

            posiciones_x, posiciones_y, direcciones_x, direcciones_y = \
                self.rutas_vectoriales.regresa_posiciones_direcciones()

            x_pos_antes_consecuencia, x_pos_despues_consecuencia = posiciones_x
            y_pos_antes_consecuencia, y_pos_despues_consecuencia = posiciones_y

            x_direct_antes, x_direct_despues = direcciones_x
            y_direct_antes, y_direct_despues = direcciones_y

            plt.quiver(x_pos_antes_consecuencia, y_pos_antes_consecuencia,
                       x_direct_antes, y_direct_antes,
                       angles='xy', scale_units='xy', scale=1, color='blue')
            plt.quiver(x_pos_despues_consecuencia[:-1], y_pos_despues_consecuencia[:-1],
                       x_direct_despues, y_direct_despues,
                       angles='xy', scale_units='xy', scale=1, color='red')
            plt.set_xlim(0, self.dimension_caja[0])
            plt.set_ylim(0, self.dimension_caja[1])

        elif nombre_grafica == 'distancias':
            print("Entro a distancias")
            lista_valores_minimos = []
            lista_valores_maximos = []

            if objeto_1_seleccionado is True:
                print(1)
                print(self.dist_objeto_1)
                print(self.dist_objeto_1.max())
                plt.plot(self.tiempo, self.dist_objeto_1, color='blue', label='Objeto 1')
                lista_valores_minimos.append(self.dist_objeto_1.min())
                lista_valores_maximos.append(self.dist_objeto_1.max())
            if objeto_2_seleccionado is True:
                print(2)
                print(self.dist_objeto_2)
                print(self.dist_objeto_2.max())
                plt.plot(self.tiempo, self.dist_objeto_2, color='green', label='Objeto 2')
                lista_valores_minimos.append(self.dist_objeto_2.min())
                lista_valores_maximos.append(self.dist_objeto_2.max())
            if objeto_3_seleccionado is True:
                print(3)
                print(self.dist_objeto_3)
                print(self.dist_objeto_3.max())
                plt.plot(self.tiempo, self.dist_objeto_3, color='red', label='Objeto 3')
                lista_valores_minimos.append(self.dist_objeto_3.min())
                lista_valores_maximos.append(self.dist_objeto_3.max())
            if objeto_4_seleccionado is True:
                print(4)
                print(self.dist_objeto_4)
                print(self.dist_objeto_4.max())
                plt.plot(self.tiempo, self.dist_objeto_4, color='orange', label='Objeto 4')
                lista_valores_minimos.append(self.dist_objeto_4.min())
                lista_valores_maximos.append(self.dist_objeto_4.max())
            y_min = min(lista_valores_minimos)
            y_max = max(lista_valores_maximos)

            if lim_inf_y is None and lim_sup_y is None:
                plt.set_ylim(y_min, y_max + 30)

            # plt.legend()

        elif nombre_grafica == 'dist_prom':
            print("Entro a distancia promediada a objeto")

            objetos_a_utilizar, objeto_a_promediar, tamanio_intervalo_para_promedio = \
                config_grafica.regresa_config_grafica_distancias()

            self.calcula_distancia_promediada_con_objeto(objeto_a_promediar,
                                                         tamanio_intervalo_para_promedio)

            if lim_inf_y is None and lim_sup_y is None:
                plt.set_ylim(min(self.dist_objeto_1), max(self.dist_objeto_1) + 5)

            plt.plot(self.tiempo, self.dist_objeto_1, linestyle=':', color='gray', label='Distancia original')
            plt.plot(self.tiempo, self.distancia_a_objeto_promediado, color='red',
                     label='Distancia a objeto promediado')

            # plt.legend()

        elif nombre_grafica == 'dist_min':

            print("Entro a dist_min")

            if lim_inf_y is None and lim_sup_y is None:
                plt.set_ylim(min(self.distancia_minima_objetos_2_3_4.min(), self.dist_objeto_1.min()),
                             max(self.distancia_minima_objetos_2_3_4.max(), self.dist_objeto_1.max()) + 30)

            plt.plot(self.tiempo, self.distancia_minima_objetos_2_3_4, color='red', label='Resto de objetos')
            plt.plot(self.tiempo, self.dist_objeto_1, color='blue', label='Objeto 1')

        elif nombre_grafica == 'vel':

            print("Entro a vel")
            plt.scatter(self.tiempo, self.serie_velocidad, s=1)

        elif nombre_grafica == 'vel_prom':
            print("Entro a vel_prom\n")

            promedio = config_grafica.regresa_config_grafica_vel_acel_prom()
            print("Promedio elegido: ", promedio)
            velocidad_promediada = self.velocidades_promediadas[str(promedio)]
            print("Velocidad promediada: ", velocidad_promediada)

            longitud_serie_velocidad_promediada = len(velocidad_promediada)
            tiempo = np.linspace(0, longitud_serie_velocidad_promediada, longitud_serie_velocidad_promediada)
            plt.scatter(tiempo, velocidad_promediada, s=1)

        elif nombre_grafica == 'vel_hist':
            print("Entro a vel_hist")
            print(plt.hist(self.serie_velocidad))
            plt.hist(self.serie_velocidad)

        elif nombre_grafica == 'acel':

            print("Entro a acel")
            plt.scatter(self.tiempo, self.serie_aceleracion, s=1)

        elif nombre_grafica == 'acel_prom':

            print("Entro a acelPrm")

            promedio = config_grafica.regresa_config_grafica_vel_acel_prom()
            aceleracion_promediada = self.aceleraciones_promediadas[str(promedio)]

            longitud_serie_aceleracion_promediada = len(aceleracion_promediada)
            tiempo = np.linspace(0, longitud_serie_aceleracion_promediada, longitud_serie_aceleracion_promediada)
            plt.scatter(tiempo, aceleracion_promediada, s=1)

        elif nombre_grafica == 'acel_hist':

            print("Entro a acel_hist")
            print(plt.hist(self.serie_aceleracion))
            plt.hist(self.serie_aceleracion)

        # elif grafica == 'distPeso':
        #    print("Entro a distPeso")
        #    plt.plot(self.t, self.distPeso, color='black')

        # Usa la distancia minima a las palancas y grafica 1 si estuvo mas proxima a la palanca 1,
        # 2 si estuvo mas proxima a la palanca 2 y 3 si estuvo mas proxima a la palanca 3.

        # elif grafica == 'clasePalanca':
        #    plt.set_ylim(0.8, 3.2)
        #    plt.scatter(self.t.values, self.claseMinPalanca.values, s=5, c='black')

        # Similar a la grafica 'clasePalanca', pero agregando la distancia minima al comedero y usando 0 para
        # graficarla.

        # elif grafica == 'claseTodoPalanca':
        #    plt.set_ylim(-0.2, 3.2)
        #    plt.scatter(self.t.values, self.claseMinTodo.values, s=5, c='black')

        # elif grafica == 'claseRegionesExtendidas':
        #    r_1 = 0
        #    r_2 = 0
        #    suma_total = self.regionesFrecAc['Frecuencia'].sum()
        #    for i in range(len(self.regionesFrecAc)):
        #        r_1 = r_2
        #        r_2 = ((self.regionesFrecAc['Frecuencia'].iloc[i]) / suma_total) + r_1
        #        plt.plot(np.array([r_1, r_2]),
        #                 np.array([self.regionesFrecAc['Region'].iloc[i], self.regionesFrecAc['Region'].iloc[i]]),
        #                 color='blue')
        #    plt.set_ylim(-1.2, 3.2)

        # elif grafica == 'aceleracionRegiones':
        #    plt.plot(np.arange(1, (len(self.regionesFrecAc)), 1), self.acelRegiones)

        # elif grafica == 'cambioRegiones/Acel':
        #    plt.set_ylim(-0.2, 3.2)
        #    plt.scatter(np.arange(0, len(self.regionesFrecAc['Region'])), self.regionesFrecAc['Region'], s=5, c='black')
        #    plt.plot(np.arange(1, (len(self.regionesFrecAc)), 1), coeficiente * self.acelRegiones, '-', color='red')

        # elif grafica == 'matriz_recurrencia':
        #    plt.grid(False)
        #    plt.imshow(self.matrizRec, cmap='gray', interpolation='nearest', vmin=0, vmax=5)
        #    plt.legend()

        elif nombre_grafica == 'matriz_recurrencia_cuadriculada':
            plt.grid(False)

            print("Matriz de recurrencia region cuadriculada:", self.matriz_recurrencia_region_cuadriculada)
            plt.imshow(-1 * self.matriz_recurrencia_region_cuadriculada, origin='lower', cmap='gray',
                       interpolation='nearest', vmin=-1, vmax=0)

        elif nombre_grafica == 'matriz_recurrencia_cuadriculada_objeto_1':

            matriz_recurrencia_objeto_1 = self.lista_matrices_recurrencia_regiones_importantes[0]

            plt.grid(False)
            plt.imshow(-1 * matriz_recurrencia_objeto_1, origin='lower', cmap='gray',
                       interpolation='nearest', vmin=-1, vmax=0)

        elif nombre_grafica == 'matriz_recurrencia_cuadriculada_objeto_2':

            matriz_recurrencia_objeto_2 = self.lista_matrices_recurrencia_regiones_importantes[1]

            plt.grid(False)
            plt.imshow(-1 * matriz_recurrencia_objeto_2, origin='lower', cmap='gray',
                       interpolation='nearest')

        elif nombre_grafica == 'matriz_recurrencia_cuadriculada_objeto_3':

            matriz_recurrencia_objeto_3 = self.lista_matrices_recurrencia_regiones_importantes[2]

            plt.grid(False)
            plt.imshow(-1 * matriz_recurrencia_objeto_3, origin='lower', cmap='gray',
                       interpolation='nearest')

        elif nombre_grafica == 'matriz_recurrencia_cuadriculada_objeto_4':

            matriz_recurrencia_objeto_4 = self.lista_matrices_recurrencia_regiones_importantes[3]

            plt.grid(False)
            plt.imshow(-1 * matriz_recurrencia_objeto_4, origin='lower', cmap='gray',
                       interpolation='nearest')

        elif nombre_grafica == 'matriz_recurrencia_cuadriculada_combinada':
            plt.grid(False)
            nueva_matriz_recurrencia_combinada = self.matriz_recurrencia_combinada + \
                                                 self.matriz_recurrencia_region_cuadriculada
            cmap = colors.ListedColormap(['white', 'black', 'blue', 'red', 'green', 'orange'])
            bounds = [0, 1, 2, 3, 4, 5]
            norm = colors.BoundaryNorm(bounds, cmap.N)
            plt.imshow(nueva_matriz_recurrencia_combinada, origin='lower', cmap=cmap, norm=norm,
                       interpolation='nearest')

        # elif grafica == 'matrizRecurrenciaColor':
        #    plt.grid(False)
        #    cmap = colors.ListedColormap(['blue', 'green', 'red', 'yellow', 'gray', 'white'])
        #    bounds = [0, 1, 2, 3, 4, 5, 6]
        #    norm = colors.BoundaryNorm(bounds, cmap.N)
        #    plt.imshow(self.matrizRec, cmap=cmap, norm=norm, interpolation='nearest')

        # elif grafica == 'regionCuadricula':
        #    import matplotlib.pyplot as plt
        #    print(self.matriz_cuadriculada)
        #    plt.grid(False)
        #    plt.colorbar(
        #        plt.imshow(np.flipud(self.matriz_cuadriculada)))

        elif nombre_grafica == 'regresion_lineal':

            print("Entro a regresion lineal")

            nombre_regresion_lineal = config_grafica.regresa_config_grafica_regresion_lineal()
            print("Nombre_regresion_lineal:", nombre_regresion_lineal)
            regresion_lineal_elegida = self.regresiones_lineales[nombre_regresion_lineal]
            print("Diccionario:", regresion_lineal_elegida)
            print("---------------------------------------------------------------")
            indices_tiempo = regresion_lineal_elegida["indices_tiempo"]
            series_tiempo = regresion_lineal_elegida["series_tiempo"]
            resultados = regresion_lineal_elegida["resultados"]
            pendientes = regresion_lineal_elegida["pendientes"]

            print("Indices de tiempo:", indices_tiempo)
            print("Series_tiempo:", series_tiempo)
            print("Resultados:", resultados)
            print("Pendientes:", pendientes)

            for indice in range(0, len(indices_tiempo)):
                plt.scatter(indices_tiempo[indice], series_tiempo[indice], color='blue', s=1)
                plt.plot(indices_tiempo[indice], resultados[indice], color='red')

        elif nombre_grafica == 'cilindros_objetos_importantes':
            print("Entro a volumenes_objetos_importantes")

            objetos_seleccionados, tamanio_volumenes, div_volumenes, tipo_grafica_volumen, rot_grafica_3d = \
                config_grafica.regresa_config_grafica_figuras()

            objeto_1_seleccionado = objetos_seleccionados[0]
            objeto_2_seleccionado = objetos_seleccionados[1]
            objeto_3_seleccionado = objetos_seleccionados[2]
            objeto_4_seleccionado = objetos_seleccionados[3]

            print("Tamaño_volumenes:", tamanio_volumenes)
            print("Div_volumenes:", div_volumenes)
            print("tipo_grafica_volumen:", tipo_grafica_volumen)
            print("rot_grafica_3d", rot_grafica_3d)

            self.cantidad_posiciones_volumenes, self.radios_volumenes = \
                m_ci.calcula_alturas_volumenes_circulares_objetos_relevantes(posiciones_x=self.posiciones_x,
                                                                             posiciones_y=self.posiciones_y,
                                                                             lista_objetos_relevantes=
                                                                             self.lista_objetos_relevantes,
                                                                             tamanio=tamanio_volumenes,
                                                                             divisiones=div_volumenes,
                                                                             tipo=tipo_grafica_volumen)

            print("Salgo de la funcion")

            if getattr(sys, 'frozen', False):
                os.environ['BASEMAPDATA'] = os.path.join(os.path.dirname(sys.executable), 'mplot3d')

            ax = fig.add_subplot(111, projection='3d')
            ax.view_init(azim=rot_grafica_3d % 360, elev=0)

            print("Cantidad de posiciones para volumenes:", self.cantidad_posiciones_volumenes)

            for i in range(0, len(self.cantidad_posiciones_volumenes[0])):
                if objeto_1_seleccionado is True:
                    m_ci.pintar_cilindro(self.objeto_relevante_1[0],
                                         self.objeto_relevante_1[1],
                                         self.radios_volumenes[i],
                                         self.cantidad_posiciones_volumenes[0][i],
                                         ax)
                if objeto_2_seleccionado is True:
                    m_ci.pintar_cilindro(self.objeto_relevante_2[0],
                                         self.objeto_relevante_2[1],
                                         self.radios_volumenes[i],
                                         self.cantidad_posiciones_volumenes[1][i],
                                         ax)
                if objeto_3_seleccionado is True:
                    m_ci.pintar_cilindro(self.objeto_relevante_3[0],
                                         self.objeto_relevante_3[1],
                                         self.radios_volumenes[i],
                                         self.cantidad_posiciones_volumenes[2][i],
                                         ax)
                if objeto_4_seleccionado is True:
                    m_ci.pintar_cilindro(self.objeto_relevante_4[0],
                                         self.objeto_relevante_4[1],
                                         self.radios_volumenes[i],
                                         self.cantidad_posiciones_volumenes[3][i],
                                         ax)

            ax.set_xlim(0, 100)
            ax.set_ylim(0, 100)
            ax.set_zlim(0, len(self.posiciones_x))

            if 0 < rot_grafica_3d <= 90:
                ax.xaxis._axinfo['juggled'] = (0, 0, 0)
                ax.yaxis._axinfo['juggled'] = (1, 1, 1)
                ax.zaxis._axinfo['juggled'] = (2, 2, 2)
            elif 90 < rot_grafica_3d <= 180:
                ax.xaxis._axinfo['juggled'] = (0, 0, 0)
                ax.yaxis._axinfo['juggled'] = (0, 1, 2)
                ax.zaxis._axinfo['juggled'] = (0, 2, 1)
            elif 180 < rot_grafica_3d <= 270:
                ax.xaxis._axinfo['juggled'] = (1, 0, 2)
                ax.yaxis._axinfo['juggled'] = (0, 1, 2)
                ax.zaxis._axinfo['juggled'] = (2, 2, 2)
            elif 270 < rot_grafica_3d <= 360:
                ax.xaxis._axinfo['juggled'] = (1, 0, 2)
                ax.yaxis._axinfo['juggled'] = (1, 1, 1)
                ax.zaxis._axinfo['juggled'] = (1, 2, 0)

            ax.view_init(azim=rot_grafica_3d)

        elif nombre_grafica == 'region_cuadricula_3d':

            print("Entro a regionCuadricula3d")

            rot_grafica_3d = 220

            objeto_1_x = self.objeto_relevante_1[0]
            objeto_1_y = self.objeto_relevante_1[1]

            objeto_2_x = self.objeto_relevante_2[0]
            objeto_2_y = self.objeto_relevante_2[1]

            objeto_3_x = self.objeto_relevante_3[0]
            objeto_3_y = self.objeto_relevante_3[1]

            objeto_4_x = self.objeto_relevante_4[0]
            objeto_4_y = self.objeto_relevante_4[1]

            if getattr(sys, 'frozen', False):
                os.environ['BASEMAPDATA'] = os.path.join(os.path.dirname(sys.executable), 'mplot3d')

            data_array = np.array(np.flipud(self.matriz_cuadriculada))

            print(data_array)

            ax = fig.add_subplot(111, projection='3d')

            ax.view_init(azim=rot_grafica_3d % 360, elev=0)

            x_data, y_data = np.meshgrid(np.arange(data_array.shape[1]),
                                         np.arange(data_array.shape[0]))

            x_data = x_data.flatten()
            y_data = y_data.flatten()
            z_data = data_array.flatten()

            tamanio_horizontal = self.dimension_caja[0] / self.cantidad_columnas
            tamanio_vertical = self.dimension_caja[1] / self.cantidad_filas

            objeto_1_x_pos_matriz_cuadriculada = int(objeto_1_x // tamanio_horizontal)
            objeto_1_y_pos_matriz_cuadriculada = int(objeto_1_y // tamanio_vertical)

            objeto_2_x_pos_matriz_cuadriculada = int(objeto_2_x // tamanio_horizontal)
            objeto_2_y_pos_matriz_cuadriculada = int(objeto_2_y // tamanio_vertical)

            objeto_3_x_pos_matriz_cuadriculada = int(objeto_3_x // tamanio_horizontal)
            objeto_3_y_pos_matriz_cuadriculada = int(objeto_3_y // tamanio_vertical)

            objeto_4_x_pos_matriz_cuadriculada = int(objeto_4_x // tamanio_horizontal)
            objeto_4_y_pos_matriz_cuadriculada = int(objeto_4_y // tamanio_vertical)

            print([objeto_1_x_pos_matriz_cuadriculada],
                  [objeto_2_x_pos_matriz_cuadriculada],
                  [objeto_3_x_pos_matriz_cuadriculada],
                  [objeto_4_x_pos_matriz_cuadriculada])
            print([objeto_1_y_pos_matriz_cuadriculada],
                  [objeto_2_y_pos_matriz_cuadriculada],
                  [objeto_3_y_pos_matriz_cuadriculada],
                  [objeto_4_y_pos_matriz_cuadriculada])

            ax.bar3d(x_data,
                     y_data,
                     np.zeros(len(z_data)),
                     1, 1, z_data)

            if 0 < rot_grafica_3d <= 90:
                ax.xaxis._axinfo['juggled'] = (0, 0, 0)
                ax.yaxis._axinfo['juggled'] = (1, 1, 1)
                ax.zaxis._axinfo['juggled'] = (2, 2, 2)
            elif 90 < rot_grafica_3d <= 180:
                ax.xaxis._axinfo['juggled'] = (0, 0, 0)
                ax.yaxis._axinfo['juggled'] = (0, 1, 2)
                ax.zaxis._axinfo['juggled'] = (0, 2, 1)
            elif 180 < rot_grafica_3d <= 270:
                ax.xaxis._axinfo['juggled'] = (1, 0, 2)
                ax.yaxis._axinfo['juggled'] = (0, 1, 2)
                ax.zaxis._axinfo['juggled'] = (2, 2, 2)
            elif 270 < rot_grafica_3d <= 360:
                ax.xaxis._axinfo['juggled'] = (1, 0, 2)
                ax.yaxis._axinfo['juggled'] = (1, 1, 1)
                ax.zaxis._axinfo['juggled'] = (1, 2, 0)

            ax.view_init(azim=rot_grafica_3d)

        elif nombre_grafica == 'region_cuadricula_3d_regiones_preferidas':

            print("Entro a regionCuadricula3d, regiones preferidas")

            rot_grafica_3d = 220

            objeto_1_x = self.objeto_relevante_1[0]
            objeto_1_y = self.objeto_relevante_1[1]

            objeto_2_x = self.objeto_relevante_2[0]
            objeto_2_y = self.objeto_relevante_2[1]

            objeto_3_x = self.objeto_relevante_3[0]
            objeto_3_y = self.objeto_relevante_3[1]

            objeto_4_x = self.objeto_relevante_4[0]
            objeto_4_y = self.objeto_relevante_4[1]

            if getattr(sys, 'frozen', False):
                os.environ['BASEMAPDATA'] = os.path.join(os.path.dirname(sys.executable), 'mplot3d')

            data_array = np.array(np.flipud(self.matriz_cuadriculada_regiones_preferidas))

            print(data_array)

            ax = fig.add_subplot(111, projection='3d')

            ax.view_init(azim=rot_grafica_3d % 360, elev=0)

            x_data, y_data = np.meshgrid(np.arange(data_array.shape[1]),
                                         np.arange(data_array.shape[0]))

            x_data = x_data.flatten()
            y_data = y_data.flatten()
            z_data = data_array.flatten()

            tamanio_horizontal = self.dimension_caja[0] / self.cantidad_columnas
            tamanio_vertical = self.dimension_caja[1] / self.cantidad_filas

            objeto_1_x_pos_matriz_cuadriculada = int(objeto_1_x // tamanio_horizontal)
            objeto_1_y_pos_matriz_cuadriculada = int(objeto_1_y // tamanio_vertical)

            objeto_2_x_pos_matriz_cuadriculada = int(objeto_2_x // tamanio_horizontal)
            objeto_2_y_pos_matriz_cuadriculada = int(objeto_2_y // tamanio_vertical)

            objeto_3_x_pos_matriz_cuadriculada = int(objeto_3_x // tamanio_horizontal)
            objeto_3_y_pos_matriz_cuadriculada = int(objeto_3_y // tamanio_vertical)

            objeto_4_x_pos_matriz_cuadriculada = int(objeto_4_x // tamanio_horizontal)
            objeto_4_y_pos_matriz_cuadriculada = int(objeto_4_y // tamanio_vertical)

            print([objeto_1_x_pos_matriz_cuadriculada],
                  [objeto_2_x_pos_matriz_cuadriculada],
                  [objeto_3_x_pos_matriz_cuadriculada],
                  [objeto_4_x_pos_matriz_cuadriculada])
            print([objeto_1_y_pos_matriz_cuadriculada],
                  [objeto_2_y_pos_matriz_cuadriculada],
                  [objeto_3_y_pos_matriz_cuadriculada],
                  [objeto_4_y_pos_matriz_cuadriculada])

            ax.bar3d(x_data,
                     y_data,
                     np.zeros(len(z_data)),
                     1, 1, z_data)

            if 0 < rot_grafica_3d <= 90:
                ax.xaxis._axinfo['juggled'] = (0, 0, 0)
                ax.yaxis._axinfo['juggled'] = (1, 1, 1)
                ax.zaxis._axinfo['juggled'] = (2, 2, 2)
            elif 90 < rot_grafica_3d <= 180:
                ax.xaxis._axinfo['juggled'] = (0, 0, 0)
                ax.yaxis._axinfo['juggled'] = (0, 1, 2)
                ax.zaxis._axinfo['juggled'] = (0, 2, 1)
            elif 180 < rot_grafica_3d <= 270:
                ax.xaxis._axinfo['juggled'] = (1, 0, 2)
                ax.yaxis._axinfo['juggled'] = (0, 1, 2)
                ax.zaxis._axinfo['juggled'] = (2, 2, 2)
            elif 270 < rot_grafica_3d <= 360:
                ax.xaxis._axinfo['juggled'] = (1, 0, 2)
                ax.yaxis._axinfo['juggled'] = (1, 1, 1)
                ax.zaxis._axinfo['juggled'] = (1, 2, 0)

            ax.view_init(azim=rot_grafica_3d)

        elif nombre_grafica == 'region_cuadricula_3d_solo_regiones_preferidas':

            print("Entro a regionCuadricula3d, solo regiones preferidas")

            regiones_preferidas = config_grafica.regiones_preferidas_3d
            print("Regiones preferidas: ", regiones_preferidas)
            total_regiones = list(range(0, self.cantidad_columnas * self.cantidad_filas))
            regiones_no_preferidas = m_reg_pref.obtener_complemento_de_sublista(lista=total_regiones,
                                                                                sublista=regiones_preferidas)
            print("Regiones no preferidas: ", regiones_no_preferidas)

            self.matriz_cuadriculada_solo_regiones_preferidas = \
                m_reg_pref.obtener_submatriz_indices_dados(np.flipud(self.matriz_cuadriculada),
                                                           regiones_preferidas)
            self.matriz_cuadriculada_solo_regiones_preferidas = \
                np.flipud(self.matriz_cuadriculada_solo_regiones_preferidas)

            rot_grafica_3d = config_grafica.rot_grafica_3d

            objeto_1_x = self.objeto_relevante_1[0]
            objeto_1_y = self.objeto_relevante_1[1]

            objeto_2_x = self.objeto_relevante_2[0]
            objeto_2_y = self.objeto_relevante_2[1]

            objeto_3_x = self.objeto_relevante_3[0]
            objeto_3_y = self.objeto_relevante_3[1]

            objeto_4_x = self.objeto_relevante_4[0]
            objeto_4_y = self.objeto_relevante_4[1]

            if getattr(sys, 'frozen', False):
                os.environ['BASEMAPDATA'] = os.path.join(os.path.dirname(sys.executable), 'mplot3d')

            data_array = np.array(np.flipud(self.matriz_cuadriculada_solo_regiones_preferidas))

            print(data_array)

            ax = fig.add_subplot(111, projection='3d')

            ax.view_init(azim=rot_grafica_3d % 360, elev=0)

            x_data, y_data = np.meshgrid(np.arange(data_array.shape[1]),
                                         np.arange(data_array.shape[0]))

            x_data = x_data.flatten()
            y_data = y_data.flatten()
            z_data = data_array.flatten()

            tamanio_horizontal = self.dimension_caja[0] / self.cantidad_columnas
            tamanio_vertical = self.dimension_caja[1] / self.cantidad_filas

            objeto_1_x_pos_matriz_cuadriculada = int(objeto_1_x // tamanio_horizontal)
            objeto_1_y_pos_matriz_cuadriculada = int(objeto_1_y // tamanio_vertical)

            objeto_2_x_pos_matriz_cuadriculada = int(objeto_2_x // tamanio_horizontal)
            objeto_2_y_pos_matriz_cuadriculada = int(objeto_2_y // tamanio_vertical)

            objeto_3_x_pos_matriz_cuadriculada = int(objeto_3_x // tamanio_horizontal)
            objeto_3_y_pos_matriz_cuadriculada = int(objeto_3_y // tamanio_vertical)

            objeto_4_x_pos_matriz_cuadriculada = int(objeto_4_x // tamanio_horizontal)
            objeto_4_y_pos_matriz_cuadriculada = int(objeto_4_y // tamanio_vertical)

            print([objeto_1_x_pos_matriz_cuadriculada],
                  [objeto_2_x_pos_matriz_cuadriculada],
                  [objeto_3_x_pos_matriz_cuadriculada],
                  [objeto_4_x_pos_matriz_cuadriculada])
            print([objeto_1_y_pos_matriz_cuadriculada],
                  [objeto_2_y_pos_matriz_cuadriculada],
                  [objeto_3_y_pos_matriz_cuadriculada],
                  [objeto_4_y_pos_matriz_cuadriculada])

            ax.bar3d(x_data,
                     y_data,
                     np.zeros(len(z_data)),
                     1, 1, z_data)

            if 0 < rot_grafica_3d <= 90:
                ax.xaxis._axinfo['juggled'] = (0, 0, 0)
                ax.yaxis._axinfo['juggled'] = (1, 1, 1)
                ax.zaxis._axinfo['juggled'] = (2, 2, 2)
            elif 90 < rot_grafica_3d <= 180:
                ax.xaxis._axinfo['juggled'] = (0, 0, 0)
                ax.yaxis._axinfo['juggled'] = (0, 1, 2)
                ax.zaxis._axinfo['juggled'] = (0, 2, 1)
            elif 180 < rot_grafica_3d <= 270:
                ax.xaxis._axinfo['juggled'] = (1, 0, 2)
                ax.yaxis._axinfo['juggled'] = (0, 1, 2)
                ax.zaxis._axinfo['juggled'] = (2, 2, 2)
            elif 270 < rot_grafica_3d <= 360:
                ax.xaxis._axinfo['juggled'] = (1, 0, 2)
                ax.yaxis._axinfo['juggled'] = (1, 1, 1)
                ax.zaxis._axinfo['juggled'] = (1, 2, 0)

            ax.view_init(azim=rot_grafica_3d)

        elif nombre_grafica == 'region_cuadricula_3d_solo_regiones_no_preferidas':

            print("Entro a regionCuadricula3d, solo regiones no preferidas")

            regiones_preferidas = config_grafica.regiones_preferidas_3d
            print("Regiones preferidas: ", regiones_preferidas)
            total_regiones = list(range(0, self.cantidad_columnas * self.cantidad_filas))
            regiones_no_preferidas = m_reg_pref.obtener_complemento_de_sublista(lista=total_regiones,
                                                                                sublista=regiones_preferidas)
            print("Regiones no preferidas: ", regiones_no_preferidas)

            self.matriz_cuadriculada_solo_regiones_no_preferidas = \
                m_reg_pref.obtener_submatriz_indices_dados(np.flipud(self.matriz_cuadriculada),
                                                           regiones_no_preferidas)
            self.matriz_cuadriculada_solo_regiones_no_preferidas = \
                np.flipud(self.matriz_cuadriculada_solo_regiones_no_preferidas)

            rot_grafica_3d = config_grafica.rot_grafica_3d

            objeto_1_x = self.objeto_relevante_1[0]
            objeto_1_y = self.objeto_relevante_1[1]

            objeto_2_x = self.objeto_relevante_2[0]
            objeto_2_y = self.objeto_relevante_2[1]

            objeto_3_x = self.objeto_relevante_3[0]
            objeto_3_y = self.objeto_relevante_3[1]

            objeto_4_x = self.objeto_relevante_4[0]
            objeto_4_y = self.objeto_relevante_4[1]

            if getattr(sys, 'frozen', False):
                os.environ['BASEMAPDATA'] = os.path.join(os.path.dirname(sys.executable), 'mplot3d')

            data_array = np.array(np.flipud(self.matriz_cuadriculada_solo_regiones_no_preferidas))

            print(data_array)

            ax = fig.add_subplot(111, projection='3d')

            ax.view_init(azim=rot_grafica_3d % 360, elev=0)

            x_data, y_data = np.meshgrid(np.arange(data_array.shape[1]),
                                         np.arange(data_array.shape[0]))

            x_data = x_data.flatten()
            y_data = y_data.flatten()
            z_data = data_array.flatten()

            tamanio_horizontal = self.dimension_caja[0] / self.cantidad_columnas
            tamanio_vertical = self.dimension_caja[1] / self.cantidad_filas

            objeto_1_x_pos_matriz_cuadriculada = int(objeto_1_x // tamanio_horizontal)
            objeto_1_y_pos_matriz_cuadriculada = int(objeto_1_y // tamanio_vertical)

            objeto_2_x_pos_matriz_cuadriculada = int(objeto_2_x // tamanio_horizontal)
            objeto_2_y_pos_matriz_cuadriculada = int(objeto_2_y // tamanio_vertical)

            objeto_3_x_pos_matriz_cuadriculada = int(objeto_3_x // tamanio_horizontal)
            objeto_3_y_pos_matriz_cuadriculada = int(objeto_3_y // tamanio_vertical)

            objeto_4_x_pos_matriz_cuadriculada = int(objeto_4_x // tamanio_horizontal)
            objeto_4_y_pos_matriz_cuadriculada = int(objeto_4_y // tamanio_vertical)

            print([objeto_1_x_pos_matriz_cuadriculada],
                  [objeto_2_x_pos_matriz_cuadriculada],
                  [objeto_3_x_pos_matriz_cuadriculada],
                  [objeto_4_x_pos_matriz_cuadriculada])
            print([objeto_1_y_pos_matriz_cuadriculada],
                  [objeto_2_y_pos_matriz_cuadriculada],
                  [objeto_3_y_pos_matriz_cuadriculada],
                  [objeto_4_y_pos_matriz_cuadriculada])

            ax.bar3d(x_data,
                     y_data,
                     np.zeros(len(z_data)),
                     1, 1, z_data)

            if 0 < rot_grafica_3d <= 90:
                ax.xaxis._axinfo['juggled'] = (0, 0, 0)
                ax.yaxis._axinfo['juggled'] = (1, 1, 1)
                ax.zaxis._axinfo['juggled'] = (2, 2, 2)
            elif 90 < rot_grafica_3d <= 180:
                ax.xaxis._axinfo['juggled'] = (0, 0, 0)
                ax.yaxis._axinfo['juggled'] = (0, 1, 2)
                ax.zaxis._axinfo['juggled'] = (0, 2, 1)
            elif 180 < rot_grafica_3d <= 270:
                ax.xaxis._axinfo['juggled'] = (1, 0, 2)
                ax.yaxis._axinfo['juggled'] = (0, 1, 2)
                ax.zaxis._axinfo['juggled'] = (2, 2, 2)
            elif 270 < rot_grafica_3d <= 360:
                ax.xaxis._axinfo['juggled'] = (1, 0, 2)
                ax.yaxis._axinfo['juggled'] = (1, 1, 1)
                ax.zaxis._axinfo['juggled'] = (1, 2, 0)

            ax.view_init(azim=rot_grafica_3d)

        return fig
