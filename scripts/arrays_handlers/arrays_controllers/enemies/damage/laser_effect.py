from logging import info
from typing import Callable

from scripts.arrays_handlers.arrays_controllers.enemies.damage.effect import Effect


class LaserEffect(Effect):
    def __init__(self, damage: int, is_not_end:Callable[[], bool]=lambda:True):
        super().__init__(damage, 0)
        self._is_not_end = is_not_end

    @property
    def damage(self)->int:
        return self._damage + self._duration

    def check_duration(self)->bool:
        return self._is_not_end()

    def decrease_duration(self)->None:
        self._duration += 1

    def __copy__(self):
        return LaserEffect(self._damage, self._is_not_end)

    def __str__(self):
        return f'[Dam: {self._damage+self._duration}]'

    def __add__(self, other:int):
        return Effect(self._damage + other, self._duration)

    @property
    def is_not_end(self)->Callable[[], bool]:
        return self._is_not_end

    @is_not_end.setter
    def is_not_end(self, value:Callable[[], bool]):
        self._is_not_end = value