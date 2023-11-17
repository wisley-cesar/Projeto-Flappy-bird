 import pygame
import os
import random

# Constantes
TELA_LARGURA = 500
TELA_ALTURA = 800
GRAVIDADE = 1.5
DISTANCIA_ENTRE_CANOS = 200
VELOCIDADE_CANOS = 5
VELOCIDADE_CHAO = 5
IMAGEM_PATH = os.path.join('imgs')

# Carregando imagens
IMAGEM_CANO = pygame.transform.scale2x(pygame.image.load(os.path.join(IMAGEM_PATH, 'pipe.png')))
IMAGEM_CHAO = pygame.transform.scale2x(pygame.image.load(os.path.join(IMAGEM_PATH, 'base.png')))
IMAGEM_BACKGROUND = pygame.transform.scale2x(pygame.image.load(os.path.join(IMAGEM_PATH, 'bg.png')))
IMAGEM_GAMEOVER = pygame.transform.scale2x(pygame.image.load(os.path.join(IMAGEM_PATH, "levou ferro.png")))
IMAGENS_PASSARO = [
    pygame.transform.scale2x(pygame.image.load(os.path.join(IMAGEM_PATH, 'bird1.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join(IMAGEM_PATH, 'bird2.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join(IMAGEM_PATH, 'bird3.png'))),
]

pygame.font.init()
FONTE_PONTOS = pygame.font.SysFont('arial', 50)


class Passaro:
    IMGS = IMAGENS_PASSARO
    ROTACAO_MAXIMA = 25
    VELOCIDADE_ROTACAO = 20
    TEMPO_ANIMACAO = 5

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angulo = 0
        self.velocidade = 0
        self.altura = self.y
        self.tempo = 0
        self.contagem_imagem = 0
        self.imagem = self.IMGS[0]

    def pular(self):
        self.velocidade = -10.5
        self.tempo = 0
        self.altura = self.y

    def mover(self):
        self.tempo += 1
        deslocamento = 1.5 * (self.tempo**2) + self.velocidade * self.tempo
        if deslocamento > 16:
            deslocamento = 16
        elif deslocamento < 0:
            deslocamento -= 2
        self.y += deslocamento
        if deslocamento < 0 or self.y < (self.altura + 50):
            if self.angulo < self.ROTACAO_MAXIMA:
                self.angulo = self.ROTACAO_MAXIMA
        else:
            if self.angulo > -90:
                self.angulo -= self.VELOCIDADE_ROTACAO

    def desenhar(self, tela):
        self.contagem_imagem += 1
        if self.contagem_imagem < self.TEMPO_ANIMACAO:
            self.imagem = self.IMGS[0]
        elif self.contagem_imagem < self.TEMPO_ANIMACAO*2:
            self.imagem = self.IMGS[1]
        elif self.contagem_imagem < self.TEMPO_ANIMACAO*3:
            self.imagem = self.IMGS[2]
        elif self.contagem_imagem < self.TEMPO_ANIMACAO*4:
            self.imagem = self.IMGS[1]
        elif self.contagem_imagem >= self.TEMPO_ANIMACAO*4 + 1:
            self.imagem = self.IMGS[0]
            self.contagem_imagem = 0
        if self.angulo <= -80:
            self.imagem = self.IMGS[1]
            self.contagem_imagem = self.TEMPO_ANIMACAO*2
        imagem_rotacionada = pygame.transform.rotate(self.imagem, self.angulo)
        pos_centro_imagem = self.imagem.get_rect(topleft=(self.x, self.y)).center
        retangulo = imagem_rotacionada.get_rect(center=pos_centro_imagem)
        tela.blit(imagem_rotacionada, retangulo.topleft)

    def get_mask(self):
        return pygame.mask.from_surface(self.imagem)


class Cano:
    def __init__(self, x):
        self.x = x
        self.altura = 0
        self.pos_topo = 0
        self.pos_base = 0
        self.CANO_TOPO = pygame.transform.flip(IMAGEM_CANO, False, True)
        self.CANO_BASE = IMAGEM_CANO
        self.passou = False
        self.definir_altura()

    def definir_altura(self):
        self.altura = random.randrange(50, 450)
        self.pos_topo = self.altura - self.CANO_TOPO.get_height()
        self.pos_base = self.altura + DISTANCIA_ENTRE_CANOS

    def mover(self):
        self.x -= VELOCIDADE_CANOS

    def desenhar(self, tela):
        tela.blit(self.CANO_TOPO, (self.x, self.pos_topo))
        tela.blit(self.CANO_BASE, (self.x, self.pos_base))

    def colidir(self, passaro):
        passaro_mask = passaro.get_mask()
        topo_mask = pygame.mask.from_surface(self.CANO_TOPO)
        base_mask = pygame.mask.from_surface(self.CANO_BASE)
        distancia_topo = (self.x - passaro.x, self.pos_topo - round(passaro.y))
        distancia_base = (self.x - passaro.x, self.pos_base - round(passaro.y))
        topo_ponto = passaro_mask.overlap(topo_mask, distancia_topo)
        base_ponto = passaro_mask.overlap(base_mask, distancia_base)
        return base_ponto or topo_ponto


class Chao:
    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = IMAGEM_CHAO.get_width()

    def mover(self):
        self.x1 -= VELOCIDADE_CHAO
        self.x2 -= VELOCIDADE_CHAO
        if self.x1 + IMAGEM_CHAO.get_width() < 0:
            self.x1 = self.x2 + IMAGEM_CHAO.get_width()
        if self.x2 + IMAGEM_CHAO.get_width() < 0:
            self.x2 = self.x1 + IMAGEM_CHAO.get_width()

    def desenhar(self, tela):
        tela.blit(IMAGEM_CHAO, (self.x1, self.y))
        tela.blit(IMAGEM_CHAO, (self.x2, self.y))


def desenhar_tela(tela, passaros, canos, chao, pontos):
    tela.blit(IMAGEM_BACKGROUND, (0, 0))
    for passaro in passaros:
        passaro.desenhar(tela)
    for cano in canos:
        cano.desenhar(tela)
    texto = FONTE_PONTOS.render(f"Pontuação: {pontos}", 1, (255, 255, 255))
    tela.blit(texto, (TELA_LARGURA - 10 - texto.get_width(), 10))
    chao.desenhar(tela)
    pygame.display.update()


class Jogo:
    def __init__(self):
        self.passaros = [Passaro(230, 350)]
        self.chao = Chao(730)
        self.canos = [Cano(700)]
        self.tela = pygame.display.set_mode((TELA_LARGURA, TELA_ALTURA))
        self.pontos = 0
        self.relogio = pygame.time.Clock()
        self.game_over = False

    def exibir_game_over(self):
        self.tela.blit(IMAGEM_GAMEOVER, (-30, -300))
        texto_pontuacao = FONTE_PONTOS.render(f"Pontuação: {self.pontos}", 1, (255, 255, 255))
        self.tela.blit(texto_pontuacao, (TELA_LARGURA // 2 - texto_pontuacao.get_width() // 2, 400))
        pygame.display.update()

        esperando_resposta = True
        while esperando_resposta:
            for evento in pygame.event.get():
                if evento.key == pygame.K_BACKSPACE:
                    pygame.quit()
                    quit()
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_SPACE:
                        self.resetar_jogo()

    def resetar_jogo(self):
        self.__init__()
        self.main()

    def desenhar_tela(self):
        self.tela.blit(IMAGEM_BACKGROUND, (0, 0))
        for passaro in self.passaros:
            passaro.desenhar(self.tela)
        for cano in self.canos:
            cano.desenhar(self.tela)

        if self.game_over:
            self.exibir_game_over()
        else:
            texto = FONTE_PONTOS.render(f"Pontuação: {self.pontos}", 1, (255, 255, 255))
            self.tela.blit(texto, (TELA_LARGURA - 10 - texto.get_width(), 10))
            self.chao.desenhar(self.tela)
            pygame.display.update()

    def main(self):
        rodando = True
        while rodando:
            self.relogio.tick(30)

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    rodando = False
                if evento.type == pygame.KEYDOWN and not self.game_over:
                    if evento.key == pygame.K_SPACE:
                        for passaro in self.passaros:
                            passaro.pular()

            if not self.game_over:
                for passaro in self.passaros:
                    passaro.mover()
                self.chao.mover()

                adicionar_cano = False
                remover_canos = []
                for cano in self.canos:
                    for i, passaro in enumerate(self.passaros):
                        if cano.colidir(passaro):
                            self.game_over = True
                            rodando = False
                        if not cano.passou and passaro.x > cano.x:
                            cano.passou = True
                            adicionar_cano = True
                    cano.mover()
                    if cano.x + IMAGEM_CANO.get_width() < 0:
                        remover_canos.append(cano)

                if adicionar_cano:
                    self.pontos += 1
                    self.canos.append(Cano(TELA_LARGURA))

                for cano in remover_canos:
                    self.canos.remove(cano)

                for i, passaro in enumerate(self.passaros):
                    if (passaro.y + passaro.imagem.get_height()) > self.chao.y or passaro.y < 0:
                        self.game_over = True
                        rodando = False

            self.desenhar_tela()


if __name__ == '__main__':
    jogo = Jogo()
    jogo.main()
