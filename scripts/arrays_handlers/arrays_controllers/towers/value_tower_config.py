from typing import Optional

from scripts.arrays_handlers.arrays_controllers.enemies.damage.effect import Effect
from scripts.arrays_handlers.arrays_controllers.enemies.damage.laser_effect import LaserEffect
from scripts.arrays_handlers.arrays_controllers.towers.towers_config import Radius


class ValueTowerConfig:
    __products = {
        'basic': dict(basic_damage=2, cost=3, radius=Radius(1), improve_cost_array=(4, 6), additional_money=2,
                      targets_state='one_target'),
        'sniper': dict(basic_damage=4, cost=5, radius=Radius(2), improve_cost_array=(6, 8),
                       targets_state='one_target'),
        'anty_shield': dict(basic_damage=3, cost=4, radius=Radius(1.5), improve_cost_array=(5, 7),
                            armor_piercing=True, targets_state='one_target'),
        'venom': dict(basic_damage=2, cost=5, radius=Radius(1), improve_cost_array=(4, 6), poison=Effect(2, 2),
                      targets_state='one_target'),
        'anty_invisible': dict(basic_damage=3, cost=4, radius=Radius(1.5), improve_cost_array=(6, 8), vision=True,
                               targets_state='one_target'),
        'cutter': dict(basic_damage=2, cost=5, radius=Radius(type_radius='infinity'), improve_cost_array=(8, 10),
                       targets_state='ray'),
        'laser': dict(basic_damage=0, cost=6, radius=Radius(1.5), improve_cost_array=(8, 10), laser=LaserEffect(0),
                      targets_state='one_target'),
        'cannon': dict(basic_damage=3, cost=8, radius=Radius(value=0.5, type_radius='infinity_splash'),
                       improve_cost_array=(10, 12), targets_state='cannon')
    }

    __sprites_towers_foundations_dict = {
        'basic': "images2d/tower/common_foundation.png",
        'sniper': "images2d/tower/sniper_foundation.png",
        'anty_shield': "images2d/tower/anty_shield.png",
        'venom': "images2d/tower/venom_foundation.png",
        'anty_invisible': "images2d/tower/anty_invisibility_tower.png",
        'cutter': 'images2d/tower/cutter_foundation.png',
        'laser': 'images2d/tower/laser_foundation.png',
        'cannon': 'images2d/tower/cannon.png'
    }

    __sprites_towers_guns_dict = {
        'basic': "images2d/tower/common_gun.png",
        'sniper': "images2d/tower/sniper_gun.png",
        'venom': "images2d/tower/venom_gun.png",
        'cutter': 'images2d/tower/cutter_gun.png',
        'laser': 'images2d/tower/laser_gun.png'
    }

    @classmethod
    def get_products(cls)->dict:
        return cls.__products.copy()

    @classmethod
    def get_sprites_towers_foundations(cls, type_tower)->str:
        return cls.__sprites_towers_foundations_dict[type_tower]

    @classmethod
    def get_sprites_towers_guns(cls, type_tower)->Optional[str]:
        if type_tower in cls.__sprites_towers_guns_dict.keys():
            return cls.__sprites_towers_guns_dict[type_tower]
        return None
