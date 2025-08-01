from logging import warning, error

from panda3d.core import PandaNode

from scripts.arrays_handlers.arrays_controllers.maps.creating_map.map_tiles_builder import MapTilesBuilder
from scripts.arrays_handlers.arrays_controllers.maps.maps_config import MapsConfig
from scripts.arrays_handlers.arrays_controllers.maps.tile import Tile
from scripts.arrays_handlers.parts_handler.using_element_controller import UsingElementController
from scripts.interface.i_context import IContext
from scripts.main_classes.settings import Settings
from scripts.sprite.rect import Rect3D
from scripts.sprite.sprite3D import Sprite3D


class TilesController:
    """Содержит группу всех тайлов"""
    def __init__(self, maps_config:MapsConfig, maps_node:PandaNode, loader, context:IContext):
        self.__map_tiles_builder = MapTilesBuilder(maps_config, maps_node, loader)
        self.__tile_selector = UsingElementController(using_action=self.using_action, unused_action=lambda cont=context: cont.buttons_controller.close_shop())
        self.__context = context

    def create_map_tiles(self, level, settings:Settings):
        """Создает тайлы для карты карту"""
        self.__map_tiles_builder.create_map_tiles(level, settings)

    def reset_tiles(self):
        """Очищает карту"""
        self.__map_tiles_builder.reset_map()

    def using_action(self):
        if self.__tile_selector.using_tile_sprite.external_object.effect != 'road' and not self.__tile_selector.using_tile_sprite.main_node.find('tower'):
            self.__context.buttons_controller.open_shop()

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
    def selected_tile(self)->Tile:
        return self.__tile_selector.using_tile_sprite.external_object

    @property
    def track(self):
        return self.__map_tiles_builder.track