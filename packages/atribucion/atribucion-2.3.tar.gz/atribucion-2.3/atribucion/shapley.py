from itertools import combinations, permutations
from collections import Counter

def calcular(input):
    '''
    El input es una lista con una lista de recorridos a la conversion.
    El output es la cantidad de conversiones atribuidas a cada canal en los recorridos.
    '''
    # crear una copia para no alterar la data
    data = input.copy()

    # pasar a lista
    data = data.values.tolist()
    
    # chequear si estan filtrados los caminos sin conversion y canales duplicados
    data = [[list(sorted(set(recorrido[0]))), recorrido[1]] for recorrido in data if recorrido[1]!=0]

    # calcular conversiones totales
    conversiones_totales = sum([recorrido[1] for recorrido in data])

    # armar lista de canales unicos y sus combinaciones
    canales_unicos = sorted(set([canal for recorrido in data for canal in recorrido[0]]))
    canales_combinados = combinar(canales_unicos)

    # crear diccionario con todas las subcoaliciones
    sub_coaliciones = {camino:0 for camino in canales_combinados}

    # calcular la gran coalicion y todas sus permutaciones
    gran_coalicion = list(permutations(canales_unicos))

    # obtener los canales unicos de cada recorrido ordenados
    recorridos = [tuple(recorrido[0]) for recorrido in data]

    # contar ocurrencias de cada sub coalicion
    sub_coaliciones.update(Counter(recorridos))

    # calcular el valor de shapley para cada canal
    shapley = valor_shapley(gran_coalicion, sub_coaliciones)

    # aplicar conversiones totales al valor de shapley
    atribucion = {k:round(v*conversiones_totales,2) for k,v in shapley.items()}

    return atribucion

def combinar(lista):
    '''
    Pasando una lista de elementos, devuelve una lista con la combinatoria de los elementos, ordenados y no repetidos.
    '''    
    # calcular el numero de elementos en la lista
    numero_de_elementos = len(lista)
    
    # crear un rango inclusivo de 1 al numero de elementos
    rango = range(1,numero_de_elementos+1)
    
    # hacer la combinatoria de los elementos para cada valor del rango
    combinacion = [list(combinations(lista,i)) for i in rango]
    
    # desanidar las listas
    resultado = [tupla for sublista in combinacion for tupla in sublista]
    
    return resultado

def valor_shapley(gran_coalicion, sub_coaliciones):
    '''
    Calcula el valor de Shapley maximizando por 0 para cada fila
    '''
    conversiones = {}

    # para cada permutacion de la gran coalicion
    for permutacion in gran_coalicion:
        suma = 0
        # calcular en orden para cada canal en la sub coalicion
        for orden,canal in enumerate(permutacion):
            # maximizar con 0 para la fila
            valor = max(sub_coaliciones[tuple(sorted(permutacion[0:orden+1]))] - suma,0)
            # obtener la diferencia con el valor acumulado
            if valor > 0:
                conversiones[canal] = conversiones.get(canal, 0) + valor
                suma += valor

    # devolver el valor normalizado para cada canal
    proporcion = {k:v/sum(conversiones.values()) for k,v in conversiones.items()}

    return proporcion
