from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from widgets.stats_display import StatsDisplay
from widgets.best_times_scores_table import BestTimesScoresTable

class MainMenu(Screen):
    def __init__(self, **kwargs):
        super(MainMenu, self).__init__(**kwargs)
        self.main_layout = None
        self.stats_display = None
        self.best_times_scores_table = None  # New widget
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
        
        title = Label(text="Jogo de Memória", font_size=74, size_hint=(1, 0.2))
        menu_layout.add_widget(title)
        
        buttons = [
            ("Iniciar Jogo", self.start_game),
            ("Opções", self.show_options),
            ("Adaptações", self.show_adaptations),
            ("Regras", self.show_rules),
            ("Sair", self.quit_game)
        ]
        
        for text, callback in buttons:
            btn = Button(text=text, size_hint=(1, 0.2), background_color=(0, 0.5, 0, 1))
            btn.bind(on_release=callback)
            menu_layout.add_widget(btn)
        
        self.main_layout.add_widget(menu_layout)
        
        # Adjusted StatsDisplay widget to be above BestTimesScoresTable and slightly to the left
        self.stats_display = StatsDisplay(
            size_hint=(0.4, None),  # Match width with BestTimesScoresTable
            pos_hint={'x': 0.55, 'y': 0.5}  # Slightly shifted to the left and placed above BestTimesScoresTable
        )
        self.main_layout.add_widget(self.stats_display)

        # Adjusted BestTimesScoresTable widget to be below StatsDisplay and slightly to the left
        self.best_times_scores_table = BestTimesScoresTable(
            size_hint=(0.4, None),  # Match width with StatsDisplay
            pos_hint={'x': 0.55, 'y': 0.2},  # Slightly shifted to the left and placed below StatsDisplay
            opacity=0  # Initially hidden
        )
        self.main_layout.add_widget(self.best_times_scores_table)
        
        self.add_widget(self.main_layout)
    
    def on_enter(self):
        """Called when the screen is entered"""
        # Always update statistics when returning to the main menu
        app = App.get_running_app()
        casual_mode = app.settings.get('casual_mode', False) if hasattr(app, 'settings') else False

        if self.stats_display:
            print("Updating stats display")
            self.stats_display.update_stats()

        if self.best_times_scores_table:
            print("Updating best times and scores table")
            self.best_times_scores_table.update_table()
            # Show or hide the table based on casual mode
            self.best_times_scores_table.opacity = 1 if not casual_mode else 0
    
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
