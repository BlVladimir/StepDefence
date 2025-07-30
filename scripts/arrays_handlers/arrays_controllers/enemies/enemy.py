from scripts.arrays_handlers.arrays_controllers.enemies.effects.effect_state import EffectState
from scripts.sprite.sprite3D import Sprite3D


class Enemy:
    """Класс врагов"""
    def __init__(self, sprite:Sprite3D, health:int, effect_state:EffectState):
        self._sprite = sprite
        self._sprite.external_object = self

        self._health = health

        self._effect_state = effect_state