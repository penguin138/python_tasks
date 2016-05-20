from kivy.app import App
from kivy.uix.widget import Widget


class LifeGame(Widget):
    pass


class LifeApp(App):
    def build(self):
        return LifeGame()

if __name__ == '__main__':
    LifeApp().run()
