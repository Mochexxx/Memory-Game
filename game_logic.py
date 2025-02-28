import pygame
import random
from dificuldade_menu import exibir_menu_dificuldade
from main_menu_functions import main_menu

# Inicializa o pygame
pygame.init()

# Configurações do jogo
screen_width = 1600
screen_height = 960
card_spacing = 20

# Fonte para o texto
font = pygame.font.Font(None, 36)
complete_font = pygame.font.Font(None, 74)

# Função para desenhar as cartas
def draw_cards(screen, cards):
    for card in cards:
        if card["flipped"] or card["matched"]:
            pygame.draw.rect(screen, card["color"], card["rect"])
        else:
            pygame.draw.rect(screen, (0, 0, 0), card["rect"])  # Cor do verso das cartas (preto)

# Função para calcular a escala
def calculate_scale(game_area, num_cards):
    if num_cards == 8:
        rows, cols = 2, 4
    elif num_cards == 16:
        rows, cols = 4, 4
    elif num_cards == 32:
        rows, cols = 4, 8
    else:
        rows = cols = int(num_cards ** 0.5)
    
    card_width = (game_area.width - (cols + 1) * card_spacing) // cols
    card_height = (game_area.height - (rows + 1) * card_spacing) // rows
    return card_width, card_height, rows, cols

# Função para exibir a tela de jogo completo
def exibir_tela_completa(screen, num_cartas, main_menu_callback):
    screen.fill((0, 0, 0))
    complete_text = complete_font.render("Jogo Completo!", True, (255, 255, 255))
    screen.blit(complete_text, (screen_width // 2 - complete_text.get_width() // 2, screen_height // 2 - 100))

    buttons = [
        {"text": "Menu Inicial", "rect": pygame.Rect(screen_width // 2 - 150, screen_height // 2, 300, 50), "action": main_menu_callback},
        {"text": "Jogar de Novo", "rect": pygame.Rect(screen_width // 2 - 150, screen_height // 2 + 60, 300, 50), "action": lambda: exibir_jogo(screen, num_cartas)}
    ]

    for button in buttons:
        pygame.draw.rect(screen, (0, 128, 0), button["rect"])
        text_surface = font.render(button["text"], True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=button["rect"].center)
        screen.blit(text_surface, text_rect)

    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for button in buttons:
                        if button["rect"].collidepoint(event.pos):
                            button["action"]()
                            waiting = False

# Função para exibir o jogo
def exibir_jogo(screen, num_cartas):
    global score
    score = 0

    game_area = pygame.Rect(100, 100, screen.get_width() - 200, screen.get_height() - 200)  # Área de jogo delimitada
    card_width, card_height, rows, cols = calculate_scale(game_area, num_cartas)

    # Gerar cores para as cartas
    colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255), (128, 0, 128), (0, 128, 128)]
    colors = colors[:num_cartas // 2] * 2
    random.shuffle(colors)

    cards = []
    for i in range(rows):
        for j in range(cols):
            rect = pygame.Rect(game_area.x + j * (card_width + card_spacing) + card_spacing, game_area.y + i * (card_height + card_spacing) + card_spacing, card_width, card_height)
            cards.append({"rect": rect, "color": colors.pop(), "flipped": False, "matched": False})

    selected_cards = []

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Verifica se o botão esquerdo do mouse foi pressionado
                    for card in cards:
                        if card["rect"].collidepoint(event.pos) and not card["flipped"] and not card["matched"]:
                            card["flipped"] = True
                            selected_cards.append(card)
                            if len(selected_cards) == 2:
                                if selected_cards[0]["color"] == selected_cards[1]["color"]:
                                    selected_cards[0]["matched"] = True
                                    selected_cards[1]["matched"] = True
                                    score += 1
                                else:
                                    pygame.time.wait(1000)
                                    selected_cards[0]["flipped"] = False
                                    selected_cards[1]["flipped"] = False
                                selected_cards = []

        # Verificar se todas as cartas estão viradas
        if all(card["matched"] for card in cards):
            exibir_tela_completa(screen, num_cartas, lambda: main_menu(screen, exibir_jogo))
            running = False

        # Desenhar a imagem de fundo
        screen.fill((0, 0, 0))

        # Desenhar a área de jogo
        pygame.draw.rect(screen, (200, 200, 200), game_area)  # Cor de fundo da área de jogo (cinza claro)

        # Desenhar as cartas
        draw_cards(screen, cards)

        # Desenhar a pontuação
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (50, 10))

        # Atualizar a tela
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    screen = pygame.display.set_mode((screen_width, screen_height))
    exibir_menu_dificuldade(screen, lambda num_cartas: exibir_jogo(screen, num_cartas))
