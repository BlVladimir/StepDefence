from scripts.arrays_handlers.arrays_controllers.maps.maps_config import MapsConfig
from scripts.arrays_handlers.arrays_controllers.maps.tile import Tile
from scripts.arrays_handlers.arrays_controllers.maps.tiles_controller import TilesController
from scripts.interface.i_context import IContext
from scripts.main_classes.interaction.render_manager import RenderManager
from scripts.main_classes.settings import Settings
from scripts.sprite.rect import Rect3D
from scripts.sprite.sprite3D import Sprite3D


class MapsController:
    """Обработчик карт"""
    def __init__(self, render:RenderManager, context:IContext, settings:Settings):
        self.__map_node = render.main_node3d.attachNewNode("map_node")
        self.__map_config = MapsConfig()
        self.__tiles_controller = TilesController(self.__map_config, self.__map_node, render.loader, context)
        self._settings = settings

    def create_map(self, level):
        """Создать карту"""
        self.__tiles_controller.create_map_tiles(level, self._settings)

    def clear_map(self):
        """Очистить карту"""
        self.__map_node.getChildren().detach()
        self.__tiles_controller.reset_tiles()

    def select_element(self, sprite:Sprite3D):
        """Выделить спрайт"""
        match sprite.main_node.getName():
            case 'tile':
                self.__tiles_controller.handle_tile_action('select', sprite)

    def unselect_element(self, sprite:Sprite3D):
        """Отменить выделение у спрайта"""
        match sprite.main_node.getName():
            case 'tile':
                self.__tiles_controller.handle_tile_action('unselect')

    def using_element(self):
        """Назначить спрайт активным"""
        self.__tiles_controller.handle_tile_action('using')

    def get_selected_tile(self)->Tile:
        return self.__tiles_controller.selected_tile

    @property
    def first_tile_rect(self)->Rect3D:
        return self.__tiles_controller.first_tile_rect

    @property
    def track(self):
        return self.__tiles_controller.track