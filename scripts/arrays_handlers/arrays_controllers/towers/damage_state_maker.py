from typing import Dict

from scripts.arrays_handlers.arrays_controllers.towers.states.damage_state import DamageState


class DamageStateMaker:
    """Создает состояния урона для башни"""

    def __init__(self):
        self.__priority_array = ('addition_money', 'basic_damage', 'poison', 'armor_piercing')
        self.__func_dict = {'poison':self.__poison_func,
                            'armor_piercing':self.__piercing_armor_func,
                            'basic_damage':self.__basic_damage_func,
                            'addition_money':self.__addition_money}

    @staticmethod
    def __basic_damage_func(enemy, func=None, **kwargs)->None:
        enemy.reduce_health_with_armor(kwargs['damage'])
        func(enemy, kwargs)

    @staticmethod
    def __poison_func(enemy, func=None, **kwargs)->None:
        enemy.to_poison(kwargs['poison_damage'])
        func(enemy, kwargs)

    @staticmethod
    def __piercing_armor_func(enemy, func=None, **kwargs)->None:
        enemy.reduce_health(kwargs['damage'])
        func(enemy, kwargs)

    @staticmethod
    def __addition_money(enemy, func=None, **kwargs)->None:
        enemy.increase_additional_money(kwargs['additional_money'])
        func(enemy, kwargs)

    def create_state(self, characteristic_dict:Dict)->DamageState:
        states = []
        for i in self.__priority_array:
            if i in characteristic_dict.keys():
                states.append(i)
        func_array = []
        for i in states:
            func_array.append(self.__func_dict[i])
        return DamageState(func_array, characteristic_dict)
