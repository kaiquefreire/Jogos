import pygame
from abc import ABCMeta, abstractmethod
import random

from pygame.constants import QUIT
pygame.init()

#Tamanho da tela em largura e altura
screen = pygame.display.set_mode((800, 600), 0)

#Fontes
fonte = pygame.font.SysFont("arial", 28, True, False)

#RGB 
ROSA     = (252, 255, 255)
AMARELO  = (255, 255, 0)
PRETO    = (0, 0, 0)
AZUL     = (0, 127, 255)
VERMELHO = (255, 0, 0)
BRANCO   = (255, 255, 255)

velocidade = 1
ACIMA      = 1 
ABAIXO     = 2 
DIREITA    = 3 
ESQUERDA   = 4

class ElementoJogo(metaclass=ABCMeta):
    
    @abstractmethod 
    def pintar(self,tela):
        pass
    
    @abstractmethod 
    def calcular_regras(self):
        pass
    
    @abstractmethod 
    def processar_eventos(self, eventos):
        pass

#Desenhando o Cenario em que 0 = vazio e 2 = parede
class Cenario:
    def __init__(self, tamanho, pac,fan):    
        self.pacman = pac
        self.pontos = 0 
        self.fantasma = fan
        self.tamanho = tamanho    
        self.matriz = [
            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
            [2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 1, 1, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 2],
            [2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2],
            [2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2],
            [2, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 0, 0, 0, 0, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 0, 0, 0, 0, 0, 0, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 1, 1, 1, 1, 1, 2, 2, 1, 2, 0, 0, 0, 0, 0, 0, 2, 1, 2, 2, 1, 1, 1, 1, 1, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 0, 0, 0, 0, 0, 0, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 2],
            [2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2],
            [2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2],
            [2, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 1, 1, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2],
            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
        ]
        
    def pintar_pontos(self, tela):
        pontosx =30*self.tamanho
        img_pontos = fonte.render('Score: {}'.format(self.pontos), True, AMARELO)
        tela.blit(img_pontos, (pontosx, 50))
                
    def pintar_linha(self, tela, numero_linha, linha):
        for numero_coluna, coluna in enumerate(linha):
            x = numero_coluna*self.tamanho
            y = numero_linha*self.tamanho
            metade = self.tamanho//2
            cor = PRETO
            if coluna == 2:
                cor = AZUL
            pygame.draw.rect(tela, cor, (x, y, self.tamanho, self.tamanho),0)
            if coluna ==1:
                pygame.draw.circle(tela, AMARELO, (x + metade, y + metade), self.tamanho//10, 0)
    
    def pintar(self, tela):
        for numero_linha, linha in enumerate(self.matriz):
            self.pintar_linha(tela, numero_linha, linha)
        self.pintar_pontos(tela)
    
    def get_direcoes(self, linha, coluna):
        direcoes = []
        if self.matriz[int(linha - 1)][int(coluna)] != 2:
            direcoes.append(ACIMA)
        if self.matriz[int(linha + 1)][int(coluna)] != 2:
            direcoes.append(ABAIXO)
        if self.matriz[int(linha)][int(coluna - 1)] != 2:
            direcoes.append(ESQUERDA)
        if self.matriz[int(linha)][int(coluna - 2)] != 2:
            direcoes.append(DIREITA)   
        return direcoes
    
    def calcular_regras(self):
        direcoes = self.get_direcoes(self.fantasma.linha, self.fantasma.coluna)
        if len(direcoes) >= 3:
            self.fantasma.esquina(direcoes) 
        col = self.pacman.coluna_intencao
        lin = self.pacman.linha_intencao
        
        if 0 <= col < 28 and 0 <= lin < 29:
            if self.matriz[lin][col]!= 2:
                self.pacman.aceitar_movimento()
                #Verifica pontuação
                if self.matriz [lin][col] == 1:
                    self.pontos += 1
                    self.matriz[lin][col] = 0
                    
        col = int(self.fantasma.coluna_intencao)
        lin = int(self.fantasma.linha_intencao)
        
        if 0 <= col < 28 and 0 <= lin < 29 and self.matriz[lin][col] != 2:
            self.fantasma.aceitar_movimento()
        else: 
            self.fantasma.recusar_movimento(direcoes)
            

    def processar_eventos(self, evt):
        for e in evt:
            if e.type == pygame.QUIT:
                exit()
                    
class Pacman(ElementoJogo):
    def __init__(self, tamanho):
        self.coluna = 1
        self.linha = 1
        self.centro_x = 400
        self.centro_y = 300
        self.tamanho  = tamanho
        self.vel_x = 0
        self.vel_y = 0
        self.raio = self.tamanho // 2
        self.coluna_intencao = self.coluna
        self.linha_intencao = self.linha
        
    def calcular_regras(self):    
        self.coluna_intencao = self.coluna + self.vel_x
        self.linha_intencao = self.linha + self.vel_y
        self.centro_x = int(self.coluna*self.tamanho + self.raio)
        self.centro_y = int(self.linha*self.tamanho + self.raio)
    
    def pintar(self, tela):
        # Desenhar o corpo do pacman
        pygame.draw.circle(tela, ROSA, (self.centro_x, self.centro_y), self.raio, 0)

        # Desenhar a boca do pacman
        canto_boca     = (self.centro_x, self.centro_y)
        labio_superior = (self.centro_x + self.raio, self.centro_y - self.raio)
        labio_inferior = (self.centro_x + self.raio, self.centro_y)
        pontos = [canto_boca, labio_superior, labio_inferior]

        pygame.draw.polygon(tela, PRETO, pontos, 0)

        # Desenhar o olho do pacman
        olho_x    = int(self.centro_x + self.raio / 3)
        olho_y    = int(self.centro_y - self.raio / 1.70)
        olho_raio = int(self.raio / 8)
        pygame.draw.circle(tela, PRETO, (olho_x, olho_y), olho_raio, 0)
        
    def processar_eventos(self, eventos):
        
        for e in eventos:
            if e.type == pygame.KEYDOWN:
                
                if e.key == pygame.K_RIGHT:
                    self.vel_x= velocidade
                elif e.key == pygame.K_LEFT:
                    self.vel_x = -velocidade
                elif e.key == pygame.K_UP:
                    self.vel_y = -velocidade
                elif e.key == pygame.K_DOWN:
                    self.vel_y = velocidade
            
            elif e.type == pygame.KEYUP:    
        
                if e.key == pygame.K_RIGHT:
                    self.vel_x = 0
                elif e.key == pygame.K_LEFT:
                    self.vel_x = 0
                elif e.key == pygame.K_UP:
                    self.vel_y = 0
                elif e.key == pygame.K_DOWN:
                    self.vel_y = 0
                    
    def aceitar_movimento(self):
        self.linha = self.linha_intencao
        self.coluna = self.coluna_intencao

class Fantasma(ElementoJogo): 
    def __init__(self, cor, tamanho):
        #Posição do fantasma 
        self.coluna = 13.0 
        self.linha = 15.0 
        self.linha_intencao = self.linha
        self.coluna_intencao = self.coluna
        self.tamanho = tamanho
        self.velocidade = 1 
        self.direcao = 0 
        self.cor = cor 
        
    def pintar(self, tela):
        #1/8 de divisão do fantasma
        fatia = self.tamanho//8        
        px = int(self.coluna*self.tamanho)
        py = int(self.linha *self.tamanho)        
        contorno = [(px, py + self.tamanho),
                    (px + fatia, py + fatia * 2),
                    (px + fatia * 2, py + fatia//2),
                    (px + fatia * 3, py),
                    (px + fatia * 5, py),
                    (px + fatia * 6, py + fatia // 2),
                    (px + fatia * 7, py + fatia * 2),
                    (px + self.tamanho, py + self.tamanho)]
          
        #Pintando o fantasma na tela 
        pygame.draw.polygon(tela, self.cor, contorno, 0)

        olho_raio_ext = fatia 
        olho_raio_int = fatia//2
        
        olho_e_x = int(px + fatia * 3)
        olho_e_y = int(py + fatia * 3)
        
        olho_d_x = int(px + fatia * 6)
        olho_d_y = int(py + fatia * 3)
        
        pygame.draw.circle(tela, BRANCO, (olho_e_x, olho_e_y), olho_raio_ext, 0)
        pygame.draw.circle(tela, PRETO, (olho_e_x, olho_e_y), olho_raio_int, 0)
        
        pygame.draw.circle(tela, BRANCO, (olho_d_x, olho_d_y), olho_raio_ext, 0)
        pygame.draw.circle(tela, PRETO, (olho_d_x, olho_d_y), olho_raio_int, 0)
        
    def calcular_regras(self):
        if self.direcao == ACIMA:
            self.linha_intencao  -= self.velocidade
        elif self.direcao == ABAIXO:
            self.linha_intencao  += self.velocidade
        elif self.direcao == ESQUERDA:
            self.coluna_intencao -= self.velocidade       
        elif self.direcao == DIREITA:
            self.coluna_intencao  += self.velocidade
    
    def mudar_direcao(self, direcoes):
        self.direcao = random.choice(direcoes)
    
    def esquina(self, direcoes):
        self.mudar_direcao(direcoes)
        
    def aceitar_movimento(self):
        self.linha = self.linha_intencao
        self.coluna = self.coluna_intencao
        
    def recusar_movimento(self, direcoes):
        self.linha_intencao = self.linha
        self.coluna_intencao= self.coluna
        self.mudar_direcao(direcoes)
        
    def processar_eventos(self, eventos):
        pass

if __name__ == "__main__": 
    size = 600//30
    
    #personagens
    pacman = Pacman(size)
    blinky = Fantasma(VERMELHO,size)
    
    #cenario 
    cenario = Cenario(size, pacman, blinky)
    
    while True:
        
        # Calcular regras
        pacman.calcular_regras()
        blinky.calcular_regras()
        cenario.calcular_regras()
        
        # Pintar tela
        screen.fill(PRETO)
        cenario.pintar(screen)
        pacman.pintar(screen)
        blinky.pintar(screen)
        
        pygame.display.update()
        pygame.time.delay(100)

        # Captura de Eventos 
        eventos = pygame.event.get()            
        pacman.processar_eventos(eventos)
        cenario.processar_eventos(eventos)