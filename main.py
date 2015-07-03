# -*- coding: utf8 -*-
from events import CTBShooter

from kivy.app import App
from kivy.clock import Clock


class CTBShooterApp(App):
    def build(self):
        '''
        Initializing the game and start game cycle
        '''
        w = CTBShooter()
        Clock.schedule_interval(w.update, 1.0 / 60.0)
        return w

if __name__ == "__main__":
    CTBShooterApp().run()
