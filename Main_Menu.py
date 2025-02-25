import pygame
import random
import Menu_de_regras  # Importar o módulo do menu de regras
import Adaptacoes
import Como_jogar
import estrutura_de_jogo

# Inicializa o pygame
pygame.init()

# Configurações do jogo
screen_width = 1600
screen_height = 960

# Configurar as dimensões e nome da aplicação
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Jogo de Memória")

# Carregar a imagem de fundo
background = pygame.image.load("imagem.png")  # diretório da imagem (cor de rosa)
background = pygame.transform.scale(background, (screen_width, screen_height))

# Fonte para o texto
font = pygame.font.Font(None, 74)

# Função para desenhar botões
def draw_button(screen, text, font, color, rect):
    pygame.draw.rect(screen, color, rect)
    text_surface = font.render(text, True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)

# Função para abrir o menu de regras
def abrir_menu_regras():
    Menu_de_regras.exibir_menu_regras(screen)

# Funções para outros menus (exemplo)
def adaptacoes1():
    Adaptacoes.exibir_menu_adaptações(screen)

def como_jogar2():
    Como_jogar.exibir_menu_como_jogar(screen)

def estrutura_de_jogo3():
    estrutura_de_jogo.exibir_menu_estrutura_de_jogo(screen)

# Configurações dos botões
button_width = 300
button_height = 100
button_color = (0, 128, 255)
button_spacing = 50

buttons = [
    {"text": "Menu de Regras", "rect": pygame.Rect(50, screen_height - 250, button_width, button_height), "action": abrir_menu_regras},
    {"text": "Adaptações", "rect": pygame.Rect(50 + button_width + button_spacing, screen_height - 250, button_width, button_height), "action": adaptacoes1},
    {"text": "Como Jogar", "rect": pygame.Rect(50, screen_height - 250 + button_height + button_spacing, button_width, button_height), "action": como_jogar2},
    {"text": "Estrutura do Jogo", "rect": pygame.Rect(50 + button_width + button_spacing, screen_height - 250 + button_height + button_spacing, button_width, button_height), "action": estrutura_de_jogo3},
    {"text": "Quit", "rect": pygame.Rect(screen_width - button_width - 50, screen_height - button_height - 50, button_width, button_height), "action": pygame.quit}
]

# Loop principal do jogo
def main_menu():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Verifica se o botão esquerdo do mouse foi pressionado
                    for button in buttons:
                        if button["rect"].collidepoint(event.pos):
                            button["action"]()
                            if button["text"] == "Quit":
                                running = False

        # Desenhar a imagem de fundo
        screen.blit(background, (0, 0))

        # Desenhar os botões
        for button in buttons:
            draw_button(screen, button["text"], font, button_color, button["rect"])

        # Atualizar a tela
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main_menu()