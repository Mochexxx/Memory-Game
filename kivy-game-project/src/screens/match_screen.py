from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.uix.modalview import ModalView
from kivy.graphics import Color, Rectangle

class MatchScreen(Screen):
    def __init__(self, **kwargs):
        super(MatchScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', spacing=20, padding=50)
        
        self.match_label = Label(
            text="Par!",
            font_size=74,
            size_hint=(1, 0.5),
            halign='center',
            valign='middle'
        )
        layout.add_widget(self.match_label)
        
        self.add_widget(layout)
        
        # Create a modal popup for displaying match notification
        self.match_popup = ModalView(
            size_hint=(0.5, 0.3),
            auto_dismiss=False,
            background_color=[0, 0, 0, 0]  # Transparent background
        )
        
        # Popup content
        popup_layout = BoxLayout()
        with popup_layout.canvas.before:
            Color(0, 0.7, 0, 0.8)  # Green semi-transparent background
            self.rect = Rectangle(pos=popup_layout.pos, size=popup_layout.size)
        popup_layout.bind(pos=self.update_rect, size=self.update_rect)
        
        self.popup_label = Label(
            text="Par!",
            font_size=60,
            color=(1, 1, 1, 1)
        )
        popup_layout.add_widget(self.popup_label)
        self.match_popup.add_widget(popup_layout)
    
    def update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size
    
    def show_match(self):
        # Instead of changing screens, show a popup on top of the game screen
        self.match_popup.open()
        Clock.schedule_once(self.hide_match, 1)  # Show the match notification for 1 second
    
    def hide_match(self, dt):
        # Simply dismiss the popup instead of changing screens
        self.match_popup.dismiss()
