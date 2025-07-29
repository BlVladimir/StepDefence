from scripts.arrays_handlers.arrays_controllers.towers.states.damage_state import DamageState
from scripts.arrays_handlers.arrays_controllers.towers.states.gun_state import GunState
from scripts.sprite.sprite3D import Sprite3D


class Tower:
    """Класс башни"""
    def __init__(self, type_tower: str, sprite:Sprite3D, damage_state:'DamageState', gun_state:'GunState', radius_state:'AbstractRadiusState', visitor_improve:'VisitorImprove'):
        self.__type_tower = type_tower

        self.__damage_state = damage_state
        self.__gun_strategy = gun_state
        self.__radius_strategy = radius_state

        self._tower_sprite = sprite

        self.__visitor_improve = visitor_improve

        self.__is_used = False  # башня выстрелила или нет
        self.__level = 1  # уровень башни

    def push(self):
        pass

    def upgrade(self)->None:
        self.__damage_state.upgrade(self.__visitor_improve)
        self.__radius_strategy.upgrade(self.__visitor_improve)