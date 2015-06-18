import random
from fireball import RedFireballEffect, YellowFireballEffect, GreenFireballEffect
from kivy.app import App
from kivy.properties import (
    ObjectProperty,
    NumericProperty,
    StringProperty,
    ObjectProperty,
    ReferenceListProperty
)
from kivy.uix.effectwidget import EffectWidget

from kivy.uix.widget import Widget
from kivy.clock import Clock

class Background(Widget):
    pass

class EnemyCircle(Widget):
    pass

class EnemyBox(Widget):
    pass

class EnemyTriangle(Widget):
    pass

class Launchers(Widget):
    pass

class FireballTriangle(EffectWidget):
    pass


type_enemy_map = {
    'circle': EnemyCircle,
    'triangle': EnemyTriangle,
    'box': EnemyBox
}

effets_map = {
    'circle': YellowFireballEffect,
    'triangle': RedFireballEffect,
    'box': GreenFireballEffect,
}

class Enemy(object):
    speed = 0
    col = 0
    diameter = 25
    type = 'circle'
    state = 'alive'

    def __init__(self, col):
        self.col = col
        self.type = random.choice(type_enemy_map.keys())
        self.speed = 1
        self.widget = type_enemy_map.get(self.type)()

    def move(self):
        x, y = self.get_pos()
        y -= self.speed
        self.set_pos([x, y])

    def set_pos(self, pos):
        self.widget.pos = pos

    def get_pos(self):
        return self.widget.pos



class StateManager(object):
    enemies = []
    fireballs = []
    MIN_SPAWN_INTERVAL = 1
    COL_WIDTH = 106
    GAME_ZONE_TOPLEFT_CORNER = [0, 0]
    time_acc = [0, 0, 0]

    def __init__(self, root):
        self.root = root
        w, h = self.root.size

        bg = Background()
        self.GAME_ZONE_TOPLEFT_CORNER = [w-320, 480]
        bg.pos = (w-320, 0)

        self.root.add_widget(bg)

        l = Launchers()
        l.pos = (w-320, 0)
        self.root.add_widget(l)

        f = EffectWidget(
            size=(100, 100),
            pos=(w-320, 0),
            background_color = [0,0,0,0]
        )
        f.effects = [GreenFireballEffect()]
        self.fireballs.append(f)
        self.root.add_widget(f)

    def spawn_fireball(self, start_pos, end_pos):
        pass

    def tick(self, dt):

        for i, v in enumerate(self.time_acc):
            v += dt

            if v > self.MIN_SPAWN_INTERVAL + random.random() * 3.5:
                self.spawn_random_enemy(i)
                v = 0
            self.time_acc[i] = v

        for e in self.enemies:
            e.move()

        for f in self.fireballs:
            pass

    def on_slide(self, start_pos, end_pos):
        if start_pos[1] < 60 < end_pos[1]:
            self.spawn_fireball(start_pos, end_pos)

    def on_touch_move(self, pos):
        pass

    def spawn_random_enemy(self, col):
        e = Enemy(col)
        self.set_initial_enemy_pos(e)
        self.enemies.append(e)
        self.root.add_widget(e.widget)

    def set_initial_enemy_pos(self, enemy):
        cw = float(self.COL_WIDTH)
        mid_x = self.GAME_ZONE_TOPLEFT_CORNER[0] + cw * enemy.col + (cw/2.0) - enemy.diameter
        mid_y = self.GAME_ZONE_TOPLEFT_CORNER[1] + enemy.diameter
        enemy.set_pos([mid_x, mid_y])



class CTBShooter(Widget):
    is_app_ready = False
    state_manager = ObjectProperty(None)
    touch_coords = None

    def on_ready(self):
        self.state_manager = StateManager(self)

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


class CTBShooterApp(App):
    def build(self):

        w = CTBShooter()
        Clock.schedule_interval(w.update, 1.0 / 60.0)
        return w

if __name__ == "__main__":
    CTBShooterApp().run()
