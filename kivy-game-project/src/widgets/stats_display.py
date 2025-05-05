from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.metrics import dp
from kivy.graphics import Color, RoundedRectangle, Line, Rectangle
from kivy.app import App
from utils.stats_manager import load_stats, format_time

class StatsDisplay(BoxLayout):
    """Elegant stats display panel"""
    
    def __init__(self, **kwargs):
        super(StatsDisplay, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = dp(20)
        self.spacing = dp(10)  # Reduced spacing to make it more compact
        
        # Set size_hint_y to None so we can determine our own height
        self.size_hint_y = None
        
        # Enhanced background
        with self.canvas.before:
            # Semitransparent background
            Color(0.1, 0.1, 0.2, 0.85)
            self.bg_rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(15)])
            
            # Add a subtle border
            Color(0.4, 0.4, 0.6, 0.7)
            self.border = Line(rounded_rectangle=(self.pos[0], self.pos[1], self.size[0], self.size[1], dp(15)), width=1.2)
        
        # Stats title
        self.title = Label(
            text="Statistics",  # Translated from "Estatísticas"
            font_size=24, 
            color=(0.9, 0.9, 1, 1),
            size_hint=(1, None),
            height=dp(30),  # Reduced height
            bold=True
        )
        self.add_widget(self.title)
        
        # Separator
        separator = BoxLayout(size_hint=(1, None), height=dp(1))  # Thinner separator
        with separator.canvas:
            Color(0.4, 0.4, 0.8, 0.8)
            Rectangle(pos=separator.pos, size=(separator.width, dp(1)))
        self.add_widget(separator)
        
        # Create placeholder rows for stats that will be populated later
        self.stats_rows = {}
        self.row_heights = dp(30)  # Reduced row height
        
        stat_keys = [
            ("Games Played", "0"),
            ("Best Score", "0"),
            ("Total Time", "0s"),
            ("Pairs Found", "0")
        ]
        
        for key, default_value in stat_keys:
            row = BoxLayout(orientation='horizontal', size_hint=(1, None), height=self.row_heights)
            
            name = Label(
                text=key, 
                font_size=16,  # Smaller font
                color=(0.9, 0.9, 0.9, 1),
                halign='left',
                size_hint=(0.7, 1),
                text_size=(0, None)
            )
            name.bind(size=lambda s, w: setattr(s, 'text_size', (s.width, None)))
            
            val = Label(
                text=default_value, 
                font_size=16,  # Smaller font
                color=(1, 1, 0.8, 1),
                halign='right',
                size_hint=(0.3, 1),
                text_size=(0, None)
            )
            val.bind(size=lambda s, w: setattr(s, 'text_size', (s.width, None)))
            
            row.add_widget(name)
            row.add_widget(val)
            self.add_widget(row)
            
            self.stats_rows[key] = val
        
        # Calculate total height based on contents
        total_height = dp(30)  # Title height
        total_height += dp(1)   # Separator height
        total_height += self.row_heights * len(stat_keys)  # Rows height
        total_height += self.padding[1] * 2  # Top and bottom padding
        total_height += self.spacing * (len(stat_keys) + 1)  # Spacing between elements
        
        # Set the widget height
        self.height = total_height
        
        # Bind to update the background rectangle and border when size changes
        self.bind(
            size=self._update_canvas,
            pos=self._update_canvas
        )
        
        # Load stats initially
        self.update_stats()
    
    def _update_canvas(self, instance, value):
        """Update the background rectangle and border"""
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size
        self.border.rounded_rectangle = (self.pos[0], self.pos[1], self.size[0], self.size[1], dp(15))
    
    def update_stats(self):
        """Update the displayed statistics"""
        try:
            stats = load_stats()
            
            self.stats_rows["Games Played"].text = str(stats['games_played'])
            self.stats_rows["Best Score"].text = str(stats['best_score'])
            self.stats_rows["Total Time"].text = format_time(stats['total_time'])
            self.stats_rows["Pairs Found"].text = str(stats['pairs_matched'])
            
            print("Statistics loaded successfully")
        except Exception as e:
            print(f"Error updating statistics display: {e}")
