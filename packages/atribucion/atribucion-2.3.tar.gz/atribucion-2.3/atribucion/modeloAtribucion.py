from . import markov, shapley, heuristicos

class Modelo():
    """
    Datos para formatear y calcular modelos.
    
    :param data: data con la cual crear los modelos.
    :type data: dataframe or list
    :param formateada: si la data tiene una columna con una lista o array de recorridos y otra con la conversion.
    :type formateada: bool
    """
    def __init__(self, data, formateada=True):
        self.data = data
        self.formateada = formateada

        return None

    def formatear_markov(self, ventana, touchpoints, conversion):
        """
        Formatea la data para Markov: recorridos con y sin conversion, canales duplicados.

        :param ventana: La cantidad de dias que se toman antes de cada conversion.
        :type ventana: int
        :param touchpoints: La cantidad de canales maxima que se toma por cada conversion.
        :type touchpoints: int
        :param conversion: Si se corta el camino con cada nueva conversion.
        :type conversion: bool

        """
        print("Proceso de formateo")

        self.data_markov = self.data
        
        return

    def markov(self, orden=1):
        """
        Si la data esta formateada o se formateo con la funcion, calcula el modelo de Markov.
        
        :param orden: El orden del modelo de Markov, entre 1 y 4.
        :type orden: int
        """
        # si esta formateada, asignarla
        if self.formateada == True:
            self.data_markov = self.data

        # si no hay data para markov, arrojar error
        try:
            self.data_markov
        except:
            print("La data no está formateada. Usar la función formatear_markov o pasar data ya formateada.")

        # calcular el modelo de markov
        resultado = markov.calcular(self.data_markov, orden)

        return resultado

    def formatear_shapley(self, ventana=30, touchpoints=8):
        """
        Formatea la data para Shapley: recorridos con conversion, sin canales duplicados.

        :param ventana: La cantidad de dias que se toman antes de cada conversion.
        :type ventana: int
        :param touchpoints: La cantidad de canales maxima que se toma por cada conversion.
        :type touchpoints: int        
        """
        print("Proceso de formateo")

        self.data_shapley = self.data

        return

    def shapley(self):
        """
        Si la data esta formateada o se formateo con la funcion, calcula el modelo de Shapley.
        """
        # si esta formateada, asignarla
        if self.formateada == True:
            self.data_shapley = self.data

        # si no hay data para markov, arrojar error
        try:
            self.data_shapley
        except:
            print("La data no está formateada. Usar la función formatear_shapley o pasar data ya formateada.")

        # calcular el modelo de markov
        resultado = shapley.calcular(self.data_shapley)

        return resultado

    def first(self):
        """
        Usa la data ya formateada para Markov o Shapley y crea un modelo First Click.
        """
        # usar la data ya formateada para Markov o Shapley
        if hasattr(self, "data_shapley"):
            resultado = heuristicos.calcular_first_click(self.data_shapley)
            return resultado
        elif hasattr(self, "data_markov"):
            resultado = heuristicos.calcular_first_click(self.data_markov)
            return resultado
        # o la data ya formateada
        else:
            if self.formateada == True:
                resultado = heuristicos.calcular_first_click(self.data)
                return resultado
            else:
                raise Exception("Hace falta formatear los datos")
    
    def last(self):
        """
        Usa la data ya formateada para Markov o Shapley y crea un modelo Last Click.
        """
        # usar la data ya formateada para Markov o Shapley
        if hasattr(self, "data_shapley"):
            resultado = heuristicos.calcular_last_click(self.data_shapley)
            return resultado
        elif hasattr(self, "data_markov"):
            resultado = heuristicos.calcular_last_click(self.data_markov)
            return resultado
        # o la data ya formateada
        else:
            if self.formateada == True:
                resultado = heuristicos.calcular_last_click(self.data)
                return resultado
            else:
                raise Exception("Hace falta formatear los datos")

    def linear(self):
        """
        Usa la data ya formateada para Markov o Shapley y crea un modelo Linear.
        """
        # usar la data ya formateada para Markov o Shapley
        if hasattr(self, "data_shapley"):
            resultado = heuristicos.calcular_linear(self.data_shapley)
            return resultado
        elif hasattr(self, "data_markov"):
            resultado = heuristicos.calcular_linear(self.data_markov)
            return resultado
        else:
            if self.formateada == True:
                resultado = heuristicos.calcular_linear(self.data)
                return resultado
            else:
                raise Exception("Hace falta formatear los datos")

    def comparacion(self):
        pass


