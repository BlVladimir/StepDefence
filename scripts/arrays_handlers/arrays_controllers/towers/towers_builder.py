from abc import ABC, abstractmethod

from panda3d.core import Loader

from scripts.arrays_handlers.arrays_controllers.towers.tower import Tower


class AbstractTowerBuilder(ABC):
    """Абстракция создания башни"""
    def __init__(self, loader:Loader)->None:
        self.__loader = loader

    @abstractmethod
    def create_tower(self, type_tower, tile)->Tower:
        pass

class TowerBuilder(AbstractTowerBuilder):
    """Создает башни"""
    def __init__(self, loader:Loader)->None:
        super().__init__(loader)

    def create_tower(self, type_tower, tile)->Tower:
        pass