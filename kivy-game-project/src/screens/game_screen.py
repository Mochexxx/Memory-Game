from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.clock import Clock
from kivy.app import App
from kivy.core.window import Window
from kivy.animation import Animation
from kivy.uix.image import Image
from kivy.core.audio import SoundLoader
from kivy.properties import NumericProperty, StringProperty
from kivy.uix.widget import Widget
import os
import math
from logic.game_logic import start_game, check_win_condition  # Fix the import
from utils.stats_manager import update_stats
from pathlib import Path

# Carrega o arquivo .kv
from kivy.lang import Builder
kv_file = Path(__file__).parent / 'game_screen.kv'
Builder.load_file(str(kv_file))

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
    return os.path.join('C:', os.sep, 'Users', username, 'Documents', 'GitHub', 'IPC')

def get_card_back_path():
    """Retorna o caminho para a carta traseira azul"""
    project_root = find_project_root()
    return os.path.join(project_root, "Items_Jogo", "Parte_Traseira_Cartas", "cardBack_blue3.png")

def get_wood_texture_path():
    """Retorna o caminho para a textura de madeira"""
    project_root = find_project_root()
    return os.path.join(project_root, "Items_Jogo", "Icons", "wood_sign.png")

class CardButton(Button):
    rotation = NumericProperty(0)
    card_width = NumericProperty(0)
    card_height = NumericProperty(0)
    card_back_path = StringProperty('')

class WoodLabel(BoxLayout):
    text = StringProperty('')
    font_size = StringProperty('24sp')

class GameScreen(Screen):
    def __init__(self, **kwargs):
        super(GameScreen, self).__init__(**kwargs)
        
        # Main layout
        self.main_layout = BoxLayout(orientation='vertical', spacing=10, padding=15)
        
        # HUD (Score and Timer)
        self.hud_layout = BoxLayout(size_hint_y=0.12, spacing=20, padding=[10, 5])
        self.score_label = Label(text="Score: 0", size_hint_x=0.4, opacity=1, disabled=False)
        self.timer_label = Label(text="Tempo: 0s", size_hint_x=0.4, opacity=1, disabled=False)
        self.hud_layout.add_widget(self.score_label)
        self.hud_layout.add_widget(self.timer_label)
        self.main_layout.add_widget(self.hud_layout)
        
        # Game grid
        self.game_grid = GridLayout(cols=4, spacing=10, padding=10, size_hint_y=0.8)
        self.main_layout.add_widget(self.game_grid)
        
        # Buttons
        self.button_layout = BoxLayout(size_hint_y=0.1, spacing=10, padding=[10, 5])
        self.reveal_button = Button(
            text="Revelar Cartas", size_hint_x=0.3, background_color=(0.5, 0.5, 0.5, 1),
            color=(1, 1, 1, 1), font_size='18sp', opacity=0, disabled=True
        )
        self.reveal_button.bind(on_release=self.reveal_cards)
        self.back_button = Button(
            text="Voltar", size_hint_x=0.3, background_color=(0.8, 0.2, 0.2, 1),
            color=(1, 1, 1, 1), font_size='18sp'
        )
        self.back_button.bind(on_release=self.go_back)
        self.button_layout.add_widget(self.reveal_button)
        self.button_layout.add_widget(Widget(size_hint_x=0.4))  # Spacer
        self.button_layout.add_widget(self.back_button)
        self.main_layout.add_widget(self.button_layout)
        
        # Add main layout to the screen
        self.add_widget(self.main_layout)
        
        # Inicialização de variáveis
        self.cards = []
        self.selected_cards = []
        self.is_checking = False
        self.current_theme = None
        self.current_difficulty = None
        self.multiplier = 1
        self.consecutive_matches = 0
        self.easy_mode_used = False
        self.sounds = {}
        self.card_animations = {}
        self.card_back_path = get_card_back_path()
        
        # Configuração do timer
        self.elapsed_time = 0
        self.timer_event = None
        
        # Configuração do score
        self.score = 0
        self.lives = 3
        
        # Configuração do grid
        self.grid_cols = 4
        self.grid_rows = 4
        
        # Bind para redimensionamento da janela
        Window.bind(on_resize=self.on_window_resize)
        
        # Atualização das configurações
        self.update_settings()
    
    def update_settings(self):
        """Update display settings based on app settings"""
        app = App.get_running_app()
        if hasattr(app, 'settings'):
            self.accessibility_mode = app.settings.get('visual_feedback', True)
            self.colorblind_mode = app.settings.get('colorblind_mode', False)
            self.audio_mode = app.settings.get('audio_assist', False)
            self.score_display = app.settings.get('score_display', True)
            self.timer_display = app.settings.get('timer_display', True)
            self.casual_mode = app.settings.get('casual_mode', False)  # Default to False
        else:
            self.accessibility_mode = True
            self.colorblind_mode = False
            self.audio_mode = False
            self.score_display = True
            self.timer_display = True
            self.casual_mode = False
        
        # Update HUD visibility
        self.score_label.opacity = 1 if self.score_display else 0
        self.score_label.disabled = not self.score_display
        self.timer_label.opacity = 1 if self.timer_display else 0
        self.timer_label.disabled = not self.timer_display
        
        # Update reveal button visibility
        self.reveal_button.opacity = 1 if app.settings.get('easy_mode', False) else 0
        self.reveal_button.disabled = not app.settings.get('easy_mode', False)
    
    def apply_theme(self, theme, num_cards):
        # Limpa o grid atual
        self.game_grid.clear_widgets()
        
        # Inicia o novo jogo
        self.cards = start_game(theme, num_cards)
        self.current_theme = theme
        self.current_difficulty = num_cards
        
        # Calcula o layout ótimo
        optimal_cols, card_width, card_height = self.calculate_optimal_grid(len(self.cards))
        self.game_grid.cols = optimal_cols
        
        # Limpa as cartas selecionadas
        self.selected_cards = []
        
        # Adiciona os botões das cartas
        for card in self.cards:
            self.game_grid.add_widget(self.create_card_button(card, card_width, card_height))
        
        # Configura os sons
        self.setup_sounds(theme)
        
        # Reseta o jogo
        self.reset_game()
    
    def reset_game(self):
        """Reseta o estado do jogo"""
        self.score = 0
        self.lives = 3
        self.easy_mode_used = False
        self.consecutive_matches = 0
        self.multiplier = 1
        
        # Atualiza o HUD
        self.score_label.text = "Score: 0"
        
        # Reseta e inicia o timer
        self.stop_timer()
        self.start_timer()
    
    def setup_sounds(self, theme):
        """Configura os sons para o tema atual"""
        project_root = find_project_root()
        sound_folder = None
        
        if "baralho_animais" in theme.lower():
            sound_folder = os.path.join(project_root, "Items_Jogo", "audios_wav_animais")
        elif "baralho_numeros" in theme.lower():
            sound_folder = os.path.join(project_root, "Items_Jogo", "audios_numeros_wav")
        else:
            sound_folder = os.path.join(project_root, "Items_Jogo", "audios_wav_animais")
        
        # Limpa sons anteriores
        for sound in self.sounds.values():
            if sound:
                sound.unload()
        self.sounds.clear()
        
        # Carrega novos sons
        for card in self.cards:
            base_filename = os.path.basename(card["image"])
            sound_path = os.path.join(sound_folder, base_filename.replace(".png", ".wav"))
            
            if os.path.exists(sound_path):
                self.sounds[card["image"]] = SoundLoader.load(sound_path)
    
    def calculate_optimal_grid(self, num_cards):
        """Calculate the optimal card size based on screen dimensions and grid size"""
        # Card aspect ratio (height/width)
        card_aspect_ratio = 1.5
        
        # Get available space
        screen_width = Window.width
        screen_height = Window.height
        
        # Calculate space available for cards
        available_width = screen_width - 40
        available_height = screen_height * 0.8  # 80% da altura da tela
        
        # Use the predefined grid size or calculate optimal
        cols = self.grid_cols if hasattr(self, 'grid_cols') else math.ceil(math.sqrt(num_cards))
        rows = self.grid_rows if hasattr(self, 'grid_rows') else math.ceil(num_cards / cols)
        
        # Calculate card dimensions
        card_width = (available_width - (cols - 1) * 10) / cols
        card_height = (available_height - (rows - 1) * 10) / rows
        
        # Adjust card size to maintain aspect ratio
        if card_height / card_width > card_aspect_ratio:
            card_height = card_width * card_aspect_ratio
        else:
            card_width = card_height / card_aspect_ratio
        
        return cols, card_width, card_height
    
    def on_window_resize(self, instance, width, height):
        """Handle window resize events by recalculating card layout"""
        if self.cards:
            # Recalculate and update the layout
            self.update_card_layout()
    
    def update_card_layout(self):
        """Update the card layout based on current screen dimensions"""
        if not self.cards:
            return
            
        num_cards = len(self.cards)
        optimal_cols, card_width, card_height = self.calculate_optimal_grid(num_cards)
        
        # Update grid columns
        self.game_grid.cols = optimal_cols
        
        # Update card sizes
        for widget in self.game_grid.children:
            widget.size_hint = (None, None)
            widget.size = (card_width, card_height)
    
    def start_timer(self):
        if not self.timer_display:
            return
        # Reset and start the timer
        self.elapsed_time = 0
        self.timer_label.text = "Tempo: 0s"
        # Schedule timer update every second
        self.timer_event = Clock.schedule_interval(self.update_timer, 1)
    
    def update_timer(self, dt):
        if not self.timer_display:
            return
        self.elapsed_time += 1
        self.timer_label.text = f"Tempo: {self.elapsed_time}s"
    
    def stop_timer(self):
        if not self.timer_display:
            return
        # Stop the timer if it's running
        if self.timer_event:
            self.timer_event.cancel()
            self.timer_event = None
    
    def create_card_button(self, card_data, card_width, card_height):
        """Create a card button with flip animation"""
        btn = CardButton(
            size_hint=(None, None),
            size=(card_width, card_height),
            background_normal=self.card_back_path,
            background_down=self.card_back_path,
            card_width=card_width,
            card_height=card_height,
            card_back_path=self.card_back_path,
            rotation=0.0
        )
        
        def on_card_press(instance):
            self.flip_card(instance, card_data)
        
        btn.bind(on_release=on_card_press)
        return btn

    def flip_card(self, instance, card):
        # Prevent flipping cards while checking a match or if card is already flipped/matched
        if self.is_checking or card["flipped"] or card["matched"]:
            return
        
        print(f"Flipping card: {card['image']}")  # Debug print
            
        # Cancel any existing animation for this card
        if instance in self.card_animations:
            self.card_animations[instance].cancel(self.card_animations[instance])
        
        # Create flip animation
        card["flipped"] = True
        
        # Create the flip animation
        anim = Animation(rotation=180, duration=0.5)
        
        def on_complete(animation, widget):
            # Update the card image after the flip
            widget.background_normal = card["image"]
            widget.background_down = card["image"]
            self.selected_cards.append((widget, card))
            
            # Play sound if enabled
            app = App.get_running_app()
            if app.settings.get('audio_assist', False):
                if card["image"] in self.sounds and self.sounds[card["image"]]:
                    print(f"Playing sound for {card['image']}")
                    self.sounds[card["image"]].play()
            
            if len(self.selected_cards) == 2:
                self.is_checking = True
                Clock.schedule_once(self.check_match, 1)
        
        anim.bind(on_complete=on_complete)
        self.card_animations[instance] = anim
        anim.start(instance)
    
    def check_match(self, dt):
        # Make sure we have exactly 2 cards to check
        if len(self.selected_cards) != 2:
            print(f"Warning: check_match called with {len(self.selected_cards)} cards")
            self.is_checking = False
            return
        
        print(f"Checking match between: {self.selected_cards[0][1]['image']} and {self.selected_cards[1][1]['image']}")
            
        if self.selected_cards[0][1]["image"] == self.selected_cards[1][1]["image"]:
            # This is a match! Mark cards as matched
            self.selected_cards[0][1]["matched"] = True
            self.selected_cards[1][1]["matched"] = True
            self.consecutive_matches += 1
            self.multiplier = min(self.consecutive_matches, 5)  # Cap multiplier at 5
            self.score += 1 * self.multiplier
            if self.score_display:
                self.score_label.text = f"Score: {self.score}"
            
            # Solução simplificada: Apenas verifique se este é o último par
            total_pairs = len(self.cards) // 2
            matched_pairs = sum(1 for card in self.cards if card["matched"]) // 2
            
            # Se NÃO for o último par (ainda falta pelo menos um par), mostre a tela de match
            if matched_pairs < total_pairs:
                match_screen = self.manager.get_screen('match_screen')
                match_screen.show_match()
                print(f"[MATCH] Mostrando a tela de match - par {matched_pairs}/{total_pairs}")
            else:
                print(f"[LAST] Último par encontrado - não mostrando a tela de match")
            
        else:
            self.consecutive_matches = 0
            self.multiplier = 1
            if self.lives > 0:
                self.lives -= 1
            else:
                self.score = max(self.score - 1, 0)  # Ensure score does not go below zero
                if self.score_display:
                    self.score_label.text = f"Score: {self.score}"
            
            # Animate cards back to face down
            for widget, card in self.selected_cards:
                if widget in self.card_animations:
                    self.card_animations[widget].cancel(self.card_animations[widget])
                
                card["flipped"] = False
                anim = Animation(rotation=0, duration=0.5)
                
                def on_complete(animation, widget):
                    widget.background_normal = self.card_back_path
                    widget.background_down = self.card_back_path
                
                anim.bind(on_complete=on_complete)
                self.card_animations[widget] = anim
                anim.start(widget)
        
        # Clear selected cards and allow new selections
        self.selected_cards = []
        self.is_checking = False
        
        # More accurate debug info
        total_cards = len(self.cards)
        matched_cards = sum(1 for card in self.cards if card["matched"])
        print(f"Final state: Matched cards: {matched_cards}/{total_cards}, Remaining: {total_cards - matched_cards}")
        
        # Check win condition and ensure we transition to win screen
        if check_win_condition(self.cards):
            print("Condição de vitória encontrada! A parar o relógio e a dar display da victory screen.")
            self.stop_timer()
            # Remove delay to prevent any race conditions
            self.show_win_screen()

    def show_win_screen(self):
        print("Showing win screen")  # Debug print
        
        # Save game statistics
        game_data = {
            'score': self.score,
            'time': self.elapsed_time,
            'theme': self.current_theme,
            'difficulty': self.current_difficulty,
            'pairs_matched': len(self.cards) // 2
        }
        update_stats(game_data)
        
        # Pass the elapsed time, theme, and difficulty to the win screen
        win_screen = self.manager.get_screen('win_screen')
        
        # Make sure we have the latest settings
        app = App.get_running_app()
        if hasattr(app, 'settings'):
            self.score_display = app.settings.get('score_display', True)
            self.timer_display = app.settings.get('timer_display', True)
        
        print(f"Settings: show score={self.score_display}, show timer={self.timer_display}")  # Debug print
        
        # Set game stats first
        win_screen.set_game_stats(self.elapsed_time, self.current_theme, self.current_difficulty)
        
        # Display score and time based on settings
        if self.score_display:
            win_screen.display_score(self.score)
        
        # Important: Ensure all changes to the win screen are done before switching to it
        win_screen.update_labels_visibility()
        
        # Switch to win screen directly
        self.manager.current = 'win_screen'
    
    def on_leave(self):
        # Stop the timer when leaving the game screen
        self.stop_timer()

    def reveal_cards(self, instance):
        if self.easy_mode_used:
            return
        
        self.easy_mode_used = True
        self.reveal_button.disabled = True
        
        # Reveal all cards with animation
        for card, widget in zip(self.cards, self.game_grid.children):
            if widget in self.card_animations:
                self.card_animations[widget].cancel(self.card_animations[widget])
            
            card["flipped"] = True
            anim = Animation(rotation=180, duration=0.5)
            
            def on_complete(animation, widget, card):
                widget.background_normal = card["image"]
                widget.background_down = card["image"]
            
            anim.bind(on_complete=on_complete)
            self.card_animations[widget] = anim
            anim.start(widget)
        
        # Schedule to hide cards after 2 seconds
        Clock.schedule_once(self.hide_cards, 2)
    
    def hide_cards(self, dt):
        for card, widget in zip(self.cards, self.game_grid.children):
            if not card["matched"]:
                if widget in self.card_animations:
                    self.card_animations[widget].cancel(self.card_animations[widget])
                
                card["flipped"] = False
                anim = Animation(rotation=0, duration=0.5)
                
                def on_complete(animation, widget):
                    widget.background_normal = self.card_back_path
                    widget.background_down = self.card_back_path
                
                anim.bind(on_complete=on_complete)
                self.card_animations[widget] = anim
                anim.start(widget)
    
    def go_back(self, instance):
        self.manager.current = 'main_menu'

    def set_grid_size(self, grid_size):
        """Define o tamanho do grid (colunas x linhas)"""
        self.grid_cols, self.grid_rows = grid_size
        self.game_grid.cols = self.grid_cols
        self.update_card_layout()

    def get_wood_texture_path(self):
        """Retorna o caminho para a textura de madeira"""
        return self.wood_texture_path
