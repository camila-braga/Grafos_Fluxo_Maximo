from collections import deque
import time

#------------------------------------------------------------------------------------------------------
#                                   FUNÇÃO QUE CRIA O RELATÓRIO
#------------------------------------------------------------------------------------------------------
def criaRelatorio(
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
):
    relatorio = []
    relatorio.append(f"Caso {escolha}")
    relatorio.append(f"\nQuantidade de vertices: {quantidade_vertices}")
    relatorio.append(f"Quantidade de arestas: {quantidade_arestas}")
    relatorio.append(f"Fonte: {fonte}")
    relatorio.append(f"Sumidouro: {sumidouro}")

    relatorio.append("\nLista de Adjacencia:")
    for k in range(quantidade_vertices):
        relatorio.append(f"  {k}: {adjacencia[k]}")

    relatorio.append("\nLista de Adjacencia com arestas reversas:")
    for k in range(quantidade_vertices):
        relatorio.append(f"  {k}: {adjacencia_com_reversa[k]}")

    relatorio.append("\nMatriz de Capacidades Residuais inicial:")
    for linha in range(quantidade_vertices):
        linha_str = " ".join(f"{capacidade_residual_inicial[linha][coluna]:3}" for coluna in range(quantidade_vertices))
        relatorio.append(linha_str)

    relatorio.append("\nMatriz de Capacidades Residuais final:")
    for linha in range(quantidade_vertices):
        linha_str = " ".join(f"{capacidade_residual[linha][coluna]:3}" for coluna in range(quantidade_vertices))
        relatorio.append(linha_str)

    #Fluxo inicial total saindo da fonte
    fluxo_inicial_total = sum(
        capacidade_residual_inicial[v][fonte] 
        for v in range(quantidade_vertices) 
        if capacidade_residual_inicial[v][fonte] > 0
    )
    if escolha == 6:
        fluxo_inicial_total = fluxo_inicial_total / 100
        fluxo_maximo = fluxo_maximo / 100

    fluxo_maximo_relatorio = fluxo_maximo
        
    relatorio.append(f"\nFluxo inicial: {fluxo_inicial_total}L")
    
    fluxo_total_relatorio = fluxo_inicial_total + fluxo_maximo
    
    if fluxo_maximo > 0:
        relatorio.append(f"Fluxo adicional da fonte {fonte} ao sumidouro {sumidouro} encontrado: {fluxo_maximo_relatorio}L")
        relatorio.append(f"Fluxo maximo total (fluxo inicial + adicional): {fluxo_inicial_total}L + {fluxo_maximo_relatorio}L = {fluxo_total_relatorio}L")
    else:
        relatorio.append(f"\nNao foram encontrados caminhos de aumento da fonte {fonte} ao sumidouro {sumidouro}")

    relatorio.append(f"Tempo de execucao: {fim - inicio:.8f} segundos")
    return relatorio
#------------------------------------------------------------------------------------------------------
#                                   FUNÇÃO QUE EXIBE O RELATÓRIO
#------------------------------------------------------------------------------------------------------
def exibeRelatorio (relatorio):
    print("\n\033[35mRelatório do experimento:\033[0m")
    for linha in relatorio:
        print(linha)

#------------------------------------------------------------------------------------------------------
#                                   FUNÇÃO QUE SALVA O RELATÓRIO EM ARQUIVO TXT
#------------------------------------------------------------------------------------------------------
def salvaRelatorio (escolha, relatorio):
    arquivo_relatorio = f"Caso_{escolha}.txt"
    with open(arquivo_relatorio, "w") as f_out:

        for linha in relatorio:
            f_out.write(linha + "\n")
            
    print(f"\n\033[32mRelatório salvo em arquivo: {arquivo_relatorio}\033[0m")

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
# LEITURA DO ARQUIVO DE CASOS DE TESTE
#------------------------------------------------------------------------------------------------------
arquivo = "casos_testes.txt"
with open(arquivo, "r") as f:
    lido = [lido.strip() for lido in f]

condicao = True
while (condicao):

    #------------------------------------------------------------------------------------------------------
    # EXIBIÇÃO DO MENU DOS CASOS DE TESTE
    #------------------------------------------------------------------------------------------------------
    print("\n\033[34mTemos os seguintes casos de teste:\033[0m")
    for c in range (0, 6):
        print(f"\n    Caso {c+1};")

    #------------------------------------------------------------------------------------------------------
    # ENTRADA DA ESCOLHA DO USUÁRIO
    #------------------------------------------------------------------------------------------------------
    escolha = int (input("\n\033[34mEscolha o caso que deseja testar ou '0' para sair:\033[0m "))

    if escolha == 0:
        print("\n\033[31mPrograma encerrado.\033[0m")
        condicao = False
        continue

    #------------------------------------------------------------------------------------------------------
    # PROCURA DO BLOCO REFERENTE AO CASO ESCOLHIDO
    #------------------------------------------------------------------------------------------------------
    i = 0
    encontrado = False

    while i < len(lido) and not encontrado:
        numero_caso = int(lido[i].split()[1])
        quantidade_arestas = int(lido[i+2])

        if numero_caso == escolha: 
            #------------------------------------------------------------------------------------------------------
            # LEITURA DOS DADOS DO CASO ESCOLHIDO
            #------------------------------------------------------------------------------------------------------
            quantidade_vertices = int(lido[i+1])
            fonte = int(lido[i+3])
            sumidouro = int(lido[i+4])

            adjacencia = [[] for a in range(quantidade_vertices)]
            adjacencia_com_reversa = [[] for a in range(quantidade_vertices)]

            capacidade_residual_inicial = [
                [0]*quantidade_vertices 
                for c in range(quantidade_vertices)
            ]

            capacidade_residual= [
                [0]*quantidade_vertices 
                for c in range(quantidade_vertices)
            ]

            for k in range(quantidade_arestas):
                u, v, capacidade, fluxo_inicial = map(int, lido[i+5+k].split())
                adjacencia[u].append((v, capacidade))
                adjacencia_com_reversa[u].append((v, capacidade))

                adjacencia_com_reversa[v].append((u, 0)) #Aresta reversa para usar na busca em largura

                capacidade_residual_inicial[u][v] = capacidade - fluxo_inicial #Capacidade disponível = capacidade máxima - fluxo já usado
                capacidade_residual[u][v] = capacidade_residual_inicial[u][v]

                capacidade_residual_inicial[v][u] = fluxo_inicial #Capacidade disponível = fluxo inicial
                capacidade_residual[v][u] = capacidade_residual_inicial[v][u]
            
            encontrado = True

        else:
            #Próximo caso
            i += 5 + quantidade_arestas

    if not encontrado:
        print("\n\033[31mCaso não encontrado!\033[0m")
        continue

    #------------------------------------------------------------------------------------------------------
    # ALGORITMO DE EDMONDS-KARP
    #------------------------------------------------------------------------------------------------------
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
    relatorio = criaRelatorio(
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
    
    exibeRelatorio (relatorio)
    salvaRelatorio (escolha, relatorio)