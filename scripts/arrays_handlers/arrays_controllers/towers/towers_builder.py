from abc import ABC, abstractmethod
from logging import debug

from panda3d.core import Loader, CullBinManager

from scripts.arrays_handlers.arrays_controllers.maps.tile import Tile
from scripts.arrays_handlers.arrays_controllers.towers.damage_state_maker import DamageStateMaker
from scripts.arrays_handlers.arrays_controllers.towers.states.gun_state import GunState
from scripts.arrays_handlers.arrays_controllers.towers.states.radius_state import RoundRadius
from scripts.arrays_handlers.arrays_controllers.towers.tower import Tower
from scripts.arrays_handlers.arrays_controllers.towers.towers_config import TowersConfig
from scripts.main_classes.settings import Settings
from scripts.sprite.sprite3D import CopyingSprite3D, Sprite3D


class AbstractTowerBuilder(ABC):
    """Абстракция создания башни"""
    def __init__(self, loader:Loader)->None:
        self._loader = loader
        self._counter = 0

        CullBinManager.get_global_ptr().add_bin('tower', CullBinManager.BT_fixed, 2)
        CullBinManager.get_global_ptr().add_bin('gun', CullBinManager.BT_fixed, 3)

    @abstractmethod
    def create_tower(self, type_tower:str, tile:Tile, settings:Settings)->None:
        pass

    def reset_counter(self):
        self._counter = 0


class TowerBuilder(AbstractTowerBuilder):
    """Создает башни"""
    def __init__(self, loader:Loader)->None:
        super().__init__(loader)
        self.__config = TowersConfig()
        self.__damage_states_maker = DamageStateMaker()

    def create_tower(self, type_tower:str, tile:Tile, settings:Settings)->None:
        damage_state = self.__damage_states_maker.create_state(self.__config.get_started_characteristic_dict(type_tower))

        match self.__config.get_radius(type_tower).type_radius:
            case 'round':
                radius_state = RoundRadius(self.__config.get_radius(type_tower).value)
            case _:
                raise Exception('Incorrect radius type')


        if self.__config.get_gun(type_tower):
            gun_state = GunState(sprite=Sprite3D(tile.sprite.rect, self.__config.get_gun(type_tower),
                                                 tile.sprite, self._loader, 'gun', self._counter))
        else:
            gun_state = None

        Tower(
            type_tower=type_tower,
            sprite=Sprite3D(tile.sprite.rect, self.__config.get_image_foundation(type_tower),
                            tile.sprite, self._loader, 'tower', self._counter, settings.debug_mode),
            damage_state=damage_state,
            radius_state=radius_state,
            gun_state=gun_state,
            visitor_improve=self.__config.get_visitor_improve(type_tower)
        )

        self._counter += 1