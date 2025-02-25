
import pygame
import sys

# Inicializa o pygame
pygame.init()

# Configurações do jogo
screen_width = 1600
screen_height = 960

# Configurar a tela
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Regras do Jogo de Memória")

# Carregar a imagem de fundo
background = pygame.image.load("imagem.png") # diretório da imagem de fundo para as regras
background = pygame.transform.scale(background, (screen_width, screen_height))

# Fonte para o texto
font = pygame.font.Font(None, 36)

# Texto das regras

como_jogar=[
    " O jogador deve clicar em duas cartas para virá-las, se as mesmas foram iguais irá pontuar e as cartas permanecerão viradas",
    " Se as cartas forem diferentes, elas voltarão a posição original",
    " O jogo termina quando todas as cartas forem viradas"
    " Existe também um contador de tempo para medir o tempo de jogo"
    " O jogador pode escolher entre 3 níveis de dificuldade: fácil, médio e difícil"
    " O jogador pode escolher entre 3 temas: animais, frutas e números"
]


# Loop principal do jogo
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    # Desenhar a imagem de fundo
    screen.blit(background, (0, 0))

    # Desenhar como jogar
    y_offset = 100
    for line in como_jogar:
        text = font.render(line, True, (255, 255, 255))
        screen.blit(text, (50, y_offset))
        y_offset += 40

    # Atualizar a tela
    pygame.display.flip()

pygame.quit()
sys.exit()