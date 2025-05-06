from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView

class RulesSubmenu(Screen):
    def __init__(self, **kwargs):
        super(RulesSubmenu, self).__init__(**kwargs)
        self.layout = None
        self.button_widgets = []  # Store button references
        self.setup_ui()
        
        # Apply current font size factor from app settings on initialization
        from kivy.app import App
        app = App.get_running_app()
        if hasattr(app, 'settings'):
            font_factor = app.settings.get('text_size_factor', 1.0)
            self.update_font_size(font_factor)

    def setup_ui(self):
        if self.layout:
            return

        self.layout = BoxLayout(orientation='vertical', spacing=20, padding=50)
        
        self.title = Label(
            text="Rules",
            font_size=60,  # Base font size without scaling
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
        
        self.button_widgets = []  # Clear button references
        for text, callback in self.buttons:
            btn = Button(
                text=text,
                size_hint=(1, 0.2),
                background_color=(0, 0.5, 0, 1),
                font_size=32  # Base font size without scaling
            )
            btn.bind(on_release=callback)
            self.layout.add_widget(btn)
            self.button_widgets.append(btn)  # Store reference to button
        
        self.add_widget(self.layout)
    
    def show_how_to_play(self, instance):
        self.manager.current = 'how_to_play_screen'
    
    def show_game_structure(self, instance):
        self.manager.current = 'game_structure_screen'
    
    def reset_menu(self, instance):
        # Reset the layout without recreating widgets
        self.layout.clear_widgets()
        self.setup_ui()
        
        # Re-apply font size after reset
        from kivy.app import App
        app = App.get_running_app()
        if hasattr(app, 'settings'):
            font_factor = app.settings.get('text_size_factor', 1.0)
            self.update_font_size(font_factor)
    
    def go_back(self, instance):
        self.manager.current = 'main_menu'

    def update_font_size(self, font_size_factor):
        """Update font sizes dynamically based on the font size factor."""
        # Apply standard scaling factor of 0.7 to match other screens
        scaled_factor = font_size_factor * 0.7
        self.title.font_size = 60 * scaled_factor
        
        # Update buttons using our stored references 
        for btn in self.button_widgets:
            btn.font_size = 32 * scaled_factor
