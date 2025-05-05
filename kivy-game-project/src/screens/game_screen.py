from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.clock import Clock
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.core.audio import SoundLoader
from kivy.properties import NumericProperty, StringProperty
from kivy.uix.widget import Widget
import os
import math
from logic.game_logic import start_game, check_win_condition  # Fix the import
from utils.stats_manager import update_stats
from pathlib import Path
from kivy.metrics import dp
from kivy.uix.floatlayout import FloatLayout

# Load the .kv file
from kivy.lang import Builder
kv_file = Path(__file__).parent / 'game_screen.kv'
# Removed the line that loads the KV file since it is missing and not required for the current functionality.
# Builder.load_file(str(kv_file))

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
    return os.path.join('C:', os.sep, 'Users', username, 'Documents', 'GitHub', 'IPC')

def get_card_back_path():
    """Returns the path to the blue card back"""
    project_root = find_project_root()
    return os.path.join(project_root, "Items_Jogo", "Parte_Traseira_Cartas", "cardBack_blue3.png")

def get_wood_texture_path():
    """Returns the path to the wood texture"""
    project_root = find_project_root()
    return os.path.join(project_root, "Items_Jogo", "Icons", "wood_sign.png")

class CardButton(Button):
    card_width = NumericProperty(0)
    card_height = NumericProperty(0)
    card_back_path = StringProperty('')

class WoodLabel(BoxLayout):
    text = StringProperty('')
    font_size = StringProperty('24sp')

class GameScreen(Screen):
    def __init__(self, **kwargs):
        super(GameScreen, self).__init__(**kwargs)
        
        # Main layout
        self.main_layout = BoxLayout(orientation='vertical', spacing=5, padding=0) # Reduced spacing

        # HUD (Score and Timer) - Changed to FloatLayout for positioning
        self.hud_layout = FloatLayout(size_hint_y=0.1) 

        # Score Label
        self.score_label = Label(
            text="Score: 0", 
            size_hint=(0.4, None), 
            height=dp(50),  # Increased height for larger font
            font_size='24sp',  # Increased font size
            font_name='Roboto-Bold',  # Use a wider and bolder font
            pos_hint={'x': 0.05, 'top': 0.95}, 
            opacity=1, 
            disabled=False,
            halign='left', 
            valign='top'
        )
        self.score_label.bind(size=self.score_label.setter('text_size'))

        # Timer Label
        self.timer_label = Label(
            text="Time: 0s", 
            size_hint=(0.4, None), 
            height=dp(50),  # Increased height for larger font
            font_size='24sp',  # Increased font size
            font_name='Roboto-Bold',  # Use a wider and bolder font
            pos_hint={'right': 0.95, 'top': 0.95}, 
            opacity=1, 
            disabled=False,
            halign='right', 
            valign='top'
        )
        self.timer_label.bind(size=self.timer_label.setter('text_size'))

        # Add labels to the layout
        self.hud_layout.add_widget(self.score_label)
        self.hud_layout.add_widget(self.timer_label)
        self.main_layout.add_widget(self.hud_layout)

        # Game grid - Adjusted size_hint_y
        self.game_grid = GridLayout(
            cols=4, 
            spacing=10, 
            padding=10, 
            size_hint=(None, 0.8),  # Adjusted size_hint_y slightly down
            pos_hint={'center_x': 0.5} 
        )
        self.main_layout.add_widget(self.game_grid)
        
        # Buttons - Adjusted size_hint_y
        self.button_layout = BoxLayout(
            size_hint_y=0.1, # Adjusted size_hint_y slightly up
            spacing=10, 
            padding=[10, 5],
        )
        self.reveal_button = Button(
            text="Reveal Cards", 
            size_hint=(None, 0.8), # size_hint_x=None, adjust height if needed
            width=dp(200), # Give it a fixed width or calculate based on text
            pos_hint={'center_x': 0.5}, # Center horizontally
            background_color=(0, 0.7, 0, 1), # Green
            color=(1, 1, 1, 1), 
            font_size='18sp', 
            opacity=0, 
            disabled=True
        )
        self.reveal_button.bind(on_release=self.reveal_cards)
        self.button_layout.add_widget(self.reveal_button)
        # Removed the Spacer widget
        self.main_layout.add_widget(self.button_layout)
        
        # Add main layout to the screen
        self.add_widget(self.main_layout)
        
        # Initialization of variables
        self.cards = []
        self.selected_cards = []
        self.is_checking = False
        self.current_theme = None
        self.current_difficulty = None
        self.multiplier = 1
        self.consecutive_matches = 0
        self.easy_mode_used = False
        self.sounds = {}
        self.card_back_path = get_card_back_path()
        
        # Timer configuration
        self.elapsed_time = 0
        self.timer_event = None
        
        # Score configuration
        self.score = 0
        self.lives = 0  # No longer used
        
        # Grid configuration
        self.grid_cols = 4
        self.grid_rows = 4
        
        # Bind for window resize
        Window.bind(on_resize=self.on_window_resize)
        
        # Update settings and initial layout
        self.update_settings()
        # Call update_card_layout once initially after widgets are created
        Clock.schedule_once(lambda dt: self.update_card_layout()) 
    
    def on_enter(self):
        """Called when the screen is entered. Updates settings display."""
        self.update_settings()
    
    def update_settings(self):
        """Update display settings based on app settings"""
        app = App.get_running_app()
        if hasattr(app, 'settings'):
            self.accessibility_mode = app.settings.get('visual_feedback', True)
            self.colorblind_mode = app.settings.get('colorblind_mode', False)
            self.audio_mode = app.settings.get('audio_assist', False)
            self.score_display = app.settings.get('score_display', True)
            self.timer_display = app.settings.get('timer_display', True)
            self.casual_mode = app.settings.get('casual_mode', False)  # Default to False
            easy_mode_enabled = app.settings.get('easy_mode', False)
        else:
            self.accessibility_mode = True
            self.colorblind_mode = False
            self.audio_mode = False
            self.score_display = True
            self.timer_display = True
            self.casual_mode = False
            easy_mode_enabled = False
        
        # Update HUD visibility
        self.score_label.opacity = 1 if self.score_display else 0
        self.score_label.disabled = not self.score_display
        self.timer_label.opacity = 1 if self.timer_display else 0
        self.timer_label.disabled = not self.timer_display
        
        # Update reveal button visibility and enable/disable state
        # Only show if easy mode is enabled AND it hasn't been used yet
        if easy_mode_enabled and not self.easy_mode_used:
            self.reveal_button.opacity = 1
            self.reveal_button.disabled = False
        else:
            self.reveal_button.opacity = 0
            self.reveal_button.disabled = True
    
    def apply_theme(self, theme, num_cards):
        # Clear the current grid
        self.game_grid.clear_widgets()
        
        # Start the new game
        self.cards = start_game(theme, num_cards)
        self.current_theme = theme
        self.current_difficulty = num_cards
        
        # Calculate the optimal layout
        optimal_cols, card_width, card_height = self.calculate_optimal_grid(len(self.cards))
        self.game_grid.cols = optimal_cols
        
        # Clear selected cards
        self.selected_cards = []
        
        # Add card buttons
        for card in self.cards:
            self.game_grid.add_widget(self.create_card_button(card, card_width, card_height))
        
        # Configure sounds for the current theme
        self.setup_sounds(theme)
        
        # Reset the game
        self.reset_game()
    
    def reset_game(self):
        """Resets the game state, including Easy Mode usage."""
        self.score = 0
        self.lives = 0  # No longer used
        self.easy_mode_used = False  # Reset Easy Mode usage
        self.consecutive_matches = 0
        self.multiplier = 1

        # Update the HUD
        self.score_label.text = f"Score: {self.score}"

        # Reset and start the timer
        self.stop_timer()
        self.start_timer()

        # Re-enable the reveal button if Easy Mode is active
        app = App.get_running_app()
        if app.settings.get('easy_mode', False):
            self.reveal_button.disabled = False
    
    def setup_sounds(self, theme):
        """Configure sounds for the current theme"""
        project_root = find_project_root()
        sound_folder = None
        
        if "baralho_animais" in theme.lower():
            sound_folder = os.path.join(project_root, "Items_Jogo", "audios_wav_animais")
        elif "baralho_numeros" in theme.lower():
            sound_folder = os.path.join(project_root, "Items_Jogo", "audios_numeros_wav")
        else:
            sound_folder = os.path.join(project_root, "Items_Jogo", "audios_wav_animais")
        
        # Clear previous sounds
        for sound in self.sounds.values():
            if sound:
                sound.unload()
        self.sounds.clear()
        
        # Load new sounds
        for card in self.cards:
            base_filename = os.path.basename(card["image"])
            sound_path = os.path.join(sound_folder, base_filename.replace(".png", ".wav"))
            
            if os.path.exists(sound_path):
                self.sounds[card["image"]] = SoundLoader.load(sound_path)
    
    def calculate_optimal_grid(self, num_cards):
        """Calculate the optimal card size based on screen dimensions and grid size"""
        # Card aspect ratio (height/width)
        card_aspect_ratio = 1.5
        
        # Get available space
        screen_width = Window.width
        screen_height = Window.height
        
        # Calculate space available for cards
        available_width = screen_width - 40
        available_height = screen_height * 0.8  # 80% of screen height
        
        # Use the predefined grid size or calculate optimal
        cols = self.grid_cols if hasattr(self, 'grid_cols') else math.ceil(math.sqrt(num_cards))
        rows = self.grid_rows if hasattr(self, 'grid_rows') else math.ceil(num_cards / cols)
        
        # Calculate card dimensions
        card_width = (available_width - (cols - 1) * 10) / cols
        card_height = (available_height - (rows - 1) * 10) / rows
        
        # Apply specific adjustments for 6x6 and 6x7 difficulties
        if cols == 6 and (rows == 6 or rows == 7):
            card_width *= 1.1  # Make cards wider
            card_height *= 1.1  # Make cards 10% taller
        
        # Adjust card size to maintain aspect ratio
        if card_height / card_width > card_aspect_ratio:
            card_height = card_width * card_aspect_ratio
        else:
            card_width = card_height / card_aspect_ratio
        
        return cols, card_width, card_height
    
    def on_window_resize(self, instance, width, height):
        """Handle window resize events by recalculating card layout"""
        if self.cards:
            # Recalculate and update the layout
            self.update_card_layout()
    
    def update_card_layout(self):
        """Update the card layout based on current screen dimensions"""
        if not self.cards:
            return
            
        num_cards = len(self.cards)
        optimal_cols, card_width, card_height = self.calculate_optimal_grid(num_cards)
        
        # Update grid columns
        self.game_grid.cols = optimal_cols
        
        # Calculate the number of rows
        rows = math.ceil(num_cards / optimal_cols)
        
        # Calculate the total grid width based on cards, spacing, and padding
        # Padding: left + right = padding[0] + padding[2]
        # Spacing: (cols - 1) * spacing_x = (optimal_cols - 1) * self.game_grid.spacing[0]
        grid_width = (optimal_cols * card_width + 
                      max(0, optimal_cols - 1) * self.game_grid.spacing[0] + 
                      self.game_grid.padding[0] + self.game_grid.padding[2])
        
        # Set the calculated width for the grid (important for pos_hint centering)
        self.game_grid.width = grid_width
        
        # Update individual card sizes (still necessary)
        for widget in self.game_grid.children:
            if isinstance(widget, CardButton): # Ensure we only resize CardButtons
                widget.size_hint = (None, None)
                widget.size = (card_width, card_height)
    
    def start_timer(self):
        if not self.timer_display:
            return
        
        # Always update the label text immediately when starting/resuming
        self.timer_label.text = f"Time: {self.elapsed_time}s"
        
        # Schedule the interval only if it's not already running
        if self.timer_event is None: 
            self.timer_event = Clock.schedule_interval(self.update_timer, 1)
    
    def update_timer(self, dt):
        if not self.timer_display:
            return
        self.elapsed_time += 1
        self.timer_label.text = f"Time: {self.elapsed_time}s"
    
    def stop_timer(self):
        if not self.timer_display:
            return
        # Stop the timer if it's running
        if self.timer_event:
            self.timer_event.cancel()
            self.timer_event = None
    
    def create_card_button(self, card_data, card_width, card_height):
        """Create a card button with flip animation"""
        btn = CardButton(
            size_hint=(None, None),
            size=(card_width, card_height),
            background_normal=self.card_back_path,
            background_down=self.card_back_path,
            card_width=card_width,
            card_height=card_height,
            card_back_path=self.card_back_path
        )
        
        def on_card_press(instance):
            self.flip_card(instance, card_data)
        
        btn.bind(on_release=on_card_press)
        return btn

    def flip_card(self, instance, card):
        # Prevent flipping cards while checking a match or if card is already flipped/matched
        if self.is_checking or card["flipped"] or card["matched"]:
            return
        
        # Mark the card as flipped immediately to prevent double-clicks
        card["flipped"] = True
        
        # Update the card image immediately with no animation
        instance.background_normal = card["image"]
        instance.background_down = card["image"]
        
        # Add to selected cards
        self.selected_cards.append((instance, card))
        
        # Play sound if enabled
        app = App.get_running_app()
        if app.settings.get('audio_assist', False):
            if card["image"] in self.sounds and self.sounds[card["image"]]:
                self.sounds[card["image"]].play()
        
        # Check for match immediately if we have two cards
        if len(self.selected_cards) == 2:
            self.is_checking = True
            Clock.schedule_once(self.check_match, 0.5)  # Keep a small delay for better UX
    
    def check_match(self, dt):
        # Make sure we have exactly 2 cards to check
        if len(self.selected_cards) != 2:
            print(f"Warning: check_match called with {len(self.selected_cards)} cards")
            self.is_checking = False
            return
        
        # Get the card data for easier reference
        widget1, card1 = self.selected_cards[0]
        widget2, card2 = self.selected_cards[1]
        is_match = card1["image"] == card2["image"]
            
        if is_match:
            # This is a match! Mark cards as matched
            card1["matched"] = True
            card2["matched"] = True
            self.consecutive_matches += 1
            self.multiplier = min(self.consecutive_matches, 5)  # Cap multiplier at 5
            self.score += 1 * self.multiplier
            if self.score_display:
                self.score_label.text = f"Score: {self.score}"
            
            # Simplified solution: Just check if this is the last pair
            total_pairs = len(self.cards) // 2
            matched_pairs = sum(1 for card in self.cards if card["matched"]) // 2
            
            # If NOT the last pair (at least one pair is still missing), show the match screen
            if matched_pairs < total_pairs:
                match_screen = self.manager.get_screen('match_screen')
                match_screen.show_match()
            
            # Clear selected cards and allow new selections immediately
            self.selected_cards = []
            self.is_checking = False
        else:
            self.consecutive_matches = 0
            self.multiplier = 1
            self.score = max(self.score, 0)  # Score remains non-negative
            if self.score_display:
                self.score_label.text = f"Score: {self.score}"
            
            # Turn cards back to face down immediately - no animation
            for widget, card in self.selected_cards:
                card["flipped"] = False
                widget.background_normal = self.card_back_path
                widget.background_down = self.card_back_path
            
            # Clear selected cards and allow new selections
            self.selected_cards = []
            # Small delay to allow player to see the cards before they flip back
            Clock.schedule_once(lambda dt: setattr(self, 'is_checking', False), 0.5)
        
        # Check win condition and ensure we transition to win screen
        if check_win_condition(self.cards):
            print("Win condition met! Stopping the clock and displaying the victory screen.")
            self.stop_timer()
            self.show_win_screen()
    
    def show_win_screen(self):
        print("Showing win screen")  # Debug print
        
        # Save game statistics
        game_data = {
            'score': self.score,
            'time': self.elapsed_time,
            'theme': self.current_theme,
            'difficulty': self.current_difficulty,
            'pairs_matched': len(self.cards) // 2
        }
        update_stats(game_data)
        
        # Pass the elapsed time, theme, and difficulty to the win screen
        win_screen = self.manager.get_screen('win_screen')
        
        # Make sure we have the latest settings
        app = App.get_running_app()
        if hasattr(app, 'settings'):
            self.score_display = app.settings.get('score_display', True)
            self.timer_display = app.settings.get('timer_display', True)
        
        print(f"Settings: show score={self.score_display}, show timer={self.timer_display}")  # Debug print
        
        # Set game stats first
        win_screen.set_game_stats(self.elapsed_time, self.current_theme, self.current_difficulty)
        
        # Display score and time based on settings
        if self.score_display:
            win_screen.display_score(self.score)
        
        # Important: Ensure all changes to the win screen are done before switching to it
        win_screen.update_labels_visibility()
        
        # Switch to win screen directly
        self.manager.current = 'win_screen'
    
    def on_leave(self):
        # Stop the timer when leaving the game screen
        self.stop_timer()

    def reveal_cards(self, instance):
        if self.easy_mode_used:
            return  # Prevent multiple uses

        self.easy_mode_used = True
        self.reveal_button.disabled = True
        self.reveal_button.opacity = 0 # Make button disappear after use

        # Reveal all cards immediately - no animation
        for card, widget in zip(self.cards, self.game_grid.children):
            card["flipped"] = True
            widget.background_normal = card["image"]
            widget.background_down = card["image"]

        # Schedule to hide cards after 2 seconds
        Clock.schedule_once(self.hide_cards, 2)

    def hide_cards(self, dt):
        for card, widget in zip(self.cards, self.game_grid.children):
            if not card["matched"]:  # Only hide unmatched cards
                card["flipped"] = False
                widget.background_normal = self.card_back_path
                widget.background_down = self.card_back_path
    
    def go_back(self, instance):
        pass  # Removed the functionality for the 'Voltar' button

    def set_grid_size(self, grid_size):
        """Set the grid size (columns x rows)"""
        self.grid_cols, self.grid_rows = grid_size
        self.game_grid.cols = self.grid_cols
        self.update_card_layout()

    def get_wood_texture_path(self):
        """Returns the path to the wood texture"""
        return self.wood_texture_path
