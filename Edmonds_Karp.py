from collections import deque
import time
import utils

#------------------------------------------------------------------------------------------------------
#                                   FUNÇÃO BUSCA EM LARGURA
#------------------------------------------------------------------------------------------------------
def BuscaLargura(
    adjacencia_com_reversa, 
    capacidade_residual, 
    quantidade_vertices, 
    fonte, 
    sumidouro
):
    vizinhos_visitados = [-1] * quantidade_vertices
    Q = deque() #deque usado como fila vazia apenas por motivos de melhorar a complexidade
    Q.append(fonte)
    vizinhos_visitados[fonte] = fonte

    while Q:
        atual = Q.popleft()

        for vizinho, w in adjacencia_com_reversa[atual]:

            if vizinhos_visitados[vizinho] == -1 and capacidade_residual[atual][vizinho] > 0:
                vizinhos_visitados[vizinho] = atual

                if vizinho == sumidouro:
                    return True, vizinhos_visitados
                Q.append(vizinho)

    return False, vizinhos_visitados #Retorna se encontrou caminho de aumento de fulxo

#------------------------------------------------------------------------------------------------------
# ALGORITMO DE EDMONDS-KARP
#------------------------------------------------------------------------------------------------------
def FuncaoEdmondsKarp(
    escolha,
    adjacencia,
    adjacencia_com_reversa,
    capacidade_residual_inicial, 
    capacidade_residual, 
    quantidade_vertices,
    quantidade_arestas, 
    fonte, 
    sumidouro
):
    inicio = time.perf_counter()
    fluxo_maximo = 0

    while True:
        #Procura por caminhos de aumetno:
        encontrou_caminho, pai = BuscaLargura(
            adjacencia_com_reversa, 
            capacidade_residual, 
            quantidade_vertices, 
            fonte, 
            sumidouro
        )
        
        if not encontrou_caminho:
            break

        #Fluxo mínimo ao longo do caminho encontrado:
        fluxo_caminho = float('inf')
        v = sumidouro
        while v != fonte:
            u = pai[v]
            fluxo_caminho = min(fluxo_caminho, capacidade_residual[u][v])
            v = u

        #Atualização das capacidades residuais:
        v = sumidouro
        while v != fonte:
            u = pai[v]
            capacidade_residual[u][v] -= fluxo_caminho
            capacidade_residual[v][u] += fluxo_caminho
            v = u

        fluxo_maximo += fluxo_caminho

    fim = time.perf_counter()
    
    #------------------------------------------------------------------------------------------------------
    # CRIAÇÃO E EXIBIÇÃO DO RELATÓRIO DO CASO ESCOLHIDO
    #------------------------------------------------------------------------------------------------------
    relatorio = utils.criaRelatorio(
        escolha,
        quantidade_vertices,
        quantidade_arestas,
        fonte,
        sumidouro,
        adjacencia,
        adjacencia_com_reversa,
        capacidade_residual_inicial,
        capacidade_residual,
        fluxo_maximo,
        fim,
        inicio
    )
    
    utils.exibeRelatorio (relatorio)
    utils.salvaRelatorio (escolha, relatorio)
    