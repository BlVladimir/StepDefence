from _weakrefset import WeakSet
from logging import debug, warning
from typing import Dict

from scripts.arrays_handlers.arrays_controllers.enemies.damage.damage_calculater import DamageCalculater
from scripts.arrays_handlers.arrays_controllers.enemies.damage.effects_lists import EffectsSets
from scripts.arrays_handlers.arrays_controllers.enemies.movement.movement_calculator import MovementCalculator
from scripts.main_classes.interaction.event_bus import EventBus
from scripts.sprite.sprite3D import Sprite3D


class Enemy:
    """Класс врагов"""
    instances = WeakSet()

    @classmethod
    def warning(cls):
        if len(cls.instances) != 0:
            warning(f"Leftover instances: {len(cls.instances)}!!!")

    @classmethod
    def subscribe(cls):
        EventBus.subscribe('change_scene', lambda event_type, data: cls.warning())

    def __init__(self, sprite:Sprite3D, health:int, effect_dict:Dict, movement_calculator:MovementCalculator, damage_calculator:DamageCalculater):
        self._sprite = sprite
        self._sprite.external_object = self

        self._health = health

        self._effect_state = effect_dict

        self.__movement_calculator = movement_calculator

        self.__damage_calculator = damage_calculator
        self.__effects_lists = EffectsSets

        Enemy.subscribe()

    def move(self):
        """Двигает всех врагов"""
        movement_array = self.__movement_calculator.get_movement_array()
        self._sprite.move(movement_array)


    def __del__(self):
        debug(f'Node {self._sprite.main_node} deleted')
