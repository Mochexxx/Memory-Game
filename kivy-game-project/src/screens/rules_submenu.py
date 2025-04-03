from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView

class RulesSubmenu(Screen):
    def __init__(self, **kwargs):
        super(RulesSubmenu, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', spacing=20, padding=50)
        
        self.title = Label(text="Regras", font_size=74, size_hint=(1, 0.2))
        self.layout.add_widget(self.title)
        
        self.buttons = [
            ("Como Jogar", self.show_how_to_play),
            ("Estrutura do Jogo", self.show_game_structure),
            ("Adaptações", self.show_adaptations),
            ("Voltar", self.go_back)
        ]
        
        for text, callback in self.buttons:
            btn = Button(text=text, size_hint=(1, 0.2), background_color=(0, 0.5, 0, 1))
            btn.bind(on_release=callback)
            self.layout.add_widget(btn)
        
        self.add_widget(self.layout)
    
    def show_how_to_play(self, instance):
        self.manager.current = 'how_to_play_screen'
    
    def show_game_structure(self, instance):
        self.manager.current = 'game_structure_screen'
    
    def show_adaptations(self, instance):
        # Clear the layout and display the adaptations text
        self.layout.clear_widgets()
        
        self.title.text = "Adaptações"
        self.layout.add_widget(self.title)
        
        scroll_view = ScrollView(size_hint=(1, 0.7), do_scroll_x=False)
        content_layout = BoxLayout(orientation='vertical', spacing=15, padding=10, size_hint_y=None)
        content_layout.bind(minimum_height=content_layout.setter('height'))
        
        adaptations = [
            "O jogo possui um modo para jogadores com daltonismo, aumentando o contraste e utilizando cores adequadas.",
            "O jogo oferece assistência por áudio, fornecendo dicas sonoras e narração para jogadores com deficiência visual.",
            "O jogo inclui feedback visual, com dicas visuais e animações para jogadores com deficiência auditiva.",
            "O modo fácil permite revelar todas as cartas uma vez por jogo, facilitando a experiência para iniciantes."
        ]
        
        for adaptation in adaptations:
            lbl = Label(
                text=adaptation,
                font_size=36,
                size_hint_y=None,
                height=100,
                halign='center',
                valign='middle',
                text_size=(None, None)
            )
            lbl.bind(size=lambda instance, value: setattr(instance, 'text_size', (instance.width, None)))
            content_layout.add_widget(lbl)
        
        scroll_view.add_widget(content_layout)
        self.layout.add_widget(scroll_view)
        
        back_btn = Button(
            text="Voltar",
            size_hint=(1, 0.1),
            background_color=(0.5, 0, 0, 1),
            font_size=32
        )
        back_btn.bind(on_release=self.reset_menu)
        self.layout.add_widget(back_btn)
    
    def reset_menu(self, instance):
        # Reset the layout to the original menu
        self.layout.clear_widgets()
        self.__init__()
    
    def go_back(self, instance):
        self.manager.current = 'main_menu'
