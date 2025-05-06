from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from widgets.stats_display import StatsDisplay
from kivy.metrics import dp

class MainMenu(Screen):
    def __init__(self, **kwargs):
        super(MainMenu, self).__init__(**kwargs)
        self.main_layout = None
        self.stats_display = None
        self.game_logo = None  # Reference to the game logo
        self.buttons = []
        # Removed best_times_scores_table
        self.setup_ui()

    def setup_ui(self):
        # Avoid recreating layouts unnecessarily
        if self.main_layout:
            return

        self.main_layout = FloatLayout()
        
        # Menu buttons in a vertical layout
        menu_layout = BoxLayout(
            orientation='vertical', 
            spacing=20, 
            padding=50,
            size_hint=(0.5, 0.7),  # Reduced width to ensure no overlap
            pos_hint={'x': 0.05, 'center_y': 0.5}
        )
        
        # Create a bigger logo that won't be affected by the text size slider
        self.game_logo = Label(
            text="Memory Game",
            font_size=dp(120),  # Much larger fixed size
            size_hint=(1, 0.25),  # Larger size hint
            color=(0.9, 0.2, 0.2, 1),  # Bright red color to make it stand out
            bold=True,
            halign='center',
            valign='middle'
        )
        menu_layout.add_widget(self.game_logo)
        
        button_definitions = [
            ("Start Game", self.start_game),
            ("Options", self.show_options),
            ("Adaptations", self.show_adaptations),
            ("Rules", self.show_rules),
            ("Quit", self.quit_game)
        ]
        
        self.buttons = []
        for text, callback in button_definitions:
            btn = Button(text=text, size_hint=(1, 0.15), background_color=(0, 0.5, 0, 1))
            btn.bind(on_release=callback)
            menu_layout.add_widget(btn)
            self.buttons.append(btn)
        
        self.main_layout.add_widget(menu_layout)
        
        # Stats display widget - adjusted position now that best_times_scores_table is removed
        self.stats_display = StatsDisplay(
            size_hint=(0.4, None),
            pos_hint={'x': 0.55, 'center_y': 0.5}  # Centered vertically in the right side of the screen
        )
        self.main_layout.add_widget(self.stats_display)
        
        self.add_widget(self.main_layout)
    
    def update_font_size(self, font_size_factor):
        """Update font sizes dynamically based on the font size factor."""
        # Do NOT update the game logo font size - it stays fixed
        
        # Update button font sizes
        for btn in self.buttons:
            btn.font_size = 32 * font_size_factor * 0.7
        
        # Update stats display if it implements update_font_size
        if self.stats_display and hasattr(self.stats_display, 'update_font_size'):
            self.stats_display.update_font_size(font_size_factor)
    
    def on_enter(self):
        """Called when the screen is entered"""
        # Always update statistics when returning to the main menu
        app = App.get_running_app()
        casual_mode = app.settings.get('casual_mode', False) if hasattr(app, 'settings') else False

        if self.stats_display:
            print("Updating stats display")
            self.stats_display.update_stats()

    def start_game(self, instance):
        self.manager.current = 'theme_selection'
    
    def show_options(self, instance):
        self.manager.current = 'options_screen'
    
    def show_adaptations(self, instance):
        self.manager.current = 'adaptations_screen'
    
    def show_rules(self, instance):
        self.manager.current = 'rules_submenu'
    
    def quit_game(self, instance):
        App.get_running_app().stop()
