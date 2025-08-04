from typing import List


class EffectsLists:
    def __init__(self):
        self._poison_list = []

    def append_effect(self, effect_list:List[int, int], name='poison')->None:
        match name:
            case 'poison':
                self._poison_list.append(effect_list)

    def end_round(self)->int:
        damage = max(self._poison_list, key=lambda x: x[0])[0]
        for poison in self._poison_list.copy():
            poison[1] -= 1
            if poison[1] == 0:
                self._poison_list.remove(poison)
        return damage
