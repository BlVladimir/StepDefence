from logging import error
from random import randrange
from typing import Dict


class EnemiesConfig:
    """Содержит объекты врагов для копирования и их числовые значения"""
    def __init__(self):
        self.__enemies_image = {'basic':'images2d/enemy/common.png',
                                'big':'images2d/enemy/armored_enemy.png',
                                'regen':'images2d/enemy/regen.png',
                                'armored':'images2d/enemy/shield_enemy.png',
                                'invisible':'images2d/enemy/invisible.png',
                                'giant':'images2d/enemy/giant.png'
                                }

        self.__started_characteristic = {'basic': {'health':3},
                                         'big': {'health':6},
                                         'regen': {'health':4, 'regen':2},
                                         'armored': {'health':3, 'armor':3},
                                         'invisible': {'health':4,'invisible':True},
                                         'giant':{'health':10}
                                         }


    def get_image_enemy(self, type_enemy:str)->str:
        try:
            return self.__enemies_image[type_enemy]
        except Exception as Er:
            error('Error in get_image_enemy')
            raise ValueError(Er)

    def get_started_characteristic(self, type_enemy: str) -> Dict:
        try:
            return self.__started_characteristic[type_enemy].copy()
        except Exception as Er:
            error('Error in get_started_characteristic')
            raise ValueError(Er)

    @staticmethod
    def get_wave_health_modifier(wave:int)->float:
        if wave != 0:
            return 1 + (0.1 * (randrange(-1, 2)+wave//2))
        else:
            return 1