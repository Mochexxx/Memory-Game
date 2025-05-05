from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label

class EscSubmenu(Screen):
    def __init__(self, **kwargs):
        super(EscSubmenu, self).__init__(**kwargs)

        # Main layout
        layout = BoxLayout(orientation='vertical', spacing=20, padding=50)

        # Title
        title = Label(
            text="ESC Menu",
            font_size=74,
            size_hint=(1, 0.2),
            halign='center',
            valign='middle'
        )
        layout.add_widget(title)

        # Buttons
        buttons = [
            ("Resume Game", self.resume_game),
            ("Back to Main Menu", self.go_to_main_menu)
        ]

        for text, callback in buttons:
            if text == "Resume Game":
                btn = Button(
                    text=text,
                    size_hint=(1, 0.2),
                    background_color=(0, 0.7, 0, 1)  # Green for Resume Game
                )
            else:
                btn = Button(
                    text=text,
                    size_hint=(1, 0.2),
                    background_color=(1, 0, 0, 1)  # Red for other buttons
                )
            btn.bind(on_release=callback)
            layout.add_widget(btn)

        self.add_widget(layout)

    def go_to_main_menu(self, instance):
        # Stop the game and go back to the main menu
        from kivy.app import App
        app = App.get_running_app()
        game_screen = self.manager.get_screen('game_screen')
        game_screen.stop_timer()  # Stop the timer
        self.manager.current = 'main_menu'

    def resume_game(self, instance):
        # Resume the game and restart the timer
        self.manager.current = 'game_screen'
        game_screen = self.manager.get_screen('game_screen')
        game_screen.start_timer()  # Restart the timer

    def show_options(self, instance):
        self.manager.current = 'options_screen'

    def quit_game(self, instance):
        from kivy.app import App
        App.get_running_app().stop()