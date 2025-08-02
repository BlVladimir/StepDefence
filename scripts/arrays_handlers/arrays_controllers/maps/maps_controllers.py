from typing import Optional

from panda3d.core import CollisionNode, CollisionPlane, Vec3, Point3, Plane, NodePath, Loader

from scripts.arrays_handlers.arrays_controllers.maps.maps_config import MapsConfig
from scripts.arrays_handlers.arrays_controllers.maps.tile import Tile
from scripts.arrays_handlers.arrays_controllers.maps.tiles_controller import TilesController
from scripts.main_classes.interaction.render_manager import RenderManager
from scripts.main_classes.settings import Settings
from scripts.sprite.rect import Rect3D
from scripts.sprite.sprite3D import Sprite3D


class MapsController:
    """Обработчик карт"""
    def __init__(self,scene_gameplay_node:NodePath, loader:Loader, settings:Settings):
        self.__map_node = scene_gameplay_node.attachNewNode("map_node")
        self.__map_config = MapsConfig()
        self.__tiles_controller = TilesController(self.__map_config, self.__map_node, loader)
        self._settings = settings

        self._global_collision_node = None

    def create_map(self, level):
        """Создать карту"""
        self.__tiles_controller.create_map_tiles(level, self._settings)

        global_collision = CollisionNode('global_collision')
        global_collision.addSolid(CollisionPlane(Plane(Vec3(0.0, 0.0, 1), Point3(0.0, 0.0, 0.0))))

        self._global_collision_node = self.__map_node.attachNewNode(global_collision)

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

    def get_selected_tile(self)->Optional[Tile]:
        return self.__tiles_controller.selected_tile

    @property
    def first_tile_rect(self)->Rect3D:
        return self.__tiles_controller.first_tile_rect

    @property
    def track(self):
        return self.__tiles_controller.track