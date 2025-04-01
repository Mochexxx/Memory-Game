from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.metrics import dp

class DifficultySelectionScreen(Screen):
    def __init__(self, **kwargs):
        super(DifficultySelectionScreen, self).__init__(**kwargs)
        
        # Main layout
        main_layout = BoxLayout(orientation='vertical', spacing=dp(20), padding=dp(50))
        
        # Title
        title = Label(
            text="CONCENTRATION",
            font_size=74,
            size_hint=(1, 0.2),
            halign='center',
            valign='middle'
        )
        main_layout.add_widget(title)
        
        # Grid para os botões de dificuldade
        button_grid = GridLayout(cols=2, spacing=dp(20), size_hint=(1, 0.7))
        
        # Definição das dificuldades com seus respectivos grids
        difficulties = [
            ("EASY 4x4", 16, (4, 4), (0, 0, 1, 1)),    # Azul
            ("EASY 5x4", 20, (5, 4), (0, 0, 1, 1)),    # Azul
            ("MEDIUM 6x4", 24, (6, 4), (0, 0, 1, 1)),  # Azul
            ("MEDIUM 6x5", 30, (6, 5), (0, 0, 1, 1)),  # Azul
            ("HARD 6x6", 36, (6, 6), (0, 0, 1, 1)),    # Azul
            ("HARD 6x7", 42, (6, 7), (0, 0, 1, 1))     # Azul
        ]
        
        # Criar botões de dificuldade
        for text, num_cards, grid_size, color in difficulties:
            btn = Button(
                text=text,
                size_hint=(1, None),
                height=dp(60),
                background_color=color,
                background_normal='',  # Remove o gradiente padrão
                font_size=dp(24)
            )
            btn.bind(on_release=lambda instance, nc=num_cards, gs=grid_size: 
                    self.select_difficulty(instance, nc, gs))
            button_grid.add_widget(btn)
        
        main_layout.add_widget(button_grid)
        
        # Botão Voltar
        back_btn = Button(
            text="Voltar",
            size_hint=(0.3, 0.1),
            pos_hint={'center_x': 0.5},
            background_color=(0.5, 0, 0, 1)
        )
        back_btn.bind(on_release=self.go_back)
        main_layout.add_widget(back_btn)
        
        self.add_widget(main_layout)
    
    def select_difficulty(self, instance, num_cards, grid_size):
        theme = self.manager.get_screen('theme_selection').selected_theme
        game_screen = self.manager.get_screen('game_screen')
        game_screen.apply_theme(theme, num_cards)
        game_screen.set_grid_size(grid_size)  # Novo método para definir o tamanho do grid
        self.manager.current = 'game_screen'
    
    def go_back(self, instance):
        self.manager.current = 'theme_selection'
