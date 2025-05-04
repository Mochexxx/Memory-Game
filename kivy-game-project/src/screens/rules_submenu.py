from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView

class RulesSubmenu(Screen):
    def __init__(self, **kwargs):
        super(RulesSubmenu, self).__init__(**kwargs)
        self.layout = None
        self.setup_ui()

    def setup_ui(self):
        if self.layout:
            return

        self.layout = BoxLayout(orientation='vertical', spacing=20, padding=50)
        
        self.title = Label(text="Regras", font_size=74, size_hint=(1, 0.2))
        self.layout.add_widget(self.title)
        
        self.buttons = [
            ("Como Jogar", self.show_how_to_play),
            ("Estrutura do Jogo", self.show_game_structure),
            ("Voltar", self.go_back)
        ]
        
        for text, callback in self.buttons:
            if text == "Voltar":
                btn = Button(text=text, size_hint=(1, 0.2), background_color=(1, 0, 0, 1))  # Changed to red
            else:
                btn = Button(text=text, size_hint=(1, 0.2), background_color=(0, 0.5, 0, 1))
            btn.bind(on_release=callback)
            self.layout.add_widget(btn)
        
        self.add_widget(self.layout)
    
    def show_how_to_play(self, instance):
        self.manager.current = 'how_to_play_screen'
    
    def show_game_structure(self, instance):
        self.manager.current = 'game_structure_screen'
    
    def reset_menu(self, instance):
        # Reset the layout without recreating widgets
        self.layout.clear_widgets()
        self.setup_ui()
    
    def go_back(self, instance):
        self.manager.current = 'main_menu'
