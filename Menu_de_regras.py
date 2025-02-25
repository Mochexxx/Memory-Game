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
background = pygame.image.load("imagem.png")  # diretório da imagem de fundo para as regras
background = pygame.transform.scale(background, (screen_width, screen_height))

# Fonte para o texto
font = pygame.font.Font(None, 36)

# Texto das regras
regras_de_jogo = [
    "Regras do Jogo de Memória:",
    "1. Encontre todos os pares de cartas.",
    "2. Clique em uma carta para virá-la.",
    "3. Se duas cartas viradas forem iguais, elas permanecem viradas.",
    "4. Se não forem iguais, elas voltam a ficar viradas para baixo.",
    "5. O jogo termina quando todos os pares forem encontrados.",
    "Pressione ESC para voltar ao menu principal."
]

# Função para exibir o menu de regras
def exibir_menu_regras(screen):
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

        # Desenhar o texto das regras
        y_offset = 100
        for line in regras_de_jogo:
            text = font.render(line, True, (255, 255, 255))
            screen.blit(text, (50, y_offset))
            y_offset += 40

        # Atualizar a tela
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    exibir_menu_regras(screen)