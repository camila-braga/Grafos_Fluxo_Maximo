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
    arquivo_relatorio = f"Caso_{escolha}_EdmondsKarp.txt"
    with open(arquivo_relatorio, "w") as f_out:

        for linha in relatorio:
            f_out.write(linha + "\n")
            
    print(f"\n\033[32mRelatório salvo em arquivo: {arquivo_relatorio}\033[0m")