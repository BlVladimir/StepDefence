from logging import debug, getLogger
from typing import Dict, Tuple

from panda3d.core import Texture

from scripts.arrays_handlers.arrays_controllers.enemies.damage.damage_calculater import DamageCalculater
from scripts.arrays_handlers.arrays_controllers.enemies.damage.effects_sets import EffectsSets
from scripts.arrays_handlers.arrays_controllers.enemies.enemy_visitor import EnemyVisitor
from scripts.arrays_handlers.arrays_controllers.enemies.movement.movement_calculator import MovementCalculator
from scripts.arrays_handlers.arrays_controllers.enemies.ui_enemy.health_display import HealthDisplay
from scripts.main_classes.interaction.event_bus import EventBus
from scripts.sprite.sprite3D import Sprite3D


class Enemy:
    """Класс врагов"""
    def __init__(self, type_enemy:str, sprite:Sprite3D, characteristic_dict:Dict, movement_calculator:MovementCalculator, damage_calculator:DamageCalculater, cost:int, textures:Tuple[Texture, Texture]):
        self._type_enemy = type_enemy
        self._sprite = sprite
        self._sprite.external_object = self
        self._characteristic_dict = characteristic_dict

        self.__movement_calculator = movement_calculator

        self.__damage_calculator = damage_calculator
        self.__effects_sets = EffectsSets()

        self.__cost = cost

        self.__health_display = HealthDisplay(self._sprite.main_node, self._characteristic_dict['health'])
        self._textures = textures
        self.__update_texture()

        self.__log = getLogger(__name__)

    def update(self, mediator)->None:
        mediator.has_vision(self)
        self.__update_texture()

    def end_turn(self)->None:
        """Двигает всех врагов"""
        self._characteristic_dict['health'] -= self.__damage_calculator.calculate_end_round(self._characteristic_dict, self.__effects_sets)
        self.__health_display.update_health(self._characteristic_dict['health'])
        self.__chack_health()
        if self._characteristic_dict['health'] > 0:
            movement_array = self.__movement_calculator.get_movement_array()
            self._sprite.move(movement_array)

    def __chack_health(self, add_money:int=0)->None:
        """Проверка на смерть"""
        if self._characteristic_dict['health'] <= 0:
            self._sprite.main_node.detachNode()
            self._sprite.external_object = None
            EventBus.publish('enemy_die', self.__cost+add_money)

    def hit(self, tower_dict:Dict)->None:
        """Атака по врагу"""
        self._characteristic_dict['health'] -= self.__damage_calculator.calculate_physic_damage(self._characteristic_dict, tower_dict)
        self.__damage_calculator.calculate_effect(tower_dict, self.__effects_sets)
        self.__health_display.update_health(self._characteristic_dict['health'])
        self.__chack_health(tower_dict['additional_money'] if 'additional_money' in tower_dict.keys() else 0)
        self.__log.debug(f'health: {self._characteristic_dict['health']}, {self.__effects_sets}')

    def visit(self, visitor:EnemyVisitor):
        """Применяет visitor к врагу"""
        visitor.visit_characteristic_dict(self._characteristic_dict)
        visitor.visit_invisible_value(self._characteristic_dict)
        self.__update_texture()
        self.__health_display.update_health(self._characteristic_dict['health'])


    @property
    def characteristic(self)->Dict:
        char = self._characteristic_dict.copy()
        poison_str = self.__effects_sets.get_poison_str()
        if poison_str:
            char['poison'] = poison_str
        else:
            char.pop('poison', None)

        laser_str = self.__effects_sets.get_laser_str()
        if laser_str:
            char['laser'] = laser_str
        else:
            char.pop('laser', None)

        char['type_enemy'] = self._type_enemy
        return char

    @property
    def sprite(self)->Sprite3D:
        return self._sprite

    def __update_texture(self):
        if 'invisible' in self._characteristic_dict.keys():
            if self._characteristic_dict['invisible']:
                self._sprite.main_node.getPythonTag('texture_node').setTexture(self._textures[1])
            else:
                self._sprite.main_node.getPythonTag('texture_node').setTexture(self._textures[0])
