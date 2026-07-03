import math

def distancia_euclidiana(a, b):
    dx = a[0] - b[0]
    dy = a[1] - b[1]
    return math.floor(math.sqrt(dx * dx + dy * dy))


def distancia_manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


HEURISTICAS = {
    "DE": distancia_euclidiana,
    "DM": distancia_manhattan,
}


def com_fator(heuristica, fator):
    return lambda a, b: fator * heuristica(a, b)
