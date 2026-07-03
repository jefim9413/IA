import os
import random

from grid import gerar_conjunto_instancias
from heuristicas import HEURISTICAS, com_fator
from algoritmos import (
    sde_gulosa_deterministica,
    sde_maior_aclive,
    sde_gulosa_estocastica,
    busca_gulosa,
    a_estrela,
)
from utils_json import salvar_instancias, salvar_resultados_csv, agregados_por_chave

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIR_INSTANCIAS = os.path.join(RAIZ, "data", "instancias")
DIR_RESULTADOS = os.path.join(RAIZ, "data", "resultados")


def _linha_base(inst, **extra):
    linha = {"codigo_entrada": inst["codigo"]}
    linha.update(extra)
    return linha


def experimento1():
    instancias = gerar_conjunto_instancias("E1", 15, 0.0, semente=101)
    salvar_instancias(instancias, os.path.join(DIR_INSTANCIAS, "exp1_instancias.json"))

    variacoes = [
        ("SdE Gulosa Deterministica", sde_gulosa_deterministica),
        ("SdE Maior Aclive", sde_maior_aclive),
        ("SdE Gulosa Estocastica", sde_gulosa_estocastica),
    ]

    rng_estocastica = random.Random(202)

    linhas = []

    for inst in instancias:
        for nome_var, funcao in variacoes:
            for nome_heur, heur in HEURISTICAS.items():
                if funcao is sde_gulosa_estocastica:
                    r = funcao(
                        inst["matriz"],
                        inst["origem"],
                        inst["destino"],
                        heur,
                        rng=rng_estocastica,
                    )
                else:
                    r = funcao(
                        inst["matriz"],
                        inst["origem"],
                        inst["destino"],
                        heur,
                    )

                linhas.append(_linha_base(
                    inst,
                    variacao=nome_var,
                    heuristica=nome_heur,
                    estados_gerados=r["estados_gerados"],
                    estados_visitados=r["estados_visitados"],
                    custo_total=r["custo_total"],
                    sucesso=r["sucesso"],
                ))

    salvar_resultados_csv(
        linhas,
        os.path.join(DIR_RESULTADOS, "exp1_resultados.csv"),
    )

    resumo = agregados_por_chave(
        linhas,
        ["variacao", "heuristica"],
        ["estados_gerados", "estados_visitados", "custo_total"],
    )

    salvar_resultados_csv(
        resumo,
        os.path.join(DIR_RESULTADOS, "exp1_resumo.csv"),
    )

    return linhas, resumo


def experimento2():
    instancias = gerar_conjunto_instancias("E2", 20, 0.0, semente=103)
    salvar_instancias(instancias, os.path.join(DIR_INSTANCIAS, "exp2_instancias.json"))

    algoritmos = [
        ("Busca Gulosa", busca_gulosa),
        ("A*", a_estrela),
    ]

    linhas = []

    for inst in instancias:
        for nome_alg, funcao in algoritmos:
            for nome_heur, heur in HEURISTICAS.items():
                r = funcao(
                    inst["matriz"],
                    inst["origem"],
                    inst["destino"],
                    heur,
                )

                linhas.append(_linha_base(
                    inst,
                    algoritmo=nome_alg,
                    heuristica=nome_heur,
                    estados_gerados=r["estados_gerados"],
                    estados_visitados=r["estados_visitados"],
                    custo_total=r["custo_total"],
                    sucesso=r["sucesso"],
                ))

    salvar_resultados_csv(
        linhas,
        os.path.join(DIR_RESULTADOS, "exp2_resultados.csv"),
    )

    resumo = agregados_por_chave(
        linhas,
        ["algoritmo", "heuristica"],
        ["estados_gerados", "estados_visitados", "custo_total"],
    )

    salvar_resultados_csv(
        resumo,
        os.path.join(DIR_RESULTADOS, "exp2_resumo.csv"),
    )

    return linhas, resumo


def experimento3():
    instancias = gerar_conjunto_instancias("E3", 20, 0.20, semente=105)
    salvar_instancias(instancias, os.path.join(DIR_INSTANCIAS, "exp3_instancias.json"))

    variacoes_heuristica = [
        ("h1_DEx1", HEURISTICAS["DE"], 1),
        ("h2_DEx3", HEURISTICAS["DE"], 3),
        ("h3_DEx6", HEURISTICAS["DE"], 6),
        ("h4_DMx1", HEURISTICAS["DM"], 1),
        ("h5_DMx3", HEURISTICAS["DM"], 3),
        ("h6_DMx6", HEURISTICAS["DM"], 6),
    ]

    linhas = []

    for inst in instancias:
        for nome_h, heur_base, fator in variacoes_heuristica:
            heur = com_fator(heur_base, fator)

            r = a_estrela(
                inst["matriz"],
                inst["origem"],
                inst["destino"],
                heur,
            )

            linhas.append(_linha_base(
                inst,
                heuristica=nome_h,
                fator=fator,
                estados_gerados=r["estados_gerados"],
                estados_visitados=r["estados_visitados"],
                custo_total=r["custo_total"],
                sucesso=r["sucesso"],
            ))

    salvar_resultados_csv(
        linhas,
        os.path.join(DIR_RESULTADOS, "exp3_resultados.csv"),
    )

    resumo = agregados_por_chave(
        linhas,
        ["heuristica", "fator"],
        ["estados_gerados", "estados_visitados", "custo_total"],
    )

    salvar_resultados_csv(
        resumo,
        os.path.join(DIR_RESULTADOS, "exp3_resumo.csv"),
    )

    return linhas, resumo


def experimento4():
    densidades = [0.10, 0.20, 0.30, 0.40]

    algoritmos = [
        ("SdE Maior Aclive", sde_maior_aclive),
        ("Busca Gulosa", busca_gulosa),
        ("A*", a_estrela),
    ]

    todas_instancias = []
    linhas = []

    for densidade in densidades:
        instancias = gerar_conjunto_instancias(
            f"E4_{int(densidade * 100):02d}",
            20,
            densidade,
            semente=1000 + int(densidade * 100),
        )

        todas_instancias.extend(instancias)

        for inst in instancias:
            for nome_alg, funcao in algoritmos:
                r = funcao(
                    inst["matriz"],
                    inst["origem"],
                    inst["destino"],
                    HEURISTICAS["DM"],
                )

                linhas.append(_linha_base(
                    inst,
                    densidade_obstaculos=densidade,
                    algoritmo=nome_alg,
                    estados_gerados=r["estados_gerados"],
                    estados_visitados=r["estados_visitados"],
                    custo_total=r["custo_total"],
                    sucesso=r["sucesso"],
                ))

    salvar_instancias(
        todas_instancias,
        os.path.join(DIR_INSTANCIAS, "exp4_instancias.json"),
    )

    salvar_resultados_csv(
        linhas,
        os.path.join(DIR_RESULTADOS, "exp4_resultados.csv"),
    )

    resumo = agregados_por_chave(
        linhas,
        ["algoritmo", "densidade_obstaculos"],
        ["estados_gerados", "estados_visitados", "custo_total"],
    )

    salvar_resultados_csv(
        resumo,
        os.path.join(DIR_RESULTADOS, "exp4_resumo.csv"),
    )

    return linhas, resumo


def main():
    for diretorio in (DIR_INSTANCIAS, DIR_RESULTADOS):
        os.makedirs(diretorio, exist_ok=True)

    print("Executando Experimento 1 (variações da Subida de Encosta)...")
    experimento1()

    print("Executando Experimento 2 (Busca Gulosa vs A*)...")
    experimento2()

    print("Executando Experimento 3 (A* e admissibilidade)...")
    experimento3()

    print("Executando Experimento 4 (densidade de obstáculos)...")
    experimento4()

    print("Concluído. Dados em data/instancias e data/resultados.")


if __name__ == "__main__":
    main()