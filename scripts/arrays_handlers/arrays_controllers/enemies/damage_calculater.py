from typing import Dict

from scripts.arrays_handlers.arrays_controllers.enemies.movement.effects_lists import EffectsLists


class DamageCalculater:
    @staticmethod
    def calculate_physic_damage(enemy_char_dict:Dict, tower_char_dict:Dict)->int:
        if 'armor_piercing' in tower_char_dict.keys() or not 'armor' in enemy_char_dict.keys():
            return tower_char_dict['damage']
        else:
            damage = tower_char_dict['damage']-enemy_char_dict['armor']
            return damage if damage > 0 else 0

    @staticmethod
    def calculate_effect(tower_char_dict:Dict, effects_lists:EffectsLists)->None:
        if 'poison' in tower_char_dict.keys():
            effects_lists.append_effect(tower_char_dict['poison'], 'poison')

    @staticmethod
    def calculate_end_round(enemy_char_dict:Dict, effects_lists:EffectsLists)->int:
        result = 0
        if 'regen' in enemy_char_dict.keys():
            result += enemy_char_dict['regen']
        result -= effects_lists.end_round()
        return result