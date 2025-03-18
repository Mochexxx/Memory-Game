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

class OptionsScreen(Screen):
    def __init__(self, **kwargs):
        super(OptionsScreen, self).__init__(**kwargs)
        
        # Main layout
        main_layout = BoxLayout(orientation='vertical', spacing=dp(10), padding=dp(20))
        
        # Title with dynamic font size
        title = Label(
            text="Opções de Acessibilidade",
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
            "Modo Daltonismo", 
            "Aumenta o contraste e usa cores adequadas para daltonismo",
            self.colorblind_switch_factory
        )
        content_layout.add_widget(option_layout1)
        
        # Audio assistance with explanation
        option_layout2 = self.create_option_layout(
            "Assistência por Áudio", 
            "Fornece dicas sonoras e narração para jogadores com deficiência visual",
            self.audio_assist_switch_factory
        )
        content_layout.add_widget(option_layout2)
        
        # Visual feedback with explanation
        option_layout3 = self.create_option_layout(
            "Feedback Visual", 
            "Mostra dicas visuais e animações para jogadores com deficiência auditiva",
            self.visual_feedback_switch_factory
        )
        content_layout.add_widget(option_layout3)
        
        # Text size with explanation
        option_layout4 = self.create_option_layout(
            "Tamanho do Texto", 
            "Controla o tamanho de todos os textos no jogo",
            self.text_size_slider_factory,
            is_slider=True
        )
        content_layout.add_widget(option_layout4)
        
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
    
    def text_size_slider_factory(self):
        self.text_size_slider = Slider(min=0.5, max=1.5, value=1.0, step=0.1)
        self.text_size_slider.bind(value=self.on_text_size_change)
        return self.text_size_slider
    
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
            self.text_size_slider.value = app.settings.get('text_size_factor', 1.0)
    
    def on_colorblind_toggle(self, instance, value):
        print(f"Colorblind mode: {'on' if value else 'off'}")
    
    def on_audio_assist_toggle(self, instance, value):
        print(f"Audio assistance: {'on' if value else 'off'}")
    
    def on_visual_feedback_toggle(self, instance, value):
        print(f"Visual feedback: {'on' if value else 'off'}")
    
    def on_text_size_change(self, instance, value):
        print(f"Text size factor: {value}")
    
    def save_options(self, instance):
        # Save all settings to a global app state or file
        app = App.get_running_app()
        if not hasattr(app, 'settings'):
            app.settings = {}
        
        app.settings['colorblind_mode'] = self.colorblind_switch.active
        app.settings['audio_assist'] = self.audio_assist_switch.active
        app.settings['visual_feedback'] = self.visual_feedback_switch.active
        app.settings['text_size_factor'] = self.text_size_slider.value
        
        print("Settings saved!")
        self.go_back(instance)
    
    def go_back(self, instance):
        self.manager.current = 'main_menu'
