# -*- coding: utf8 -*-
import random
from items import Fireball, Enemy
from settings import Settings
from widgets import Background, Launchers


class CTBShooterGame(object):
    enemies = []
    fireballs = []
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
        '''
        Main game loop
        '''

        # Spawning new enemies
        for i, e in enumerate(self.last_enemies):
            tly = Settings.GAME_ZONE_TOPLEFT_CORNER[1]
            rand = random.randint(0, 120)
            dist = Settings.MIN_DISTANCE_BETWEEN_ENEMIES_IN_ROW + rand
            if not e or e.get_pos()[1] < tly - dist:
                e = self.spawn_random_enemy(i)
                self.last_enemies[e.col] = e

        # Removing enemies which reached launchers zone
        for i, e in enumerate(self.enemies):
            if e.get_pos()[1] < 60:
                e.state = 'dying'
                self.root.remove_widget(e.widget)
                self.enemies.pop(i)
                continue
            e.move()

        # Testing collisions of fireballs with enemies
        for i, f in enumerate(self.fireballs):
            x, y = f.get_pos()
            cx, cy = Settings.GAME_ZONE_TOPLEFT_CORNER
            tlx = cx - 45
            tly = cy + 45
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
        '''
        Detecting fireball launch gesture
        if user drags pointer from launchers zone to enemies zone
        '''
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
        cw = float(Settings.COL_WIDTH)
        tlx, tly = Settings.GAME_ZONE_TOPLEFT_CORNER
        mid_x = tlx + cw * enemy.col + (cw/2.0) - enemy.diameter
        mid_y = tly + enemy.diameter
        enemy.set_pos([mid_x, mid_y + random.randint(0, 220)])
