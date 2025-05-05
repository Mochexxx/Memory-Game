from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.metrics import dp
from kivy.graphics import Color, RoundedRectangle, Line
from utils.stats_manager import load_stats

class BestTimesScoresTable(BoxLayout):
    """Widget to display the best times and scores for each difficulty."""

    def __init__(self, **kwargs):
        super(BestTimesScoresTable, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = dp(20)
        self.spacing = dp(10)
        self.size_hint_y = None

        # Enhanced background
        with self.canvas.before:
            Color(0.1, 0.1, 0.2, 0.85)
            self.bg_rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(15)])

            Color(0.4, 0.4, 0.6, 0.7)
            self.border = Line(rounded_rectangle=(self.pos[0], self.pos[1], self.size[0], self.size[1], dp(15)), width=1.2)

        # Title
        self.title = Label(
            text="Melhores Tempos e Pontuações",
            font_size=24,
            color=(0.9, 0.9, 1, 1),
            size_hint=(1, None),
            height=dp(30),
            bold=True
        )
        self.add_widget(self.title)

        # Separator
        separator = BoxLayout(size_hint=(1, None), height=dp(1))
        with separator.canvas:
            Color(0.4, 0.4, 0.8, 0.8)
            Line(points=[separator.x, separator.y, separator.x + separator.width, separator.y], width=1)
        self.add_widget(separator)

        # Table header
        header = BoxLayout(orientation='horizontal', size_hint=(1, None), height=dp(30))
        header.add_widget(Label(text="Dificuldade", font_size=16, bold=True, color=(1, 1, 1, 1)))
        header.add_widget(Label(text="Melhor Tempo", font_size=16, bold=True, color=(1, 1, 1, 1)))
        header.add_widget(Label(text="Melhor Pontuação", font_size=16, bold=True, color=(1, 1, 1, 1)))
        self.add_widget(header)

        # Placeholder rows for difficulties
        self.difficulty_rows = {}
        difficulties = ["Easy", "Medium", "Hard"]

        for difficulty in difficulties:
            row = BoxLayout(orientation='horizontal', size_hint=(1, None), height=dp(30))

            name = Label(
                text=difficulty,
                font_size=16,
                color=(0.9, 0.9, 0.9, 1),
                halign='left',
                size_hint=(0.4, 1),
                text_size=(0, None)
            )
            name.bind(size=lambda s, w: setattr(s, 'text_size', (s.width, None)))

            best_time = Label(
                text="-",
                font_size=16,
                color=(1, 1, 0.8, 1),
                halign='center',
                size_hint=(0.3, 1),
                text_size=(0, None)
            )
            best_time.bind(size=lambda s, w: setattr(s, 'text_size', (s.width, None)))

            best_score = Label(
                text="-",
                font_size=16,
                color=(1, 1, 0.8, 1),
                halign='center',
                size_hint=(0.3, 1),
                text_size=(0, None)
            )
            best_score.bind(size=lambda s, w: setattr(s, 'text_size', (s.width, None)))

            row.add_widget(name)
            row.add_widget(best_time)
            row.add_widget(best_score)
            self.add_widget(row)

            self.difficulty_rows[difficulty] = (best_time, best_score)

        # Calculate total height
        total_height = dp(30)  # Title height
        total_height += dp(1)  # Separator height
        total_height += dp(30)  # Header height
        total_height += dp(30) * len(difficulties)  # Rows height
        total_height += self.padding[1] * 2  # Top and bottom padding
        total_height += self.spacing * (len(difficulties) + 2)  # Spacing between elements

        self.height = total_height

        # Bind to update the background rectangle and border when size changes
        self.bind(size=self._update_canvas, pos=self._update_canvas)

        # Load stats initially
        self.update_table()

    def _update_canvas(self, instance, value):
        """Update the background rectangle and border"""
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size
        self.border.rounded_rectangle = (self.pos[0], self.pos[1], self.size[0], self.size[1], dp(15))

    def update_table(self):
        """Update the table with the best times and scores."""
        try:
            stats = load_stats()

            difficulties = {
                "Fácil": ("easy",),
                "Médio": ("medium",),
                "Difícil": ("hard",)
            }

            for difficulty, keys in difficulties.items():
                best_time_label, best_score_label = self.difficulty_rows[difficulty]

                # Get best time and score for the difficulty
                best_time = min((stats['best_times'].get(key, float('inf')) for key in keys), default=float('inf'))
                best_score = max((stats['best_score'] for key in keys), default=0)

               

                best_time_label.text = "-" if best_time == float('inf') else f"{best_time}"
                

            print("Table updated successfully")
        except Exception as e:
            print(f"Error updating table: {e}")