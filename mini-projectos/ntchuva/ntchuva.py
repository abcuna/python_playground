import random
import copy
import sys

tabuleiro_player_2 = [[2, 2, 2, 2, 2, 2], [2, 2, 2, 2, 2, 2]]

tabuleiro_player_1 = [[2, 2, 2, 2, 2, 2], [2, 2, 2, 2, 2, 2]]

coordenadas_P2 = {f"A{i + 1}": (0, i) for i in range(6)}
coordenadas_P1 = {f"C{i + 1}": (0, i) for i in range(6)}
coordenadas_P1.update({f"D{i + 1}": (1, i) for i in range(6)})
coordenadas_P2.update({f"B{i + 1}": (1, i) for i in range(6)})

pontos_player_2: int = 0
pontos_player_1: int = 0

total_pedras_p1, total_pedras_p2 = sum(map(sum, tabuleiro_player_1)), sum(map(sum, tabuleiro_player_2))

quem_joga = 1
vencedor = None
simulacao = 0
max_recursion = 20


def ver_tabuleiro():
    print("   ", " ".join(str(i + 1) for i in range(6)))
    print("   --------------")
    for linha_index_p2, linha_p2 in enumerate(tabuleiro_player_2):
        print(chr(65 + linha_index_p2), "|", " ".join(str(coluna_p2) for coluna_p2 in linha_p2), "|", chr(65 + linha_index_p2))
    print("   --------------")
    for linha_index_p1, linha_p1 in enumerate(tabuleiro_player_1):
        print(chr(67 + linha_index_p1), "|", " ".join(str(coluna_p1) for coluna_p1 in linha_p1), "|", chr(67 + linha_index_p1))
    print("   --------------")
    print("   ", " ".join(str(i + 1) for i in range(6)))
    print(f"\n  P1 = {pontos_player_1:02d}  P2 = {pontos_player_2:02d}\n  Pedras Capuradas")


def obter_coordenadas(coordenada: str, tabuleiro: dict):
    if coordenada in tabuleiro:
        return tabuleiro.get(coordenada)
    else:
        return "Posição desconhecida."


def obter_proximo_movimento(x, y):
    movimentos = [(1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (0, 5), (0, 4), (0, 3), (0, 2), (0, 1), (0, 0)]
    return movimentos[(movimentos.index((x, y)) + 1) % len(movimentos)]


def captura_de_pecas(tabuleiro, x, y):
    global pontos_player_1, pontos_player_2, quem_joga, tabuleiro_player_2  # número actual de pontos dos jogadores.
    pecas_capturadas, pedras_externas = 0, 0
    if quem_joga == 2:
        tabuleiro_player_2 = copy.deepcopy(tabuleiro)
    
    if tabuleiro == tabuleiro_player_1 and x == 0:  # verifica se está na posição interna
        if tabuleiro_player_2[x + 1][y] > 0:  # verifica se o numero de pedras do adversário na linha imediatamente a seguir do jogador 1 tem ou não peças
            pedras_internas = tabuleiro_player_2[x + 1][y]  # helper
            tabuleiro_player_2[x + 1][y] = 0  # recolhe as pedras internas do adversário
            
            if tabuleiro_player_2[x][y] > 0:  # verfica se a coluna externa tem ou não pedras
                pedras_externas = tabuleiro_player_2[x][y]  # helper
                tabuleiro_player_2[x][y] = 0  # recolhe as pedras externas

            pecas_capturadas = pedras_externas + pedras_internas
            pontos_player_1 += pecas_capturadas
            print(f"\nCapturadas {pecas_capturadas} peças do Jogador 2")  # informa aos jogadores quantas peças foram removidas
        
    elif tabuleiro == tabuleiro_player_2 and x == 1:
        if tabuleiro_player_1[x - 1][y] > 0:
            pedras_internas = tabuleiro_player_1[x - 1][y]
            tabuleiro_player_1[x - 1][y] = 0

            if tabuleiro_player_1[x][y] > 0:
                pedras_externas = tabuleiro_player_1[x][y]
                tabuleiro_player_1[x][y] = 0
            pecas_capturadas = pedras_externas + pedras_internas
            pontos_player_2 += pecas_capturadas
            if simulacao == 0:
                print(f"\nCapturadas {pecas_capturadas} peças do Jogador 1")
    return pecas_capturadas


def mover_peca(x: int, y: int, tabuleiro: list):
    casas_a_percorrer = tabuleiro[x][y]  # define o numero de casas que irá percorrer
    casas_percorridas = 0  # helper
    global max_recursion

    while casas_a_percorrer > casas_percorridas:
        for _ in range(casas_a_percorrer + 1):  # +1 para adicionar mais um movimento, pois inicia a contagem a partir da remoção da pedra.
            valor = tabuleiro[x][y]  # helper
            next_x, next_y = obter_proximo_movimento(x, y)  # Verifica a posição e e diz ao programa que posição é a proxima a mover

            if casas_percorridas == 0:  # Movimento da primeira casa, que remove as pedras da casa e inicia a distribuição na proxima casa no sentido anti-horário.
                casas_percorridas += 1
                tabuleiro[x][y] = 0
                if simulacao == 0:
                    print(f"\n{casas_percorridas}. pos(x={x}, y={y}), {valor} -> {tabuleiro[x][y]}")
            
            else:  # Caso não seja a primeira casa continua a distribuição no sentido anti-horário.
                casas_percorridas += 1
                tabuleiro[x][y] += 1
                if simulacao == 0:
                    print(f"{casas_percorridas}. pos(x={x}, y={y}), {valor} -> {tabuleiro[x][y]}")  # Imprime o relatório da posição actual, pedras existentes anteriorimente e novo número de pedras.
                if casas_percorridas - 1 == casas_a_percorrer:  # Verifica se está no ultimo movimento
                    if tabuleiro[x][y] > 1:  # se a casa onde foi feito o ultimo movimento número de peças for maior que 1
                        if simulacao == 0:
                            print(f"\nPeças a mover: {tabuleiro[x][y]}")  # Informa o número de peças que irá mover
                            
                        max_recursion -= 1
                        mover_peca(x, y, tabuleiro)  # Aplica novamente a função usando os parametros da posição actual.
                        if max_recursion == 0:
                            print("Distribuição Interropida, Limite Atingido")
                            sys.exit()
                    elif tabuleiro[x][y] == 1:  # CAPTURA DE PEÇA
                        captura_de_pecas(tabuleiro, x, y)
                        max_recursion = 20
            x, y = next_x, next_y
    return tabuleiro


def obter_posicoes_validas(tabuleiro: list):
    global coordenadas_P1, coordenadas_P2

    if tabuleiro == tabuleiro_player_1:
        coordenadas = coordenadas_P1
    else:
        coordenadas = coordenadas_P2

    key_list = list(coordenadas.keys())
    val_list = list(coordenadas.values())

    posicoes_validas = [[], []]  # Array 2D que no primeiro index sao colocados elementos == 1, e no segundo index apenas elementos maiores que 1.

    for x_index, x in enumerate(tabuleiro):
        for y_index, y in enumerate(x):
            if tabuleiro[x_index][y_index] == 1:
                valor = (x_index, y_index)

                if valor in val_list:
                    proxima_casa = obter_proximo_movimento(x_index, y_index)
                    if tabuleiro[proxima_casa[0]][proxima_casa[1]] == 0:
                        posicao = val_list.index(valor)
                        posicoes_validas[0].append(key_list[posicao])

            elif tabuleiro[x_index][y_index] > 1:  # Verfiica se o elemento é maior que 1
                valor = (x_index, y_index)  # obtem as coordenadas

                if valor in val_list:  # verifica se as coordenadas está presente nos valores das coordenas do dicionario
                    posicao = val_list.index(valor)  # obtem a posição da coordenada no dicionario
                    posicoes_validas[1].append(key_list[posicao])  # adiciona na lista posicoes_validas[1] a chave do elemento

    if len(posicoes_validas[1]) >= 1:
        return posicoes_validas[1], "Fase Regular"
    else:
        return posicoes_validas[0], "Fase Final"


def jogar(tabuleiro_jogador):
    global simulacao
    while True:
        if tabuleiro_jogador == tabuleiro_player_1:
            texto = input("\nDigite a coordenada: ").capitalize()
            coordenada = coordenadas_P1
        elif tabuleiro_jogador == tabuleiro_player_2:
            simulacao = 1
            texto = melhor_jogada_player_2()
            simulacao = 0
            coordenada = coordenadas_P2
            print(f"\nJogador 2 escolheu: {texto}")

        coordenada = obter_coordenadas(texto, coordenada)
        if coordenada != "Posição desconhecida.":
            x, y = coordenada[0], coordenada[1]
            if tabuleiro_jogador[x][y] > 0:
                if texto in obter_posicoes_validas(tabuleiro_jogador)[0]:
                    mover_peca(coordenada[0], coordenada[1], tabuleiro_jogador)
                    print()
                    ver_tabuleiro()
                    break
                else:
                    if obter_posicoes_validas(tabuleiro_jogador)[1] == "Fase Regular":
                        print("Existem casas com mais de uma pedra. Tente novamente.")
                    elif obter_posicoes_validas(tabuleiro_jogador)[1] == "Fase Final":
                        print("Fase final do jogo, já não pode juntar pedras. Tente novamente.")
            else:
                print("Nenhuma peça nesta posição. Tente novamente.")
        else:
            print("Coordenada desconhecida. Tente novamente.")
            break


def melhor_jogada_player_2():
    global tabuleiro_player_1, tabuleiro_player_2, pontos_player_1, pontos_player_2

    # Copias
    og_tabuleiro_P1, og_tabuleiro_P2 = copy.deepcopy(tabuleiro_player_1), copy.deepcopy(tabuleiro_player_2)
    og_pontos_P1, og_pontos_P2 = copy.deepcopy(pontos_player_1), copy.deepcopy(pontos_player_2)

    resultados_de_movimentos = {}
    melhores_jogadas_sorted = []

    coordenadas_validas = obter_posicoes_validas(tabuleiro_player_2)[0]

    for jogada_valida in coordenadas_validas:
        coordenada_a_jogar = obter_coordenadas(jogada_valida, coordenadas_P2)
        mover_peca(coordenada_a_jogar[0], coordenada_a_jogar[1], copy.deepcopy(tabuleiro_player_2))
        pontos_colectados = sum(map(sum, og_tabuleiro_P1)) - sum(map(sum, tabuleiro_player_1))
        resultados_de_movimentos.update({f"{jogada_valida}":pontos_colectados})
        
        # Devolução das Copias
        tabuleiro_player_1, tabuleiro_player_2 = copy.deepcopy(og_tabuleiro_P1), copy.deepcopy(og_tabuleiro_P2)
        pontos_player_1, pontos_player_2 = copy.deepcopy(og_pontos_P1), copy.deepcopy(og_pontos_P2)
    
    melhores_jogadas = sorted(resultados_de_movimentos.items(), key=lambda x:x[1], reverse= True)
    
    for x in melhores_jogadas:
        melhores_jogadas_sorted.append(x[0])
    
    if len(melhores_jogadas_sorted) != 0:
        return melhores_jogadas_sorted[0]
    else:
        return random.choice(coordenadas_validas)


def main():
    global quem_joga, vencedor, pontos_player_1, pontos_player_2
    ver_tabuleiro()
    while vencedor is None:
        if quem_joga == 1:
            jogar(tabuleiro_player_1)
            if pontos_player_1 > total_pedras_p2 - 1:
                vencedor = pontos_player_1
                print("\n   GAME OVER  \nJOGADOR 1 VENCEU\n")
            else:
                quem_joga = 2
        else:
            jogar(tabuleiro_player_2)
            if pontos_player_2 > total_pedras_p1 - 1:
                vencedor = pontos_player_2
                print("\n   GAME OVER  \nJOGADOR 2 VENCEU\n")
            else:
                quem_joga = 1


if __name__ == "__main__":
    main()