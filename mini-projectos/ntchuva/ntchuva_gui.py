import pygame, sys
import random
import copy

pygame.init()

tabuleiro_player_2 = [[2, 2, 2, 2, 2, 2], 
                      [2, 2, 2, 2, 2, 2]]

tabuleiro_player_1 = [[2, 2, 2, 2, 2, 2], 
                      [2, 2, 2, 2, 2, 2]]


pontos_de_colisao = [{"rect": pygame.Rect(285 + (105 * i), 402, 80, 80), "coor": f"C{i + 1}"} for i in range(6)]
pontos_de_colisao.extend({"rect": pygame.Rect(285 + (105 * i), 517, 80, 80), "coor": f"D{i + 1}"} for i in range(6))


coordenadas_P2 = {f"A{i + 1}": (0, i) for i in range(6)}
coordenadas_P1 = {f"C{i + 1}": (0, i) for i in range(6)}
coordenadas_P1.update({f"D{i + 1}": (1, i) for i in range(6)})
coordenadas_P2.update({f"B{i + 1}": (1, i) for i in range(6)})

ROW_HEIGHT = 115
COL_WIDTH = 105
MARGIN = 6

tipo_de_letra = pygame.font.Font(None, 25)  

pontos_player_2:int = 0
pontos_player_1:int = 0

total_pedras_p1, total_pedras_p2 = sum(map(sum,tabuleiro_player_1)), sum(map(sum,tabuleiro_player_2))

quem_joga = 1
vencedor = None
simulacao = 0
max_recursion = 20

class TABULEIRO:
    def __init__(self) -> None:

        self.tabuleiro_vazio = pygame.image.load('mini-projectos/resources/02_ntchuva/tabuleiro/tabuleiro_vazio.png')
        self.cova_pontos = pygame.image.load('mini-projectos/resources/02_ntchuva/tabuleiro/covas_pontos.png')
        
        self.valores_pedras = {i: pygame.image.load(f'mini-projectos/resources/02_ntchuva/tabuleiro/cova_{i:02d}.png') for i in range(13)}
        self.valores_pedras.update({13: pygame.image.load('mini-projectos/resources/02_ntchuva/tabuleiro/cova_12+.png')})

    def desenhar_tabuleiro(self):
        self.rect_cova_pontos = self.cova_pontos.get_rect()
        rect_cova_pontos = 52, 196
        screen.blit(self.cova_pontos, rect_cova_pontos)

        rect_cova_pontos = 1003, 196
        screen.blit(tabuleiro.cova_pontos, rect_cova_pontos)

        self.desenhar_numero_de_pedras(tabuleiro_player_2, 319, 223)
        self.desenhar_numero_de_pedras(tabuleiro_player_1, 319, 493)

    def desenhar_numero_de_pedras(self, tabuleiro, x_offset, y_offset):
        global pontos_de_colisao
        for row in range(len(tabuleiro)):
            for col in range(len(tabuleiro[row])):
                x = x_offset + COL_WIDTH * col + MARGIN
                y = y_offset + ROW_HEIGHT * row + MARGIN

                # TEXTO DE NUMERO DE PEDRAS
                numero_de_pedras = tabuleiro[row][col]
                camada_pedras_numeros = tipo_de_letra.render(str(numero_de_pedras), True, ("black"))

                numero_render = camada_pedras_numeros.get_rect(center=(x, y))
                screen.blit(camada_pedras_numeros, numero_render)

                # IMAGEM DE NUMERO DE PEDRAS

                y_pedras = (y_offset + ROW_HEIGHT * row + MARGIN) - 58
                img_pedras_surface = numero_de_pedras
                if img_pedras_surface > 12:
                    img_pedras_surface = 13
                
                img_pedras = self.valores_pedras.get(img_pedras_surface)

                pedras_render = img_pedras.get_rect(center=(x, y_pedras))
                screen.blit(img_pedras, pedras_render)

    def display_update(self):
        screen.fill((217, 217, 217))
        rect_bg = bg_img.get_rect()
        rect_bg.center = 588, 379
        screen.blit(bg_img, rect_bg)
        tabuleiro.desenhar_tabuleiro()
        pygame.display.flip()

class JOGADAS:
    def __init__(self):
        ...

    def obter_coordenadas(self, coordenada: str, tabuleiro: dict):
        if coordenada in tabuleiro:
            return tabuleiro.get(coordenada)
        else:
            return "Posição desconhecida."
        
    def jogo_principal(self):
        global quem_joga, vencedor, pontos_player_1, pontos_player_2, simulacao

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  
                    mouse_x, mouse_y = event.pos
                    for ponto in pontos_de_colisao:
                        if ponto["rect"].collidepoint(mouse_x, mouse_y):
                            if vencedor is None:
                                if quem_joga == 1:
                                    if jogada.jogar(tabuleiro_player_1, ponto['coor']):
                                        if pontos_player_1 > total_pedras_p2 - 1:
                                            vencedor = pontos_player_1
                                            print("\n   GAME OVER  \nJOGADOR 1 VENCEU\n")
                                            break
                                        else:
                                            quem_joga = 2
        if quem_joga == 2:
            simulacao = 1
            texto = jogada.melhor_jogada_player_2()
            simulacao = 0
            jogada.jogar(tabuleiro_player_2, texto)
            if pontos_player_2 > total_pedras_p1 - 1:
                vencedor = pontos_player_2
                print("\n   GAME OVER  \nJOGADOR 2 VENCEU\n")
                quem_joga = 1
            else:
                quem_joga = 1
        
        return True

    def obter_proximo_movimento(self, x, y):
        movimentos = [(1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (0, 5), (0, 4), (0, 3), (0, 2), (0, 1), (0, 0)]
        return movimentos[(movimentos.index((x, y)) + 1) % len(movimentos)]
    
    def captura_de_pecas(self, tabuleiro, x, y):
        global pontos_player_1, pontos_player_2, quem_joga, tabuleiro_player_2   # número actual de pontos dos jogadores.
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
                if simulacao == 0:
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

    def jogar(self, tabuleiro_jogador, coor_escolhida):
        global simulacao
        texto = coor_escolhida
        if tabuleiro_jogador == tabuleiro_player_1:
            coordenada = coordenadas_P1
        elif tabuleiro_jogador == tabuleiro_player_2:
            coordenada = coordenadas_P2
            print(f"\nJogador 2 escolheu: {texto}")

        coordenada = self.obter_coordenadas(texto, coordenada)
        if coordenada != "Posição desconhecida.":
            x, y = coordenada[0], coordenada[1]
            if tabuleiro_jogador[x][y] > 0:
                if texto in self.obter_posicoes_validas(tabuleiro_jogador)[0]:
                    self.mover_peca(coordenada[0], coordenada[1], tabuleiro_jogador)
                    return True
                else:
                    if self.obter_posicoes_validas(tabuleiro_jogador)[1] == "Fase Regular":
                        print("Existem casas com mais de uma pedra. Tente novamente.")
                    elif self.obter_posicoes_validas(tabuleiro_jogador)[1] == "Fase Final":
                        print("Fase final do jogo, já não pode juntar pedras. Tente novamente.")
                    return False
            else:
                print("Nenhuma peça nesta posição. Tente novamente.")
                return False
        else:
            print("Coordenada desconhecida. Tente novamente.")
            return False

    def obter_posicoes_validas(self, tabuleiro: list):
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
                        proxima_casa = self.obter_proximo_movimento(x_index, y_index)
                        if tabuleiro[proxima_casa[0]][proxima_casa[1]] == 0:
                            posicao = val_list.index(valor)
                            posicoes_validas[0].append(key_list[posicao])

                elif tabuleiro[x_index][y_index] > 1:  # Verifica se o elemento é maior que 1
                    valor = (x_index, y_index)  # obtem as coordenadas

                    if valor in val_list:  # verifica se as coordenadas está presente nos valores das coordenas do dicionario
                        posicao = val_list.index(valor)  # obtem a posição da coordenada no dicionario
                        posicoes_validas[1].append(key_list[posicao])  # adiciona na lista posicoes_validas[1] a chave do elemento

        if len(posicoes_validas[1]) >= 1:
            return posicoes_validas[1], "Fase Regular"
        else:
            return posicoes_validas[0], "Fase Final"

    def mover_peca(self, x: int, y: int, tabuleiro:list):
        tab = TABULEIRO()
        casas_a_percorrer = tabuleiro[x][y] # define o numero de casas que irá percorrer
        casas_percorridas = 0 # helper
        global pontos_player_1, pontos_player_2, max_recursion# número actual de pontos dos jogadores.

        while casas_a_percorrer+1 > casas_percorridas: # +1 para adicionar mais um movimento, pois inicia a contagem a partir da remoção da pedra.
            valor = tabuleiro[x][y] # helper
            if simulacao == 0:
                pygame.time.wait(250)
            next_x, next_y = self.obter_proximo_movimento(x, y)
            
            # Movimento da primeira casa, que remove as pedras da casa e inicia a distribuição na proxima casa no sentido anti-horário.
            if casas_percorridas == 0:
                if simulacao == 0:
                    tab.display_update()
                casas_percorridas += 1
                tabuleiro[x][y] = 0
                if simulacao == 0:
                    print(f"{casas_percorridas}. pos(x={x}, y={y}), {valor} -> {tabuleiro[x][y]}")
                

            else:
                # Caso não seja a primeira casa continua a distribuição no sentido anti-horário.
                if simulacao == 0:
                    tab.display_update()
                casas_percorridas += 1
                tabuleiro[x][y] += 1
                if simulacao == 0:
                    print(f"{casas_percorridas}. pos(x={x}, y={y}), {valor} -> {tabuleiro[x][y]}")
                
                    # Imprime o relatório da posição actual, pedras existentes anteriorimente e novo número de pedras.
                if (casas_percorridas-1 == casas_a_percorrer): # Verifica se está no ultimo movimento
                    if tabuleiro[x][y] > 1: # se a casa onde foi feito o ultimo movimento número de peças for maior que 1
                        if simulacao == 0:
                            print(f"\nPeças a mover: {tabuleiro[x][y]}") # Informa o número de peças que irá mover
                        max_recursion -= 1
                        self.mover_peca(x, y, tabuleiro) # Aplica novamente a função usando os parametros da posição actual.
                        if max_recursion == 0:
                            print("Distribuição Interropida, Limite Atingido")
                            sys.exit()
                        
                    elif tabuleiro[x][y] == 1: # CAPTURA DE PEÇA
                        self.captura_de_pecas(tabuleiro, x, y)
                        if simulacao == 0:
                            tab.display_update()
            x, y = next_x, next_y
            self.play = 1
    
    def melhor_jogada_player_2(self):
        global tabuleiro_player_1, tabuleiro_player_2, pontos_player_1, pontos_player_2

        # Copias
        og_tabuleiro_P1, og_tabuleiro_P2 = copy.deepcopy(tabuleiro_player_1), copy.deepcopy(tabuleiro_player_2)
        og_pontos_P1, og_pontos_P2 = copy.deepcopy(pontos_player_1), copy.deepcopy(pontos_player_2)

        resultados_de_movimentos = {}
        melhores_jogadas_sorted = []

        coordenadas_validas = jogada.obter_posicoes_validas(tabuleiro_player_2)[0]

        for jogada_valida in coordenadas_validas:
            coordenada_a_jogar = jogada.obter_coordenadas(jogada_valida, coordenadas_P2)
            jogada.mover_peca(coordenada_a_jogar[0], coordenada_a_jogar[1], copy.deepcopy(tabuleiro_player_2))
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

class BANNERS:
    ...


tabuleiro = TABULEIRO()
jogada = JOGADAS()
banner = BANNERS()
screen = pygame.display.set_mode([1176, 758])

bg_img = tabuleiro.tabuleiro_vazio
relogio = pygame.time.Clock()

def main():
    running = True
    while running:
        
        running = jogada.jogo_principal()

        screen.fill((217, 217, 217))
        rect_bg = bg_img.get_rect()
        rect_bg.center = 588, 379
        screen.blit(bg_img, rect_bg)

        tabuleiro.desenhar_tabuleiro()
        
        pygame.display.flip()
        relogio.tick(24)

    pygame.quit()

if __name__ == "__main__":
    main()   

