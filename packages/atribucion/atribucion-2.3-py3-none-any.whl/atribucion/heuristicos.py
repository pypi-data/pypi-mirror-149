from collections import Counter

def calcular_first_click(data):
    """ Calcula el modelo first click, atribuyendo la conversion al primer canal del recorrido."""

    # tomar solo el primer canal de cada conversion
    first_channel = [camino[0][0] for camino in data.values if camino[1]!=0]
    
    # contar conversiones de cada canal
    results = dict(Counter(first_channel))
    
    return results

def calcular_last_click(data):
    """ Calcula el modelo last click, atribuyendo la conversion al ultimo canal del recorrido."""

    # tomar solo el ultimo canal de cada conversion
    last_channel = [camino[0][-1] for camino in data.values if camino[1]!=0]

    # contar conversiones de cada canal
    results = dict(Counter(last_channel))

    return results

def calcular_linear(data):
    """Calcula el modelo linear, atribuyendo la conversion proporcionalmente a todos los canales del recorrido."""
    
    results = {}
    
    for camino in data.values:
        # si el camino termina en conversion
        if camino[1] != 0:
            # distribuir linealmente la conversion
            for canal in camino[0]:
                results[canal] = results.get(canal,0) + camino[1]/len(camino[0])
    
    results = {k:round(v,2) for k,v in results.items()}

    return results
    