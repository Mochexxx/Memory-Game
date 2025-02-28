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

# Variável para controlar o modo fullscreen
fullscreen = False

# Função para redimensionar a tela mantendo o aspect ratio
def resize_screen(screen, width, height):
    aspect_ratio = screen_width / screen_height
    if width / height > aspect_ratio:
        new_width = int(height * aspect_ratio)
        new_height = height
    else:
        new_width = width
        new_height = int(width / aspect_ratio)
    return pygame.transform.scale(screen, (new_width, new_height))

# Função para alternar o modo fullscreen
def toggle_fullscreen():
    global fullscreen
    fullscreen = not fullscreen
    if fullscreen:
        pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
    else:
        pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)

# Função para desenhar um botão
def draw_button(screen, text, font, color, rect):
    pygame.draw.rect(screen, color, rect)
    text_surface = font.render(text, True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)

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
            elif event.type == pygame.VIDEORESIZE and not fullscreen:
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                screen = resize_screen(screen, event.w, event.h)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Verifica se o botão esquerdo do mouse foi pressionado
                    if fullscreen_button.collidepoint(event.pos):
                        toggle_fullscreen()

        # Desenhar a imagem de fundo
        screen.blit(background, (0, 0))

        # Desenhar o texto da estrutura do jogo
        y_offset = 100
        for line in estrutura_de_jogo:
            text = font.render(line, True, (255, 255, 255))
            screen.blit(text, (50, y_offset))
            y_offset += 40

        # Desenhar o botão de fullscreen
        fullscreen_button = pygame.Rect(50, screen_height - 100, 200, 50)
        draw_button(screen, "Fullscreen", font, (0, 0, 0), fullscreen_button)

        # Atualizar a tela
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    exibir_menu_estrutura_de_jogo(screen)