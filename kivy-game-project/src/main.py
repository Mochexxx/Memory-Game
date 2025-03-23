from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image

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
from screens.adaptations_screen import AdaptationsScreen
from screens.match_screen import MatchScreen
# Removed elegant menu import

class BackgroundFloatLayout(FloatLayout):
    """A float layout with a background image"""
    def __init__(self, **kwargs):
        super(BackgroundFloatLayout, self).__init__(**kwargs)
        
        # Add background image as the first (bottom) widget
        try:
            # Check if the file exists first
            import os
            fundo_dir = "C:\\Users\\pedro\\Documents\\GitHub\\IPC_24-25\\Items_Jogo\\fundo"
            if os.path.exists(fundo_dir):
                fundo_files = os.listdir(fundo_dir)
                print(f"Available files in fundo directory: {fundo_files}")
                
                if 'fundo.jpg' in fundo_files:
                    bg_file = os.path.join(fundo_dir, 'fundo.jpg')
                elif len(fundo_files) > 0 and any(f.endswith(('.jpg','.png','.jpeg')) for f in fundo_files):
                    # Use the first image file found
                    image_files = [f for f in fundo_files if f.endswith(('.jpg','.png','.jpeg'))]
                    bg_file = os.path.join(fundo_dir, image_files[0])
                    print(f"Using alternative background file: {bg_file}")
                else:
                    # Fallback to a solid color
                    print("No suitable background image found. Using solid color.")
                    with self.canvas.before:
                        Color(0.1, 0.1, 0.3, 1)  # Dark blue background
                        self.rect = Rectangle(pos=self.pos, size=self.size)
                    return
            else:
                print(f"Background directory does not exist: {fundo_dir}")
                # Fallback to a solid color
                with self.canvas.before:
                    Color(0.1, 0.1, 0.3, 1)  # Dark blue background
                    self.rect = Rectangle(pos=self.pos, size=self.size)
                return
                
            print(f"Loading background image: {bg_file}")
            bg_image = Image(
                source=bg_file,
                allow_stretch=True,
                keep_ratio=False,
                size_hint=(1, 1),
                pos_hint={'center_x': 0.5, 'center_y': 0.5}
            )
            self.add_widget(bg_image)
        except Exception as e:
            print(f"Error loading background image: {e}")
            # Fallback to a solid color if image loading fails
            with self.canvas.before:
                Color(0.1, 0.1, 0.3, 1)  # Dark blue background
                self.rect = Rectangle(pos=self.pos, size=self.size)

class MyScreenManager(ScreenManager):
    pass

class MemoryGameApp(App):
    def __init__(self, **kwargs):
        super(MemoryGameApp, self).__init__(**kwargs)
        # Load settings from file
        self.settings = load_settings()
        
        # Initialize the music manager
        self.music_manager = MusicManager()
        
        # Apply window settings based on fullscreen preference but ensure maximum resolution
        if self.settings.get('fullscreen', False):
            # Set to fullscreen mode at maximum resolution
            Window.fullscreen = 'auto'  # Use 'auto' for best fullscreen mode
        else:
            # Set to windowed mode but maximized
            Window.fullscreen = False
            Window.maximize()
    
    def on_start(self):
        """Called when the application starts"""
        # Import here to avoid circular imports
        from utils.stats_manager import load_stats
        
        # Make sure stats are loaded at startup
        try:
            stats = load_stats()
            print(f"Loaded player statistics: {len(stats)} records")
        except Exception as e:
            print(f"Error loading statistics: {e}")
    
    def build(self):
        # Create a root layout that will contain the background and screen manager
        root = BackgroundFloatLayout()
        
        # Create and set up the screen manager
        sm = MyScreenManager()
        sm.add_widget(MainMenu(name='main_menu'))
        sm.add_widget(GameScreen(name='game_screen'))
        sm.add_widget(ThemeSelectionScreen(name='theme_selection'))
        sm.add_widget(DifficultySelectionScreen(name='difficulty_selection'))
        sm.add_widget(OptionsScreen(name='options_screen'))
        sm.add_widget(AdaptationsScreen(name='adaptations_screen'))
        sm.add_widget(HowToPlayScreen(name='how_to_play_screen'))
        sm.add_widget(GameStructureScreen(name='game_structure_screen'))
        sm.add_widget(WinScreen(name='win_screen'))
        sm.add_widget(RulesSubmenu(name='rules_submenu'))
        sm.add_widget(MatchScreen(name='match_screen'))
        
        # Add the screen manager to the root layout (on top of the background)
        root.add_widget(sm)
        
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
        
        return root
    
    def on_stop(self):
        """Called when the application is closing"""
        # Save settings when app is closed
        save_settings(self.settings)
        
        # Stop music
        self.music_manager.stop()
        
        return True

if __name__ == '__main__':
    MemoryGameApp().run()