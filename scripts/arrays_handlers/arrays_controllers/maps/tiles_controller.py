from logging import error
from typing import Optional

from panda3d.core import PandaNode

from scripts.arrays_handlers.arrays_controllers.maps.creating_map.map_tiles_builder import MapTilesBuilder
from scripts.arrays_handlers.arrays_controllers.maps.tile import Tile
from scripts.arrays_handlers.arrays_controllers.towers.tower_config import TowerConfig
from scripts.arrays_handlers.objects_manager import ObjectsManager
from scripts.arrays_handlers.selector.tile_selector.tile_selector import TileSelector
from scripts.main_classes.interaction.event_bus import EventBus
from scripts.sprite.rect import Rect3D
from scripts.sprite.sprite3D import Sprite3D
from scripts.sprite.sprites_factory import SpritesFactory


class TilesController:
    """Содержит группу всех тайлов"""
    def __init__(self, maps_node:PandaNode, sprites_factory:SpritesFactory, mediator:'MediatorControllers'):
        self.__tile_manager = ObjectsManager()
        self.__map_tiles_builder = MapTilesBuilder(maps_node, sprites_factory, self.__tile_manager)
        self.__tile_selector = TileSelector()
        self.__mediator = mediator

        EventBus.subscribe('sell_tower', lambda event_type, data: self.__sell_tower())

    def create_map_tiles(self, level):
        """Создает тайлы для карты карту"""
        self.__map_tiles_builder.create_map_tiles(level)

    def reset_tiles(self):
        """Очищает карту"""
        self.__map_tiles_builder.reset_map()
        for tile in self.__tile_manager:
            tile.sprite.external_object = None

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

    def __sell_tower(self):
        try:
            tower = self.__tile_selector.used_sprite.main_node.find('tower').getPythonTag('sprite').external_object
            cost = TowerConfig.get_cost(tower.type_tower)
            for lvl in range(tower.level):
                cost += TowerConfig.get_improve_cost_array(tower.type_tower)[lvl]
            self.__mediator.remove_money(round(-cost / 2))
            EventBus.publish('not_using_tower')
            EventBus.publish('open_shop')
            tower.destroy()
        except:
            error('tower not found')

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