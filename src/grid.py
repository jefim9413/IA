import random
from collections import deque

TAMANHO_PADRAO = 15
PESO_MIN, PESO_MAX = 3, 6
BLOQUEADO = -1

DIRECOES_NLSO = [
    ("N", (0, -1)),
    ("L", (1, 0)),
    ("S", (0, 1)),
    ("O", (-1, 0)),
]


def gerar_matriz_pesos(tamanho=TAMANHO_PADRAO, rng=None):
    rng = rng or random
    return [[rng.randint(PESO_MIN, PESO_MAX) for _ in range(tamanho)] for _ in range(tamanho)]


def aplicar_obstaculos(matriz, percentual_obstaculos, origem, destino, rng=None):
    rng = rng or random
    tamanho = len(matriz)
    celulas_livres = [
        (x, y)
        for y in range(tamanho)
        for x in range(tamanho)
        if (x, y) not in (origem, destino)
    ]
    quantidade = round(percentual_obstaculos * tamanho * tamanho)
    quantidade = min(quantidade, len(celulas_livres))
    for x, y in rng.sample(celulas_livres, quantidade):
        matriz[y][x] = BLOQUEADO
    return matriz


def dentro_dos_limites(pos, tamanho):
    x, y = pos
    return 0 <= x < tamanho and 0 <= y < tamanho


def vizinhos(pos, matriz, ordem=DIRECOES_NLSO):
    x, y = pos
    tamanho = len(matriz)
    resultado = []
    for direcao, (dx, dy) in ordem:
        nx, ny = x + dx, y + dy
        if 0 <= nx < tamanho and 0 <= ny < tamanho and matriz[ny][nx] != BLOQUEADO:
            resultado.append((direcao, (nx, ny)))
    return resultado


def custo_celula(matriz, pos):
    x, y = pos
    return matriz[y][x]


def esta_conectado(matriz, origem, destino):
    if origem == destino:
        return True
    fila = deque([origem])
    visitados = {origem}
    while fila:
        atual = fila.popleft()
        for _, viz in vizinhos(atual, matriz):
            if viz == destino:
                return True
            if viz not in visitados:
                visitados.add(viz)
                fila.append(viz)
    return False


def gerar_instancia(codigo, tamanho=TAMANHO_PADRAO, percentual_obstaculos=0.0, rng=None, max_tentativas=500):
    rng = rng or random
    for _ in range(max_tentativas):
        matriz = gerar_matriz_pesos(tamanho, rng)
        origem = (rng.randrange(tamanho), rng.randrange(tamanho))
        destino = (rng.randrange(tamanho), rng.randrange(tamanho))
        if origem == destino:
            continue
        if percentual_obstaculos > 0:
            aplicar_obstaculos(matriz, percentual_obstaculos, origem, destino, rng)
        if esta_conectado(matriz, origem, destino):
            return {
                "codigo": codigo,
                "tamanho": tamanho,
                "percentual_obstaculos": percentual_obstaculos,
                "origem": origem,
                "destino": destino,
                "matriz": matriz,
            }
    raise RuntimeError(
        f"Não foi possível gerar instância conectada para '{codigo}' após {max_tentativas} tentativas"
    )


def gerar_conjunto_instancias(prefixo, quantidade, percentual_obstaculos, semente, tamanho=TAMANHO_PADRAO):
    rng = random.Random(semente)
    instancias = []
    for i in range(quantidade):
        codigo = f"{prefixo}_{i:02d}"
        instancias.append(gerar_instancia(codigo, tamanho, percentual_obstaculos, rng))
    return instancias
