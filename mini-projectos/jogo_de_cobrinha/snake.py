import pygame, sys, random
from pygame.math import Vector2

class COBRA:
    def __init__(self):
        self.corpo = [Vector2(5,10), Vector2(4,10), (3,10)]
        self.direcao = Vector2(0,0)
        self.novo_bloco = False

        self.head_up = pygame.image.load('mini-projectos/resources/resources/visuais/head_up.png').convert_alpha()
        self.head_down = pygame.image.load('mini-projectos/resources/resources/visuais/head_down.png').convert_alpha()
        self.head_right = pygame.image.load('mini-projectos/resources/resources/visuais/head_right.png').convert_alpha()
        self.head_left = pygame.image.load('mini-projectos/resources/resources/visuais/head_left.png').convert_alpha ()

        self.tail_up = pygame.image.load('mini-projectos/resources/resources/visuais/tail_up.png'). convert_alpha()
        self.tail_down = pygame.image.load('mini-projectos/resources/resources/visuais/tail_down.png').convert_alpha()
        self.tail_right = pygame.image.load('mini-projectos/resources/resources/visuais/tail_right.png').convert_alpha()
        self.tail_left = pygame.image.load('mini-projectos/resources/resources/visuais/tail_left.png').convert_alpha()

        self.corpo_vertical = pygame.image.load('mini-projectos/resources/resources/visuais/body_vertical.png').convert_alpha()
        self.corpo_horizontal = pygame.image.load('mini-projectos/resources/resources/visuais/body_horizontal.png').convert_alpha()

        self.body_tr = pygame.image.load('mini-projectos/resources/resources/visuais/body_tr.png').convert_alpha()
        self.body_tl = pygame.image.load('mini-projectos/resources/resources/visuais/body_tl.png').convert_alpha()
        self.body_br = pygame.image.load('mini-projectos/resources/resources/visuais/body_br.png').convert_alpha()
        self.body_bl = pygame.image.load('mini-projectos/resources/resources/visuais/body_bl.png').convert_alpha()


    def desenhar_cobra(self):
        self.actualizar_cabeca()
        self.actualizar_cauda()

        for index, bloco in enumerate(self.corpo):
            pos_x = int(bloco[0] * tamanho_celula) 
            pos_y = int(bloco[1] * tamanho_celula)
            cobra_rect = pygame.Rect(pos_x, pos_y, tamanho_celula, tamanho_celula)

            if index == 0:
                tela.blit(self.cabeca, cobra_rect)
            elif index == len(self.corpo) -1:
                tela.blit(self.cauda,cobra_rect)
            else:
                bloco_prev =  self.corpo[index + 1] - bloco
                bloco_next = self.corpo[index - 1] - bloco

                if bloco_prev.x == bloco_next.x:
                    tela.blit(self.corpo_vertical, cobra_rect)
                elif bloco_prev.y == bloco_next.y:
                    tela.blit(self.corpo_horizontal, cobra_rect)
                else:
                    if bloco_prev.x == -1 and bloco_next.y == -1 or bloco_prev.y == -1 and bloco_next.x == -1:
                        tela.blit(self.body_tl, cobra_rect)
                    elif bloco_prev.x == 1 and bloco_next.y == -1 or bloco_prev.y == -1 and bloco_next.x == 1:
                        tela.blit(self.body_tr,cobra_rect)
                    elif bloco_prev.x == 1 and bloco_next.y == 1 or bloco_prev.y == 1 and bloco_next.x == 1:
                        tela.blit(self.body_br, cobra_rect)
                    elif bloco_prev.x == -1 and bloco_next.y == 1 or bloco_prev.y == 1 and bloco_next.x == -1:
                        tela.blit(self.body_bl, cobra_rect)

    def actualizar_cabeca(self):
        resultado_cabeca_vect = self.corpo[1] - self.corpo[0]
        if resultado_cabeca_vect == Vector2(1,0): self.cabeca = self.head_left
        elif resultado_cabeca_vect == Vector2(-1,0): self.cabeca = self.head_right
        elif resultado_cabeca_vect == Vector2(0,-1): self.cabeca = self.head_down
        elif resultado_cabeca_vect == Vector2(0,1): self.cabeca = self.head_up

    def actualizar_cauda(self):
        resultado_cauda_vect = self.corpo[-2] - self.corpo[-1]
        if resultado_cauda_vect == Vector2(1,0): self.cauda = self.tail_left
        elif resultado_cauda_vect == Vector2(-1,0): self.cauda = self.tail_right
        elif resultado_cauda_vect == Vector2(0,-1): self.cauda = self.tail_down
        elif resultado_cauda_vect == Vector2(0,1): self.cauda = self.tail_up 
         
    def movimentar_cobra(self):
        if self.novo_bloco == True:
            copia_corpo = self.corpo[:]
            self.novo_bloco = False
        else:
            copia_corpo = self.corpo[:-1]
            
        copia_corpo.insert(0,copia_corpo[0] + self.direcao)
        self.corpo = copia_corpo[:]
            
    def add_bloco(self):
        self.novo_bloco = True

    def reinciar(self):
        self.corpo = [Vector2(5,10), Vector2(4,10), (3,10)]

class FRUTA:
    def __init__(self):
        self.randomize()
    
    def desenhar_fruta(self):
        fruta_rect = pygame.Rect(int(self.pos.x * tamanho_celula), int(self.pos.y * tamanho_celula), tamanho_celula, valor_celula)
        tela.blit(maca, fruta_rect)
        #pygame.draw.rect(tela, (126,166,114), fruta_rect)
    
    def randomize(self):
        self.y = random.randint(0, valor_celula - 1)
        self.x = random.randint(0, valor_celula - 1) 
        self.pos = Vector2(self.x, self.y)

class MAIN:
    def __init__(self):
        self.cobra = COBRA()
        self.fruta = FRUTA()
    
    def update(self):
        self.cobra.movimentar_cobra()
        self.ver_colisao()
        self.ver_falha()
    
    def desenhar_elementos(self):
        self.desenhar_relva()
        self.fruta.desenhar_fruta()
        self.cobra.desenhar_cobra()
        self.render_pontos()

    def ver_colisao(self):
        if self.fruta.pos == self.cobra.corpo[0]:
             self.fruta.randomize()
             self.cobra.add_bloco()

        for bloco in self.cobra.corpo[1:]:
            if bloco == self.fruta.pos:
                self.fruta.randomize()
    
    def ver_falha(self):
        cabeca_x = self.cobra.corpo[0].x
        cabeca_y = self.cobra.corpo[0].y
        if not 0 <= cabeca_x < valor_celula or not 0 <= cabeca_y < valor_celula:
            self.game_over()

        for block in self.cobra.corpo[1:]:
            if block == self.cobra.corpo[0]:
                self.game_over()
    
    def desenhar_relva(self):
        cor_relva = (167,209,61)
        for linha in range(valor_celula):
            if linha % 2 == 0:
                for col in range(valor_celula):
                    if col % 2 == 0:
                        relva_rect = pygame.Rect(col * tamanho_celula,linha * tamanho_celula,tamanho_celula, tamanho_celula)
                        pygame.draw.rect(tela,cor_relva,relva_rect)
            else:
                for col in range(valor_celula):
                    if col % 2 != 0:
                        relva_rect = pygame.Rect(col * tamanho_celula,linha * tamanho_celula,tamanho_celula, tamanho_celula)
                        pygame.draw.rect(tela,cor_relva,relva_rect)       
    
    def render_pontos(self):
        texto_pontos = str(len(self.cobra.corpo) - 3)
        camada_pontos = tipo_de_letra.render(texto_pontos, True, (56,74,12))

        pontos_x = int(tamanho_celula * valor_celula - 60)
        pontos_y = int(tamanho_celula * valor_celula - 40)

        pontos_rect = camada_pontos.get_rect(center = (pontos_x, pontos_y))
        maca_rect = maca.get_rect(midright = (pontos_rect.left, pontos_rect.centery))
        background_rect = pygame.Rect(maca_rect.left, maca_rect.top, maca_rect.width + (pontos_rect.width + 15), maca_rect.height)

        pygame.draw.rect(tela,(167,209,61),background_rect )
        tela.blit(camada_pontos, pontos_rect)
        tela.blit(maca, maca_rect)
        pygame.draw.rect(tela,(56,74,12),background_rect,2)

    def game_over(self):
        self.cobra.reinciar()
        self.direcao = Vector2(0,0)
    
pygame.init()
tamanho_celula = 40
valor_celula = 20 
tela = pygame.display.set_mode((tamanho_celula * valor_celula,tamanho_celula * valor_celula))
relogio = pygame.time.Clock()
maca = pygame.image.load('mini-projectos/resources/resources/visuais/apple.png').convert_alpha()
tipo_de_letra = pygame.font.Font(None, 50)  
main_game = MAIN()

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)

while True: 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SCREEN_UPDATE:
            main_game.update()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and main_game.cobra.direcao.y != 1:
                     main_game.cobra.direcao = Vector2(0,-1)
            if event.key == pygame.K_DOWN and main_game.cobra.direcao.y != -1:
                main_game.cobra.direcao = Vector2(0,1)
            if event.key == pygame.K_LEFT and main_game.cobra.direcao.x != 1:
                main_game.cobra.direcao = Vector2(-1,0)
            if event.key == pygame.K_RIGHT and main_game.cobra.direcao.x != -1:
                main_game.cobra.direcao = Vector2(1,0)

    tela.fill((175,215,70))
    main_game.desenhar_elementos()
    pygame.display.update()
    relogio.tick(60)