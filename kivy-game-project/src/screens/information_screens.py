from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView

class InformationScreenBase(Screen):
    """Base class for information screens with common functionality"""
    
    def get_font_size(self, base_size):
        return base_size * 0.7  # Scale factor to adjust based on testing
        
    def update_text_size(self, instance, value):
        instance.text_size = (instance.width, None)
        
    def update_height(self, instance, value):
        instance.height = value[1]
    
    def go_back(self, instance):
        self.manager.current = 'rules_submenu'

class AdaptationsScreen(InformationScreenBase):
    def __init__(self, **kwargs):
        super(AdaptationsScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', spacing=10, padding=20)
        
        # Title with dynamic font size
        title = Label(
            text="Adaptações",
            font_size=self.get_font_size(74),
            size_hint=(1, 0.2),
            halign='center',
            valign='middle'
        )
        title.bind(size=self.update_text_size)
        layout.add_widget(title)
        
        # Create a scrollable content area
        scroll_view = ScrollView(size_hint=(1, 0.7), do_scroll_x=False)
        content_layout = BoxLayout(orientation='vertical', spacing=15, padding=10, size_hint_y=None)
        content_layout.bind(minimum_height=content_layout.setter('height'))
        
        adaptations = [
            "O jogo possui um modo para jogadores com daltonismo.",
            "O jogo possui um modo para jogadores com deficiência auditiva.",
            "O jogo possui um modo para jogadores com deficiência visual."
        ]
        
        for adaptation in adaptations:
            lbl = Label(
                text=adaptation,
                font_size=self.get_font_size(36),
                size_hint_y=None,
                height=100,
                halign='center',
                valign='middle',
                text_size=(None, None)
            )
            lbl.bind(size=self.update_text_size, texture_size=self.update_height)
            content_layout.add_widget(lbl)
        
        scroll_view.add_widget(content_layout)
        layout.add_widget(scroll_view)
        
        # Back button
        btn = Button(
            text="Voltar",
            size_hint=(1, 0.1),
            background_color=(0, 0.5, 0, 1),
            font_size=self.get_font_size(24)
        )
        btn.bind(on_release=self.go_back)
        layout.add_widget(btn)
        
        self.add_widget(layout)

class HowToPlayScreen(InformationScreenBase):
    def __init__(self, **kwargs):
        super(HowToPlayScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', spacing=10, padding=20)
        
        # Title with dynamic font size
        title = Label(
            text="Como Jogar",
            font_size=self.get_font_size(74),
            size_hint=(1, 0.2),
            halign='center',
            valign='middle'
        )
        title.bind(size=self.update_text_size)
        layout.add_widget(title)
        
        # Create a scrollable content area
        scroll_view = ScrollView(size_hint=(1, 0.7), do_scroll_x=False)
        content_layout = BoxLayout(orientation='vertical', spacing=15, padding=10, size_hint_y=None)
        content_layout.bind(minimum_height=content_layout.setter('height'))
        
        how_to_play = [
            "O jogador deve clicar em duas cartas para virá-las, se as mesmas forem iguais irá pontuar e as cartas permanecerão viradas.",
            "Se as cartas forem diferentes, elas voltarão à posição original.",
            "O jogo termina quando todas as cartas forem viradas.",
            "Existe também um contador de tempo para medir o tempo de jogo.",
            "O jogador pode escolher entre 3 níveis de dificuldade: fácil, médio e difícil.",
            "O jogador pode escolher entre 3 temas: animais, frutas e números."
        ]
        
        for line in how_to_play:
            lbl = Label(
                text=line,
                font_size=self.get_font_size(36),
                size_hint_y=None,
                height=100,
                halign='center',
                valign='middle',
                text_size=(None, None)
            )
            lbl.bind(size=self.update_text_size, texture_size=self.update_height)
            content_layout.add_widget(lbl)
        
        scroll_view.add_widget(content_layout)
        layout.add_widget(scroll_view)
        
        # Back button
        btn = Button(
            text="Voltar",
            size_hint=(1, 0.1),
            background_color=(0, 0.5, 0, 1),
            font_size=self.get_font_size(24)
        )
        btn.bind(on_release=self.go_back)
        layout.add_widget(btn)
        
        self.add_widget(layout)

class GameStructureScreen(InformationScreenBase):
    def __init__(self, **kwargs):
        super(GameStructureScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', spacing=10, padding=20)
        
        # Title with dynamic font size
        title = Label(
            text="Estrutura do Jogo",
            font_size=self.get_font_size(74),
            size_hint=(1, 0.2),
            halign='center',
            valign='middle'
        )
        title.bind(size=self.update_text_size)
        layout.add_widget(title)
        
        # Create a scrollable content area
        scroll_view = ScrollView(size_hint=(1, 0.7), do_scroll_x=False)
        content_layout = BoxLayout(orientation='vertical', spacing=15, padding=10, size_hint_y=None)
        content_layout.bind(minimum_height=content_layout.setter('height'))
        
        game_structure = [
            "O jogo consiste num jogo de tabuleiro onde as cartas inicialmente estarão viradas para baixo.",
            "As cartas possuem formas e padrões diferentes para facilitar a identificação visual.",
            "Cada carta tem um efeito sonoro único (dentro da mesma categoria) para facilitar a memorização.",
            "Há um alto contraste de cores para facilitar a visualização das cartas para jogadores com daltonismo."
        ]
        
        for line in game_structure:
            lbl = Label(
                text=line,
                font_size=self.get_font_size(36),
                size_hint_y=None,
                height=100,
                halign='center',
                valign='middle',
                text_size=(None, None)
            )
            lbl.bind(size=self.update_text_size, texture_size=self.update_height)
            content_layout.add_widget(lbl)
        
        scroll_view.add_widget(content_layout)
        layout.add_widget(scroll_view)
        
        # Back button
        btn = Button(
            text="Voltar",
            size_hint=(1, 0.1),
            background_color=(0, 0.5, 0, 1),
            font_size=self.get_font_size(24)
        )
        btn.bind(on_release=self.go_back)
        layout.add_widget(btn)
        
        self.add_widget(layout)
