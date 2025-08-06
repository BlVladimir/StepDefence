from typing import Optional

from panda3d.core import PandaNode

from scripts.arrays_handlers.arrays_controllers.maps.creating_map.map_tiles_builder import MapTilesBuilder
from scripts.arrays_handlers.arrays_controllers.maps.maps_config import MapsConfig
from scripts.arrays_handlers.arrays_controllers.maps.tile import Tile
from scripts.arrays_handlers.using_element_controller import UsingElementController
from scripts.main_classes.interaction.event_bus import EventBus
from scripts.sprite.rect import Rect3D
from scripts.sprite.sprite3D import Sprite3D
from scripts.sprite.sprites_factory import SpritesFactory


class TilesController:
    """Содержит группу всех тайлов"""
    def __init__(self, maps_config:MapsConfig, maps_node:PandaNode, sprites_factory:SpritesFactory):
        self.__map_tiles_builder = MapTilesBuilder(maps_config, maps_node, sprites_factory)
        self.__tile_selector = UsingElementController(using_action=self.__using_action, unused_action=self.__unused_action)

    def create_map_tiles(self, level):
        """Создает тайлы для карты карту"""
        self.__map_tiles_builder.create_map_tiles(level)

    def reset_tiles(self):
        """Очищает карту"""
        self.__map_tiles_builder.reset_map()

    def __unused_action(self):
        tower_node = self.__tile_selector.sel_using_sprite.main_node.find('tower')
        if self.__tile_selector.sel_using_sprite.external_object.effect != 'road' and not tower_node:
            EventBus.publish('close_shop')
        elif tower_node:
            tower_node.getPythonTag('sprite').external_object.hide_radius()
            EventBus.publish('close_upgrade_table')

    def __using_action(self):
        tower_node = self.__tile_selector.sel_using_sprite.main_node.find('tower')
        if self.__tile_selector.sel_using_sprite.external_object.effect != 'road' and not tower_node:
            EventBus.publish('open_shop')
        elif tower_node:
            tower_node.getPythonTag('sprite').external_object.show_radius()
            EventBus.publish('open_upgrade_table')

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
                self.__tile_selector.using_sprite()

    @property
    def first_tile_rect(self)->Rect3D:
        return self.__map_tiles_builder.first_tile_rect

    @property
    def selected_tile(self)->Optional[Tile]:
        if self.__tile_selector.sel_using_sprite:
            return self.__tile_selector.sel_using_sprite.external_object
        return None

    @property
    def track(self):
        return self.__map_tiles_builder.track