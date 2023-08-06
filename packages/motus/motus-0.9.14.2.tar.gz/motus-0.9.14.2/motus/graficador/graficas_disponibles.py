class GraficasDisponibles:
    def __init__(self):
        self.graficas_disponibles = {
            "Normales": False,
            "Rutas/Distancias": False,
            "Consecuencias": False,
            "Velocidad/Aceleracion": False,
            "Figuras 3D": False,
            "Regresion lineal": False,
            "Regiones preferidas": False,
        }

        self.tipos_graficas = {
            "Normales": ["Ruta",
                         "Velocidad",
                         "Histograma de velocidad",
                         "Aceleracion",
                         "Histograma de aceleracion"],
            "Rutas/Distancias": ["Distancias a objetos relevantes",
                                 "Distancia promediada a objeto",
                                 "Distancia minima del organismo a objetos relevantes"],
            "Consecuencias": ["Ruta vectorizada con consecuencias"],
            "Velocidad/Aceleracion": ["Velocidad promediada", "Aceleracion promediada"],
            "Figuras 3D": ["Volumenes para posiciones cercanas a objetos"],
            "Regiones preferidas": ["Matriz de recurrencia",
                                    "Matriz de recurrencia combinada",
                                    "Tiempo acumulado en regiones",
                                    "Tiempo acumulado solo en regiones preferidas",
                                    "Tiempo acumulado solo en regiones no preferidas"],
            "Regresion lineal": ["Regresion lineal"]
        }

        self.lista_graficas = []

    def cambiar_estado_grafica_disponible(self, tipo_graficas, valor):
        self.graficas_disponibles[tipo_graficas] = valor

    def formar_lista_graficas_disponibles(self):
        lista_graficas = []
        for tipo_grafica in self.graficas_disponibles.keys():
            if self.graficas_disponibles[tipo_grafica] is True:
                graficas = self.tipos_graficas[tipo_grafica]
                lista_graficas.append(graficas)
        print("lista_graficas", lista_graficas)
        lista_resultante = []
        for lista in lista_graficas:
            for grafica in lista:
                lista_resultante.append(grafica)
        self.lista_graficas = lista_resultante



