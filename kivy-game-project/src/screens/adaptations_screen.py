from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.switch import Switch
from kivy.uix.slider import Slider
from kivy.app import App
from kivy.metrics import dp
from utils.settings_manager import save_settings

class AdaptationsScreen(Screen):
    def __init__(self, **kwargs):
        super(AdaptationsScreen, self).__init__(**kwargs)
        
        # Main layout
        main_layout = BoxLayout(orientation='vertical', spacing=dp(10), padding=dp(20))
        
        # Title with dynamic font size
        title = Label(
            text="Accessibility Options",
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
        
        # Colorblind mode with explanation
        option_layout1 = self.create_option_layout(
            "Colorblind Mode", 
            "Cards will be displayed in black and white to help colorblind players",
            self.colorblind_switch_factory
        )
        content_layout.add_widget(option_layout1)
        
        # Audio assistance with explanation
        option_layout2 = self.create_option_layout(
            "Audio Assistance", 
            "Provides sound cues and narration for visually impaired players",
            self.audio_assist_switch_factory
        )
        content_layout.add_widget(option_layout2)
        
        # Visual feedback with explanation
        option_layout3 = self.create_option_layout(
            "Visual Feedback", 
            "Displays visual cues and animations for hearing-impaired players",
            self.visual_feedback_switch_factory
        )
        content_layout.add_widget(option_layout3)
        
        # Easy mode with explanation
        option_layout_easy_mode = self.create_option_layout(
            "Easy Mode", 
            "Allows revealing all cards once per game",
            self.easy_mode_switch_factory
        )
        content_layout.add_widget(option_layout_easy_mode)
        
        # Text size scaling with explanation
        option_layout_text_size_scaling = self.create_option_layout(
            "Text Size Scaling", 
            "Adjusts text size throughout the game",
            self.text_size_scaling_slider_factory,
            is_slider=True
        )
        content_layout.add_widget(option_layout_text_size_scaling)
        
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
    
    def colorblind_switch_factory(self):
        self.colorblind_switch = Switch(active=False)
        self.colorblind_switch.bind(active=self.on_colorblind_toggle)
        return self.colorblind_switch
    
    def audio_assist_switch_factory(self):
        self.audio_assist_switch = Switch(active=False)
        self.audio_assist_switch.bind(active=self.on_audio_assist_toggle)
        return self.audio_assist_switch
    
    def visual_feedback_switch_factory(self):
        self.visual_feedback_switch = Switch(active=True)
        self.visual_feedback_switch.bind(active=self.on_visual_feedback_toggle)
        return self.visual_feedback_switch
    
    def easy_mode_switch_factory(self):
        self.easy_mode_switch = Switch(active=False)
        self.easy_mode_switch.bind(active=self.on_easy_mode_toggle)
        return self.easy_mode_switch
    
    def text_size_scaling_slider_factory(self):
        self.text_size_scaling_slider = Slider(min=0.5, max=2.0, value=1.0)
        self.text_size_scaling_slider.bind(value=self.on_text_size_scaling_change)
        return self.text_size_scaling_slider
    
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
            self.colorblind_switch.active = app.settings.get('colorblind_mode', False)
            self.audio_assist_switch.active = app.settings.get('audio_assist', False)
            self.visual_feedback_switch.active = app.settings.get('visual_feedback', True)
            self.easy_mode_switch.active = app.settings.get('easy_mode', False)
            self.text_size_scaling_slider.value = app.settings.get('text_size_factor', 1.0)
    
    def on_colorblind_toggle(self, instance, value):
        app = App.get_running_app()
        if hasattr(app, 'settings'):
            app.settings['colorblind_mode'] = value
            save_settings(app.settings)
        print(f"Colorblind mode: {'on' if value else 'off'}")
    
    def on_audio_assist_toggle(self, instance, value):
        app = App.get_running_app()
        if hasattr(app, 'settings'):
            app.settings['audio_assist'] = value
            save_settings(app.settings)
        print(f"Audio assistance: {'on' if value else 'off'}")
    
    def on_visual_feedback_toggle(self, instance, value):
        app = App.get_running_app()
        if hasattr(app, 'settings'):
            app.settings['visual_feedback'] = value
            save_settings(app.settings)
        print(f"Visual feedback: {'on' if value else 'off'}")
    
    def on_easy_mode_toggle(self, instance, value):
        app = App.get_running_app()
        if hasattr(app, 'settings'):
            app.settings['easy_mode'] = value
            save_settings(app.settings)
        print(f"Easy mode: {'on' if value else 'off'}")
    
    def on_text_size_scaling_change(self, instance, value):
        app = App.get_running_app()
        if hasattr(app, 'settings'):
            app.settings['text_size_factor'] = value
            save_settings(app.settings)
        print(f"Text size scaling: {value}")
    
    def save_options(self, instance):
        # Save all settings to a global app state or file
        app = App.get_running_app()
        if not hasattr(app, 'settings'):
            app.settings = {}
        
        app.settings['colorblind_mode'] = self.colorblind_switch.active
        app.settings['audio_assist'] = self.audio_assist_switch.active
        app.settings['visual_feedback'] = self.visual_feedback_switch.active
        app.settings['easy_mode'] = self.easy_mode_switch.active
        app.settings['text_size_factor'] = self.text_size_scaling_slider.value
        
        # Save settings to file
        save_settings(app.settings)
        
        print("Settings saved!")
        self.go_back(instance)
    
    def go_back(self, instance):
        self.manager.current = 'main_menu'
