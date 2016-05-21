from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.togglebutton import ToggleButton
from kivy.properties import BooleanProperty, NumericProperty
from kivy.clock import Clock
from kivy.uix.label import Label


class LifeGame(BoxLayout):
    pause_pressed = BooleanProperty(True)
    update_rate = NumericProperty(60)

    def __init__(self, **kwargs):
        super(LifeGame, self).__init__(**kwargs)
        blue = (0.55, 0.7, 0.92, 0.5)
        light_sky = (0.8, 1, 1, 0.5)
        self.field = self.read_field()
        self.updates_called = 1

        def on_press_pause(instance):
            root = instance.parent.parent
            root.pause_pressed = True

        def on_press_start(instance):
            root = instance.parent.parent
            root.pause_pressed = False

        def on_press_field_cell(instance):
            root = instance.parent.parent
            i, j = instance.coordinates
            if root.pause_pressed:
                if instance.state == 'down':
                    root.field[i][j] = 1
                else:
                    root.field[i][j] = 0

        def wrap_on_press_rate(rate):
            def on_press_rate(instance):
                root = instance.parent.parent
                root.update_rate = 60 // rate
            return on_press_rate
        self.grid = GridLayout(cols=len(self.field[0]), rows=len(self.field))
        for i, line in enumerate(self.field):
            for j, cell in enumerate(line):
                btn = ToggleButton(background_color=blue,
                                   background_normal='',
                                   on_press=on_press_field_cell)
                if cell == 1:
                    btn = ToggleButton(background_normal='',
                                       background_color=blue,
                                       state='down',
                                       on_press=on_press_field_cell)
                btn.coordinates = (i, j)
                self.grid.add_widget(btn)
        controls = BoxLayout(orientation='vertical', size_hint=(.25, 1))
        start_btn = ToggleButton(text='[b][color=2f4f4f]start[/color][/b]',
                                 markup=True,
                                 background_color=light_sky,
                                 background_normal='',
                                 group="game",
                                 on_press=on_press_start, padding=(2, 2))
        pause_btn = ToggleButton(text='[b][color=2f4f4f]pause[/color][/b]', markup=True,
                                 background_color=light_sky,
                                 background_normal='',
                                 group="game",
                                 on_press=on_press_pause)
        rate_label = Label(text='[b][color=234f4f]Rate:[/color][/b]', markup=True,
                           size_hint=(1, 0.5))
        controls.add_widget(rate_label)
        for i in range(4):
            rate_btn = ToggleButton(text="[color=234f4f]{}x[/color]".format(2**i), group="rate",
                                    markup=True,
                                    background_color=light_sky,
                                    background_normal='',
                                    size_hint=(1, 0.5),
                                    on_press=wrap_on_press_rate(2**i))
            if i == 0:
                rate_btn.state = 'down'
            controls.add_widget(rate_btn)
        controls.add_widget(start_btn)
        controls.add_widget(pause_btn)
        self.add_widget(self.grid)
        self.add_widget(controls)

    def run_iteration(self):
        height = len(self.field)
        width = len(self.field[0])
        new_field = []
        for i in range(height):
            new_line = []
            for j in range(width):
                new_line.append(self.update_cell(i, j))
            new_field.append(new_line)
        self.field = new_field

    def update_cell(self, i, j):
        new_cell = 0
        num_of_neighbours = self.num_of_neighbours(i, j)
        if self.field[i][j]:
            new_cell = int(num_of_neighbours == 2 or num_of_neighbours == 3)
        else:
            new_cell = int(num_of_neighbours == 3)
        return new_cell

    def num_of_neighbours(self, i, j):
        height = len(self.field)
        width = len(self.field[0])
        sum_ = 0
        p, q = 0, 0
        for delta_i in [-1, 0, 1]:
            for delta_j in [-1, 0, 1]:
                p = i + delta_i
                q = j + delta_j
                if p >= height:
                    p = 0
                if q >= width:
                    q = 0
                sum_ += self.field[p][q]
        sum_ -= self.field[i][j]
        return sum_

    def update_grid(self, dt):
        if not self.pause_pressed and self.updates_called % self.update_rate == 0:
            self.run_iteration()
            # self.print_field()
            height = len(self.field)
            width = len(self.field[0])
            btns = self.grid.children
            for i in range(height):
                for j in range(width):
                    btn = btns[(height - i - 1) * width + (width - j - 1)]
                    if self.field[i][j]:
                        btn.state = 'down'
                    else:
                        btn.state = 'normal'
        self.updates_called += 1

    def print_field(self):
        for line in self.field:
            print()
            for cell in line:
                if cell:
                    print("*", end=" ")
                else:
                    print(".", end=" ")

    def read_field(self, filename="field.csv"):
        """
           Reads game of life field from file.
           File is expected to be in csv format with whitespace delimiter.
        """
        grid = []
        with open(filename, 'r') as fin:
            for line in fin:
                grid_line = list(map(int, line.split(" ")))
                grid.append(grid_line)
        return grid


class LifeApp(App):
    def build(self):
        game = LifeGame()
        Clock.schedule_interval(game.update_grid, 1.0/60.0)
        return game

if __name__ == '__main__':
    LifeApp().run()
