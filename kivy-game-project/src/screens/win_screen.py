from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.app import App

class WinScreen(Screen):
    def __init__(self, **kwargs):
        super(WinScreen, self).__init__(**kwargs)
        self.elapsed_time = 0
        self.current_theme = None
        self.current_difficulty = None
        self.should_display_score = True
        self.should_display_time = True
        self.best_times = {}  # Dictionary to store best times by theme and difficulty
        
        # Create the layout
        self.layout = BoxLayout(orientation='vertical', spacing=20, padding=50)
        
        # Title - always visible
        self.title_label = Label(
            text="Parabéns! Você Venceu!",
            font_size=74,
            size_hint=(1, 0.4),  # Increased size when other elements are hidden
            halign='center',
            valign='middle'
        )
        self.layout.add_widget(self.title_label)
        
        # Time display container
        self.time_container = BoxLayout(orientation='vertical', size_hint=(1, 0.3))
        
        # Time information
        self.time_label = Label(
            text="Seu tempo: 0s",
            font_size=48,
            size_hint=(1, 0.5)
        )
        self.time_container.add_widget(self.time_label)
        
        # Record information
        self.record_label = Label(
            text="",
            font_size=36,
            size_hint=(1, 0.5),
            color=(1, 0.8, 0, 1)  # Gold color for records
        )
        self.time_container.add_widget(self.record_label)
        
        self.layout.add_widget(self.time_container)
        
        # Score information
        self.score_label = Label(
            text="",
            font_size=32,
            size_hint=(1, 0.2),
            halign='center',
            valign='middle'
        )
        self.layout.add_widget(self.score_label)
        
        # Buttons container - always visible
        self.buttons_layout = BoxLayout(orientation='horizontal', spacing=20, size_hint=(1, 0.3))
        
        # Play Again button
        self.play_again_btn = Button(
            text="Jogar Novamente",
            font_size=32,
            background_color=(0, 0.7, 0, 1)
        )
        self.play_again_btn.bind(on_release=self.play_again)
        self.buttons_layout.add_widget(self.play_again_btn)
        
        # Main Menu button
        self.main_menu_btn = Button(
            text="Menu Principal",
            font_size=32,
            background_color=(0.5, 0, 0, 1)
        )
        self.main_menu_btn.bind(on_release=self.go_to_main_menu)
        self.buttons_layout.add_widget(self.main_menu_btn)
        
        self.layout.add_widget(self.buttons_layout)
        
        self.add_widget(self.layout)
    
    def on_enter(self):
        """Called when the screen is entered"""
        # Update the visibility of the labels based on settings
        print("Win screen entered")  # Debug print
        
        # Check settings from app again to ensure we have latest values
        app = App.get_running_app()
        if hasattr(app, 'settings'):
            self.should_display_score = app.settings.get('score_display', True)
            self.should_display_time = app.settings.get('timer_display', True)
        
        self.update_labels_visibility()
    
    def update_labels_visibility(self):
        """Update the visibility of time and score labels based on settings"""
        print(f"Updating labels - Show time: {self.should_display_time}, Show score: {self.should_display_score}")  # Debug print
        
        # Adjust title size based on what's visible
        if not self.should_display_time and not self.should_display_score:
            self.title_label.size_hint_y = 0.7  # Make title bigger when other elements are hidden
        else:
            self.title_label.size_hint_y = 0.4  # Normal size when other elements are visible
        
        # For time label and record label container
        if self.should_display_time:
            self.time_container.opacity = 1
            self.time_container.size_hint_y = 0.3
            self.time_container.height = self.time_container.minimum_height if hasattr(self.time_container, 'minimum_height') else None
            self.time_label.disabled = False
            self.record_label.disabled = False
        else:
            self.time_container.opacity = 0
            self.time_container.size_hint_y = 0
            self.time_container.height = 0
            self.time_label.disabled = True
            self.record_label.disabled = True
        
        # For score label
        if self.should_display_score:
            self.score_label.opacity = 1
            self.score_label.size_hint_y = 0.2
            self.score_label.disabled = False
        else:
            self.score_label.opacity = 0
            self.score_label.size_hint_y = 0
            self.score_label.disabled = True
        
        # Always keep buttons visible
        self.buttons_layout.size_hint_y = 0.3
        self.play_again_btn.disabled = False
        self.main_menu_btn.disabled = False
        
        # Force layout update
        self.layout.do_layout()
    
    def set_game_stats(self, time, theme, difficulty):
        print(f"Setting game stats: time={time}, theme={theme}, difficulty={difficulty}")  # Add debug print
        
        self.elapsed_time = time
        self.current_theme = theme
        self.current_difficulty = difficulty
        
        # Check settings from app
        app = App.get_running_app()
        if hasattr(app, 'settings'):
            self.should_display_score = app.settings.get('score_display', True)
            self.should_display_time = app.settings.get('timer_display', True)
            print(f"Settings loaded: show_score={self.should_display_score}, show_time={self.should_display_time}")  # Add debug print
        
        # Update the time label
        self.time_label.text = f"Seu tempo: {self.elapsed_time}s"
            
        # Check if it's a record time
        theme_diff_key = f"{theme}_{difficulty}"
        if theme_diff_key not in self.best_times or self.elapsed_time < self.best_times[theme_diff_key]:
            self.best_times[theme_diff_key] = self.elapsed_time
            self.record_label.text = "Novo Recorde!"
        else:
            self.record_label.text = f"Recorde atual: {self.best_times[theme_diff_key]}s"
        
        # Don't call update_labels_visibility() here, let the caller handle it
    
    def display_score(self, score):
        self.score_label.text = f"Score: {score}"
    
    def display_time(self, elapsed_time):
        self.time_label.text = f"Tempo: {elapsed_time}s"
    
    def play_again(self, instance):
        # Start a new game with the same theme and difficulty
        print("Play Again clicked")  # Debug print
        game_screen = self.manager.get_screen('game_screen')
        game_screen.apply_theme(self.current_theme, self.current_difficulty)
        self.manager.current = 'game_screen'
    
    def go_to_main_menu(self, instance):
        print("Main Menu clicked")  # Debug print
        self.manager.current = 'main_menu'
