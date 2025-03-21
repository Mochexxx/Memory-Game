from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock

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
    
    def show_match(self):
        self.manager.current = 'match_screen'
        Clock.schedule_once(self.hide_match, 1)  # Show the match screen for 1 second
    
    def hide_match(self, dt):
        # Check if we're still on the match screen before transitioning back
        if self.manager.current == 'match_screen':
            self.manager.current = 'game_screen'
