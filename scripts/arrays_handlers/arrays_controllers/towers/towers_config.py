from typing import Tuple, Dict, Optional

from scripts.arrays_handlers.arrays_controllers.enemies.damage.effect import Effect
from scripts.arrays_handlers.arrays_controllers.towers.upgrade_visitor import UpgradeVisitor

class Radius:
    def __init__(self, value:float, type_radius:str='round'):
        self._value = value
        self._type_radius = type_radius

    @property
    def value(self):
        return self._value

    @property
    def type_radius(self):
        return self._type_radius

class TowersConfig:
    """Содержит объекты башен для копирования и их числовые значения"""
    def __init__(self):
        self.__products = {
            'basic': dict(basic_damage=2, cost=3, radius=Radius(1), improve_cost_array=(4, 6), additional_money=2),
            'sniper': dict(basic_damage=4, cost=5, radius=Radius(2), improve_cost_array=(6, 8)),
            'anty_shield': dict(basic_damage=3, cost=4, radius=Radius(1.5), improve_cost_array=(5, 7), armor_piercing=True),
            'venom': dict(basic_damage=2, cost=5, radius=Radius(1), improve_cost_array=(4, 6), poison=Effect(2, 2))}

        self.__sprites_towers_foundations_dict = {
            'basic':"images2d/tower/common_foundation.png",
            'sniper':"images2d/tower/sniper_foundation.png",
            'anty_shield':"images2d/tower/anty_shield.png",
            'venom':"images2d/tower/venom_foundation.png"}

        self.__sprites_towers_guns_dict = {
            'basic':"images2d/tower/common_gun.png",
            'sniper':"images2d/tower/sniper_gun.png",
            'venom':"images2d/tower/venom_gun.png"}

        self.__visitors_dict = {
            'basic': UpgradeVisitor(damage=2, radius=1.2),
            'sniper': UpgradeVisitor(damage=2, radius=1.2),
            'anty_shield': UpgradeVisitor(damage=2, radius=1.2),
            'venom': UpgradeVisitor(damage=2, radius=1.2)}

    def get_visitor_improve(self, type_tower:str)->UpgradeVisitor:
        return self.__visitors_dict[type_tower]

    def get_improve_cost_array(self, type_tower:str)->Tuple:
        return self.__products[type_tower]['improve_cost_array']

    def get_started_characteristic_dict(self, type_tower:str)->Dict:
        r = {}
        for i in ['basic_damage', 'armor_piercing', 'poison', 'additional_money']:
            if i in self.__products[type_tower].keys():
                r[i] = self.__products[type_tower][i]
        return r

    def get_cost(self, type_tower:str)->int:
        return self.__products[type_tower]['cost']

    def get_image_foundation(self, type_tower:str)->str:
        return self.__sprites_towers_foundations_dict[type_tower]

    def get_gun(self, type_tower: str)->Optional[str]:
        if type_tower in self.__sprites_towers_guns_dict.keys():
            return self.__sprites_towers_guns_dict[type_tower]
        return None

    def get_radius(self, type_tower: str)->Radius:
        return self.__products[type_tower]['radius']