import pygame
import random

# Inicializa o pygame
pygame.init()

# Configurações do jogo
screen_width = 1600
screen_height = 960


# Configurar a tela
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Jogo de Memória Acessível")


# Loop principal do jogo
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

  
pygame.quit()


