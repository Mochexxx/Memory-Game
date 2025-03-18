from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

class MainMenu(Screen):
    def __init__(self, **kwargs):
        super(MainMenu, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', spacing=20, padding=50)
        
        title = Label(text="Jogo de Memória", font_size=74, size_hint=(1, 0.2))
        layout.add_widget(title)
        
        buttons = [
            ("Iniciar Jogo", self.start_game),
            ("Opções", self.show_options),
            ("Como Jogar", self.show_how_to_play),
            ("Adaptações", self.show_adaptations),
            ("Estrutura do Jogo", self.show_game_structure),
            ("Sair", self.quit_game)
        ]
        
        for text, callback in buttons:
            btn = Button(text=text, size_hint=(1, 0.2), background_color=(0, 0.5, 0, 1))
            btn.bind(on_release=callback)
            layout.add_widget(btn)
        
        self.add_widget(layout)
    
    def start_game(self, instance):
        self.manager.current = 'theme_selection'
    
    def show_options(self, instance):
        self.manager.current = 'options_screen'
    
    def show_how_to_play(self, instance):
        self.manager.current = 'how_to_play_screen'
    
    def show_adaptations(self, instance):
        self.manager.current = 'adaptations_screen'
    
    def show_game_structure(self, instance):
        self.manager.current = 'game_structure_screen'
    
    def quit_game(self, instance):
        App.get_running_app().stop()
