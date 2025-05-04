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
            text="Menu ESC",
            font_size=74,
            size_hint=(1, 0.2),
            halign='center',
            valign='middle'
        )
        layout.add_widget(title)

        # Buttons
        buttons = [
            ("Voltar ao Menu Principal", self.go_to_main_menu),
            ("Retomar Jogo", self.resume_game)
        ]

        for text, callback in buttons:
            btn = Button(
                text=text,
                size_hint=(1, 0.2),
                background_color=(0, 0.5, 0, 1)
            )
            btn.bind(on_release=callback)
            layout.add_widget(btn)

        self.add_widget(layout)

    def go_to_main_menu(self, instance):
        self.manager.current = 'main_menu'

    def resume_game(self, instance):
        self.manager.current = 'game_screen'

    def show_options(self, instance):
        self.manager.current = 'options_screen'

    def quit_game(self, instance):
        from kivy.app import App
        App.get_running_app().stop()