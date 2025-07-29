from abc import ABC, abstractmethod

from panda3d.core import Loader

from scripts.arrays_handlers.arrays_controllers.maps.tile import Tile
from scripts.arrays_handlers.arrays_controllers.towers.damage_state_maker import DamageStateMaker
from scripts.arrays_handlers.arrays_controllers.towers.states.gun_state import GunState
from scripts.arrays_handlers.arrays_controllers.towers.states.radius_state import RoundRadius
from scripts.arrays_handlers.arrays_controllers.towers.tower import Tower
from scripts.arrays_handlers.arrays_controllers.towers.towers_config import TowersConfig
from scripts.sprite.sprite3D import CopyingSprite3D, Sprite3D


class AbstractTowerBuilder(ABC):
    """Абстракция создания башни"""
    def __init__(self, loader:Loader)->None:
        self.__loader = loader


    @abstractmethod
    def create_tower(self, type_tower:str, tile:Tile)->None:
        pass




class TowerBuilder(AbstractTowerBuilder):
    """Создает башни"""
    def __init__(self, loader:Loader)->None:
        super().__init__(loader)
        self.__config = TowersConfig()
        self.__damage_states_maker = DamageStateMaker()

    def create_tower(self, type_tower:str, tile:Tile)->None:
        damage_state = self.__damage_states_maker.create_state(self.__config.get_started_characteristic_dict(type_tower))

        match self.__config.get_radius(type_tower).type_radius:
            case 'round':
                radius_state = RoundRadius(self.__config.get_radius(type_tower).value)
            case _:
                raise Exception('Incorrect radius type')

        if self.__config.get_gun:
            gun_state = GunState(sprite=Sprite3D(tile.sprite.rect, self.__config.get_image_foundation(type_tower),
                                                 tile.sprite.main_node, self.__loader, 3, 'gun'))
        else:
            gun_state = None

        Tower(
            type_tower=type_tower,
            sprite=Sprite3D(tile.sprite.rect, self.__config.get_image_foundation(type_tower),
                            tile.sprite.main_node, self.__loader, 2, 'tower'),
            damage_state=damage_state,
            radius_state=radius_state,
            gun_state=gun_state,
            visitor_improve=self.__config.get_visitor_improve(type_tower)
        )