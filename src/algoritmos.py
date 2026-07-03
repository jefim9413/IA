import heapq
import random

from grid import vizinhos, custo_celula

def _soma_custo_caminho(matriz, caminho):
    return sum(custo_celula(matriz, p) for p in caminho[1:])


def _resultado(caminho, matriz, estados_gerados, estados_visitados, sucesso):
    if not sucesso:
        return {
            "caminho": caminho,
            "custo_total": None,
            "estados_gerados": estados_gerados,
            "estados_visitados": estados_visitados,
            "sucesso": False,
        }
    return {
        "caminho": caminho,
        "custo_total": _soma_custo_caminho(matriz, caminho),
        "estados_gerados": estados_gerados,
        "estados_visitados": estados_visitados,
        "sucesso": True,
    }



def sde_gulosa_deterministica(matriz, origem, destino, heuristica):
    atual = origem
    caminho = [atual]
    estados_gerados = 0
    while atual != destino:
        h_atual = heuristica(atual, destino)
        candidatos = vizinhos(atual, matriz)
        estados_gerados += len(candidatos)
        proximo = None
        for _, viz in candidatos:
            if heuristica(viz, destino) < h_atual:
                proximo = viz
                break
        if proximo is None:
            return _resultado(caminho, matriz, estados_gerados, len(caminho), False)
        caminho.append(proximo)
        atual = proximo
    return _resultado(caminho, matriz, estados_gerados, len(caminho), True)


def sde_maior_aclive(matriz, origem, destino, heuristica):
    atual = origem
    caminho = [atual]
    estados_gerados = 0
    while atual != destino:
        h_atual = heuristica(atual, destino)
        candidatos = vizinhos(atual, matriz)
        estados_gerados += len(candidatos)
        melhor_viz = None
        melhor_h = h_atual
        for _, viz in candidatos:
            h_viz = heuristica(viz, destino)
            if h_viz < melhor_h:
                melhor_h = h_viz
                melhor_viz = viz
        if melhor_viz is None:
            return _resultado(caminho, matriz, estados_gerados, len(caminho), False)
        caminho.append(melhor_viz)
        atual = melhor_viz
    return _resultado(caminho, matriz, estados_gerados, len(caminho), True)


def sde_gulosa_estocastica(matriz, origem, destino, heuristica, rng=None):
    rng = rng or random
    atual = origem
    caminho = [atual]
    estados_gerados = 0
    while atual != destino:
        h_atual = heuristica(atual, destino)
        candidatos = vizinhos(atual, matriz)
        estados_gerados += len(candidatos)
        melhores = [viz for _, viz in candidatos if heuristica(viz, destino) < h_atual]
        if not melhores:
            return _resultado(caminho, matriz, estados_gerados, len(caminho), False)
        proximo = rng.choice(melhores)
        caminho.append(proximo)
        atual = proximo
    return _resultado(caminho, matriz, estados_gerados, len(caminho), True)


def _reconstroi_caminho(veio_de, origem, destino):
    caminho = [destino]
    atual = destino
    while atual != origem:
        atual = veio_de[atual]
        caminho.append(atual)
    caminho.reverse()
    return caminho


def busca_gulosa(matriz, origem, destino, heuristica):
    contador = 0
    estados_gerados = 0
    fronteira = [(heuristica(origem, destino), contador, origem)]
    veio_de = {}
    visitados = set()

    while fronteira:
        _, _, atual = heapq.heappop(fronteira)
        if atual in visitados:
            continue
        visitados.add(atual)
        if atual == destino:
            caminho = _reconstroi_caminho(veio_de, origem, destino)
            return _resultado(caminho, matriz, estados_gerados, len(visitados), True)
        for _, viz in vizinhos(atual, matriz):
            estados_gerados += 1
            if viz in visitados:
                continue
            if viz not in veio_de:
                veio_de[viz] = atual
                contador += 1
                heapq.heappush(fronteira, (heuristica(viz, destino), contador, viz))

    return _resultado([], matriz, estados_gerados, len(visitados), False)


def a_estrela(matriz, origem, destino, heuristica):
    contador = 0
    estados_gerados = 0
    g = {origem: 0}
    veio_de = {}
    fronteira = [(heuristica(origem, destino), contador, origem, 0)]
    expandidos = set()

    while fronteira:
        _, _, atual, g_na_entrada = heapq.heappop(fronteira)
        if g_na_entrada > g.get(atual, float("inf")):
            continue
        expandidos.add(atual)
        if atual == destino:
            caminho = _reconstroi_caminho(veio_de, origem, destino)
            return _resultado(caminho, matriz, estados_gerados, len(expandidos), True)
        for _, viz in vizinhos(atual, matriz):
            estados_gerados += 1
            novo_g = g_na_entrada + custo_celula(matriz, viz)
            if novo_g < g.get(viz, float("inf")):
                g[viz] = novo_g
                veio_de[viz] = atual
                contador += 1
                heapq.heappush(fronteira, (novo_g + heuristica(viz, destino), contador, viz, novo_g))

    return _resultado([], matriz, estados_gerados, len(expandidos), False)
