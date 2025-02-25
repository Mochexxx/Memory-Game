import pygame
import sys

# Inicializa o pygame
pygame.init()

# Configurações do jogo
screen_width = 1600
screen_height = 960

# Configurar a tela
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Estrutura do Jogo de Memória")

# Carregar a imagem de fundo
background = pygame.image.load("imagem.png")  # diretório da imagem de fundo para as regras
background = pygame.transform.scale(background, (screen_width, screen_height))

# Fonte para o texto
font = pygame.font.Font(None, 36)

# Texto da estrutura do jogo
estrutura_de_jogo = [
    " O jogo consiste num jogo de tabuleiro onde as cartas inicialmente estarão viradas para baixo.",
    " As cartas possuem formas e padrões diferentes para facilitar a identificação visual",
    " Cada carta tem um efeito sonoro unico ( dentro da mesma categoria) para facilitar a memorização",
    " Há um alto contraste de cores para facilitar a vizualição das cartas para jogadores com daltonismo",
]

# Função para exibir o menu de estrutura do jogo
def exibir_menu_estrutura_de_jogo(screen):
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

        # Desenhar o texto da estrutura do jogo
        y_offset = 100
        for line in estrutura_de_jogo:
            text = font.render(line, True, (255, 255, 255))
            screen.blit(text, (50, y_offset))
            y_offset += 40

        # Atualizar a tela
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    exibir_menu_estrutura_de_jogo(screen)