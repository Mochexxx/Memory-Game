from kivy.uix.screenmanager import Screen
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

class ThemeSelectionScreen(Screen):
    def __init__(self, **kwargs):
        super(ThemeSelectionScreen, self).__init__(**kwargs)
        self.selected_theme = "C:\\Users\\pedri\\Documents\\GitHub\\IPC_24-25\\Items_Jogo\\baralho_animais"  # Default theme
        layout = BoxLayout(orientation='vertical', spacing=20, padding=50)
        
        title = Label(text="Seleção de Tema", font_size=74, size_hint=(1, 0.2))
        layout.add_widget(title)
        
        themes = [
            ("Tema Animais", self.select_theme_animals, "C:\\Users\\pedri\\Documents\\GitHub\\IPC_24-25\\Items_Jogo\\baralho_animais"),
            ("Tema Números", self.select_theme_numbers, "C:\\Users\\pedri\\Documents\\GitHub\\IPC_24-25\\Items_Jogo\\baralho_numeros"),
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
