from abc import ABC, abstractmethod
from scripts.interface.i_scene import IScene


class Scene(ABC, IScene):
    """Абстрактная сцена"""

    @staticmethod
    def hide():
        """Скрывает сцену"""
        pass

    @staticmethod
    @abstractmethod
    def name()->str:
        pass