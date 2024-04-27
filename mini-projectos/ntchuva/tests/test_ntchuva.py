from aulas_python.ntchuva import obter_coordenadas, mover_peca, obter_posicoes_validas

coordenadas_P2 = {f"A{i + 1}": (0, i) for i in range(6)}
coordenadas_P1 = {f"C{i + 1}": (0, i) for i in range(6)}
coordenadas_P1.update({f"D{i + 1}": (1, i) for i in range(6)})
coordenadas_P2.update({f"B{i + 1}": (1, i) for i in range(6)})

def test_posicoes_validas():
    tabuleiro_player_2 = [[2, 2, 2, 2, 2, 2],
                          [0, 1, 1, 1, 1, 1]]
    assert obter_posicoes_validas(tabuleiro_player_2) == (["A1", "A2", "A3", "A4", "A5", "A6"], "Fase Regular")

    tabuleiro_player_2 = [[0, 0, 0, 0, 0, 0],
                          [1, 0, 1, 1, 1, 1]]
    assert obter_posicoes_validas(tabuleiro_player_2) == (["B1", "B6"], "Fase Final")

def test_obter_coordenadas():
    assert obter_coordenadas("A1", coordenadas_P2) == (0,0)
    assert obter_coordenadas("A20", coordenadas_P2) == "Posição desconhecida."

def test_mover_peca():
    tabuleiro_player_1 = [[2, 2, 2, 2, 2, 2],
                          [2, 2, 2, 2, 2, 2]]
    assert mover_peca(0,2, tabuleiro_player_1) == [[1, 4, 1, 0, 3, 3], [3, 3, 0, 3, 3, 0]]

    tabuleiro_player_1 = [[2, 0, 0, 2, 2, 2],
                          [2, 2, 2, 2, 2, 2]]
    assert mover_peca(0, 3, tabuleiro_player_1) == [[2, 1, 1, 0, 2, 2], [2, 2, 2, 2, 2, 2]]

    tabuleiro_player_2 = [[0, 2, 2, 2, 2, 2],
                          [0, 2, 2, 2, 2, 2]]
    assert mover_peca(0, 3, tabuleiro_player_2) == [[1, 1, 4, 1, 0, 3], [1, 0, 3, 3, 0, 3]]

