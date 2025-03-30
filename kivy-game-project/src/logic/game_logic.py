import random
import os
from pathlib import Path

def find_project_root():
    """Find the project root directory by looking for known directories"""
    # Start with the directory of this file and go up until we find the project root
    current_dir = Path(__file__).resolve().parent.parent.parent.parent
    
    # Check if we're at the project root
    if (current_dir / "Items_Jogo").exists():
        return str(current_dir)
    if (current_dir.parent / "Items_Jogo").exists():
        return str(current_dir.parent)
    
    # Fallback to a hardcoded path but with the correct username from the file path
    file_path = Path(__file__).resolve()
    username = file_path.parts[2]  # Extract username from path
    return os.path.join('C:', os.sep, 'Users', username, 'Documents', 'GitHub', 'IPC_24-25')

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
    
    # Get project root directory
    project_root = find_project_root()
    
    # Determine the appropriate sound folder based on the theme
    sound_folder = None
    if "baralho_animais" in theme.lower():
        sound_folder = os.path.join(project_root, "Items_Jogo", "audios_wav_animais")
    elif "baralho_numeros" in theme.lower():
        sound_folder = os.path.join(project_root, "Items_Jogo", "audios_numeros_wav")
    else:
        # Fallback to the default folder
        sound_folder = os.path.join(project_root, "Items_Jogo", "audios_wav_animais")
    
    for img_path in images:
        base_filename = os.path.basename(img_path)
        
        # For number theme, cards use 0-indexed filenames (0.png = number 1, 31.png = number 32)
        # Audio files follow the same naming convention (0.wav = spoken "one", etc.)
        sound_path = os.path.join(sound_folder, base_filename.replace(".png", ".wav"))
        
        cards.append({
            "image": img_path, 
            "flipped": False, 
            "matched": False, 
            "sound": sound_path if os.path.exists(sound_path) else None
        })
    
    return cards