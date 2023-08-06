import pandas as pd
import numpy as np

def calcular(input, orden):
    """
    El input es un dataframe: recorridos de cada usuario, terminan en conversion o no.
    El output es la cantidad de conversiones atribuidas a cada canal en los recorridos.
    """
    # crear una copia para no alterar la data original
    data = input.copy()

    # pasar a lista para hacer mas eficiente
    lista = data.values.tolist()

    # calcular conversiones totales
    conversiones_totales = sum([camino[1] for camino in lista])

    # obtener la matriz de transicion de los canales
    matriz = calcular_matriz_transicion(lista)

    # obtener el diciconario del removal effect de cada canal
    proporcion = calcular_removal_effect(matriz)

    # si el orden es mayor a 1, distribuir el resultado
    if orden>1:
        distribuido = {}
        # distribuir linealmente en cada combinacion de canales
        for k,v in proporcion.items():
            for canal in (k.split(">")):
                distribuido[canal] = distribuido.get(canal,0) + v/len(k.split(">"))
                proporcion = distribuido

    # aplicar conversiones a proporcion
    atribucion = {k:round(v*conversiones_totales,2) for k,v in proporcion.items()}

    return atribucion

def calcular_matriz_transicion(data):
    '''
    Agregar el estado inicial (start) y los estados absorbentes (conversion), (null).
    Calcula la matriz como la probabilidad de transicion entre dos estados.
    Agrega las columnas necesarias para obtener una matriz cuadrada.
    '''
    # agregar start y conversion o null segun corresponda
    recorridos = [['(start)'] + camino[0] + ['(null)'] if camino[1]==0 else ['(start)'] + camino[0] + ['(conversion)'] for camino in data]

    # obtener las transiciones entre pares de estados
    transiciones = [list(transicion) for camino in recorridos for transicion in zip(camino[:],camino[1:])]

    # dar formato de tabla
    df = pd.DataFrame(transiciones,columns=['(start)','(end)'])

    # crear matriz de transicion
    matriz = pd.crosstab(index=df['(start)'], columns=df['(end)'], normalize = 'index', dropna = False)

    # validar si estan todas las columnas
    for columna in ['(conversion)','(null)']:
        if columna not in matriz.columns:
            matriz.insert(0,columna,np.zeros(matriz.shape[0]))

    # agregar start como estado final para lograr matriz cuadrada
    matriz.insert(0,'(start)',np.zeros(matriz.shape[0]))

    return matriz

def calcular_markov(data):
    '''
    Toma una matriz de transiciones entre los canales (con null, start y conversion).
    Devuelve la tasa de conversion partienda del estado start.
    '''
    # armar matriz de convergencia (columnas finales)
    matriz_convergencia = data[['(null)','(conversion)']]
    
    # armar matriz de canales (filas de canales)
    matriz_canales = data.drop(['(conversion)','(null)'],axis=1)
    
    # calcular la inversa de (I - canales)
    matriz_inversa = np.linalg.inv(np.identity(len(matriz_canales.columns)) - np.asarray(matriz_canales))
    
    # calcular producto matricial de la inversa y la de convergencia
    matriz_probabilidades = np.dot(matriz_inversa, np.asarray(matriz_convergencia))
    
    # devolver la probabilidad de conversion del inicio en start
    cvr = pd.DataFrame(matriz_probabilidades,index=matriz_convergencia.index)[[1]].loc['(start)'].values[0]

    return cvr

def calcular_removal_effect(data):
    '''
    Toma una matriz de transiciones entre los canales (con null, start y conversion) y calcula el removal effect
    de cada uno de los canales.
    
    Para eso, itera sobre los canales (sin start, conversion y null) y calcula la tasa de conversion general. 
    Luego, borra la fila del canal, asigna sus probabilidades de transicion a null y recalcula la
    tasa de conversion.
    
    Devuelve la proporcion normalizada en que disminuye la tasa de conversion original.
    
    '''
    # calcular conversion general y guardar
    cr_general = calcular_markov(data)

    # crear un diccionario para almacenar removal effect de cada canal
    removal_effect = {}
    
    # iterar sobre canales validos
    for canal in data.columns:
        if canal not in ['(start)','(conversion)','(null)']:

            # borrar linea y columna del canal
            matriz_canal = data.drop(canal, axis=1).drop(canal, axis=0)
            
            # reasignar probabilidad a nulo
            for column in matriz_canal.columns:
                if column not in ['(conversion)','(null)']:
                    faltante = float(1) - np.sum(list(matriz_canal.loc[column]))
                    if faltante != 0:
                        matriz_canal.loc[column]['(null)'] += faltante

            # calcular la conversion
            cr_canal = calcular_markov(matriz_canal)

            # calcular la variacion de la conversion
            removal_effect_canal = 1 - (cr_canal / cr_general)

            # maximizar con 0 y guardar en diccionario
            removal_effect[canal] = max(removal_effect_canal,0)

    # calcular valor total
    suma = np.sum(list(removal_effect.values()))
    
    # normalizar
    removal_effect_normalizado = {key: (value / suma) for key, value in removal_effect.items()}

    # devolver diccionario
    return removal_effect_normalizado
