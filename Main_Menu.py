import pygame
import random
import main_menu_functions  # Import the new module
import game_logic  # Import the game logic module

# Inicializa o pygame
pygame.init()

# Configurações do jogo
screen_width = 1600
screen_height = 960

# Configurar as dimensões e nome da aplicação
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Jogo de Memória")

# Cor de fundo
background_color = (255, 182, 193)  # Cor de fundo (rosa claro)

# Fonte para o texto
font = pygame.font.Font(None, 74)

# Função para desenhar botões com cantos arredondados
def draw_button(screen, text, font, color, rect, radius=20):
    pygame.draw.rect(screen, color, rect, border_radius=radius)
    text_surface = font.render(text, True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)

# Função para calcular a escala
def calculate_scale(screen_width, screen_height, num_buttons):
    rows = cols = int(num_buttons ** 0.5)
    button_width = (screen_width - (cols + 1) * button_spacing) // cols
    button_height = (screen_height - (rows + 1) * button_spacing) // rows
    return button_width, button_height, rows, cols

# Definir a área de jogo
game_area = pygame.Rect(100, 100, 1400, 760)  # Área de jogo delimitada

# Função para redimensionar a tela mantendo o aspect ratio
def resize_screen(width, height):
    global screen, buttons, game_area
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

# Variável para controlar o modo fullscreen
fullscreen = False

# Função para alternar o modo fullscreen
def toggle_fullscreen():
    global fullscreen, screen
    fullscreen = not fullscreen
    if fullscreen:
        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    else:
        screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)

# Configurações dos botões
button_spacing = 20  # Reduced spacing
num_buttons = 7  # Increased number of buttons
button_color = (0, 128, 0)  # Define button color
button_width, button_height, rows, cols = calculate_scale(screen_width, screen_height, num_buttons)
large_button_width = button_width
large_button_height = button_height
small_button_width = button_width // 2
small_button_height = button_height // 2

# Loop principal do jogo
main_menu_functions.main_menu(screen, game_logic.exibir_jogo)