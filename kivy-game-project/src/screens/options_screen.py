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

class OptionsScreen(Screen):
    def __init__(self, **kwargs):
        super(OptionsScreen, self).__init__(**kwargs)
        
        # Main layout
        main_layout = BoxLayout(orientation='vertical', spacing=dp(10), padding=dp(20))
        
        # Title with dynamic font size
        title = Label(
            text="Opções do Jogo",
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
            "Modo Tela Cheia", 
            "Alterna entre modo janela e tela cheia",
            self.fullscreen_switch_factory
        )
        content_layout.add_widget(option_layout_fullscreen)
        
        # Text size with explanation
        option_layout_text_size = self.create_option_layout(
            "Tamanho do Texto", 
            "Controla o tamanho de todos os textos no jogo",
            self.text_size_slider_factory,
            is_slider=True
        )
        content_layout.add_widget(option_layout_text_size)
        
        # Sound effects with explanation
        option_layout_sound_effects = self.create_option_layout(
            "Efeitos Sonoros", 
            "Ativa ou desativa os efeitos sonoros do jogo",
            self.sound_effects_switch_factory
        )
        content_layout.add_widget(option_layout_sound_effects)
        
        # Music with explanation
        option_layout_music = self.create_option_layout(
            "Música", 
            "Ativa ou desativa a música de fundo do jogo",
            self.music_switch_factory
        )
        content_layout.add_widget(option_layout_music)
        
        # Casual Mode - replaces separate score and timer options
        option_layout_casual_mode = self.create_option_layout(
            "Modo Casual", 
            "Quando ativado, desativa a pontuação e o temporizador para uma experiência mais relaxante",
            self.casual_mode_switch_factory
        )
        content_layout.add_widget(option_layout_casual_mode)
        
        scroll_view.add_widget(content_layout)
        main_layout.add_widget(scroll_view)
        
        # Buttons layout
        buttons_layout = BoxLayout(orientation='horizontal', spacing=dp(20), size_hint=(1, 0.15))
        
        # Save button
        save_btn = Button(
            text="Salvar Alterações",
            font_size=self.get_font_size(32),
            background_color=(0, 0.7, 0, 1)
        )
        save_btn.bind(on_release=self.save_options)
        buttons_layout.add_widget(save_btn)
        
        # Back button
        back_btn = Button(
            text="Voltar",
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
            self.text_size_slider.value = app.settings.get('text_size_factor', 1.0)
            self.sound_effects_switch.active = app.settings.get('sound_effects', True)
            self.music_switch.active = app.settings.get('music', True)
            
            # Set casual mode based on whether both score and timer displays are disabled
            score_display = app.settings.get('score_display', True)
            timer_display = app.settings.get('timer_display', True)
            self.casual_mode_switch.active = not (score_display or timer_display)
    
    def on_fullscreen_toggle(self, instance, value):
        Window.fullscreen = value
        print(f"Fullscreen mode: {'on' if value else 'off'}")
    
    def on_text_size_change(self, instance, value):
        print(f"Text size factor: {value}")
    
    def on_sound_effects_toggle(self, instance, value):
        print(f"Sound effects: {'on' if value else 'off'}")
    
    def on_music_toggle(self, instance, value):
        print(f"Music: {'on' if value else 'off'}")
    
    def on_casual_mode_toggle(self, instance, value):
        print(f"Casual mode: {'on' if value else 'off'}")
    
    def save_options(self, instance):
        # Save all settings to a global app state or file
        app = App.get_running_app()
        if not hasattr(app, 'settings'):
            app.settings = {}
        
        app.settings['fullscreen'] = self.fullscreen_switch.active
        app.settings['text_size_factor'] = self.text_size_slider.value
        app.settings['sound_effects'] = self.sound_effects_switch.active
        app.settings['music'] = self.music_switch.active
        
        # Set both score_display and timer_display based on the inverse of casual mode
        # (casual mode means hiding both score and timer)
        app.settings['score_display'] = not self.casual_mode_switch.active
        app.settings['timer_display'] = not self.casual_mode_switch.active
        
        print("Settings saved!")
        self.go_back(instance)
    
    def go_back(self, instance):
        self.manager.current = 'main_menu'
