from motus.experimento import Experimento
import motus.entropia_divergencia.entropia_divergencia as m_ed
import motus.regresion_lineal.distancias_pendientes as m_dp
from matplotlib.figure import Figure


class MultiplesExperimentos:

    def __init__(self,
                 lista_archivos,
                 dimension_caja=None,
                 cantidad_filas=10,
                 cantidad_columnas=10,
                 procesar_tiempo_archivo_irregular=False,
                 puntos_importantes=None,
                 objeto_a_promediar=1,
                 tamanio_intervalo_para_promedio=100,
                 epsilon_distancias_pendientes=1):
        self.lista_archivos = lista_archivos
        self.lista_experimentos = list()
        self.resultados_entropia = dict()
        self.resultados_divergencia = dict()
        self.pendientes_regresion_lineal = dict()
        self.resultados_pendientes_regresion_lineal = dict()

        if dimension_caja is None:
            self.dimension_caja = [100, 100]

        self.dimension_caja = dimension_caja
        self.cantidad_filas = cantidad_filas
        self.cantidad_columnas = cantidad_columnas
        self.procesar_tiempo_archivo_irregular = procesar_tiempo_archivo_irregular
        self.puntos_importantes = puntos_importantes
        self.objeto_a_promediar = objeto_a_promediar
        self.tamanio_intervalo_para_promedio = tamanio_intervalo_para_promedio
        self.epsilon_distancias_pendientes = epsilon_distancias_pendientes

    def inicializa_experimentos(self):

        print("Procesar tiempo irregular: ", self.procesar_tiempo_archivo_irregular)
        if isinstance(self.lista_archivos, dict):

            count = 0

            print("Diccionario de archivos: ", self.lista_archivos)

            for (nombre, valor) in self.lista_archivos.items():
                if valor.get() is True:
                    count += 1
                    print("conteo de experimentos: ", count)
                    nuevo_experimento = Experimento(str(nombre),
                                                    dimension_caja=self.dimension_caja,
                                                    cantidad_filas=self.cantidad_filas,
                                                    cantidad_columnas=self.cantidad_columnas,
                                                    procesar_tiempo_archivo_irregular=
                                                    self.procesar_tiempo_archivo_irregular,
                                                    puntos_importantes=self.puntos_importantes)

                    self.lista_experimentos.append(nuevo_experimento)
        else:
            for archivo in self.lista_archivos:
                nuevo_experimento = Experimento(archivo,
                                                dimension_caja=self.dimension_caja,
                                                cantidad_filas=self.cantidad_filas,
                                                cantidad_columnas=self.cantidad_columnas,
                                                procesar_tiempo_archivo_irregular=
                                                self.procesar_tiempo_archivo_irregular,
                                                )
                self.lista_experimentos.append(nuevo_experimento)

    def calcula_velocidades_multiples_experimentos(self):
        for experimento in self.lista_experimentos:
            experimento.calcula_velocidades()

    def calcula_regiones_cuadriculadas(self, arreglo_regiones_preferidas):
        for experimento in self.lista_experimentos:
            experimento.calcula_regiones_cuadriculadas()
            experimento.calcula_matrices_solo_regiones_preferidas(regiones_preferidas=arreglo_regiones_preferidas)

    def calcula_entropias_divergencias(self,
                                       tamanio_vectores=2,
                                       umbral=3,
                                       sobreposicion=True):
        for experimento in self.lista_experimentos:
            experimento.calcula_entropias(tamanio_vectores, umbral, sobreposicion)

    def calcula_regresiones_lineales(self, brinco_temporal, longitud_ventana_tiempo):
        for experimento in self.lista_experimentos:
            for tipo_arreglo in ["Velocidad", "Aceleracion"]:
                arreglo_seleccionado = experimento.regresa_tipo_arreglo(tipo_arreglo)

                procesador = experimento.procesador_regresion_lineal
                procesador.arreglo_a_procesar = arreglo_seleccionado
                procesador.brinco_temporal = brinco_temporal
                procesador.longitud_ventana_tiempo = longitud_ventana_tiempo

                procesador.realiza_procesamiento()
                procesador.agrega_categoria_regresion_lineal(experimento.regresiones_lineales,
                                                             tipo_arreglo)

    def procesa_pendientes(self):
        experimento_inicial = self.lista_experimentos[0]

        for tipo_regresion_lineal in sorted(experimento_inicial.regresiones_lineales):
            lista_pendientes = []
            for experimento in self.lista_experimentos:
                diccionario_regresion_lineal_experimento = experimento.regresiones_lineales[tipo_regresion_lineal]
                pendiente_experimento = diccionario_regresion_lineal_experimento["pendientes"]
                lista_pendientes.append(pendiente_experimento)
            self.pendientes_regresion_lineal[tipo_regresion_lineal] = lista_pendientes

    def procesa_distancias_pendientes(self, epsilon):
        print("-------------------------------------------------------------------------------")
        for tipo_regresion_lineal in sorted(self.pendientes_regresion_lineal):
            print("Regresion lineal a procesar distancias pendientes: ", tipo_regresion_lineal)
            lista_pendientes = self.pendientes_regresion_lineal[tipo_regresion_lineal]
            print("Lista de pendientes para", tipo_regresion_lineal, ": ", lista_pendientes)
            resultados_pendientes_funcion_signo = m_dp.procesa_lista_pendientes_funcion_signo(lista_pendientes,
                                                                                              epsilon)
            resultados_distancias = m_dp.calcula_distancias_para_lista_pendientes(resultados_pendientes_funcion_signo)
            self.resultados_pendientes_regresion_lineal[tipo_regresion_lineal] = resultados_distancias

    def procesa_diccionario_entropias(self):
        """
        Se lee uno de los diccionarios de entropia para conocer sus llaves. Por cada llave, se obtienen todos
        los datos correspondientes a esa entropia para cada experimento. La lista resultante se guarda en un
        diccionario, donde la llave es el tipo de entropia y el registro es la lista con los valores encontrados.

        El resultado es un diccionario con todas las entropias registradas, y listas con los valores de
        cada experimento
        """

        experimento_inicial = self.lista_experimentos[0]

        for tipo_entropia in sorted(experimento_inicial.entropias):
            valores_entropia = []
            for experimento in self.lista_experimentos:
                valor_entropia_experimento = experimento.entropias[tipo_entropia]
                valores_entropia.append(valor_entropia_experimento)
            self.resultados_entropia[tipo_entropia] = valores_entropia

    def procesa_diccionario_divergencias(self):
        lista_arreglos_regiones = list()
        lista_arreglos_solo_regiones_preferidas = list()
        lista_arreglos_solo_regiones_no_preferidas = list()
        for experimento in self.lista_experimentos:
            lista_arreglos_regiones.append(
                experimento.matriz_cuadriculada.flatten())
            lista_arreglos_solo_regiones_preferidas.append(
                experimento.matriz_cuadriculada_solo_regiones_preferidas.flatten())
            lista_arreglos_solo_regiones_no_preferidas.append(
                experimento.matriz_cuadriculada_solo_regiones_no_preferidas.flatten())
        self.calcula_divergencia("visitas_regiones", lista_arreglos_regiones)
        self.calcula_divergencia("visitas_regiones_preferidas", lista_arreglos_solo_regiones_preferidas)
        self.calcula_divergencia("visitas_regiones_no_preferidas", lista_arreglos_solo_regiones_no_preferidas)

    def calcula_divergencia(self, tipo_divergencia, lista_datos):
        lista_divergencia = m_ed.calcula_divergencias_de_lista_arreglos(lista_datos)
        self.resultados_divergencia[tipo_divergencia] = lista_divergencia

    def regresa_imagen_grafica(self, grafica):
        print("-----------------------------------------------")
        print("Grafica deseada:", grafica)

        fig = Figure(figsize=(6, 6))
        fig_plot = fig.add_subplot(111)
        fig_plot.grid(True)

        cantidad_experimentos = len(self.lista_experimentos)

        if grafica is 'entropia_visitas_regiones':
            fig_plot.plot(range(1, cantidad_experimentos+1),
                          self.resultados_entropia["visitas_regiones"], 'o')
            fig_plot.plot(range(1, cantidad_experimentos+1),
                          self.resultados_entropia["visitas_regiones"])

        if grafica is 'entropia_aprox_visitas_regiones':
            fig_plot.plot(range(1, cantidad_experimentos+1),
                          self.resultados_entropia["visitas_regiones_aprox"], 'o')
            fig_plot.plot(range(1, cantidad_experimentos+1),
                          self.resultados_entropia["visitas_regiones_aprox"])

        elif grafica is 'entropia_visitas_regiones_preferidas':
            fig_plot.plot(range(1, cantidad_experimentos+1),
                          self.resultados_entropia["visitas_regiones_preferidas"], 'o')
            fig_plot.plot(range(1, cantidad_experimentos+1),
                          self.resultados_entropia["visitas_regiones_preferidas"])

        elif grafica is 'entropia_visitas_regiones_no_preferidas':
            fig_plot.plot(range(1, cantidad_experimentos+1),
                          self.resultados_entropia["visitas_regiones_no_preferidas"], 'o')
            fig_plot.plot(range(1, cantidad_experimentos+1),
                          self.resultados_entropia["visitas_regiones_no_preferidas"])

        elif grafica is 'entropia_hist_velocidad':
            fig_plot.plot(range(1, cantidad_experimentos+1),
                          self.resultados_entropia["histograma_velocidad"], 'o')
            fig_plot.plot(range(1, cantidad_experimentos+1),
                          self.resultados_entropia["histograma_velocidad"])

        elif grafica is 'divergencia_regiones':
            fig_plot.plot(range(1, cantidad_experimentos),
                          self.resultados_divergencia["visitas_regiones"], 'o')
            fig_plot.plot(range(1, cantidad_experimentos),
                          self.resultados_divergencia["visitas_regiones"])

        elif grafica is 'divergencia_regiones_preferidas':
            fig_plot.plot(range(1, cantidad_experimentos),
                          self.resultados_divergencia["visitas_regiones_preferidas"], 'o')
            fig_plot.plot(range(1, cantidad_experimentos),
                          self.resultados_divergencia["visitas_regiones_preferidas"])

        elif grafica is 'divergencia_regiones_no_preferidas':
            fig_plot.plot(range(1, cantidad_experimentos),
                          self.resultados_divergencia["visitas_regiones_no_preferidas"], 'o')
            fig_plot.plot(range(1, cantidad_experimentos),
                          self.resultados_divergencia["visitas_regiones_no_preferidas"])

        elif grafica is 'pendientes_distancias_velocidad':
            fig_plot.plot(range(1, cantidad_experimentos),
                          self.resultados_pendientes_regresion_lineal['Velocidad'], 'o')
            fig_plot.plot(range(1, cantidad_experimentos),
                          self.resultados_pendientes_regresion_lineal['Velocidad'])

        elif grafica is 'pendientes_distancias_aceleracion':
            fig_plot.plot(range(1, cantidad_experimentos),
                          self.resultados_pendientes_regresion_lineal['Aceleracion'], 'o')
            fig_plot.plot(range(1, cantidad_experimentos),
                          self.resultados_pendientes_regresion_lineal['Aceleracion'])

        return fig
