from __future__ import annotations

from typing import Optional

from panda3d.core import Loader, Point3

from scripts.arrays_handlers.arrays_controllers.towers.tower import Tower
from scripts.arrays_handlers.arrays_controllers.towers.towers_builder import TowerBuilder
from scripts.main_classes.event_bus import EventBus


class TowersController:
    """Обработчик башен"""
    def __init__(self, loader:Loader, settings:'Settings', mediator:'MediatorControllers', context:'IContext'):
        self.__tower_builder = TowerBuilder(loader)
        self._settings = settings
        self.__mediator = mediator
        self.__context = context

        EventBus.subscribe('buy_tower', lambda event_type, data: self.__create_tower(data))
        EventBus.subscribe('rotate_gun', lambda event_type, data: self.__rotate_gun(data))

    def __create_tower(self, type_tower:str):
        self.__tower_builder.create_tower(type_tower, self.__mediator.selected_tile, self._settings)
        self.__context.buttons_controller.close_shop()

    def clear_towers(self):
        self.__tower_builder.reset_counter()

    def __get_selected_tower(self)->Optional[Tower]:
        tile = self.__mediator.selected_tile
        if tile:
            tower_node = tile.sprite.main_node.find('tower')
            if tower_node:
                return tower_node.getPythonTag('sprite').external_object
        return None

    def __rotate_gun(self, mouse_point:Point3)->None:
        tower = self.__get_selected_tower()
        if tower:
            tower.rotate(mouse_point)