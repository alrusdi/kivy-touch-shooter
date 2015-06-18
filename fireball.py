# -*- coding: utf8 -*-
from kivy.uix.effectwidget import AdvancedEffectBase
from kivy.uix.effectwidget import EffectBase

with open('fireball.glsl', 'r') as f:
    fireball_glsl_code = f.read()

class RedFireballEffect(EffectBase):
    glsl = fireball_glsl_code.replace('main_color = vec4(0, 0.5, 1, 0.6)', 'main_color = vec4(1.0, 0.0, 0.0, 0.8)')

class YellowFireballEffect(EffectBase):
    glsl = fireball_glsl_code.replace('main_color = vec4(0, 0.5, 1, 0.6)', 'main_color = vec4(1.0, 1.0, 0.0, 0.8)')

class GreenFireballEffect(EffectBase):
    glsl = fireball_glsl_code.replace('main_color = vec4(0, 0.5, 1, 0.6)', 'main_color = vec4(0.0, 1.0, 0.0, 0.8)')

