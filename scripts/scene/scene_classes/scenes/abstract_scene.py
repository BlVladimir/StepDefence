from abc import ABC, abstractmethod


class Scene(ABC):
    """Абстрактная сцена"""

    @staticmethod
    def hide():
        """Скрывает сцену"""
        print('scene was hide')
        pass

    @staticmethod
    @abstractmethod
    def name()->str:
        pass