from kivy.app import App
from kivy.uix.screenmanager import ScreenManager

# Import screens
from screens.main_menu import MainMenu
from screens.game_screen import GameScreen
from screens.theme_selection_screen import ThemeSelectionScreen
from screens.difficulty_selection_screen import DifficultySelectionScreen
from screens.options_screen import OptionsScreen # Add this import
from screens.win_screen import WinScreen
from screens.information_screens import (
    AdaptationsScreen,
    HowToPlayScreen,
    GameStructureScreen
)

class MyScreenManager(ScreenManager):
    pass

class MemoryGameApp(App):
    def __init__(self, **kwargs):
        super(MemoryGameApp, self).__init__(**kwargs)
        # Global settings dictionary
        self.settings = {
            'colorblind_mode': False,
            'audio_assist': False,
            'visual_feedback': True,
            'text_size_factor': 1.0
        }
    
    def build(self):
        sm = MyScreenManager()
        sm.add_widget(MainMenu(name='main_menu'))
        sm.add_widget(GameScreen(name='game_screen'))
        sm.add_widget(ThemeSelectionScreen(name='theme_selection'))
        sm.add_widget(DifficultySelectionScreen(name='difficulty_selection'))
        sm.add_widget(OptionsScreen(name='options_screen')) # Add this line
        sm.add_widget(AdaptationsScreen(name='adaptations_screen'))
        sm.add_widget(HowToPlayScreen(name='how_to_play_screen'))
        sm.add_widget(GameStructureScreen(name='game_structure_screen'))
        sm.add_widget(WinScreen(name='win_screen'))
        return sm

if __name__ == '__main__':
    MemoryGameApp().run()