from _weakrefset import WeakSet
from logging import debug, warning, getLogger
from typing import Dict

from scripts.arrays_handlers.arrays_controllers.enemies.damage.damage_calculater import DamageCalculater
from scripts.arrays_handlers.arrays_controllers.enemies.damage.effects_sets import EffectsSets
from scripts.arrays_handlers.arrays_controllers.enemies.enemy_visitor import EnemyVisitor
from scripts.arrays_handlers.arrays_controllers.enemies.movement.movement_calculator import MovementCalculator
from scripts.arrays_handlers.arrays_controllers.enemies.ui_enemy.health_display import HealthDisplay
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

    def __init__(self, sprite:Sprite3D, characteristic_dict:Dict, movement_calculator:MovementCalculator, damage_calculator:DamageCalculater, cost:int):
        self._sprite = sprite
        self._sprite.external_object = self
        self._characteristic_dict = characteristic_dict

        self.__movement_calculator = movement_calculator

        self.__damage_calculator = damage_calculator
        self.__effects_sets = EffectsSets()

        self.__cost = cost

        self.__health_display = HealthDisplay(self._sprite.main_node, self._characteristic_dict['health'])

        self.__log = getLogger(__name__)

        Enemy.subscribe()

    def end_turn(self)->None:
        """Двигает всех врагов"""
        self.__damage_calculator.calculate_end_round(self._characteristic_dict, self.__effects_sets)
        self.__health_display.update_health(self._characteristic_dict['health'])
        self.__chack_health()
        if self._characteristic_dict['health'] > 0:
            movement_array = self.__movement_calculator.get_movement_array()
            self._sprite.move(movement_array)

    def __chack_health(self, add_money:int=0)->None:
        if self._characteristic_dict['health'] <= 0:
            self._sprite.main_node.detachNode()
            EventBus.publish('enemy_die', self.__cost+add_money)

    def hit(self, tower_dict:Dict)->None:
        self._characteristic_dict['health'] -= self.__damage_calculator.calculate_physic_damage(self._characteristic_dict, tower_dict)
        self.__damage_calculator.calculate_effect(tower_dict, self.__effects_sets)
        self.__health_display.update_health(self._characteristic_dict['health'])
        self.__chack_health(tower_dict.setdefault('additional_money', 0))
        self.__log.debug(f'health: {self._characteristic_dict['health']}, {self.__effects_sets}')

    def visit(self, visitor:EnemyVisitor):
        visitor.visit_damage_dict(self._characteristic_dict)
        self.__health_display.update_health(self._characteristic_dict['health'])

    @property
    def characteristic(self)->Dict:
        char = self._characteristic_dict.copy()
        char['poison'] = str(self.__effects_sets)
        return char

    def __del__(self):
        debug(f'Node {self._sprite.main_node} deleted')
