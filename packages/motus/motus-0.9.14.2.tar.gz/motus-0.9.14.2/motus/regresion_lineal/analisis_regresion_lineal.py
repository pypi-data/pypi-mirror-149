from sklearn.linear_model import LinearRegression
import numpy as np


class ProcesamientoRegresionLineal:
    def __init__(self,
                 nombre_regresion=None,
                 arreglo_a_procesar=None,
                 brinco_temporal=None,
                 longitud_ventana_tiempo=None):
        self.nombre_regresion = nombre_regresion
        self.arreglo_a_procesar = arreglo_a_procesar
        self.brinco_temporal = brinco_temporal
        self.longitud_ventana_tiempo = longitud_ventana_tiempo
        self.indices_tiempo = None
        self.series_tiempo = None
        self.resultados_regresion_lineal = None
        self.pendientes_regresion_lineal = None

    def realiza_procesamiento(self):
        self.indices_tiempo, self.series_tiempo = \
            generar_series_tiempo(lista_a_procesar=self.arreglo_a_procesar,
                                  brinco_temporal=self.brinco_temporal,
                                  longitud_ventana_tiempo=self.longitud_ventana_tiempo)

        self.resultados_regresion_lineal = \
            generar_regresion_lineal_para_series_tiempo(indices_tiempo=self.indices_tiempo,
                                                        series_tiempo=self.series_tiempo)

        self.pendientes_regresion_lineal = \
            genera_pendientes_de_rectas_regresion_lineal(self.indices_tiempo,
                                                         self.resultados_regresion_lineal)

    def regresa_resultados_regresion_lineal(self):
        return self.indices_tiempo,\
               self.series_tiempo,\
               self.resultados_regresion_lineal,\
               self.pendientes_regresion_lineal

    def genera_diccionario_informacion_actual(self):
        diccionario_informacion = dict()
        indices, series, resultados, pendientes = self.regresa_resultados_regresion_lineal()
        diccionario_informacion["indices_tiempo"] = indices
        diccionario_informacion["series_tiempo"] = series
        diccionario_informacion["resultados"] = resultados
        diccionario_informacion["pendientes"] = pendientes
        return diccionario_informacion

    def agrega_categoria_regresion_lineal(self,
                                          diccionario_regresiones_lineales,
                                          nombre_tipo_regresion_lineal):
        nuevo_diccionario = self.genera_diccionario_informacion_actual()
        diccionario_regresiones_lineales[nombre_tipo_regresion_lineal] = nuevo_diccionario


def generar_series_tiempo(lista_a_procesar, brinco_temporal, longitud_ventana_tiempo):
    series_tiempo_resultantes = []
    indices_tiempo_resultantes = []
    for brinco in range(0, len(lista_a_procesar), brinco_temporal):
        nueva_serie = []
        nueva_lista_indices = []
        if brinco+longitud_ventana_tiempo < len(lista_a_procesar):
            for indice_lista in range(brinco, brinco+longitud_ventana_tiempo, +1):
                nueva_serie.append(lista_a_procesar[indice_lista])
                nueva_lista_indices.append(indice_lista)
            series_tiempo_resultantes.append(nueva_serie)
            indices_tiempo_resultantes.append(nueva_lista_indices)
    return np.array(indices_tiempo_resultantes), np.array(series_tiempo_resultantes)


def generar_regresion_lineal_para_series_tiempo(indices_tiempo, series_tiempo):
    lista_predicciones = []
    regresor_lineal = LinearRegression()
    for indice in range(0, len(indices_tiempo)):
        X = indices_tiempo[indice].reshape(-1, 1)
        Y = series_tiempo[indice].reshape(-1, 1)
        regresor_lineal.fit(X, Y)
        prediccion = regresor_lineal.predict(X)
        lista_predicciones.append(prediccion)
    return lista_predicciones


def genera_pendientes_de_rectas_regresion_lineal(valores_x_regresion_lineal,
                                                 valores_y_regresion_lineal):
    pendientes = []
    cantidad_listas = len(valores_y_regresion_lineal)
    for indice in range(0, cantidad_listas):
        valores_x = valores_x_regresion_lineal[indice]
        valores_y = valores_y_regresion_lineal[indice]
        delta_y = valores_y[-1] - valores_y[0]
        delta_x = valores_x[-1] - valores_x[0]
        pendiente_actual = delta_y/delta_x
        pendientes.append(pendiente_actual)
    return pendientes



