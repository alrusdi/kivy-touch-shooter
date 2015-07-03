# -*- coding: utf8 -*-
'''
Main window initialization
and events dispatcher
'''
from game import CTBShooterGame
from kivy.uix.widget import Widget


class CTBShooter(Widget):
    is_app_ready = False
    state_manager = None
    touch_coords = None

    def on_ready(self):
        self.state_manager = CTBShooterGame(self)

    def on_touch_down(self, touch):
        self.touch_coords = [touch.x, touch.y]

    def on_touch_up(self, touch):
        self.state_manager.on_slide(
            self.touch_coords,
            [touch.x, touch.y]
        )

    def on_touch_move(self, touch):
        self.state_manager.on_touch_move(touch.pos)

    def update(self, dt):
        if not self.is_app_ready:
            self.is_app_ready = True
            self.on_ready()
        else:
            self.state_manager.tick(dt)