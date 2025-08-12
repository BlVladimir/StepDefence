from abc import ABC, abstractmethod
from typing import Set

from scripts.arrays_handlers.arrays_controllers.enemies.enemy import Enemy


class AbstractSelectState(ABC):
    """Определяет, как будут выделяться и использоваться враги"""

    @staticmethod
    @abstractmethod
    def update_set(**kwargs)->None:
        """Когда обновлять множество врагов"""
        pass

    @staticmethod
    @abstractmethod
    def determine_set(enemies_set:Set[Enemy], **kwargs)->Set[Enemy]:
        """Как определить множество врагов для выстрела"""
        pass

    @staticmethod
    @abstractmethod
    def hit(**kwargs)->None:
        """В каких врагов стрелять"""
        pass