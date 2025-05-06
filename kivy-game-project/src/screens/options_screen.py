from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.switch import Switch
from kivy.uix.slider import Slider
from kivy.app import App
from kivy.metrics import dp
from kivy.core.window import Window
from kivy.clock import Clock
from utils.settings_manager import save_settings

class OptionsScreen(Screen):
    def __init__(self, **kwargs):
        super(OptionsScreen, self).__init__(**kwargs)
        
        # Main layout
        main_layout = BoxLayout(orientation='vertical', spacing=dp(10), padding=dp(20))
        
        # Title with dynamic font size
        title = Label(
            text="Game Options",
            font_size=self.get_font_size(60),
            size_hint=(1, 0.15),
            halign='center',
            valign='middle'
        )
        title.bind(size=self.update_text_size)
        main_layout.add_widget(title)
        
        # Create a scrollable content area
        scroll_view = ScrollView(size_hint=(1, 0.7), do_scroll_x=False)
        content_layout = BoxLayout(orientation='vertical', spacing=dp(15), padding=dp(10), size_hint_y=None)
        content_layout.bind(minimum_height=content_layout.setter('height'))
        
        # Fullscreen mode with explanation
        option_layout_fullscreen = self.create_option_layout(
            "Fullscreen Mode", 
            "Toggle between windowed and fullscreen mode",
            self.fullscreen_switch_factory
        )
        content_layout.add_widget(option_layout_fullscreen)
        
        # Text size with explanation
        option_layout_text_size = self.create_option_layout(
            "Text Size", 
            "Control the size of all text in the game",
            self.text_size_slider_factory,
            is_slider=True
        )
        content_layout.add_widget(option_layout_text_size)
        
        # Sound effects with explanation
        option_layout_sound_effects = self.create_option_layout(
            "Sound Effects", 
            "Enable or disable game sound effects",
            self.sound_effects_switch_factory
        )
        content_layout.add_widget(option_layout_sound_effects)
        
        # Music with explanation
        option_layout_music = self.create_option_layout(
            "Music", 
            "Enable or disable background music",
            self.music_switch_factory
        )
        content_layout.add_widget(option_layout_music)
        
        # Music volume with explanation
        option_layout_music_volume = self.create_option_layout(
            "Music Volume", 
            "Control the volume of background music",
            self.music_volume_slider_factory,
            is_slider=True
        )
        content_layout.add_widget(option_layout_music_volume)
        
        # Casual Mode - replaces separate score and timer options
        option_layout_casual_mode = self.create_option_layout(
            "Casual Mode", 
            "When enabled, disables scoring and timer for a more relaxed experience",
            self.casual_mode_switch_factory
        )
        content_layout.add_widget(option_layout_casual_mode)
        
        scroll_view.add_widget(content_layout)
        main_layout.add_widget(scroll_view)
        
        # Buttons layout
        buttons_layout = BoxLayout(orientation='horizontal', spacing=dp(20), size_hint=(1, 0.15))
        
        # Save button
        save_btn = Button(
            text="Save Changes",
            font_size=self.get_font_size(32),
            background_color=(0, 0.7, 0, 1)
        )
        save_btn.bind(on_release=self.save_options)
        buttons_layout.add_widget(save_btn)
        
        # Back button
        back_btn = Button(
            text="Back",
            font_size=self.get_font_size(32),
            background_color=(0.5, 0, 0, 1)
        )
        back_btn.bind(on_release=self.go_back)
        buttons_layout.add_widget(back_btn)
        
        main_layout.add_widget(buttons_layout)
        
        self.add_widget(main_layout)
        
        # Load current settings when screen is created
        self.load_settings()
    
    def create_option_layout(self, title_text, description_text, control_factory, is_slider=False):
        # Create a layout for a single option
        option_box = BoxLayout(orientation='vertical', spacing=dp(5), size_hint_y=None, height=dp(120))
        
        # Header with title and control
        header_box = BoxLayout(orientation='horizontal', size_hint_y=0.6)
        
        # Title
        title_label = Label(
            text=title_text,
            font_size=self.get_font_size(28),
            halign='left',
            valign='middle',
            size_hint=(0.7, 1)
        )
        title_label.bind(size=self.update_text_size)
        header_box.add_widget(title_label)
        
        # Control (switch or slider)
        control = control_factory()
        control_container = BoxLayout(size_hint=(0.3, 1))
        control_container.add_widget(control)
        header_box.add_widget(control_container)
        
        option_box.add_widget(header_box)
        
        # Description
        desc_label = Label(
            text=description_text,
            font_size=self.get_font_size(18),
            halign='left',
            valign='top',
            size_hint_y=0.4,
            color=(0.7, 0.7, 0.7, 1)
        )
        desc_label.bind(size=self.update_text_size)
        option_box.add_widget(desc_label)
        
        return option_box
    
    def fullscreen_switch_factory(self):
        self.fullscreen_switch = Switch(active=Window.fullscreen in (True, 'auto'))
        self.fullscreen_switch.bind(active=self.on_fullscreen_toggle)
        return self.fullscreen_switch
    
    def text_size_slider_factory(self):
        self.text_size_slider = Slider(min=0.5, max=1.5, value=1.0, step=0.1)
        self.text_size_slider.bind(value=self.on_text_size_change)
        return self.text_size_slider
    
    def sound_effects_switch_factory(self):
        self.sound_effects_switch = Switch(active=True)
        self.sound_effects_switch.bind(active=self.on_sound_effects_toggle)
        return self.sound_effects_switch
    
    def music_switch_factory(self):
        self.music_switch = Switch(active=True)
        self.music_switch.bind(active=self.on_music_toggle)
        return self.music_switch
    
    def music_volume_slider_factory(self):
        """Create the music volume slider"""
        self.music_volume_slider = Slider(min=0.0, max=1.0, value=0.5, step=0.1)
        self.music_volume_slider.bind(value=self.on_music_volume_change)
        return self.music_volume_slider
    
    def casual_mode_switch_factory(self):
        self.casual_mode_switch = Switch(active=False)
        self.casual_mode_switch.bind(active=self.on_casual_mode_toggle)
        return self.casual_mode_switch
    
    def get_font_size(self, base_size):
        # Scale font size based on any app-level settings
        app = App.get_running_app()
        factor = 1.0
        if hasattr(app, 'settings'):
            factor = app.settings.get('text_size_factor', 1.0)
        return base_size * factor * 0.7  # Additional 0.7 scaling for consistent scaling across screens
    
    def update_text_size(self, instance, value):
        instance.text_size = (instance.width, None)
    
    def load_settings(self):
        # Load settings from a global app state or file
        app = App.get_running_app()
        if hasattr(app, 'settings'):
            self.fullscreen_switch.active = app.settings.get('fullscreen', Window.fullscreen)
            
            # Cap the text size factor to the maximum allowed value (1.5)
            text_size_factor = app.settings.get('text_size_factor', 1.0)
            text_size_factor = min(text_size_factor, 1.5)  # Cap at maximum value
            
            # Update the app settings with the capped value to prevent future issues
            app.settings['text_size_factor'] = text_size_factor
            
            # Set the slider value
            self.text_size_slider.value = text_size_factor
            
            self.sound_effects_switch.active = app.settings.get('sound_effects', True)
            self.music_switch.active = app.settings.get('music', True)
            self.music_volume_slider.value = app.settings.get('music_volume', 0.5)
            
            # Set casual mode based on whether both score and timer displays are disabled
            score_display = app.settings.get('score_display', True)
            timer_display = app.settings.get('timer_display', True)
            self.casual_mode_switch.active = not (score_display or timer_display)
    
    def on_fullscreen_toggle(self, instance, value):
        Window.fullscreen = value
        app = App.get_running_app()
        if hasattr(app, 'settings'):
            app.settings['fullscreen'] = value
            save_settings(app.settings)
        print(f"Fullscreen mode: {'on' if value else 'off'}")
    
    def on_text_size_change(self, instance, value):
        app = App.get_running_app()
        if hasattr(app, 'settings'):
            # Update the app's settings value immediately
            app.settings['text_size_factor'] = value
            
            # First update the current screen to ensure immediate feedback
            if hasattr(app, 'root') and hasattr(app.root, 'screen_manager'):
                sm = app.root.screen_manager
                
                # Update current screen first for immediate visual feedback
                current_screen = sm.current_screen
                if hasattr(current_screen, 'update_font_size'):
                    current_screen.update_font_size(value)
                
                # Also update all other screens for when they become visible
                for screen_name in sm.screen_names:
                    screen = sm.get_screen(screen_name)
                    if screen != current_screen and hasattr(screen, 'update_font_size'):
                        screen.update_font_size(value)
                
                # Update the options screen itself (any labels that need updating)
                self.update_option_labels(value)
            
            # Save settings immediately with throttling to avoid excessive disk writes
            if not hasattr(self, '_last_save_time') or Clock.get_time() - self._last_save_time > 0.5:
                save_settings(app.settings)
                self._last_save_time = Clock.get_time()
                        
        print(f"Text size factor: {value}")
        
    def update_option_labels(self, value):
        """Update labels in the options screen itself."""
        # Find and update all labels in the options screen
        def update_labels_in_widget(widget):
            if isinstance(widget, Label):
                if hasattr(widget, 'base_font_size'):
                    widget.font_size = widget.base_font_size * value * 0.7
                else:
                    # First time, store the original size
                    widget.base_font_size = widget.font_size / (value * 0.7)
                    widget.font_size = widget.base_font_size * value * 0.7
            elif hasattr(widget, 'children'):
                for child in widget.children:
                    update_labels_in_widget(child)
        
        # Start from the root widget of this screen
        for child in self.children:
            update_labels_in_widget(child)
    
    def on_sound_effects_toggle(self, instance, value):
        app = App.get_running_app()
        if hasattr(app, 'settings'):
            app.settings['sound_effects'] = value
            save_settings(app.settings)
        print(f"Sound effects: {'on' if value else 'off'}")
    
    def on_music_toggle(self, instance, value):
        app = App.get_running_app()
        if hasattr(app, 'settings'):
            app.settings['music'] = value
            save_settings(app.settings)
            
            # Update music manager state
            if hasattr(app, 'music_manager'):
                app.music_manager.set_enabled(value)
                
        print(f"Music: {'on' if value else 'off'}")
    
    def on_music_volume_change(self, instance, value):
        app = App.get_running_app()
        if hasattr(app, 'settings'):
            app.settings['music_volume'] = value
            save_settings(app.settings)
            
            # Update music manager volume
            if hasattr(app, 'music_manager'):
                app.music_manager.set_volume(value)
                
        print(f"Music volume: {value}")
    
    def on_casual_mode_toggle(self, instance, value):
        app = App.get_running_app()
        if hasattr(app, 'settings'):
            app.settings['score_display'] = not value
            app.settings['timer_display'] = not value
            save_settings(app.settings)
        print(f"Casual mode: {'on' if value else 'off'}")
    
    def save_options(self, instance):
        # Save all settings to a global app state or file
        app = App.get_running_app()
        if not hasattr(app, 'settings'):
            app.settings = {}
        
        # Save previous music settings to detect changes
        previous_music_enabled = app.settings.get('music', True)
        previous_music_volume = app.settings.get('music_volume', 0.5)
        
        app.settings['fullscreen'] = self.fullscreen_switch.active
        app.settings['text_size_factor'] = self.text_size_slider.value
        app.settings['sound_effects'] = self.sound_effects_switch.active
        app.settings['music'] = self.music_switch.active
        app.settings['music_volume'] = self.music_volume_slider.value
        
        # Set both score_display and timer_display based on the inverse of casual mode
        app.settings['score_display'] = not self.casual_mode_switch.active
        app.settings['timer_display'] = not self.casual_mode_switch.active
        
        # Apply music settings only if they've changed
        if hasattr(app, 'music_manager'):
            # Only update the enabled state if it changed
            if previous_music_enabled != app.settings['music']:
                app.music_manager.set_enabled(app.settings['music'])
            
            # Always update volume as it's a smooth adjustment
            app.music_manager.set_volume(app.settings['music_volume'])
        
        # Save to file
        save_settings(app.settings)
        
        print("Settings saved!")
        self.go_back(instance)
    
    def go_back(self, instance):
        self.manager.current = 'main_menu'
