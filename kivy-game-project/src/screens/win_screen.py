from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

class WinScreen(Screen):
    def __init__(self, **kwargs):
        super(WinScreen, self).__init__(**kwargs)
        self.elapsed_time = 0
        self.current_theme = None
        self.current_difficulty = None
        self.best_times = {}  # Dictionary to store best times by theme and difficulty
        
        # Create the layout
        layout = BoxLayout(orientation='vertical', spacing=20, padding=50)
        
        # Title
        self.title_label = Label(
            text="Parabéns! Você Venceu!",
            font_size=74,
            size_hint=(1, 0.3)
        )
        layout.add_widget(self.title_label)
        
        # Time information
        self.time_label = Label(
            text="Seu tempo: 0s",
            font_size=48,
            size_hint=(1, 0.2)
        )
        layout.add_widget(self.time_label)
        
        # Record information
        self.record_label = Label(
            text="",
            font_size=36,
            size_hint=(1, 0.2),
            color=(1, 0.8, 0, 1)  # Gold color for records
        )
        layout.add_widget(self.record_label)
        
        # Buttons container
        buttons_layout = BoxLayout(orientation='horizontal', spacing=20, size_hint=(1, 0.3))
        
        # Play Again button
        self.play_again_btn = Button(
            text="Jogar Novamente",
            font_size=32,
            background_color=(0, 0.7, 0, 1)
        )
        self.play_again_btn.bind(on_release=self.play_again)
        buttons_layout.add_widget(self.play_again_btn)
        
        # Main Menu button
        self.main_menu_btn = Button(
            text="Menu Principal",
            font_size=32,
            background_color=(0.5, 0, 0, 1)
        )
        self.main_menu_btn.bind(on_release=self.go_to_main_menu)
        buttons_layout.add_widget(self.main_menu_btn)
        
        layout.add_widget(buttons_layout)
        
        self.add_widget(layout)
    
    def set_game_stats(self, time, theme, difficulty):
        self.elapsed_time = time
        self.current_theme = theme
        self.current_difficulty = difficulty
        
        # Update the time label
        self.time_label.text = f"Seu tempo: {self.elapsed_time}s"
        
        # Check if it's a record time
        theme_diff_key = f"{theme}_{difficulty}"
        if theme_diff_key not in self.best_times or self.elapsed_time < self.best_times[theme_diff_key]:
            self.best_times[theme_diff_key] = self.elapsed_time
            self.record_label.text = "Novo Recorde!"
        else:
            self.record_label.text = f"Recorde atual: {self.best_times[theme_diff_key]}s"
    
    def play_again(self, instance):
        # Start a new game with the same theme and difficulty
        game_screen = self.manager.get_screen('game_screen')
        game_screen.apply_theme(self.current_theme, self.current_difficulty)
        self.manager.current = 'game_screen'
    
    def go_to_main_menu(self, instance):
        self.manager.current = 'main_menu'
