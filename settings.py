# -*- coding: utf8 -*-

_game_zone_size = [320, 480]
_distance_between_enemies = 60

class Settings(object):
    GAME_ZONE_TOPLEFT_CORNER = [0, 0],
    DAMAGE_DISTANCE = 30
    GAME_ZONE_SIZE = _game_zone_size
    COL_WIDTH = int(float(_game_zone_size[0])/3.0)
    MIN_DISTANCE_BETWEEN_ENEMIES_IN_ROW = _distance_between_enemies
    MAX_DISTANCE_BETWEEN_ENEMIES_IN_ROW = _distance_between_enemies + 120
