from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.core.window import Window

# Import settings manager
from utils.settings_manager import load_settings, save_settings
from utils.music_manager import MusicManager

# Import screens
from screens.main_menu import MainMenu
from screens.game_screen import GameScreen
from screens.theme_selection_screen import ThemeSelectionScreen
from screens.difficulty_selection_screen import DifficultySelectionScreen
from screens.options_screen import OptionsScreen
from screens.win_screen import WinScreen
from screens.information_screens import (
    AdaptationsScreen,
    HowToPlayScreen,
    GameStructureScreen
)
from screens.rules_submenu import RulesSubmenu
from screens.adaptations_screen import AdaptationsScreen  # Add this import
from screens.match_screen import MatchScreen  # Ensure this import is present

class MyScreenManager(ScreenManager):
    pass

class MemoryGameApp(App):
    def __init__(self, **kwargs):
        super(MemoryGameApp, self).__init__(**kwargs)
        # Load settings from file
        self.settings = load_settings()
        
        # Initialize the music manager
        self.music_manager = MusicManager()
        
        # Apply window settings
        Window.fullscreen = self.settings.get('fullscreen', True)
    
    def build(self):
        sm = MyScreenManager()
        sm.add_widget(MainMenu(name='main_menu'))
        sm.add_widget(GameScreen(name='game_screen'))
        sm.add_widget(ThemeSelectionScreen(name='theme_selection'))
        sm.add_widget(DifficultySelectionScreen(name='difficulty_selection'))
        sm.add_widget(OptionsScreen(name='options_screen'))
        sm.add_widget(AdaptationsScreen(name='adaptations_screen'))  # Add this line
        sm.add_widget(HowToPlayScreen(name='how_to_play_screen'))
        sm.add_widget(GameStructureScreen(name='game_structure_screen'))
        sm.add_widget(WinScreen(name='win_screen'))
        sm.add_widget(RulesSubmenu(name='rules_submenu'))
        sm.add_widget(MatchScreen(name='match_screen'))  # Ensure this line is present
        
        # Start playing background music if enabled
        print("Initializing background music...")
        try:
            if self.settings.get('music', True):
                print("Music is enabled in settings. Starting playback...")
                self.music_manager.set_enabled(True)
                self.music_manager.set_volume(self.settings.get('music_volume', 0.5))
                success = self.music_manager.play_random()
                print(f"Music playback attempt result: {'Success' if success else 'Failed'}")
            else:
                print("Music is disabled in settings.")
                self.music_manager.set_enabled(False)
        except Exception as e:
            print(f"Error initializing music: {e}")
            import traceback
            traceback.print_exc()
        
        return sm
    
    def on_stop(self):
        """Called when the application is closing"""
        # Save settings when app is closed
        save_settings(self.settings)
        
        # Stop music
        self.music_manager.stop()
        
        return True

if __name__ == '__main__':
    MemoryGameApp().run()