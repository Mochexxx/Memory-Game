from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.clock import Clock
from kivy.app import App
from kivy.core.window import Window
import os
import math
from logic.game_logic import start_game, check_win_condition

class GameScreen(Screen):
    def __init__(self, **kwargs):
        super(GameScreen, self).__init__(**kwargs)
        # Create a main layout that will contain both HUD and card grid
        main_layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        
        # Create a HUD for score and timer
        hud_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.1))
        
        # Score label
        self.score = 0
        self.score_label = Label(text="Score: 0", font_size=24)
        
        # Timer elements
        self.elapsed_time = 0
        self.timer_label = Label(text="Tempo: 0s", font_size=24)
        self.timer_event = None
        
        # Add labels to HUD
        hud_layout.add_widget(self.score_label)
        hud_layout.add_widget(self.timer_label)
        
        # Create grid layout for cards - we'll adjust columns later
        self.layout = GridLayout(spacing=10, padding=20)
        
        # Add both layouts to the main layout
        main_layout.add_widget(hud_layout)
        main_layout.add_widget(self.layout)
        
        self.add_widget(main_layout)
        
        self.cards = []
        self.selected_cards = []
        self.is_checking = False  # Add flag to track if we're currently checking a match
        
        # Track current theme and difficulty for replay
        self.current_theme = None
        self.current_difficulty = None

        # Get accessibility settings from the app
        app = App.get_running_app()
        if hasattr(app, 'settings'):
            self.accessibility_mode = app.settings.get('visual_feedback', True)
            self.colorblind_mode = app.settings.get('colorblind_mode', False)
            self.audio_mode = app.settings.get('audio_assist', False)
        else:
            self.accessibility_mode = True
            self.colorblind_mode = False
            self.audio_mode = False
            
        # Bind to window resize event
        Window.bind(on_resize=self.on_window_resize)
    
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
        # Reset and start the timer
        self.elapsed_time = 0
        self.timer_label.text = "Tempo: 0s"
        # Schedule timer update every second
        self.timer_event = Clock.schedule_interval(self.update_timer, 1)
    
    def update_timer(self, dt):
        self.elapsed_time += 1
        self.timer_label.text = f"Tempo: {self.elapsed_time}s"
    
    def stop_timer(self):
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
        
        for card in self.cards:
            btn = Button(
                size_hint=(None, None),
                size=(card_width, card_height),
                background_normal='back.png',
                background_down='back.png'
            )
            btn.bind(on_release=lambda instance, c=card: self.flip_card(instance, c))
            self.layout.add_widget(btn)
        
        # Reset score and start timer for new game
        self.score = 0
        self.score_label.text = "Score: 0"
        self.stop_timer()  # Make sure to stop any existing timer
        self.start_timer()  # Start a new timer

        # Apply accessibility settings
        if self.colorblind_mode:
            # Apply colorblind-friendly visuals
            print("Using colorblind-friendly visuals")
        
        if self.audio_mode:
            # Initialize audio assistance
            print("Audio assistance enabled")
    
    def flip_card(self, instance, card):
        # Prevent flipping cards while checking a match or if card is already flipped/matched
        if self.is_checking or card["flipped"] or card["matched"]:
            return
            
        card["flipped"] = True
        instance.background_normal = card["image"]
        instance.background_down = card["image"]
        self.selected_cards.append((instance, card))
        
        if len(self.selected_cards) == 2:
            self.is_checking = True  # Set flag to prevent more cards being flipped
            Clock.schedule_once(self.check_match, 1)
    
    def check_match(self, dt):
        # Make sure we have exactly 2 cards to check
        if len(self.selected_cards) != 2:
            self.is_checking = False
            return
            
        if self.selected_cards[0][1]["image"] == self.selected_cards[1][1]["image"]:
            self.selected_cards[0][1]["matched"] = True
            self.selected_cards[1][1]["matched"] = True
            self.score += 1
            self.score_label.text = f"Score: {self.score}"
        else:
            # Only for non-matching cards, flip them back
            self.selected_cards[0][1]["flipped"] = False
            self.selected_cards[1][1]["flipped"] = False
            self.selected_cards[0][0].background_normal = 'back.png'
            self.selected_cards[0][0].background_down = 'back.png'
            self.selected_cards[1][0].background_normal = 'back.png'
            self.selected_cards[1][0].background_down = 'back.png'
        
        # Clear selected cards and allow new selections
        self.selected_cards = []
        self.is_checking = False
        
        # Debug info
        matched_count = sum(1 for card in self.cards if card["matched"])
        total_cards = len(self.cards)
        print(f"Matched cards: {matched_count}/{total_cards}")
        
        # Check win condition and ensure we transition to win screen
        if check_win_condition(self.cards):
            print("Condição de vitória encontrada! A parar o relógio e a dar display da victory screen.")
            self.stop_timer()
            # Use Clock.schedule_once to ensure the transition happens in the next frame
            Clock.schedule_once(lambda dt: self.show_win_screen(), 0.5)
    
    def show_win_screen(self):
        # Pass the elapsed time, theme, and difficulty to the win screen
        win_screen = self.manager.get_screen('win_screen')
        win_screen.set_game_stats(self.elapsed_time, self.current_theme, self.current_difficulty)
        self.manager.current = 'win_screen'
    
    def on_leave(self):
        # Stop the timer when leaving the game screen
        self.stop_timer()
