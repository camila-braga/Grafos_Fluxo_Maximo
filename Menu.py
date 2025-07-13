import Edmonds_Karp

def main():
    
    arquivo = "casos_testes.txt"
    with open(arquivo, "r") as f:
        lido = [lido.strip() for lido in f]

    condicao = True
    while (condicao):

        print("\n\033[34mTemos os seguintes casos de teste:\033[0m")
        for c in range (0, 20):
            print(f"\n    Caso {c+1};")

        escolha = int (input("\n\033[34mEscolha o caso que deseja testar ou '0' para sair:\033[0m "))

        if escolha == 0:
            print("\n\033[31mPrograma encerrado.\033[0m")
            condicao = False
            continue

        i = 0
        encontrado = False

        while i < len(lido) and not encontrado:
            try:
                if lido[i].startswith("Caso"):
                    numero_caso = int(lido[i].split()[1])

                    if numero_caso == escolha:
                        quantidade_vertices = int(lido[i+1])
                        quantidade_arestas = int(lido[i+2]) 
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
                        i += 5 + quantidade_arestas    
                #Próximo caso
                i += 1
            except (IndexError, ValueError):
                print("\n\033[31mErro ao ler o caso de teste. Verifique o formato do arquivo.\033[0m")
                encontrado = False
                break


        if encontrado:
            Edmonds_Karp.FuncaoEdmondsKarp(
                escolha,
                adjacencia,
                adjacencia_com_reversa,
                capacidade_residual_inicial, 
                capacidade_residual, 
                quantidade_vertices,
                quantidade_arestas, 
                fonte, 
                sumidouro
            )
        else:
            print("\n\033[31mCaso não encontrado!\033[0m")

if __name__ == "__main__":
    main()