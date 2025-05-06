from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.metrics import dp
from kivy.app import App

class DifficultySelectionScreen(Screen):
    def __init__(self, **kwargs):
        super(DifficultySelectionScreen, self).__init__(**kwargs)
        
        # Main layout
        self.main_layout = BoxLayout(orientation='vertical', spacing=dp(20), padding=dp(50))
        
        # Title
        self.title = Label(
            text="Difficulty Selection",
            font_size=74,
            size_hint=(1, 0.2),
            halign='center',
            valign='middle'
        )
        self.main_layout.add_widget(self.title)
        
        # Layout horizontal para as 3 seções
        sections_layout = BoxLayout(orientation='horizontal', spacing=dp(20), size_hint=(1, 0.7))
        
        # Store all labels and buttons for font updating
        self.section_labels = []
        self.all_buttons = []
        
        # Seção Fácil
        easy_section = BoxLayout(orientation='vertical', spacing=dp(10))
        self.easy_label = Label(
            text="Easy",
            font_size=dp(40),
            size_hint=(1, 0.2),
            halign='center',
            valign='middle'
        )
        easy_section.add_widget(self.easy_label)
        self.section_labels.append(self.easy_label)
        
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
            self.all_buttons.append(btn)
        
        # Seção Médio
        medium_section = BoxLayout(orientation='vertical', spacing=dp(10))
        self.medium_label = Label(
            text="Medium",
            font_size=dp(40),
            size_hint=(1, 0.2),
            halign='center',
            valign='middle'
        )
        medium_section.add_widget(self.medium_label)
        self.section_labels.append(self.medium_label)
        
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
            self.all_buttons.append(btn)
        
        # Seção Difícil
        hard_section = BoxLayout(orientation='vertical', spacing=dp(10))
        self.hard_label = Label(
            text="Hard",
            font_size=dp(40),
            size_hint=(1, 0.2),
            halign='center',
            valign='middle'
        )
        hard_section.add_widget(self.hard_label)
        self.section_labels.append(self.hard_label)
        
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
            self.all_buttons.append(btn)
        
        # Adiciona as seções ao layout horizontal
        sections_layout.add_widget(easy_section)
        sections_layout.add_widget(medium_section)
        sections_layout.add_widget(hard_section)
        
        self.main_layout.add_widget(sections_layout)
        
        # Botão Voltar
        self.back_btn = Button(
            text="Back",
            size_hint=(1, 0.1),
            background_color=(0.5, 0, 0, 1),
            font_size=dp(32)
        )
        self.back_btn.bind(on_release=self.go_back)
        self.main_layout.add_widget(self.back_btn)
        self.all_buttons.append(self.back_btn)
        
        self.add_widget(self.main_layout)
        
        # Apply current font size factor from app settings
        app = App.get_running_app()
        if hasattr(app, 'settings'):
            font_factor = app.settings.get('text_size_factor', 1.0)
            self.update_font_size(font_factor)
    
    def update_font_size(self, font_size_factor):
        """Update font sizes dynamically based on the font size factor."""
        # Update title font size
        self.title.font_size = 74 * font_size_factor * 0.7
        
        # Update section label font sizes
        for label in self.section_labels:
            label.font_size = 40 * font_size_factor * 0.7
        
        # Update button font sizes
        for btn in self.all_buttons:
            btn.font_size = 32 * font_size_factor * 0.7
    
    def select_difficulty(self, instance, num_cards, grid_size):
        theme = self.manager.get_screen('theme_selection').selected_theme
        game_screen = self.manager.get_screen('game_screen')
        game_screen.apply_theme(theme, num_cards)
        game_screen.set_grid_size(grid_size)
        self.manager.current = 'game_screen'
    
    def go_back(self, instance):
        self.manager.current = 'theme_selection'
