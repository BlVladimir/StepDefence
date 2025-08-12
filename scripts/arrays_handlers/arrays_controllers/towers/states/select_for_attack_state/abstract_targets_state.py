from abc import ABC, abstractmethod
from typing import Set

from scripts.arrays_handlers.arrays_controllers.enemies.enemy import Enemy
from scripts.arrays_handlers.arrays_controllers.towers.tower import Tower
from scripts.sprite.sprite3D import Sprite3D


class AbstractTargetsState(ABC):
    """Определяет, как будут выделяться и использоваться враги"""

    @staticmethod
    @abstractmethod
    def determine_set(enemies_set:Set[Enemy], tower:Tower, **kwargs)->Set[Sprite3D]:
        """Как определить множество врагов для выстрела"""
        pass

    @abstractmethod
    def hit(self, tower:Tower, **kwargs)->None:
        """В каких врагов стрелять"""
        pass

    @staticmethod
    def hit_condition(tower:Tower, **kwargs)->bool:
        pass