from abc import ABC, abstractmethod


class Scene(ABC):
    """Абстрактная сцена"""

    @staticmethod
    def hide():
        """Скрывает сцену"""
        pass

    @staticmethod
    @abstractmethod
    def name()->str:
        pass