from typing import List, Dict


class DamageState:
    """Состояние, влияющее на тип урона башни"""

    def __init__(self, func_array:List, damage_dict:Dict):
        self.__damage_dict = damage_dict
        self.__func_array = func_array

    def __composition_push_functions(self, enemy, functions:List, dict_arguments:Dict):
        if len(functions) == 1:
            return functions[0](enemy, dict_arguments)
        return functions[0](enemy, self.__composition_push_functions(enemy, functions.pop(0), dict_arguments),
                            dict_arguments)

    def push(self, enemy)->None:
        self.__composition_push_functions(enemy, self.__func_array, self.__damage_dict)

    def improve_damage(self, type_damage:str, value:float)->None:
        if type_damage in self.__damage_dict.keys():
            self.__damage_dict[type_damage] += value

    def upgrade(self, visitor:'UpgradeVisitor')->None:
        visitor.visit_damage_state(self)