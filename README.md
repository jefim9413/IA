# Trabalho 2 — Resolução de Problemas com Busca

Este projeto foi desenvolvido para a disciplina de Inteligência Artificial, com o objetivo de implementar e comparar algoritmos de busca aplicados ao problema de caminho em um mapa no formato de grid.

O problema utiliza uma matriz 15x15, onde cada célula representa uma posição do mapa com um custo de passagem. Algumas células também podem ser bloqueadas, representando obstáculos.

## Objetivo

Implementar e comparar algoritmos de busca heurística, analisando:

- quantidade de estados gerados;
- quantidade de estados visitados;
- custo total do caminho encontrado;
- taxa de sucesso em cenários com obstáculos.

## Algoritmos implementados

O projeto implementa os seguintes algoritmos:

- Subida de Encosta Gulosa Determinística;
- Subida de Encosta pelo Maior Aclive;
- Subida de Encosta Gulosa Estocástica;
- Busca Gulosa;
- A*.

## Heurísticas utilizadas

Foram utilizadas duas heurísticas:

- Distância Euclidiana;
- Distância Manhattan.

Também foram testadas variações dessas heurísticas com fatores multiplicativos no experimento de admissibilidade do A*.

## Estrutura do projeto

```text
IA/
├── src/
│   ├── main.py
│   ├── grid.py
│   ├── heuristicas.py
│   ├── algoritmos.py
│   └── utils_json.py
│
├── data/
│   ├── instancias/
│   └── resultados/
│
└── README.md
```

## Descrição dos arquivos

### `src/main.py`

Arquivo principal do projeto. Ele executa todos os experimentos, gera as instâncias e salva os resultados.

### `src/grid.py`

Responsável pela criação do mapa em grid 15x15, geração dos pesos, inserção de obstáculos e validação da conectividade entre origem e destino.

### `src/heuristicas.py`

Contém as funções heurísticas utilizadas pelos algoritmos:

- Distância Euclidiana;
- Distância Manhattan.

### `src/algoritmos.py`

Contém a implementação dos algoritmos de busca usados nos experimentos.

### `src/utils_json.py`

Contém funções auxiliares para salvar instâncias em JSON e resultados em CSV.

## Experimentos realizados

### Experimento 1 — Variações da Subida de Encosta

Compara três variações da Subida de Encosta usando as heurísticas Euclidiana e Manhattan em mapas sem obstáculos.

São avaliadas:

- Subida de Encosta Gulosa Determinística;
- Subida de Encosta pelo Maior Aclive;
- Subida de Encosta Gulosa Estocástica.

### Experimento 2 — Busca Gulosa e A*

Compara a Busca Gulosa e o A* em mapas sem obstáculos, utilizando as heurísticas Euclidiana e Manhattan.

### Experimento 3 — A* e Admissibilidade

Avalia o comportamento do A* com diferentes variações das heurísticas, multiplicadas pelos fatores 1, 3 e 6.

As execuções são realizadas em mapas com 20% de obstáculos.

### Experimento 4 — Influência da Densidade de Obstáculos

Analisa o comportamento dos algoritmos com diferentes densidades de obstáculos:

- 10%;
- 20%;
- 30%;
- 40%.

Os algoritmos avaliados são:

- Subida de Encosta pelo Maior Aclive;
- Busca Gulosa;
- A*.

## Como executar o projeto

Na raiz do projeto, execute:

```bash
py src/main.py
```

Ou, se o comando `python` estiver configurado no seu computador:

```bash
python src/main.py
```

## Saída gerada

Após a execução, os arquivos serão gerados dentro da pasta `data`.

### Instâncias

As instâncias usadas nos experimentos ficam em:

```text
data/instancias/
```

Arquivos gerados:

```text
exp1_instancias.json
exp2_instancias.json
exp3_instancias.json
exp4_instancias.json
```

### Resultados

Os resultados das execuções ficam em:

```text
data/resultados/
```

Arquivos gerados:

```text
exp1_resultados.csv
exp1_resumo.csv
exp2_resultados.csv
exp2_resumo.csv
exp3_resultados.csv
exp3_resumo.csv
exp4_resultados.csv
exp4_resumo.csv
```

## Validação dos mapas com obstáculos

Nos experimentos com obstáculos, as instâncias são validadas antes da execução dos algoritmos.

A validação é feita por meio de uma busca em largura, considerando apenas se existe caminho entre a origem e o destino. Os custos das células não são considerados nessa etapa, pois o objetivo é apenas garantir conectividade.

Caso uma instância não possua caminho válido entre origem e destino, ela é descartada e uma nova instância é gerada.

## Observação sobre visualização

A visualização dos caminhos foi removida do projeto, pois no enunciado ela aparece apenas como uma dica, não como requisito obrigatório.

O foco principal do trabalho está na geração dos dados, execução dos algoritmos e análise dos resultados no relatório.

## Entrega

Para a entrega, devem ser incluídos:

- código-fonte do projeto;
- instâncias geradas;
- resultados em CSV;
- relatório em PDF com a análise dos experimentos.
