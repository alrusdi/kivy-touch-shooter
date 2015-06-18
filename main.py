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
from kivy.vector import Vector


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


class Settings(object):
    GAME_ZONE_TOPLEFT_CORNER = [0, 0],
    DAMAGE_DISTANCE = 30

type_enemy_map = {
    'circle': EnemyCircle,
    'triangle': EnemyTriangle,
    'box': EnemyBox
}

effects_map = {
    'circle': YellowFireballEffect,
    'triangle': RedFireballEffect,
    'box': GreenFireballEffect,
}

class AbstractMovable(object):
    speed = 0
    center = Vector(0, 0)
    dir_vector = Vector(0, -1)

    def move(self):
        x, y = self.get_pos()
        shift = self.dir_vector * self.speed
        self.set_pos((
            x + shift.x,
            y + shift.y
        ))
        x, y = self.get_pos()
        halfd = float(self.diameter) / 2.0
        self.center = Vector(x+halfd, y-halfd)
        self.center = Vector(x+13, y-13)

    def set_pos(self, pos):
        self.widget.pos = pos

    def get_pos(self):
        return self.widget.pos


class Enemy(AbstractMovable):
    col = 0
    diameter = 25
    type = 'circle'
    state = 'alive'

    def __init__(self, col):
        self.col = col
        self.type = random.choice(type_enemy_map.keys())
        self.speed = 1
        self.widget = type_enemy_map.get(self.type)()


class Fireball(AbstractMovable):
    diameter = 45
    type = 'circle'
    state = 'alive'

    def __init__(self, start_pos, end_pos):
        xpos = start_pos[0]
        tlx = Settings.GAME_ZONE_TOPLEFT_CORNER[0]

        if xpos < tlx + 106:
            self.type = 'triangle'
        elif xpos < tlx + 106 * 2:
            self.type = 'box'
        elif xpos < tlx + 106 * 3:
            self.type = 'circle'
        else:
            raise Exception('Wrong start pos %s' % xpos)

        w = EffectWidget(
            size = (45, 45),
            background_color = (0,0,0,0),
            pos = start_pos
        )
        w.effects = [effects_map.get(self.type)()]

        self.widget = w

        self.speed = 5
        self.dir_vector = (Vector(*end_pos) - Vector(*start_pos)).normalize()


class StateManager(object):
    enemies = []
    fireballs = []
    MIN_DISTANCE_TO_NEXT = 60
    COL_WIDTH = 106
    last_enemies = [0, 0, 0]

    def __init__(self, root):
        self.root = root
        w, h = self.root.size

        bg = Background()
        Settings.GAME_ZONE_TOPLEFT_CORNER = [w-320, 480]
        bg.pos = (w-320, 0)

        self.root.add_widget(bg)

        l = Launchers()
        l.pos = (w-320, 0)
        self.root.add_widget(l)

    def spawn_fireball(self, start_pos, end_pos):
        f = Fireball(start_pos, end_pos)
        self.fireballs.append(f)
        self.root.add_widget(f.widget)

    def tick(self, dt):

        for i, e in enumerate(self.last_enemies):
            tly = Settings.GAME_ZONE_TOPLEFT_CORNER[1]
            dist = self.MIN_DISTANCE_TO_NEXT + random.randint(0, 120)
            if not e or e.get_pos()[1] < tly - dist:
                e = self.spawn_random_enemy(i)
                self.last_enemies[e.col] = e

        for i, e in enumerate(self.enemies):
            if e.get_pos()[1] < 60:
                e.state = 'dying'
                self.root.remove_widget(e.widget)
                self.enemies.pop(i)
                continue
            e.move()

        for i, f in enumerate(self.fireballs):
            x, y = f.get_pos()
            tlx = Settings.GAME_ZONE_TOPLEFT_CORNER[0] - 45
            tly = Settings.GAME_ZONE_TOPLEFT_CORNER[1] + 45
            if x < tlx or x > tlx + 320 + 45 or y > tly:
                self.root.remove_widget(f.widget)
                self.fireballs.pop(i)
                continue
            f.move()

            for j, e in enumerate(self.enemies):
                if e.center.distance(f.center) > Settings.DAMAGE_DISTANCE:
                    continue

                self.root.remove_widget(f.widget)
                self.fireballs.pop(i)

                if e.type != f.type:
                    continue

                self.root.remove_widget(e.widget)
                self.enemies.pop(j)

                break

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
        return e

    def set_initial_enemy_pos(self, enemy):
        cw = float(self.COL_WIDTH)
        tlx, tly = Settings.GAME_ZONE_TOPLEFT_CORNER
        mid_x = tlx + cw * enemy.col + (cw/2.0) - enemy.diameter
        mid_y = tly + enemy.diameter
        enemy.set_pos([mid_x, mid_y + random.randint(0, 220)])



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
