import pygame
import game_logic

# Inicializa o pygame
pygame.init()

# Configurações do jogo
screen_width = 1600
screen_height = 960

# Configurar a tela
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Seleção de Dificuldade")

# Carregar a imagem de fundo
background = pygame.image.load("imagem.png")  # diretório da imagem de fundo
background = pygame.transform.scale(background, (screen_width, screen_height))

# Fonte para o texto
font = pygame.font.Font(None, 74)

# Função para desenhar botões
def draw_button(screen, text, font, color, rect):
    pygame.draw.rect(screen, color, rect)
    text_surface = font.render(text, True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)

# Função para calcular a escala
def calculate_scale(screen_width, screen_height, num_buttons):
    rows = cols = int(num_buttons ** 0.5)
    button_width = (screen_width - (cols + 1) * button_spacing) // cols
    button_height = (screen_height - (rows + 1) * button_spacing) // rows
    return button_width, button_height, rows, cols

# Variável para controlar o modo fullscreen
fullscreen = False

# Função para alternar o modo fullscreen
def toggle_fullscreen():
    global fullscreen
    fullscreen = not fullscreen
    if fullscreen:
        pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
    else:
        pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)

# Configurações dos botões
button_spacing = 20  # Reduced spacing
num_buttons = 5  # Increased number of buttons
button_color = (0, 128, 0)  # Define button color
button_width, button_height, rows, cols = calculate_scale(screen_width, screen_height, num_buttons)

buttons = [
    {"text": "Fácil (8 cartas)", "rect": pygame.Rect(650, 200, button_width // 2, button_height // 2), "num_cartas": 8},
    {"text": "Médio (16 cartas)", "rect": pygame.Rect(650, 350, button_width // 2, button_height // 2), "num_cartas": 16},
    {"text": "Difícil (32 cartas)", "rect": pygame.Rect(650, 500, button_width // 2, button_height // 2), "num_cartas": 32},
    {"text": "Fullscreen", "rect": pygame.Rect(650, 650, button_width // 2, button_height // 2), "action": toggle_fullscreen},
    {"text": "Voltar", "rect": pygame.Rect(650, 800, button_width // 2, button_height // 2), "action": pygame.quit}
]

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

# Função para exibir o menu de seleção de dificuldade
def exibir_menu_dificuldade(screen, callback):
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Verifica se o botão esquerdo do mouse foi pressionado
                    for button in buttons:
                        if button["rect"].collidepoint(event.pos):
                            if "num_cartas" in button:
                                callback(button["num_cartas"])
                            elif "action" in button:
                                button["action"]()
                            running = False
            elif event.type == pygame.VIDEORESIZE and not fullscreen:
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                screen = resize_screen(screen, event.w, event.h)

        # Desenhar a imagem de fundo
        screen.blit(background, (0, 0))

        # Desenhar os botões
        for button in buttons:
            draw_button(screen, button["text"], font, button_color, button["rect"])

        # Atualizar a tela
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    exibir_menu_dificuldade(screen, lambda x: None)
