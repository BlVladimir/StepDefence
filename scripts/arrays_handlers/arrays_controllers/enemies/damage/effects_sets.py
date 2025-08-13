from copy import copy
from unittest import TestCase

from scripts.arrays_handlers.arrays_controllers.enemies.damage.effect import Effect
from scripts.arrays_handlers.arrays_controllers.enemies.damage.laser_effect import LaserEffect


class EffectsSets:
    def __init__(self):
        self._poison_set = set()
        self._laser_set = set()

    def append_effect(self, effect:Effect | LaserEffect, name='poison')->None:
        match name:
            case 'poison':
                self._poison_set.add(copy(effect))
            case 'laser':
                self._laser_set.add(copy(effect))


    def end_round(self)->int:
        if self._poison_set or self._laser_set:
            damage = 0
            damage += max(self._poison_set, key=lambda x: x.damage).damage if self._poison_set else 0
            damage += sum(laser.damage for laser in self._laser_set) if self._laser_set else 0
            for poison in self._poison_set.copy():
                poison.decrease_duration()
                if not poison.check_duration():
                    self._poison_set.remove(poison)
            for laser in self._laser_set.copy():
                laser.decrease_duration()
                if not laser.check_duration():
                    self._laser_set.remove(laser)
            return damage
        return 0

    def __str__(self):
        return str(',\n'.join(str(eff) for eff in self._poison_set))

class EffectSetsTest(TestCase):
    def setUp(self):
        self.effect_sets = EffectsSets()
        self.effect1 = Effect(1, 1)
        self.effect2 = Effect(2, 2)
        self.effect3 = Effect(1, 3)
        self.effect_sets.append_effect(self.effect1)
        self.effect_sets.append_effect(self.effect2)
        self.effect_sets.append_effect(self.effect3)

    def test_first_round(self):
        self.assertEqual(self.effect_sets.end_round(), 2)
        self.assertEqual(self.effect_sets.end_round(), 2)
        self.assertEqual(self.effect_sets.end_round(), 1)
        self.assertEqual(self.effect_sets.end_round(), 0)