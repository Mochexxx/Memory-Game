from kivy.uix.screenmanager import Screen
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
import os
from pathlib import Path

def find_project_root():
    """Find the project root directory by looking for known directories"""
    # Start with the directory of this file and go up until we find the project root
    current_dir = Path(__file__).resolve().parent.parent.parent.parent
    
    # Check if we're at the project root
    if (current_dir / "Items_Jogo").exists():
        return str(current_dir)
    if (current_dir.parent / "Items_Jogo").exists():
        return str(current_dir.parent)
    
    # Fallback to a hardcoded path but with the correct username from the file path
    file_path = Path(__file__).resolve()
    username = file_path.parts[2]  # Extract username from path
    return os.path.join('C:', os.sep, 'Users', username, 'Documents', 'GitHub', 'IPC_24-25')

class ThemeSelectionScreen(Screen):
    def __init__(self, **kwargs):
        super(ThemeSelectionScreen, self).__init__(**kwargs)
        
        # Get the project root directory
        project_root = find_project_root()
        
        # Use project_root to construct theme paths
        self.selected_theme = os.path.join(project_root, "Items_Jogo", "baralho_animais")  # Default theme
        
        layout = BoxLayout(orientation='vertical', spacing=20, padding=50)
        
        self.title = Label(text="Theme Selection", font_size=74, size_hint=(1, 0.2))
        layout.add_widget(self.title)
        
        # Adjust layout for smaller and more organized buttons
        grid_layout = BoxLayout(orientation='horizontal', spacing=20, size_hint=(1, 0.6))

        # Use project_root to construct paths for both themes
        themes = [
            ("Animal Theme", self.select_theme_animals, os.path.join(project_root, "Items_Jogo", "baralho_animais")),
            ("Number Theme", self.select_theme_numbers, os.path.join(project_root, "Items_Jogo", "baralho_numeros"))
        ]

        self.theme_buttons = []
        # Adjust layout for smaller buttons with reduced width and centered alignment
        for text, callback, theme in themes:
            btn = ToggleButton(
                text=text,
                size_hint=(0.5, 0.2),  # Reduced width
                pos_hint={'center_x': 0.5},  # Center horizontally
                background_color=(0, 0.5, 0, 1),
                group='theme'
            )
            btn.bind(on_release=lambda instance, cb=callback, th=theme: cb(instance, th))
            layout.add_widget(btn)
            self.theme_buttons.append(btn)

        layout.add_widget(grid_layout)

        # Adjust back button to be smaller and centered
        self.back_btn = ToggleButton(
            text="Back",
            size_hint=(0.5, 0.1),  # Reduced width
            pos_hint={'center_x': 0.5},  # Center horizontally
            background_color=(0.5, 0, 0, 1),
            group='theme'
        )
        self.back_btn.bind(on_release=lambda instance: self.go_back(instance, None))
        layout.add_widget(self.back_btn)
        
        self.add_widget(layout)
    
    def update_font_size(self, font_size_factor):
        """Update font sizes dynamically based on the font size factor."""
        # Update title font size
        self.title.font_size = 74 * font_size_factor * 0.7
        
        # Update theme button font sizes
        for btn in self.theme_buttons:
            btn.font_size = 32 * font_size_factor * 0.7
        
        # Update back button font size
        self.back_btn.font_size = 24 * font_size_factor * 0.7
    
    def select_theme_animals(self, instance, theme):
        self.selected_theme = theme
        self.manager.current = 'difficulty_selection'
    
    def select_theme_numbers(self, instance, theme):
        self.selected_theme = theme
        self.manager.current = 'difficulty_selection'
    
    def go_back(self, instance, theme):
        self.manager.current = 'main_menu'
