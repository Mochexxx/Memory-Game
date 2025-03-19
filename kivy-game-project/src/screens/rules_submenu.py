from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

class RulesSubmenu(Screen):
    def __init__(self, **kwargs):
        super(RulesSubmenu, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', spacing=20, padding=50)
        
        title = Label(text="Regras", font_size=74, size_hint=(1, 0.2))
        layout.add_widget(title)
        
        buttons = [
            ("Como Jogar", self.show_how_to_play),
            ("Estrutura do Jogo", self.show_game_structure),
            ("Adaptações", self.show_adaptations),
            ("Voltar", self.go_back)
        ]
        
        for text, callback in buttons:
            btn = Button(text=text, size_hint=(1, 0.2), background_color=(0, 0.5, 0, 1))
            btn.bind(on_release=callback)
            layout.add_widget(btn)
        
        self.add_widget(layout)
    
    def show_how_to_play(self, instance):
        self.manager.current = 'how_to_play_screen'
    
    def show_game_structure(self, instance):
        self.manager.current = 'game_structure_screen'
    
    def show_adaptations(self, instance):
        self.manager.current = 'adaptations_screen'
    
    def go_back(self, instance):
        self.manager.current = 'main_menu'
