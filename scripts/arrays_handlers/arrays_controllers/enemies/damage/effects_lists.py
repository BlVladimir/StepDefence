from scripts.arrays_handlers.arrays_controllers.enemies.damage.effect import Effect


class EffectsSets:
    def __init__(self):
        self._poison_set = set()

    def append_effect(self, effect:Effect, name='poison')->None:
        match name:
            case 'poison':
                self._poison_set.add(effect)

    def end_round(self)->int:
        damage = max(self._poison_set, key=lambda x: x.damage).damage
        for poison in self._poison_set.copy():
            poison.decrease_duration()
            if not poison.check_duration():
                self._poison_set.remove(poison)
        return damage
