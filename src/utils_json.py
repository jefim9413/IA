import csv
import json
import os

def salvar_instancias(instancias, caminho_arquivo):
    os.makedirs(os.path.dirname(caminho_arquivo), exist_ok=True)
    dados = []
    for inst in instancias:
        item = dict(inst)
        item["origem"] = list(item["origem"])
        item["destino"] = list(item["destino"])
        dados.append(item)
    with open(caminho_arquivo, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)


def carregar_instancias(caminho_arquivo):
    with open(caminho_arquivo, encoding="utf-8") as f:
        dados = json.load(f)
    instancias = []
    for item in dados:
        item = dict(item)
        item["origem"] = tuple(item["origem"])
        item["destino"] = tuple(item["destino"])
        instancias.append(item)
    return instancias


def salvar_resultados_csv(linhas, caminho_arquivo):
    os.makedirs(os.path.dirname(caminho_arquivo), exist_ok=True)
    if not linhas:
        with open(caminho_arquivo, "w", encoding="utf-8") as f:
            f.write("")
        return
    campos = list(linhas[0].keys())
    with open(caminho_arquivo, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=campos)
        writer.writeheader()
        writer.writerows(linhas)

def agregados_por_chave(linhas, chaves, campos_numericos):
    grupos = {}
    for linha in linhas:
        chave = tuple(linha[c] for c in chaves)
        grupos.setdefault(chave, []).append(linha)

    resultado = []
    for chave, grupo in grupos.items():
        item = {chave_nome: valor for chave_nome, valor in zip(chaves, chave)}
        for campo in campos_numericos:
            valores = [g[campo] for g in grupo if g.get(campo) is not None]
            item[f"media_{campo}"] = round(sum(valores) / len(valores), 3) if valores else None
        item["qtd_execucoes"] = len(grupo)
        if "sucesso" in grupo[0]:
            sucessos = sum(1 for g in grupo if g["sucesso"])
            item["taxa_sucesso"] = round(sucessos / len(grupo), 3)
        resultado.append(item)
    return resultado
