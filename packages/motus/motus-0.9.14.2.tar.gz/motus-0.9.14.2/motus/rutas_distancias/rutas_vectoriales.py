class InformacionRutasVectoriales:
    def __init__(self, posiciones_eje_x=None, posiciones_eje_y=None,
                 tamanio_vectorial=None, brinco_temporal=None,
                 indice_consecuencia=None):

        self.posiciones_eje_x = posiciones_eje_x
        self.posiciones_eje_y = posiciones_eje_y
        self.tamanio_vectorial = tamanio_vectorial
        self.brinco_temporal = brinco_temporal
        self.indice_consecuencia = indice_consecuencia

        self.posiciones_x_antes_consecuencia = None
        self.posiciones_y_antes_consecuencia = None

        self.posiciones_x_antes_consecuencia_con_consecuencia = None
        self.posiciones_y_antes_consecuencia_con_consecuencia = None

        self.posiciones_x_despues_consecuencia = None
        self.posiciones_y_despues_consecuencia = None

        self.direcciones_x_antes_consecuencia = None
        self.direcciones_y_antes_consecuencia = None
        self.direcciones_x_despues_consecuencia = None
        self.direcciones_y_despues_consecuencia = None

    def procesar_informacion_vectorial(self):
        self.obtener_posiciones_vectores()

        self.obtener_direcciones_vectores()


    def obtener_posiciones_vectores(self):
        self.posiciones_x_antes_consecuencia, self.posiciones_x_despues_consecuencia = \
            obtener_posiciones_correspondientes_direccion_eje(self.posiciones_eje_x,
                                                              self.indice_consecuencia,
                                                              self.tamanio_vectorial,
                                                              self.brinco_temporal)

        self.posiciones_y_antes_consecuencia, self.posiciones_y_despues_consecuencia = \
            obtener_posiciones_correspondientes_direccion_eje(self.posiciones_eje_y,
                                                              self.indice_consecuencia,
                                                              self.tamanio_vectorial,
                                                              self.brinco_temporal)

        self.posiciones_x_antes_consecuencia_con_consecuencia = self.posiciones_x_antes_consecuencia.copy()
        self.posiciones_x_antes_consecuencia_con_consecuencia.append(self.posiciones_eje_x[self.indice_consecuencia])

        self.posiciones_y_antes_consecuencia_con_consecuencia =  self.posiciones_y_antes_consecuencia.copy()
        self.posiciones_y_antes_consecuencia_con_consecuencia.append(self.posiciones_eje_y[self.indice_consecuencia])

    def obtener_direcciones_vectores(self):
        self.direcciones_x_antes_consecuencia, self.direcciones_y_antes_consecuencia = \
            obtener_vectores_posicion_flechas(self.posiciones_x_antes_consecuencia_con_consecuencia,
                                              self.posiciones_y_antes_consecuencia_con_consecuencia)

        self.direcciones_x_despues_consecuencia, self.direcciones_y_despues_consecuencia =\
            obtener_vectores_posicion_flechas(self.posiciones_x_despues_consecuencia,
                                              self.posiciones_y_despues_consecuencia)

    def regresa_posiciones_direcciones(self):
        arreglo_posiciones_x = [self.posiciones_x_antes_consecuencia,
                                self.posiciones_x_despues_consecuencia]

        arreglo_posiciones_y = [self.posiciones_y_antes_consecuencia,
                                self.posiciones_y_despues_consecuencia]

        arreglo_direcciones_x = [self.direcciones_x_antes_consecuencia,
                                 self.direcciones_x_despues_consecuencia]

        arreglo_direcciones_y = [self.direcciones_y_antes_consecuencia,
                                 self.direcciones_y_despues_consecuencia]

        return arreglo_posiciones_x, arreglo_posiciones_y, \
               arreglo_direcciones_x, arreglo_direcciones_y


def obtener_vectores_posicion_flechas(vector_x, vector_y):
    x_direct = []
    y_direct = []

    for i in range(0, len(vector_x) - 1):
        x1 = vector_x[i]
        x2 = vector_x[i + 1]
        y1 = vector_y[i]
        y2 = vector_y[i + 1]
        x_punta, y_punta = obtener_punta_vector(x1, x2, y1, y2)
        x_direct.append(x_punta)
        y_direct.append(y_punta)

    return x_direct, y_direct


def obtener_punta_vector(x_1, x_2, y_1, y_2):
    return x_2 - x_1, y_2 - y_1


def obtener_posiciones_correspondientes_direccion_eje(posiciones_eje_correspondiente,
                                                      consecuencia_elegida,
                                                      tamanio_vectores,
                                                      brinco_temporal):

    pos_antes_consecuencia = posiciones_eje_correspondiente.tolist()

    pos_antes_consecuencia = pos_antes_consecuencia[int(consecuencia_elegida - tamanio_vectores):
                                                    int(consecuencia_elegida):
                                                    int(brinco_temporal)]

    pos_despues_consecuencia = posiciones_eje_correspondiente.tolist()

    pos_despues_consecuencia = pos_despues_consecuencia[int(consecuencia_elegida):
                                                        int(consecuencia_elegida + tamanio_vectores):
                                                        int(brinco_temporal)]

    return pos_antes_consecuencia, pos_despues_consecuencia
