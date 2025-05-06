from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
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
            # Dark border color
            Color(0, 0.15, 0, 1)  # Very dark green for the border
            self.border = Rectangle(pos=self.pos, size=self.size)
            # Background color (slightly lighter)
            Color(0, 0.2, 0, 0.8)  # Dark green background
            # Inner rectangle (smaller by the border width)
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

class InformationScreenBase(Screen):
    """Base class for information screens with common functionality"""
    
    def get_font_size(self, base_size):
        # Scale font size based on app settings
        app = App.get_running_app()
        factor = 1.0
        if hasattr(app, 'settings'):
            factor = app.settings.get('text_size_factor', 1.0)
        return base_size * factor * 0.7  # Scale factor to adjust based on testing
        
    def update_text_size(self, instance, value):
        instance.text_size = (instance.width, None)
        
    def update_height(self, instance, value):
        instance.height = value[1]
    
    def go_back(self, instance):
        self.manager.current = 'rules_submenu'
        
    def update_font_size(self, font_size_factor):
        """Update font sizes dynamically based on the font size factor."""
        # This method should be overridden by child classes to update their specific labels
        pass

class AdaptationsScreen(InformationScreenBase):
    def __init__(self, **kwargs):
        super(AdaptationsScreen, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', spacing=10, padding=20)
        
        # Create a bordered container for scrollable content
        bordered_container = BorderedScrollContainer(size_hint=(1, 0.85))
        
        # Create a scrollable content area
        scroll_view = ScrollView(size_hint=(1, 1), do_scroll_x=False)
        content_layout = BoxLayout(orientation='vertical', spacing=15, padding=10, size_hint_y=None)
        content_layout.bind(minimum_height=content_layout.setter('height'))
        
        adaptations = [
            "The game has a mode for players with color blindness.",
            "The game has a mode for players with hearing impairments.",
            "The game has a mode for players with visual impairments."
        ]
        
        self.content_labels = []
        for adaptation in adaptations:
            lbl = BackgroundLabel(
                text=adaptation,
                font_size=self.get_font_size(36),
                size_hint_y=None,
                height=100,
                halign='center',
                valign='middle',
                text_size=(None, None)
            )
            lbl.bind(size=self.update_text_size, texture_size=self.update_height)
            content_layout.add_widget(lbl)
            self.content_labels.append(lbl)
        
        scroll_view.add_widget(content_layout)
        bordered_container.add_widget(scroll_view)
        self.layout.add_widget(bordered_container)
        
        # Back button
        self.back_button = Button(
            text="Back",
            size_hint=(1, 0.15),
            background_color=(0, 0.5, 0, 1),
            font_size=self.get_font_size(24)
        )
        self.back_button.bind(on_release=self.go_back)
        self.layout.add_widget(self.back_button)
        
        self.add_widget(self.layout)
        
    def update_font_size(self, font_size_factor):
        """Update font sizes dynamically based on the font size factor."""
        # Update content labels font sizes
        for label in self.content_labels:
            label.font_size = 36 * font_size_factor * 0.7
        
        # Update back button font size
        self.back_button.font_size = 24 * font_size_factor * 0.7

class HowToPlayScreen(InformationScreenBase):
    def __init__(self, **kwargs):
        super(HowToPlayScreen, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', spacing=10, padding=20)
        
        # Title with dynamic font size
        self.title = Label(
            text="How to Play",
            font_size=self.get_font_size(74),
            size_hint=(1, 0.15),
            halign='center',
            valign='middle'
        )
        self.title.bind(size=self.update_text_size)
        self.layout.add_widget(self.title)
        
        # Create a bordered container for scrollable content - slightly smaller than before
        bordered_container = BorderedScrollContainer(size_hint=(1, 0.7))
        
        # Create a scrollable content area
        scroll_view = ScrollView(size_hint=(1, 1), do_scroll_x=False)
        content_layout = BoxLayout(orientation='vertical', spacing=30, padding=10, size_hint_y=None)
        content_layout.bind(minimum_height=content_layout.setter('height'))
        
        how_to_play = [
            "The player must click on two cards to flip them. If they match, the player scores, and the cards remain flipped.",
            "If the cards are different, they return to their original position.",
            "The game ends when all cards are flipped.",
            "There is also a timer to measure the game duration.",
            "The player can choose between 3 difficulty levels: easy, medium, and hard.",
            "The player can choose between 3 themes: animals, fruits, and numbers."
        ]
        
        self.content_labels = []
        for line in how_to_play:
            lbl = BackgroundLabel(
                text=line,
                font_size=self.get_font_size(36),
                size_hint_y=None,
                height=100,
                halign='center',
                valign='middle',
                text_size=(None, None)
            )
            lbl.bind(size=self.update_text_size, texture_size=self.update_height)
            content_layout.add_widget(lbl)
            self.content_labels.append(lbl)
        
        scroll_view.add_widget(content_layout)
        bordered_container.add_widget(scroll_view)
        self.layout.add_widget(bordered_container)
        
        # Back button
        self.back_button = Button(
            text="Back",
            size_hint=(1, 0.15),
            background_color=(0, 0.5, 0, 1),
            font_size=self.get_font_size(24)
        )
        self.back_button.bind(on_release=self.go_back)
        self.layout.add_widget(self.back_button)
        
        self.add_widget(self.layout)
        
    def update_font_size(self, font_size_factor):
        """Update font sizes dynamically based on the font size factor."""
        # Update title font size
        self.title.font_size = 74 * font_size_factor * 0.7
        
        # Update content labels font sizes
        for label in self.content_labels:
            label.font_size = 36 * font_size_factor * 0.7
        
        # Update back button font size
        self.back_button.font_size = 24 * font_size_factor * 0.7

class GameStructureScreen(InformationScreenBase):
    def __init__(self, **kwargs):
        super(GameStructureScreen, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', spacing=10, padding=20)
        
        # Title with dynamic font size
        self.title = Label(
            text="Game Structure",
            font_size=self.get_font_size(74),
            size_hint=(1, 0.15),
            halign='center',
            valign='middle'
        )
        self.title.bind(size=self.update_text_size)
        self.layout.add_widget(self.title)
        
        # Create a bordered container for scrollable content - slightly smaller
        bordered_container = BorderedScrollContainer(size_hint=(1, 0.7))
        
        # Create a scrollable content area
        scroll_view = ScrollView(size_hint=(1, 1), do_scroll_x=False)
        content_layout = BoxLayout(orientation='vertical', spacing=30, padding=10, size_hint_y=None)
        content_layout.bind(minimum_height=content_layout.setter('height'))
        
        game_structure = [
            "The game consists of a board game where the cards are initially face down.",
            "The cards have different shapes and patterns to facilitate visual identification.",
            "Each card has a unique sound effect (within the same category) to aid memorization.",
            "For colorblind players, cards can be displayed in black and white to improve visibility."
        ]
        
        self.content_labels = []
        for line in game_structure:
            lbl = BackgroundLabel(
                text=line,
                font_size=self.get_font_size(36),
                size_hint_y=None,
                height=100,
                halign='center',
                valign='middle',
                text_size=(None, None)
            )
            lbl.bind(size=self.update_text_size, texture_size=self.update_height)
            content_layout.add_widget(lbl)
            self.content_labels.append(lbl)
        
        scroll_view.add_widget(content_layout)
        bordered_container.add_widget(scroll_view)
        self.layout.add_widget(bordered_container)
        
        # Back button
        self.back_button = Button(
            text="Back",
            size_hint=(1, 0.15),
            background_color=(0, 0.5, 0, 1),
            font_size=self.get_font_size(24)
        )
        self.back_button.bind(on_release=self.go_back)
        self.layout.add_widget(self.back_button)
        
        self.add_widget(self.layout)
        
    def update_font_size(self, font_size_factor):
        """Update font sizes dynamically based on the font size factor."""
        # Update title font size
        self.title.font_size = 74 * font_size_factor * 0.7
        
        # Update content labels font sizes
        for label in self.content_labels:
            label.font_size = 36 * font_size_factor * 0.7
        
        # Update back button font size
        self.back_button.font_size = 24 * font_size_factor * 0.7
