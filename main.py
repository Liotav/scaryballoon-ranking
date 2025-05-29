import pygame
import sys
import random
import time
import os

pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Scary Balloon")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (200, 0, 0)
TEXT_COLOR = (0, 255, 0)

font = pygame.font.SysFont("couriernew", 30, bold=True)
big_font = pygame.font.SysFont("couriernew", 45, bold=True)

img_balao = pygame.image.load("imagens/balao.png")
img_balao = pygame.transform.scale(img_balao, (80, 120))

img_susto = pygame.image.load("imagens/susto.png")
img_susto = pygame.transform.scale(img_susto, (800, 600))

pygame.mixer.init()
pygame.mixer.music.load("sons/susto.mp3")

stage = 1
max_stage = 9
baloes = []
largura, altura = 80, 120
inicio_jogo = 0
susto_ativo = False
susto_inicio = None
jogo_ativo = False
venceu = False
nome_jogador = ""
digitando_nome = True
exibir_ranking = False

def gerar_baloes():
    global baloes
    baloes = []
    posicoes_usadas = []
    while len(baloes) < 10:
        x = random.randint(50, 700)
        y = random.randint(50, 450)
        pos = pygame.Rect(x, y, largura, altura)
        if not any(pos.colliderect(p) for p in posicoes_usadas):
            posicoes_usadas.append(pos)
            baloes.append({'rect': pos, 'susto': False})
    sustos = random.sample(baloes, stage)
    for b in sustos:
        b['susto'] = True

def mostrar_texto(texto, y, centro=True, fonte=font, cor=TEXT_COLOR):
    img = fonte.render(texto, True, cor)
    rect = img.get_rect(center=(400, y)) if centro else (20, y)
    screen.blit(img, rect)

def salvar_recorde(nome, stage, tempo):
    with open("recordes.txt", "a") as f:
        f.write(f"{nome} – Stage {stage} – {tempo:.2f}s\n")

def carregar_recordes():
    if not os.path.exists("recordes.txt"):
        return []
    with open("recordes.txt", "r") as f:
        return f.readlines()[-5:]

clock = pygame.time.Clock()
running = True
gerar_baloes()

input_box = pygame.Rect(250, 300, 300, 50)
input_color = RED

while running:
    screen.fill(BLACK)
    mouse_pos = pygame.mouse.get_pos()

    if digitando_nome:
        mostrar_texto("Enter your name to start", 180, fonte=big_font)
        pygame.draw.rect(screen, input_color, input_box, 2)
        nome_img = font.render(nome_jogador, True, WHITE)
        screen.blit(nome_img, (input_box.x + 10, input_box.y + 10))
        mostrar_texto("Press Enter to start the game", 370, fonte=font)

    elif not jogo_ativo and not venceu and not exibir_ranking:
        mostrar_texto("Welcome to SCARY BALLOON", 100, fonte=big_font)
        mostrar_texto("Rules:", 180)
        mostrar_texto("- There are 10 balloons per round", 220)
        mostrar_texto("- Click the right balloon to advance", 250)
        mostrar_texto("- If you click a scary one, you're back to Stage 1!", 280)
        mostrar_texto("- Beat Stage 9 to win!", 310)
        mostrar_texto("Click to Start", 400)

    elif susto_ativo:
        screen.blit(img_susto, (0, 0))
        if time.time() - susto_inicio >= 3:
            pygame.mixer.music.stop()
            salvar_recorde(nome_jogador, stage, time.time() - inicio_jogo)
            stage = 1
            gerar_baloes()
            jogo_ativo = False
            susto_ativo = False

    elif venceu:
        tempo_final = time.time() - inicio_jogo
        mostrar_texto("YOU WIN!", 150, fonte=big_font)
        mostrar_texto(f"Time: {tempo_final:.2f} seconds", 210)
        mostrar_texto("Press any key to view ranking", 280)

    elif exibir_ranking:
        mostrar_texto("HIGH SCORES", 80, fonte=big_font)
        linhas = carregar_recordes()
        y = 150
        for linha in linhas:
            mostrar_texto(linha.strip(), y)
            y += 40
        mostrar_texto("Click to play again", 500)

    else:
        mostrar_texto(f"Stage {stage}", 40)
        for b in baloes:
            screen.blit(img_balao, (b['rect'].x, b['rect'].y))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if digitando_nome:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and nome_jogador.strip() != "":
                    digitando_nome = False
                    jogo_ativo = True
                    inicio_jogo = time.time()
                elif event.key == pygame.K_BACKSPACE:
                    nome_jogador = nome_jogador[:-1]
                else:
                    if len(nome_jogador) < 10:
                        nome_jogador += event.unicode

        elif jogo_ativo and not susto_ativo:
            if event.type == pygame.MOUSEBUTTONDOWN:
                for b in baloes:
                    if b['rect'].collidepoint(event.pos):
                        if b['susto']:
                            susto_ativo = True
                            susto_inicio = time.time()
                            pygame.mixer.music.play()
                        else:
                            if stage < max_stage:
                                stage += 1
                                gerar_baloes()
                            else:
                                venceu = True
                                salvar_recorde(nome_jogador, stage, time.time() - inicio_jogo)

        elif venceu:
            if event.type == pygame.KEYDOWN:
                venceu = False
                exibir_ranking = True

        elif exibir_ranking:
            if event.type == pygame.MOUSEBUTTONDOWN:
                nome_jogador = ""
                digitando_nome = True
                stage = 1
                venceu = False
                exibir_ranking = False
                gerar_baloes()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
