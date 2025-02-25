import pygame
import random
import Menu_de_regras  # Importar o módulo do menu de regras

# Inicializa o pygame
pygame.init()

# Configurações do jogo
screen_width = 1600
screen_height = 960

# Configurar a tela
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Jogo de Memória")

# Carregar a imagem de fundo
background = pygame.image.load("imagem.png")  # diretório da imagem (cor de rosa)
background = pygame.transform.scale(background, (screen_width, screen_height))

# Fonte para o texto
font = pygame.font.Font(None, 74)

# Texto do menu
menu_text = font.render("Pressione R para Regras", True, (255, 255, 255))

# Função para abrir o menu de regras
def abrir_menu_regras():
    Menu_de_regras.exibir_menu_regras(screen)

# Loop principal do jogo
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                abrir_menu_regras()

    # Desenhar a imagem de fundo
    screen.blit(background, (0, 0))

    # Desenhar o texto do menu
    screen.blit(menu_text, (400, 450))

    # Atualizar a tela
    pygame.display.flip()

pygame.quit()