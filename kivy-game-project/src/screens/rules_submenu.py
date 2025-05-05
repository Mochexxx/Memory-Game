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
        
        self.title = Label(
            text="Rules",
            font_size=60,  # Hardcoded font size
            size_hint=(1, 0.15),
            halign='center',
            valign='middle'
        )
        self.layout.add_widget(self.title)
        
        self.buttons = [
            ("How to Play", self.show_how_to_play),
            ("Game Structure", self.show_game_structure),
            ("Back", self.go_back)
        ]
        
        for text, callback in self.buttons:
            btn = Button(
                text=text,
                size_hint=(1, 0.2),
                background_color=(0, 0.5, 0, 1)
            )
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

    def update_font_size(self, font_size_factor):
        """Update font sizes dynamically based on the font size factor."""
        self.title.font_size = 60 * font_size_factor
        for btn in self.layout.children:
            if isinstance(btn, Button):
                btn.font_size = 32 * font_size_factor
