from scripts.arrays_handlers.arrays_controllers.maps.maps_config import MapsConfig
from scripts.arrays_handlers.arrays_controllers.maps.tile import Tile
from scripts.arrays_handlers.arrays_controllers.maps.tiles_controller import TilesController
from scripts.interface.i_context import IContext
from scripts.main_classes.interaction.render_manager import RenderManager
from scripts.sprite.sprite3D import Sprite3D


class MapsController:
    """Обработчик карт"""
    def __init__(self, render:RenderManager, context:IContext):
        self.__map_node = render.main_node3d.attachNewNode("map_node")
        self.__map_config = MapsConfig()
        self.__tiles_controller = TilesController(self.__map_config, self.__map_node, render.loader, context)

    def create_map(self, level):
        """Создать карту"""
        self.__tiles_controller.create_map_tiles(level)

    def clear_map(self):
        """Очистить карту"""
        self.__map_node.getChildren().detach()

    def select_element(self, sprite:Sprite3D):
        """Выделить спрайт"""
        match sprite.main_node.getName():
            case 'tile':
                self.__tiles_controller.select_tile(sprite)

    def unselect_element(self, sprite:Sprite3D):
        """Отменить выделение у спрайта"""
        match sprite.main_node.getName():
            case 'tile':
                self.__tiles_controller.unselect_tile()

    def using_element(self):
        """Назначить спрайт активным"""
        self.__tiles_controller.using_tile()

    def get_selected_tile(self)->Tile:
        return self.__tiles_controller.selected_tile