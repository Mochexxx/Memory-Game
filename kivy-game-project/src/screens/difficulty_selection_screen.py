from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.metrics import dp

class DifficultySelectionScreen(Screen):
    def __init__(self, **kwargs):
        super(DifficultySelectionScreen, self).__init__(**kwargs)
        
        # Main layout
        main_layout = BoxLayout(orientation='vertical', spacing=dp(20), padding=dp(50))
        
        # Title
        title = Label(
            text="Difficulty Selection",
            font_size=74,
            size_hint=(1, 0.2),
            halign='center',
            valign='middle'
        )
        main_layout.add_widget(title)
        
        # Layout horizontal para as 3 seções
        sections_layout = BoxLayout(orientation='horizontal', spacing=dp(20), size_hint=(1, 0.7))
        
        # Seção Fácil
        easy_section = BoxLayout(orientation='vertical', spacing=dp(10))
        easy_label = Label(
            text="Easy",
            font_size=dp(40),
            size_hint=(1, 0.2),
            halign='center',
            valign='middle'
        )
        easy_section.add_widget(easy_label)
        
        # Botões Fácil
        easy_buttons = [
            ("4x4", 16, (4, 4)),
            ("5x4", 20, (5, 4))
        ]
        for text, num_cards, grid_size in easy_buttons:
            btn = Button(
                text=text,
                size_hint=(1, 0.4),
                background_color=(0, 0.5, 0, 1),
                font_size=dp(32)
            )
            btn.bind(on_release=lambda instance, nc=num_cards, gs=grid_size: 
                    self.select_difficulty(instance, nc, gs))
            easy_section.add_widget(btn)
        
        # Seção Médio
        medium_section = BoxLayout(orientation='vertical', spacing=dp(10))
        medium_label = Label(
            text="Medium",
            font_size=dp(40),
            size_hint=(1, 0.2),
            halign='center',
            valign='middle'
        )
        medium_section.add_widget(medium_label)
        
        # Botões Médio
        medium_buttons = [
            ("6x4", 24, (6, 4)),
            ("6x5", 30, (6, 5))
        ]
        for text, num_cards, grid_size in medium_buttons:
            btn = Button(
                text=text,
                size_hint=(1, 0.4),
                background_color=(0, 0.5, 0, 1),
                font_size=dp(32)
            )
            btn.bind(on_release=lambda instance, nc=num_cards, gs=grid_size: 
                    self.select_difficulty(instance, nc, gs))
            medium_section.add_widget(btn)
        
        # Seção Difícil
        hard_section = BoxLayout(orientation='vertical', spacing=dp(10))
        hard_label = Label(
            text="Hard",
            font_size=dp(40),
            size_hint=(1, 0.2),
            halign='center',
            valign='middle'
        )
        hard_section.add_widget(hard_label)
        
        # Botões Difícil
        hard_buttons = [
            ("6x6", 36, (6, 6)),
            ("6x7", 42, (6, 7))
        ]
        for text, num_cards, grid_size in hard_buttons:
            btn = Button(
                text=text,
                size_hint=(1, 0.4),
                background_color=(0, 0.5, 0, 1),
                font_size=dp(32)
            )
            btn.bind(on_release=lambda instance, nc=num_cards, gs=grid_size: 
                    self.select_difficulty(instance, nc, gs))
            hard_section.add_widget(btn)
        
        # Adiciona as seções ao layout horizontal
        sections_layout.add_widget(easy_section)
        sections_layout.add_widget(medium_section)
        sections_layout.add_widget(hard_section)
        
        main_layout.add_widget(sections_layout)
        
        # Botão Voltar
        back_btn = Button(
            text="Back",
            size_hint=(1, 0.1),
            background_color=(0.5, 0, 0, 1),
            font_size=dp(32)
        )
        back_btn.bind(on_release=self.go_back)
        main_layout.add_widget(back_btn)
        
        self.add_widget(main_layout)
    
    def select_difficulty(self, instance, num_cards, grid_size):
        theme = self.manager.get_screen('theme_selection').selected_theme
        game_screen = self.manager.get_screen('game_screen')
        game_screen.apply_theme(theme, num_cards)
        game_screen.set_grid_size(grid_size)
        self.manager.current = 'game_screen'
    
    def go_back(self, instance):
        self.manager.current = 'theme_selection'
