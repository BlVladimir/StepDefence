from typing import Dict
from unittest import TestCase

from scripts.arrays_handlers.arrays_controllers.enemies.damage.effect import Effect
from scripts.arrays_handlers.arrays_controllers.enemies.damage.effects_sets import EffectsSets


class DamageCalculater:
    @staticmethod
    def calculate_physic_damage(enemy_char_dict:Dict, tower_char_dict:Dict)->int:
        if 'armor_piercing' in tower_char_dict.keys() or not 'armor' in enemy_char_dict.keys():
            return tower_char_dict['basic_damage']
        else:
            damage = tower_char_dict['basic_damage']-enemy_char_dict['armor']
            return damage if damage > 0 else 0

    @staticmethod
    def calculate_effect(tower_char_dict:Dict, effects_sets:EffectsSets)->None:
        if 'poison' in tower_char_dict.keys():
            effects_sets.append_effect(tower_char_dict['poison'], 'poison')
        if 'laser' in tower_char_dict.keys():
            effects_sets.append_effect(tower_char_dict['laser'], 'laser')

    @staticmethod
    def calculate_end_round(enemy_char_dict:Dict, effects_sets:EffectsSets)->int:
        result = 0
        if 'regen' in enemy_char_dict.keys():
            result -= enemy_char_dict['regen']
        result += effects_sets.end_round()
        return result

class DamageCalculatorTest(TestCase):
    def setUp(self):
        self.damage_calculater = DamageCalculater()
        self.effects_sets = EffectsSets()
        self.effects_sets.append_effect(Effect(1, 1))
        self.damage_dict1 = {
            'basic_damage': 3,
            'poison': Effect(2, 2)
        }
        self.damage_dict2 = {
            'basic_damage': 3,
            'poison':Effect(1, 2),
            'armor_piercing': True
        }
        self.char_dict = {
            'health': 10,
            'regen': 1,
            'armor': 2
        }

    def test_calculate_physic_damage(self):
        self.assertEqual(self.damage_calculater.calculate_physic_damage(self.char_dict, self.damage_dict1), 1)
        self.assertEqual(self.damage_calculater.calculate_physic_damage(self.char_dict, self.damage_dict2), 3)

    def test_calculate_effect(self):
        self.damage_calculater.calculate_effect(self.damage_dict1, self.effects_sets)
        self.assertEqual(self.damage_calculater.calculate_end_round(self.char_dict, self.effects_sets), 1)
        self.damage_calculater.calculate_effect(self.damage_dict2, self.effects_sets)
        self.assertEqual(self.damage_calculater.calculate_end_round(self.char_dict, self.effects_sets), 1)
        self.assertEqual(self.damage_calculater.calculate_end_round(self.char_dict, self.effects_sets), 0)