from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.clock import Clock
from kivy.app import App
from kivy.core.window import Window
from kivy.animation import Animation
from kivy.uix.image import Image
from kivy.core.audio import SoundLoader
import os
import math
from logic.game_logic import start_game, check_win_condition  # Fix the import
from utils.stats_manager import update_stats

class GameScreen(Screen):
    def __init__(self, **kwargs):
        super(GameScreen, self).__init__(**kwargs)
        # Create a main layout that will contain both HUD and card grid
        main_layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        
        # Create a HUD for score and timer
        self.hud_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.1))
        
        # Score label
        self.score = 0
        self.score_label = Label(text="Score: 0", font_size=24)
        
        # Timer elements
        self.elapsed_time = 0
        self.timer_label = Label(text="Tempo: 0s", font_size=24)
        self.timer_event = None
        
        # Get initial accessibility settings from the app
        self.update_settings()
        
        # Create grid layout for cards - we'll adjust columns later
        self.layout = GridLayout(spacing=10, padding=20)
        
        # Add both layouts to the main layout
        main_layout.add_widget(self.hud_layout)
        main_layout.add_widget(self.layout)
        
        self.add_widget(main_layout)
        
        self.cards = []
        self.selected_cards = []
        self.is_checking = False  # Add flag to track if we're currently checking a match
        
        # Track current theme and difficulty for replay
        self.current_theme = None
        self.current_difficulty = None
            
        # Bind to window resize event
        Window.bind(on_resize=self.on_window_resize)
        
        self.multiplier = 1  # Initialize score multiplier
        self.consecutive_matches = 0  # Track consecutive matches

        # Easy mode reveal button
        self.easy_mode_used = False
        self.reveal_button = Button(
            text="Revelar Cartas",
            size_hint=(0.3, 0.05),  # Make the button smaller
            background_color=(0.5, 0.5, 0.5, 1)
        )
        self.reveal_button.bind(on_release=self.reveal_cards)
        self.reveal_button.opacity = 0  # Initially invisible
        main_layout.add_widget(self.reveal_button)

        # Back button
        self.back_button = Button(
            text="Voltar",
            size_hint=(0.3, 0.05),  # Make the button smaller
            background_color=(0.5, 0, 0, 1)
        )
        self.back_button.bind(on_release=self.go_back)
        main_layout.add_widget(self.back_button)

        self.sounds = {}  # Dictionary to store sounds for each card
    
    def update_settings(self):
        """Update display settings based on app settings"""
        app = App.get_running_app()
        if hasattr(app, 'settings'):
            self.accessibility_mode = app.settings.get('visual_feedback', True)
            self.colorblind_mode = app.settings.get('colorblind_mode', False)
            self.audio_mode = app.settings.get('audio_assist', False)
            self.score_display = app.settings.get('score_display', True)
            self.timer_display = app.settings.get('timer_display', True)
        else:
            self.accessibility_mode = True
            self.colorblind_mode = False
            self.audio_mode = False
            self.score_display = True
            self.timer_display = True
        
        # Update HUD based on settings
        self.update_hud()
    
    def update_hud(self):
        """Update the HUD layout based on current settings"""
        self.hud_layout.clear_widgets()
        if self.score_display:
            self.hud_layout.add_widget(self.score_label)
        if self.timer_display:
            self.hud_layout.add_widget(self.timer_label)
    
    def on_enter(self):
        """Called when the screen is entered"""
        # Update settings when entering the screen
        self.update_settings()
    
    def calculate_optimal_grid(self, num_cards):
        """Calculate the optimal number of columns and card size based on screen dimensions"""
        # Card aspect ratio (height/width)
        card_aspect_ratio = 1.5  # standard card ratio is 3:2
        
        # Get available space (accounting for padding that will be adjusted)
        screen_width = Window.width
        screen_height = Window.height
        
        # Calculate space available for cards (accounting for HUD)
        available_width = screen_width - 40  # minimum side padding
        available_height = screen_height - 100  # account for HUD and minimal padding
        
        # For a uniform grid, we want rows and columns to be as close as possible
        # Taking into account the card aspect ratio
        # First, find the square root of card count
        sqrt_count = math.sqrt(num_cards)
        
        # Calculate ideal grid dimensions adjusted for aspect ratio
        # For a perfectly uniform grid, we want:
        # cols/rows = available_width/available_height * 1/card_aspect_ratio
        screen_ratio = available_width / available_height / card_aspect_ratio
        
        # Calculate ideal columns and rows
        ideal_cols = math.sqrt(num_cards * screen_ratio)
        ideal_rows = num_cards / ideal_cols
        
        # Round to integers (favor more columns)
        cols = round(ideal_cols)
        rows = math.ceil(num_cards / cols)
        
        # Check if we need to adjust for better fit
        # Try one less and one more column and see which gives more uniform results
        options = []
        for test_cols in [max(1, cols-1), cols, cols+1]:
            test_rows = math.ceil(num_cards / test_cols)
            # Calculate card dimensions for this configuration
            c_width = (available_width - (test_cols - 1) * self.layout.spacing[0]) / test_cols
            c_height = c_width * card_aspect_ratio
            
            # Check if cards fit vertically
            if test_rows * c_height + (test_rows - 1) * self.layout.spacing[1] > available_height:
                # Adjust height to fit
                c_height = (available_height - (test_rows - 1) * self.layout.spacing[1]) / test_rows
                c_width = c_height / card_aspect_ratio
            
            # Calculate how uniform the grid is
            # Lower score = more uniform
            # We penalize empty cells and non-square layouts
            empty_cells = (test_rows * test_cols) - num_cards
            aspect_diff = abs(1 - ((c_width * test_cols) / (c_height * test_rows)))
            uniformity_score = empty_cells + aspect_diff * 5
            
            options.append((test_cols, c_width, c_height, uniformity_score))
        
        # Choose the most uniform option
        options.sort(key=lambda x: x[3])
        cols, card_width, card_height = options[0][:3]
        rows = math.ceil(num_cards / cols)
        
        # Calculate dynamic padding to center the grid
        horizontal_padding = (screen_width - (cols * card_width + (cols - 1) * self.layout.spacing[0])) / 2
        vertical_padding = (available_height - (rows * card_height + (rows - 1) * self.layout.spacing[1])) / 2
        vertical_padding = max(10, vertical_padding)  # Ensure minimum padding
        
        # Update layout padding for centering
        self.layout.padding = [horizontal_padding, vertical_padding, horizontal_padding, vertical_padding]
        
        # Ensure consistent spacing between cards
        self.layout.spacing = [10, 10]
        
        print(f"Grid: {cols}x{rows} for {num_cards} cards, {(cols*rows)-num_cards} empty cells")
        
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
        self.layout.cols = optimal_cols
        
        # Update card sizes
        for widget in self.layout.children:
            widget.size_hint = (None, None)
            widget.size = (card_width, card_height)
    
    def start_timer(self):
        if not self.timer_display:
            return
        # Reset and start the timer
        self.elapsed_time = 0
        self.timer_label.text = "Tempo: 0s"
        # Schedule timer update every second
        self.timer_event = Clock.schedule_interval(self.update_timer, 1)
    
    def update_timer(self, dt):
        if not self.timer_display:
            return
        self.elapsed_time += 1
        self.timer_label.text = f"Tempo: {self.elapsed_time}s"
    
    def stop_timer(self):
        if not self.timer_display:
            return
        # Stop the timer if it's running
        if self.timer_event:
            self.timer_event.cancel()
            self.timer_event = None
    
    def apply_theme(self, theme, num_cards):
        self.layout.clear_widgets()
        self.cards = start_game(theme, num_cards)
        
        # Store current theme and difficulty for replay
        self.current_theme = theme
        self.current_difficulty = num_cards
        
        # Calculate optimal grid layout
        optimal_cols, card_width, card_height = self.calculate_optimal_grid(len(self.cards))
        self.layout.cols = optimal_cols
        
        # Clear selected cards when starting a new game
        self.selected_cards = []
        
        # Create a card button factory function to avoid lambda issues
        def create_card_button(card_data):
            btn = Button(
                size_hint=(None, None),
                size=(card_width, card_height),
                background_normal='back.png',
                background_down='back.png'
            )
            
            def on_card_press(instance):
                self.flip_card(instance, card_data)
            
            btn.bind(on_release=on_card_press)
            return btn
        
        # Add buttons for each card using the factory function
        for card in self.cards:
            self.layout.add_widget(create_card_button(card))
        
        # Load sounds for each card from the specified folder
        sound_folder = "C:\\Users\\pedro\\Documents\\GitHub\\IPC_24-25\\Items_Jogo\\audios_wav_animais"
        for card in self.cards:
            sound_path = os.path.join(sound_folder, os.path.basename(card["image"]).replace(".png", ".wav"))
            print(f"Loading sound for {card['image']}: {sound_path}")  # Debug print
            if os.path.exists(sound_path):
                self.sounds[card["image"]] = SoundLoader.load(sound_path)
                print(f"Loaded sound for {card['image']}")  # Debug print
            else:
                print(f"Sound file not found for {card['image']}")  # Debug print
        
        # Reset score and start timer for new game
        self.score = 0
        if self.score_display:
            self.score_label.text = "Score: 0"
        self.stop_timer()  # Make sure to stop any existing timer
        self.start_timer()  # Start a new timer

        self.lives = 3  # Reset lives for new game

        # Apply accessibility settings
        if self.colorblind_mode:
            # Apply colorblind-friendly visuals
            print("Using colorblind-friendly visuals")
        
        if self.audio_mode:
            # Initialize audio assistance
            print("Audio assistance enabled")

        # Enable or disable the reveal button based on easy mode setting
        app = App.get_running_app()
        self.easy_mode_used = False
        if app.settings.get('easy_mode', False):
            self.reveal_button.opacity = 1
            self.reveal_button.disabled = False
        else:
            self.reveal_button.opacity = 0
            self.reveal_button.disabled = True
    
    def flip_card(self, instance, card):
        # Prevent flipping cards while checking a match or if card is already flipped/matched
        if self.is_checking or card["flipped"] or card["matched"]:
            return
        
        print(f"Flipping card: {card['image']}")  # Debug print
            
        card["flipped"] = True
        instance.background_normal = card["image"]
        instance.background_down = card["image"]
        self.selected_cards.append((instance, card))
        
        print(f"Selected cards count: {len(self.selected_cards)}")  # Debug print
        
        # Play the sound associated with the card if audio assistance is enabled
        app = App.get_running_app()
        if app.settings.get('audio_assist', False):
            if card["image"] in self.sounds and self.sounds[card["image"]]:
                print(f"Playing sound for {card['image']}")  # Debug print
                self.sounds[card["image"]].play()
            else:
                print(f"No sound loaded for {card['image']}")  # Debug print
        
        if len(self.selected_cards) == 2:
            self.is_checking = True  # Set flag to prevent more cards being flipped
            Clock.schedule_once(self.check_match, 1)
    
    def check_match(self, dt):
        # Make sure we have exactly 2 cards to check
        if len(self.selected_cards) != 2:
            print(f"Warning: check_match called with {len(self.selected_cards)} cards")
            self.is_checking = False
            return
        
        print(f"Checking match between: {self.selected_cards[0][1]['image']} and {self.selected_cards[1][1]['image']}")
            
        if self.selected_cards[0][1]["image"] == self.selected_cards[1][1]["image"]:
            # This is a match! Mark cards as matched
            self.selected_cards[0][1]["matched"] = True
            self.selected_cards[1][1]["matched"] = True
            self.consecutive_matches += 1
            self.multiplier = min(self.consecutive_matches, 5)  # Cap multiplier at 5
            self.score += 1 * self.multiplier
            if self.score_display:
                self.score_label.text = f"Score: {self.score}"
            
            # Solução simplificada: Apenas verifique se este é o último par
            total_pairs = len(self.cards) // 2
            matched_pairs = sum(1 for card in self.cards if card["matched"]) // 2
            
            # Se NÃO for o último par (ainda falta pelo menos um par), mostre a tela de match
            if matched_pairs < total_pairs:
                match_screen = self.manager.get_screen('match_screen')
                match_screen.show_match()
                print(f"✓ Mostrando a tela de match - par {matched_pairs}/{total_pairs}")
            else:
                print(f"✗ Último par encontrado - não mostrando a tela de match")
            
        else:
            self.consecutive_matches = 0
            self.multiplier = 1
            if self.lives > 0:
                self.lives -= 1
            else:
                self.score = max(self.score - 1, 0)  # Ensure score does not go below zero
                if self.score_display:
                    self.score_label.text = f"Score: {self.score}"
            self.selected_cards[0][1]["flipped"] = False
            self.selected_cards[1][1]["flipped"] = False
            self.selected_cards[0][0].background_normal = 'back.png'
            self.selected_cards[0][0].background_down = 'back.png'
            self.selected_cards[1][0].background_normal = 'back.png'
            self.selected_cards[1][0].background_down = 'back.png'
        
        # Clear selected cards and allow new selections
        self.selected_cards = []
        self.is_checking = False
        
        # More accurate debug info
        total_cards = len(self.cards)
        matched_cards = sum(1 for card in self.cards if card["matched"])
        print(f"Final state: Matched cards: {matched_cards}/{total_cards}, Remaining: {total_cards - matched_cards}")
        
        # Check win condition and ensure we transition to win screen
        if check_win_condition(self.cards):
            print("Condição de vitória encontrada! A parar o relógio e a dar display da victory screen.")
            self.stop_timer()
            # Remove delay to prevent any race conditions
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
            return
        
        self.easy_mode_used = True
        self.reveal_button.disabled = True
        
        # Reveal all cards
        for card, widget in zip(self.cards, self.layout.children):
            card["flipped"] = True
            widget.background_normal = card["image"]
            widget.background_down = card["image"]
        
        # Schedule to hide cards after 2 seconds
        Clock.schedule_once(self.hide_cards, 2)
    
    def hide_cards(self, dt):
        for card, widget in zip(self.cards, self.layout.children):
            if not card["matched"]:
                card["flipped"] = False
                widget.background_normal = 'back.png'
                widget.background_down = 'back.png'
    
    def go_back(self, instance):
        self.manager.current = 'main_menu'
