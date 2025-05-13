from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.app import App
from kivy.graphics import Color, Rectangle

class BackgroundLabel(Label):
    """Label class without background - we'll use the container background instead"""
    def __init__(self, **kwargs):
        super(BackgroundLabel, self).__init__(**kwargs)

class BorderedScrollContainer(BoxLayout):
    """A container with a dark border for the scrollable content"""
    def __init__(self, **kwargs):
        super(BorderedScrollContainer, self).__init__(**kwargs)
        with self.canvas.before:
            Color(0, 0.15, 0, 1)  # Very dark green for the border
            self.border = Rectangle(pos=self.pos, size=self.size)
            Color(0, 0.2, 0, 0.8)  # Dark green background
            border_width = 3
            self.background = Rectangle(
                pos=(self.pos[0] + border_width, self.pos[1] + border_width),
                size=(self.size[0] - 2*border_width, self.size[1] - 2*border_width)
            )
        self.bind(pos=self.update_canvas, size=self.update_canvas)
    def update_canvas(self, *args):
        border_width = 3
        self.border.pos = self.pos
        self.border.size = self.size
        self.background.pos = (self.pos[0] + border_width, self.pos[1] + border_width)
        self.background.size = (self.size[0] - 2*border_width, self.size[1] - 2*border_width)

class WinScreen(Screen):
    def __init__(self, **kwargs):
        super(WinScreen, self).__init__(**kwargs)
        self.elapsed_time = 0
        self.current_theme = None
        self.current_difficulty = None
        self.should_display_score = True
        self.should_display_time = True
        self.best_times = {}  # Dictionary to store best times by theme and difficulty
        
        # Create the layout
        self.layout = BoxLayout(orientation='vertical', spacing=20, padding=50)
        
        # Title container with green background
        title_container = BorderedScrollContainer(size_hint=(1, 0.4))
        self.title_label = BackgroundLabel(
            text="Parabéns! Você Venceu!",
            font_size=74,
            size_hint=(1, 1),
            halign='center',
            valign='middle'
        )
        title_container.add_widget(self.title_label)
        self.layout.add_widget(title_container)
        
        # Time display container with green background
        self.time_container = BorderedScrollContainer(size_hint=(1, 0.3))
        time_inner_layout = BoxLayout(orientation='vertical', size_hint=(1, 1))
        self.time_label = BackgroundLabel(
            text="Seu tempo: 0s",
            font_size=48,
            size_hint=(1, 0.5),
            halign='center',
            valign='middle'
        )
        time_inner_layout.add_widget(self.time_label)
        self.record_label = BackgroundLabel(
            text="",
            font_size=36,
            size_hint=(1, 0.5),
            color=(1, 0.8, 0, 1),
            halign='center',
            valign='middle'
        )
        time_inner_layout.add_widget(self.record_label)
        self.time_container.add_widget(time_inner_layout)
        self.layout.add_widget(self.time_container)
        
        # Score container with green background
        self.score_container = BorderedScrollContainer(size_hint=(1, 0.2))
        self.score_label = BackgroundLabel(
            text="",
            font_size=32,
            size_hint=(1, 1),
            halign='center',
            valign='middle'
        )
        self.score_container.add_widget(self.score_label)
        self.layout.add_widget(self.score_container)
        
        # Buttons container - always visible
        self.buttons_layout = BoxLayout(orientation='horizontal', spacing=20, size_hint=(1, 0.3))
        
        # Play Again button
        self.play_again_btn = Button(
            text="Jogar Novamente",
            font_size=32,
            background_color=(0, 0.7, 0, 1)
        )
        self.play_again_btn.bind(on_release=self.play_again)
        self.buttons_layout.add_widget(self.play_again_btn)
        
        # Main Menu button
        self.main_menu_btn = Button(
            text="Menu Principal",
            font_size=32,
            background_color=(1, 0, 0, 1)  # Changed to red
        )
        self.main_menu_btn.bind(on_release=self.go_to_main_menu)
        self.buttons_layout.add_widget(self.main_menu_btn)
        
        self.layout.add_widget(self.buttons_layout)
        
        self.add_widget(self.layout)
    
    def on_enter(self):
        """Called when the screen is entered"""
        # Update the visibility of the labels based on settings
        print("Win screen entered")  # Debug print
        
        # Check settings from app again to ensure we have latest values
        app = App.get_running_app()
        if hasattr(app, 'settings'):
            self.should_display_score = app.settings.get('score_display', True)
            self.should_display_time = app.settings.get('timer_display', True)
        
        self.update_labels_visibility()
    
    def update_labels_visibility(self):
        """Update the visibility of time and score labels based on settings"""
        print(f"Updating labels - Show time: {self.should_display_time}, Show score: {self.should_display_score}")  # Debug print
        
        title_container = self.layout.children[-4]  # Title container is the first added (last in children list)
        # Adjust title size based on what's visible
        if not self.should_display_time and not self.should_display_score:
            title_container.size_hint_y = 0.7  # Make title bigger when other elements are hidden
        else:
            title_container.size_hint_y = 0.4  # Normal size when other elements are visible
        
        # For time label and record label container
        if self.should_display_time:
            self.time_container.opacity = 1
            self.time_container.size_hint_y = 0.3
            self.time_container.height = self.time_container.minimum_height if hasattr(self.time_container, 'minimum_height') else None
            self.time_label.disabled = False
            self.record_label.disabled = False
        else:
            self.time_container.opacity = 0
            self.time_container.size_hint_y = 0
            self.time_container.height = 0
            self.time_label.disabled = True
            self.record_label.disabled = True
        
        # For score label
        if self.should_display_score:
            self.score_container.opacity = 1
            self.score_container.size_hint_y = 0.2
            self.score_label.disabled = False
        else:
            self.score_container.opacity = 0
            self.score_container.size_hint_y = 0
            self.score_container.height = 0
            self.score_label.disabled = True
        
        # Always keep buttons visible
        self.buttons_layout.size_hint_y = 0.3
        self.play_again_btn.disabled = False
        self.main_menu_btn.disabled = False
        
        # Force layout update
        self.layout.do_layout()
    
    def set_game_stats(self, time, theme, difficulty):
        print(f"Setting game stats: time={time}, theme={theme}, difficulty={difficulty}")  # Add debug print
        
        self.elapsed_time = time
        self.current_theme = theme
        self.current_difficulty = difficulty
        
        # Check settings from app
        app = App.get_running_app()
        if hasattr(app, 'settings'):
            self.should_display_score = app.settings.get('score_display', True)
            self.should_display_time = app.settings.get('timer_display', True)
            print(f"Settings loaded: show_score={self.should_display_score}, show_time={self.should_display_time}")  # Add debug print
        
        # Update the time label
        self.time_label.text = f"Seu tempo: {self.elapsed_time}s"
            
        # Check if it's a record time
        theme_diff_key = f"{theme}_{difficulty}"
        if theme_diff_key not in self.best_times or self.elapsed_time < self.best_times[theme_diff_key]:
            self.best_times[theme_diff_key] = self.elapsed_time
            self.record_label.text = "Novo Recorde!"
        else:
            self.record_label.text = f"Recorde atual: {self.best_times[theme_diff_key]}s"
        
        # Don't call update_labels_visibility() here, let the caller handle it
    
    def display_score(self, score):
        self.score_label.text = f"Score: {score}"
    
    def display_time(self, elapsed_time):
        self.time_label.text = f"Tempo: {elapsed_time}s"
    
    def play_again(self, instance):
        # Start a new game with the same theme and difficulty
        print("Play Again clicked")  # Debug print
        game_screen = self.manager.get_screen('game_screen')
        game_screen.apply_theme(self.current_theme, self.current_difficulty)
        self.manager.current = 'game_screen'
    
    def go_to_main_menu(self, instance):
        print("Main Menu clicked")  # Debug print
        self.manager.current = 'main_menu'
