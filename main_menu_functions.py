import pygame
import random
import Menu_de_regras
import Adaptacoes
import Como_jogar
import estrutura_de_jogo
import dificuldade_menu

# Define global variables
background_color = (255, 182, 193)  # Cor de fundo (rosa claro)
font = pygame.font.Font(None, 74)
fullscreen = False
game_area = pygame.Rect(100, 100, 1400, 760)  # Área de jogo delimitada

def calculate_scale(screen_width, screen_height, num_buttons):
    button_width = screen_width // 4
    button_height = screen_height // (num_buttons + 1)
    rows = num_buttons // 2
    cols = 2
    return button_width, button_height, rows, cols

# Função para desenhar botões com cantos arredondados
def draw_button(screen, text, font, color, rect, radius=20):
    pygame.draw.rect(screen, color, rect, border_radius=radius)
    text_surface = font.render(text, True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)

# Função para redimensionar a tela mantendo o aspect ratio
def resize_screen(width, height):
    global screen, buttons, game_area, num_buttons
    screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
    game_area = pygame.Rect(100, 100, width - 200, height - 200)  # Ajustar a área de jogo
    button_width, button_height, rows, cols = calculate_scale(width, height, num_buttons)
    large_button_width = button_width
    large_button_height = button_height
    small_button_width = button_width // 2
    small_button_height = button_height // 2
    buttons[0]["rect"] = pygame.Rect(width // 4 - small_button_width // 2, height // 2 - small_button_height, small_button_width, small_button_height)
    buttons[1]["rect"] = pygame.Rect(3 * width // 4 - small_button_width // 2, height // 2 - small_button_height, small_button_width, small_button_height)
    buttons[2]["rect"] = pygame.Rect(width // 4 - small_button_width // 2, height // 2, small_button_width, small_button_height)
    buttons[3]["rect"] = pygame.Rect(3 * width // 4 - small_button_width // 2, height // 2, small_button_width, small_button_height)
    buttons[4]["rect"] = pygame.Rect(width // 2 - large_button_width // 4, height // 4 - large_button_height // 2, large_button_width // 2, large_button_height // 2)
    buttons[5]["rect"] = pygame.Rect(20, height - small_button_height - 20, small_button_width, small_button_height)
    buttons[6]["rect"] = pygame.Rect(width - small_button_width - 20, height - small_button_height - 20, small_button_width, small_button_height)

# Função para alternar o modo fullscreen
def toggle_fullscreen():
    global fullscreen, screen
    fullscreen = not fullscreen
    if fullscreen:
        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    else:
        screen = pygame.display.set_mode((screen.get_width(), screen.get_height()), pygame.RESIZABLE)

# Função para abrir o menu de regras
def abrir_menu_regras(screen):
    Menu_de_regras.exibir_menu_regras(screen)

# Funções para outros menus (exemplo)
def adaptacoes(screen):
    Adaptacoes.exibir_menu_adaptações(screen)

def como_jogar(screen):
    Como_jogar.exibir_menu_como_jogar(screen)

def estrutura_de_jogo(screen):
    estrutura_de_jogo.exibir_menu_estrutura_de_jogo(screen)

def iniciar_jogo(screen, exibir_jogo):
    dificuldade_menu.exibir_menu_dificuldade(screen, lambda num_cartas: exibir_jogo(screen, num_cartas))

def main_menu(screen, exibir_jogo):
    # Configurações dos botões
    button_spacing = 20
    num_buttons = 7
    button_color = (0, 128, 0)
    button_width, button_height, rows, cols = calculate_scale(screen.get_width(), screen.get_height(), num_buttons)
    large_button_width = button_width
    large_button_height = button_height
    small_button_width = button_width // 2
    small_button_height = button_height // 2

    buttons = [
        {"text": "Menu de Regras", "rect": pygame.Rect(screen.get_width() // 4 - small_button_width // 2, screen.get_height() // 2 - small_button_height, small_button_width, small_button_height), "action": lambda: abrir_menu_regras(screen)},
        {"text": "Adaptações", "rect": pygame.Rect(3 * screen.get_width() // 4 - small_button_width // 2, screen.get_height() // 2 - small_button_height, small_button_width, small_button_height), "action": lambda: adaptacoes(screen)},
        {"text": "Como Jogar", "rect": pygame.Rect(screen.get_width() // 4 - small_button_width // 2, screen.get_height() // 2, small_button_width, small_button_height), "action": lambda: como_jogar(screen)},
        {"text": "Estrutura de Jogo", "rect": pygame.Rect(3 * screen.get_width() // 4 - small_button_width // 2, screen.get_height() // 2, small_button_width, small_button_height), "action": lambda: estrutura_de_jogo(screen)},
        {"text": "Iniciar Jogo", "rect": pygame.Rect(screen.get_width() // 2 - large_button_width // 4, screen.get_height() // 4 - large_button_height // 2, large_button_width // 2, large_button_height // 2), "action": lambda: iniciar_jogo(screen, exibir_jogo)},
        {"text": "Fullscreen", "rect": pygame.Rect(20, screen.get_height() - small_button_height - 20, small_button_width, small_button_height), "action": toggle_fullscreen},
        {"text": "Quit", "rect": pygame.Rect(screen.get_width() - small_button_width - 20, screen.get_height() - small_button_height - 20, small_button_width, small_button_height), "action": pygame.quit}
    ]

    # Loop principal do menu
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for button in buttons:
                        if button["rect"].collidepoint(event.pos):
                            button["action"]()
            elif event.type == pygame.VIDEORESIZE and not fullscreen:
                resize_screen(event.w, event.h)

        # Desenhar a imagem de fundo
        screen.fill(background_color)

        # Desenhar a área de jogo
        pygame.draw.rect(screen, (200, 200, 200), game_area)

        # Desenhar os botões
        for button in buttons:
            draw_button(screen, button["text"], font, button_color, button["rect"])

        # Atualizar a tela
        pygame.display.flip()

    pygame.quit()
