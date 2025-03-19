from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

class DifficultySelectionScreen(Screen):
    def __init__(self, **kwargs):
        super(DifficultySelectionScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', spacing=20, padding=50)
        
        title = Label(text="Seleção de Dificuldade", font_size=74, size_hint=(1, 0.2))
        layout.add_widget(title)
        
        difficulties = [
            ("Fácil (8 cartas)", self.select_difficulty, 8),
            ("Médio (16 cartas)", self.select_difficulty, 16),
            ("Difícil (32 cartas)", self.select_difficulty, 32),
            ("Voltar", self.go_back, None)
        ]
        
        for text, callback, num_cards in difficulties:
            btn = Button(text=text, size_hint=(1, 0.2), background_color=(0, 0.5, 0, 1))
            btn.bind(on_release=lambda instance, cb=callback, nc=num_cards: cb(instance, nc))
            layout.add_widget(btn)
        
        self.add_widget(layout)
    
    def select_difficulty(self, instance, num_cards):
        theme = self.manager.get_screen('theme_selection').selected_theme
        self.manager.get_screen('game_screen').apply_theme(theme, num_cards)
        self.manager.current = 'game_screen'
    
    def go_back(self, instance):
        self.manager.current = 'theme_selection'
