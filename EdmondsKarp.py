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


arquivo = "casos_testes.txt"
with open(arquivo, "r") as f:
    lido = [lido.strip() for lido in f]

condicao = True
while (condicao):
    print("\n\033[34mTemos os seguintes casos de teste:\033[0m")
    for c in range (0, 6):
        print(f"\n    Caso {c+1};")
    escolha = int (input("\n\033[34mEscolha o caso que deseja testar ou '0' para sair:\033[0m "))
    if escolha == 0:
        print("\n\033[31mPrograma encerrado.\033[0m")
        condicao = False
    else:
        i = 0
        encontrado = False
        while i < len(lido) and not encontrado:
            #Verificando se o número do caso é o mesmo que o escolhido
            numero_caso = int(lido[i].split()[1])
            quantidade_arestas = int(lido[i+2])
            if numero_caso == escolha:
                quantidade_vertices = int(lido[i+1])
                fonte = int(lido[i+3])
                sumidouro = int(lido[i+4])
                adjacencia = [[] for a in range(quantidade_vertices)]
                capacidade_residual = [[0]*quantidade_vertices for c in range(quantidade_vertices)]

                for k in range(quantidade_arestas):
                    u, v, capacidade, fluxo_inicial = map(int, lido[i+5+k].split())
                    adjacencia[u].append((v, capacidade))
                    adjacencia[v].append((u, 0))
                    # capacidade disponível = capacidade máxima - fluxo já usado
                    capacidade_residual[u][v] = capacidade - fluxo_inicial
                    capacidade_residual[v][u] = fluxo_inicial
                
                encontrado = True
            else:
                #Próximo bloco
                i += 5 + quantidade_arestas
        if not encontrado:
            print("\n\033[31mCaso não encontrado!\033[0m")
            continue

        # Cálculo do fluxo máximo
        inicio = time.perf_counter()
        fluxo_maximo = 0
        while True:
            encontrou_caminho, pai = BuscaLargura(adjacencia, capacidade_residual, quantidade_vertices, fonte, sumidouro)
            if not encontrou_caminho:
                break

            fluxo_caminho = float('inf')
            v = sumidouro
            while v != fonte:
                u = pai[v]
                fluxo_caminho = min(fluxo_caminho, capacidade_residual[u][v])
                v = u

            v = sumidouro
            while v != fonte:
                u = pai[v]
                capacidade_residual[u][v] -= fluxo_caminho
                capacidade_residual[v][u] += fluxo_caminho
                v = u

            fluxo_maximo += fluxo_caminho
        fim = time.perf_counter()

        relatorio = []
        relatorio.append(f"Caso {escolha}")
        relatorio.append(f"\nQuantidade de vertices: {quantidade_vertices}")
        relatorio.append(f"Quantidade de arestas: {quantidade_arestas}")
        relatorio.append(f"Fonte: {fonte}")
        relatorio.append(f"Sumidouro: {sumidouro}")
        relatorio.append("\nLista de Adjacencia com arestas reversas:")
        for k in range(quantidade_vertices):
            relatorio.append(f"  {k}: {adjacencia[k]}")

        relatorio.append("\nMatriz de Capacidades Residuais:")
        for linha in range(quantidade_vertices):
            linha_str = " ".join(f"{capacidade_residual[linha][coluna]:3}" for coluna in range(quantidade_vertices))
            relatorio.append(linha_str)

        if escolha == 6:
            fluxo_maximo = fluxo_maximo / 100
        else:
            fluxo_maximo = fluxo_maximo
        relatorio.append(f"\nFluxo maximo adicional da fonte {fonte} ao sumidouro {sumidouro}: {fluxo_maximo}L")
        relatorio.append(f"Tempo de execucao: {fim - inicio:.8f} segundos")

        print("\n\033[35mRelatório do experimento:\033[0m")
        for linha in relatorio:
            print(linha)

        arquivo_relatorio = f"Caso_{escolha}.txt"
        with open(arquivo_relatorio, "w") as f_out:
            for linha in relatorio:
                f_out.write(linha + "\n")

        print(f"\n\033[32mRelatório salvo em arquivo: {arquivo_relatorio}\033[0m")