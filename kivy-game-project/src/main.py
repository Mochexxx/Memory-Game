from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.clock import Clock
import os
from logic.game_logic import start_game, check_win_condition

class MainMenu(Screen):
    def __init__(self, **kwargs):
        super(MainMenu, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', spacing=20, padding=50)
        
        title = Label(text="Jogo de Memória", font_size=74, size_hint=(1, 0.2))
        layout.add_widget(title)
        
        buttons = [
            ("Iniciar Jogo", self.start_game),
            ("Opções", self.show_options),
            ("Selecionar Tema", self.select_theme),
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
        # Implement options screen if needed
        pass
    
    def select_theme(self, instance):
        self.manager.current = 'theme_selection'
    
    def show_how_to_play(self, instance):
        self.manager.current = 'how_to_play_screen'
    
    def show_adaptations(self, instance):
        self.manager.current = 'adaptations_screen'
    
    def show_game_structure(self, instance):
        self.manager.current = 'game_structure_screen'
    
    def quit_game(self, instance):
        App.get_running_app().stop()

class GameScreen(Screen):
    def __init__(self, **kwargs):
        super(GameScreen, self).__init__(**kwargs)
        self.layout = GridLayout(cols=4, spacing=10, padding=50)
        self.add_widget(self.layout)
        self.cards = []
        self.selected_cards = []
        self.score = 0
        self.score_label = Label(text="Score: 0", font_size=24, size_hint=(1, 0.1))
        self.add_widget(self.score_label)
    
    def apply_theme(self, theme, num_cards):
        self.layout.clear_widgets()
        self.cards = start_game(theme, num_cards)
        for card in self.cards:
            btn = Button(size_hint=(None, None), size=(100, 150), background_normal='back.png', background_down='back.png')
            btn.bind(on_release=lambda instance, c=card: self.flip_card(instance, c))
            self.layout.add_widget(btn)
    
    def flip_card(self, instance, card):
        if card["flipped"] or card["matched"]:
            return
        card["flipped"] = True
        instance.background_normal = card["image"]
        instance.background_down = card["image"]
        self.selected_cards.append((instance, card))
        if len(self.selected_cards) == 2:
            Clock.schedule_once(self.check_match, 1)
    
    def check_match(self, dt):
        if self.selected_cards[0][1]["image"] == self.selected_cards[1][1]["image"]:
            self.selected_cards[0][1]["matched"] = True
            self.selected_cards[1][1]["matched"] = True
            self.score += 1
            self.score_label.text = f"Score: {self.score}"
        else:
            self.selected_cards[0][1]["flipped"] = False
            self.selected_cards[1][1]["flipped"] = False
            self.selected_cards[0][0].background_normal = 'back.png'
            self.selected_cards[0][0].background_down = 'back.png'
            self.selected_cards[1][0].background_normal = 'back.png'
            self.selected_cards[1][0].background_down = 'back.png'
        self.selected_cards = []
        if check_win_condition(self.cards):
            self.show_win_screen()
    
    def show_win_screen(self):
        # Implement win screen logic
        pass

class ThemeSelectionScreen(Screen):
    def __init__(self, **kwargs):
        super(ThemeSelectionScreen, self).__init__(**kwargs)
        self.selected_theme = "C:\\Users\\pedro\\Documents\\GitHub\\IPC_24-25\\Items_Jogo\\baralho_animais"  # Default theme
        layout = BoxLayout(orientation='vertical', spacing=20, padding=50)
        
        title = Label(text="Seleção de Tema", font_size=74, size_hint=(1, 0.2))
        layout.add_widget(title)
        
        themes = [
            ("Tema Animais", self.select_theme_animals, "C:\\Users\\pedro\\Documents\\GitHub\\IPC_24-25\\Items_Jogo\\baralho_animais"),
            ("Tema Números", self.select_theme_numbers, "C:\\Users\\pedro\\Documents\\GitHub\\IPC_24-25\\Items_Jogo\\baralho_numeros"),
            ("Voltar", self.go_back, None)
        ]
        
        for text, callback, theme in themes:
            btn = ToggleButton(text=text, size_hint=(1, 0.2), background_color=(0, 0.5, 0, 1), group='theme')
            btn.bind(on_release=lambda instance, cb=callback, th=theme: cb(instance, th))
            layout.add_widget(btn)
        
        self.add_widget(layout)
    
    def select_theme_animals(self, instance, theme):
        self.selected_theme = theme
        self.manager.current = 'difficulty_selection'
    
    def select_theme_numbers(self, instance, theme):
        self.selected_theme = theme
        self.manager.current = 'difficulty_selection'
    
    def go_back(self, instance, theme):
        self.manager.current = 'main_menu'

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

class AdaptationsScreen(Screen):
    def __init__(self, **kwargs):
        super(AdaptationsScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', spacing=20, padding=50)
        
        title = Label(text="Adaptações", font_size=74, size_hint=(1, 0.2))
        layout.add_widget(title)
        
        adaptations = [
            "O jogo possui um modo para jogadores com daltonismo.",
            "O jogo possui um modo para jogadores com deficiência auditiva.",
            "O jogo possui um modo para jogadores com deficiência visual."
        ]
        
        for adaptation in adaptations:
            lbl = Label(text=adaptation, font_size=36, size_hint=(1, 0.2))
            layout.add_widget(lbl)
        
        btn = Button(text="Voltar", size_hint=(1, 0.2), background_color=(0, 0.5, 0, 1))
        btn.bind(on_release=self.go_back)
        layout.add_widget(btn)
        
        self.add_widget(layout)
    
    def go_back(self, instance):
        self.manager.current = 'main_menu'

class HowToPlayScreen(Screen):
    def __init__(self, **kwargs):
        super(HowToPlayScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', spacing=20, padding=50)
        
        title = Label(text="Como Jogar", font_size=74, size_hint=(1, 0.2))
        layout.add_widget(title)
        
        how_to_play = [
            "O jogador deve clicar em duas cartas para virá-las, se as mesmas forem iguais irá pontuar e as cartas permanecerão viradas.",
            "Se as cartas forem diferentes, elas voltarão à posição original.",
            "O jogo termina quando todas as cartas forem viradas.",
            "Existe também um contador de tempo para medir o tempo de jogo.",
            "O jogador pode escolher entre 3 níveis de dificuldade: fácil, médio e difícil.",
            "O jogador pode escolher entre 3 temas: animais, frutas e números."
        ]
        
        for line in how_to_play:
            lbl = Label(text=line, font_size=36, size_hint=(1, 0.2))
            layout.add_widget(lbl)
        
        btn = Button(text="Voltar", size_hint=(1, 0.2), background_color=(0, 0.5, 0, 1))
        btn.bind(on_release=self.go_back)
        layout.add_widget(btn)
        
        self.add_widget(layout)
    
    def go_back(self, instance):
        self.manager.current = 'main_menu'

class GameStructureScreen(Screen):
    def __init__(self, **kwargs):
        super(GameStructureScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', spacing=20, padding=50)
        
        title = Label(text="Estrutura do Jogo", font_size=74, size_hint=(1, 0.2))
        layout.add_widget(title)
        
        game_structure = [
            "O jogo consiste num jogo de tabuleiro onde as cartas inicialmente estarão viradas para baixo.",
            "As cartas possuem formas e padrões diferentes para facilitar a identificação visual.",
            "Cada carta tem um efeito sonoro único (dentro da mesma categoria) para facilitar a memorização.",
            "Há um alto contraste de cores para facilitar a visualização das cartas para jogadores com daltonismo."
        ]
        
        for line in game_structure:
            lbl = Label(text=line, font_size=36, size_hint=(1, 0.2))
            layout.add_widget(lbl)
        
        btn = Button(text="Voltar", size_hint=(1, 0.2), background_color=(0, 0.5, 0, 1))
        btn.bind(on_release=self.go_back)
        layout.add_widget(btn)
        
        self.add_widget(layout)
    
    def go_back(self, instance):
        self.manager.current = 'main_menu'

class MyScreenManager(ScreenManager):
    pass

class MyApp(App):
    def build(self):
        sm = MyScreenManager()
        sm.add_widget(MainMenu(name='main_menu'))
        sm.add_widget(GameScreen(name='game_screen'))
        sm.add_widget(ThemeSelectionScreen(name='theme_selection'))
        sm.add_widget(DifficultySelectionScreen(name='difficulty_selection'))
        sm.add_widget(AdaptationsScreen(name='adaptations_screen'))
        sm.add_widget(HowToPlayScreen(name='how_to_play_screen'))
        sm.add_widget(GameStructureScreen(name='game_structure_screen'))
        return sm

if __name__ == '__main__':
    MyApp().run()