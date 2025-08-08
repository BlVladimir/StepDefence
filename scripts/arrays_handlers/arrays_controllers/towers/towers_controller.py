from __future__ import annotations

from typing import Optional

from panda3d.core import Point3

from scripts.arrays_handlers.arrays_controllers.towers.tower import Tower
from scripts.arrays_handlers.arrays_controllers.towers.towers_builder import TowerBuilder
from scripts.arrays_handlers.arrays_controllers.towers.towers_config import TowersConfig
from scripts.main_classes.interaction.event_bus import EventBus
from scripts.sprite.sprites_factory import SpritesFactory


class TowersController:
    """Обработчик башен"""
    def __init__(self, sprites_factory:SpritesFactory, mediator: 'MediatorControllers'):
        self.__config = TowersConfig()
        self.__tower_builder = TowerBuilder(sprites_factory, self.__config)
        self.__mediator = mediator

        EventBus.subscribe('buy_tower', lambda event_type, data: self.__create_tower(data))
        EventBus.subscribe('rotate_gun', lambda event_type, data: self.__rotate_gun(data))
        EventBus.subscribe('upgrade_tower', lambda event_type, data: self.__upgrade_tower())

    def __create_tower(self, type_tower:str):
        if self.__mediator.money >= round(self.__mediator.discount*self.__config.get_cost(type_tower)):
            self.__tower_builder.create_tower(type_tower, self.__mediator.selected_tile)
            EventBus.publish('close_shop')
            self.__mediator.remove_money(round(self.__mediator.discount*self.__config.get_cost(type_tower)))
            self.__mediator.discount = 1

    def clear_towers(self):
        self.__tower_builder.reset_counter()

    def __upgrade_tower(self):
        tower = self.__mediator.selected_tile.tower
        if tower and tower.level < 2 and self.__mediator.money >= round(self.__mediator.discount*self.__config.get_improve_cost_array(tower.type_tower)[tower.level]):
            tower.upgrade()
            self.__mediator.remove_money(round(self.__mediator.discount*self.__config.get_improve_cost_array(tower.type_tower)[tower.level-1]))
            self.__mediator.discount = 1
            EventBus.publish('open_upgrade_table', [tower.level, tower.characteristic])

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