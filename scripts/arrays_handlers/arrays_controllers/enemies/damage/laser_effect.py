from typing import Callable

from scripts.arrays_handlers.arrays_controllers.enemies.damage.effect import Effect


class LaserEffect(Effect):
    def __init__(self, damage: int):
        super().__init__(damage, 0)

    @property
    def damage(self)->int:
        return self._damage + self._duration

    def check_duration(self)->bool:
        return True

    def decrease_duration(self)->None:
        self._duration += 1

    def __copy__(self):
        return LaserEffect(self._damage)

    def __str__(self):
        return f'[Damage: {self._damage+self._duration}]'

    def __add__(self, other:int):
        return Effect(self._damage + other, self._duration)