from _weakrefset import WeakSet
from logging import debug, info

from direct.interval.LerpInterval import LerpPosInterval
from direct.interval.MetaInterval import Sequence
from panda3d.core import Vec3, LineSegs

from scripts.arrays_handlers.arrays_controllers.enemies.movement.effect_state import EffectState
from scripts.arrays_handlers.arrays_controllers.enemies.movement.movement_calculator import MovementCalculator
from scripts.main_classes.interaction.event_bus import EventBus
from scripts.sprite.sprite3D import Sprite3D


class Enemy:
    """Класс врагов"""
    instances = WeakSet()

    @classmethod
    def subscribe(cls):
        EventBus.subscribe('change_scene', lambda event_type, data: debug(f"Leftover instances: {len(cls.instances)}"))

    def __init__(self, sprite:Sprite3D, health:int, effect_state:EffectState, movement_calculator:MovementCalculator):
        self._sprite = sprite
        self._sprite.external_object = self

        self._health = health

        self._effect_state = effect_state

        self.__movement_calculator = movement_calculator

        Enemy.subscribe()


    def move(self):
        """Двигает всех врагов"""
        intervals = []
        movement_array = self.__movement_calculator.get_movement_array()
        for i in range(1, len(movement_array)):
            intervals.append(
                LerpPosInterval(
                    self._sprite.main_node,  # Ваша нода
                    duration=0.05,
                    pos=movement_array[i],
                    startPos=movement_array[i - 1]
                )
            )
        sequence = Sequence(*intervals)
        sequence.start()

    def __del__(self):
        debug(f'Node {self._sprite.main_node} deleted')
