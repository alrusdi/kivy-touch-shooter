# -*- coding: utf8 -*-
import random
from kivy.uix.effectwidget import EffectWidget
from kivy.vector import Vector
from fireball import RedFireballEffect, YellowFireballEffect, GreenFireballEffect
from settings import Settings
from widgets import EnemyBox, EnemyTriangle, EnemyCircle

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