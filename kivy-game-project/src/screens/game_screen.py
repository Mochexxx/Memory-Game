from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.clock import Clock
import os
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
        
        # Create grid layout for cards
        self.layout = GridLayout(cols=4, spacing=10, padding=50)
        
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
        
        for card in self.cards:
            btn = Button(size_hint=(None, None), size=(100, 150), background_normal='back.png', background_down='back.png')
            btn.bind(on_release=lambda instance, c=card: self.flip_card(instance, c))
            self.layout.add_widget(btn)
        
        # Reset score and start timer for new game
        self.score = 0
        self.score_label.text = "Score: 0"
        self.stop_timer()  # Make sure to stop any existing timer
        self.start_timer()  # Start a new timer
    
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
