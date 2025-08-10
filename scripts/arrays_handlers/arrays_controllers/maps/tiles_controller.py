from typing import Optional

from panda3d.core import PandaNode

from scripts.arrays_handlers.arrays_controllers.maps.creating_map.map_tiles_builder import MapTilesBuilder
from scripts.arrays_handlers.arrays_controllers.maps.maps_config import MapsConfig
from scripts.arrays_handlers.arrays_controllers.maps.tile import Tile
from scripts.arrays_handlers.arrays_controllers.selector.tile_selector.tile_selector import TileSelector
from scripts.sprite.rect import Rect3D
from scripts.sprite.sprite3D import Sprite3D
from scripts.sprite.sprites_factory import SpritesFactory


class TilesController:
    """Содержит группу всех тайлов"""
    def __init__(self, maps_config:MapsConfig, maps_node:PandaNode, sprites_factory:SpritesFactory):
        self.__map_tiles_builder = MapTilesBuilder(maps_config, maps_node, sprites_factory)
        self.__tile_selector = TileSelector()

    def create_map_tiles(self, level):
        """Создает тайлы для карты карту"""
        self.__map_tiles_builder.create_map_tiles(level)

    def reset_tiles(self):
        """Очищает карту"""
        self.__map_tiles_builder.reset_map()

    def handle_tile_action(self, action: str, tile_sprite: Sprite3D = None) -> None:
        """Обрабатывает действия с тайлами.

        Параметры:
            action (str): Тип действия ('select', 'unselect', 'using').
            tile_sprite (Sprite3D, опционально): Спрайт тайла, если действие требует его.
        """
        match action:
            case 'select':
                self.__tile_selector.select_sprite(tile_sprite)
            case 'unselect':
                self.__tile_selector.unselect_sprite()
            case 'using':
                self.__tile_selector.set_used_sprite()

    @property
    def first_tile_rect(self)->Rect3D:
        return self.__map_tiles_builder.first_tile_rect

    @property
    def selected_tile(self)->Optional[Tile]:
        if self.__tile_selector.used_sprite:
            return self.__tile_selector.used_sprite.external_object
        return None

    @property
    def track(self):
        return self.__map_tiles_builder.track