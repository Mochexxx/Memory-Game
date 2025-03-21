import random
import os

def start_game(theme, num_cards):
    # Initialize game state and variables
    cards = generate_cards(theme, num_cards)
    return cards

def end_game():
    # Handle end of game logic
    pass

def update_score(score):
    # Update the player's score
    pass

def reset_game():
    # Reset the game to its initial state
    pass

def check_win_condition(cards):
    # Check if the win condition has been met
    return all(card["matched"] for card in cards)

def load_game_data():
    # Load game data from a file or database
    pass

def save_game_data():
    # Save current game data to a file or database
    pass

def generate_cards(theme, num_cards):
    # Load images from the selected theme directory
    images = [os.path.join(theme, img) for img in os.listdir(theme) if img.endswith('.png')]
    images = images[:num_cards // 2] * 2
    random.shuffle(images)
    
    cards = []
    sound_folder = "C:\\Users\\pedro\\Documents\\GitHub\\IPC_24-25\\Items_Jogo\\audios_wav_animais"
    for img_path in images:
        sound_path = os.path.join(sound_folder, os.path.basename(img_path).replace(".png", ".wav"))
        cards.append({"image": img_path, "flipped": False, "matched": False, "sound": sound_path if os.path.exists(sound_path) else None})
    
    return cards