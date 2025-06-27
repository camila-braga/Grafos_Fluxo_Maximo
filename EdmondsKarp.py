from collections import deque
import time

def BuscaLargura(adjacencia, capacidade_residual, quantidade_vertices, fonte, sumidouro):
    vizinhos_visitados = [-1] * quantidade_vertices
    Q = deque() #deque usado como fila vazia apenas por motivos de melhorar a complexidade
    Q.append(fonte)
    vizinhos_visitados[fonte] = fonte
    
    while Q:
        atual = Q.popleft()
        for vizinho, w in adjacencia[atual]:
            if vizinhos_visitados[vizinho] == -1 and capacidade_residual[atual][vizinho] > 0:
                vizinhos_visitados[vizinho] = atual
                if vizinho == sumidouro:
                    return True, vizinhos_visitados
                Q.append(vizinho)

    return False, vizinhos_visitados

#Criando um grafo orientado, com capacidades, para fluxo em redes:
quantidade_vertices = int(input("\n\033[34mDigite o número de vértices:\033[0m "))
quantidade_arestas = int(input("\n\033[34mDigite o número de arestas:\033[0m "))

adjacencia = [[] for a in range(quantidade_vertices)]
capacidade_residual = [[0]*quantidade_vertices for c in range(quantidade_vertices)]

print("\n\033[31mAtenção! Os vértices começam no zero!")

print("\n\033[34mDigite as arestas:")
for e in range(quantidade_arestas):
    print(f"\n\033[34mAresta {e+1}:\033[0m")
    u = int(input("    Origem: "))
    v = int(input("    Destino: "))
    capacidade = int(input("    Capacidade: "))
    fluxo_inicial = int(input("    Fluxo inicial: "))

    adjacencia[u].append((v, capacidade))
    adjacencia[v].append((u, 0)) 

    # capacidade disponível = capacidade máxima - fluxo já usado
    capacidade_residual[u][v] = capacidade - fluxo_inicial
    capacidade_residual[v][u] = fluxo_inicial

print("\n\033[35mLista de Adjacência com Capacidades: (destino, capacidade)\033[0m")
for i in range(quantidade_vertices):
    print(f"{i}: {adjacencia[i]}")

print()

print("\n\033[35mMatriz de Capacidades Residuais:\033[0m")
for linha in range(quantidade_vertices):
    for coluna in range(quantidade_vertices):
        print(f"{capacidade_residual[linha][coluna]:3}", end=" ")
    print()

print("\n\033[35mArestas com capacidade residual > 0:\033[0m")
for u in range(quantidade_vertices):
    for v in range(quantidade_vertices):
        if capacidade_residual[u][v] > 0:
            print(f"{u} -> {v} (capacidade: {capacidade_residual[u][v]})")


fonte = int(input("\n\033[34mDigite o vértice da fonte:\033[0m "))
sumidouro = int(input("\n\033[34mDigite o vértice do sumidouro:\033[0m "))

#Cálculo do fluxo máximo
inicio = time.perf_counter()
fluxo_maximo = 0
while True:
    encontrou_caminho, pai = BuscaLargura(adjacencia, capacidade_residual, quantidade_vertices, fonte, sumidouro)
    if not encontrou_caminho:
        break

    # Encontrar o fluxo mínimo no caminho de aumento
    fluxo_caminho = float('inf') #Inicializado com infinito
    v = sumidouro
    while v != fonte:
        u = pai[v]
        fluxo_caminho = min(fluxo_caminho, capacidade_residual[u][v])
        v = u

    # Atualizar capacidades residuais
    v = sumidouro
    while v != fonte:
        u = pai[v]
        capacidade_residual[u][v] -= fluxo_caminho
        capacidade_residual[v][u] += fluxo_caminho
        v = u

    fluxo_maximo += fluxo_caminho

print(f"\n\033[35mFluxo máximo adicional possível da fonte {fonte} ao sumidouro {sumidouro}: \033[36m{fluxo_maximo}\033[0m") 
fim = time.perf_counter()

print(f"\n\033[35mTempo de execução: \033[36m{fim - inicio:.8f} segundos\033[0m")