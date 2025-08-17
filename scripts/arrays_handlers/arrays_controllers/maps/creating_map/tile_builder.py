from abc import ABC, abstractmethod

from panda3d.core import PandaNode, Loader, CullBinManager

from scripts.arrays_handlers.arrays_controllers.maps.maps_config import MapsConfig
from scripts.arrays_handlers.arrays_controllers.maps.tile import Tile
from scripts.main_classes.settings import Settings
from scripts.sprite.rect import Rect3D
from scripts.sprite.sprite3D import CopyingSprite3D, Sprite3D
from scripts.sprite.sprites_factory import SpritesFactory


class AbstractTilesBuilder(ABC):
    """Интерфейс для создания тайлов"""
    def __init__(self, maps_node:PandaNode, sprites_factory:SpritesFactory):
        self._maps_node = maps_node
        self._sprites_factory = sprites_factory
        self._counter = 0

        CullBinManager.get_global_ptr().add_bin('tile', CullBinManager.BT_fixed, 1)

    @abstractmethod
    def create_tile(self, type_tile:str, rect:Rect3D)->Tile:
        pass

    def reset_counter(self):
        self._counter = 0

# class TilesPrototype(AbstractTilesBuilder):
#     def __init__(self, maps_node:PandaNode, loader):
#         super().__init__(maps_node, loader)
#         self.__tiles = {'road':CopyingSprite3D('images2d/tile/for_enemies.png', super()._maps_node, super().__loader, 1, 'tile'),
#                         'base':CopyingSprite3D('images2d/tile/common_building.png', super()._maps_node, super().__loader, 1, 'tile'),
#                         'basic':CopyingSprite3D('images2d/tile/common_building.png', super()._maps_node, super().__loader, 1, 'tile'),
#                         'increase_damage':CopyingSprite3D('images2d/tile/damage_up.png', super()._maps_node, super().__loader, 1, 'tile'),
#                         'increase_radius':CopyingSprite3D('images2d/tile/radius_up.png', super()._maps_node, super().__loader, 1, 'tile'),
#                         'piercing_armor':CopyingSprite3D('images2d/tile/piercing_armor.png', super()._maps_node, super().__loader, 1, 'tile'),
#                         'poison':CopyingSprite3D('images2d/tile/poison_up.png', super()._maps_node, super().__loader, 1, 'tile'),
#                         'additional_money':CopyingSprite3D('images2d/tile/money_up.png', super()._maps_node, super().__loader, 1, 'tile')}
#
#     def  create_tile(self, type_tile:str, rect:Rect3D, settings:Settings):
#         if type_tile in self.__tiles.keys():
#             return Tile(self.__tiles[type_tile].copy(rect), type_tile)
#         else:
#             raise ValueError('Incorrect type of tile')

class TilesBuilder(AbstractTilesBuilder):
    def  create_tile(self, type_tile:str, rect:Rect3D)->Tile:
        try:
            sprite = self._sprites_factory.create_sprite(rect, MapsConfig.get_path(type_tile), self._maps_node, 'tile', self._counter)
            self._counter += 1
            return Tile(sprite, type_tile)
        except KeyError:
            raise KeyError('Incorrect type of tile')