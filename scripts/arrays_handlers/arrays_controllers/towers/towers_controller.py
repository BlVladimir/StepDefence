from __future__ import annotations

from typing import Optional

from panda3d.core import Point3, NodePath

from scripts.arrays_handlers.arrays_controllers.enemies.enemy import Enemy
from scripts.arrays_handlers.arrays_controllers.enemies.enemy_visitor import EnemyVisitor
from scripts.arrays_handlers.arrays_controllers.towers.tower import Tower
from scripts.arrays_handlers.arrays_controllers.towers.tower_config import TowerConfig
from scripts.arrays_handlers.arrays_controllers.towers.towers_builder import TowerBuilder
from scripts.arrays_handlers.objects_manager import ObjectsManager
from scripts.main_classes.interaction.event_bus import EventBus
from scripts.sprite.sprites_factory import SpritesFactory


class TowersController:
    """Обработчик башен"""
    def __init__(self, sprites_factory:SpritesFactory, mediator: 'MediatorControllers', render_root:NodePath):
        TowerConfig.load_config(sprites_factory, render_root)
        self.__towers_manager = ObjectsManager()
        self.__tower_builder = TowerBuilder(sprites_factory, self.__towers_manager)
        self.__mediator = mediator


        EventBus.subscribe('buy_tower', lambda event_type, data: self.__create_tower(data))
        EventBus.subscribe('rotate_gun', lambda event_type, data: self.__rotate_gun(data))
        EventBus.subscribe('upgrade_tower', lambda event_type, data: self.__upgrade_tower())

    def __create_tower(self, type_tower:str):
        if self.__mediator.money >= round(self.__mediator.discount*TowerConfig.get_cost(type_tower)):
            tower = self.__tower_builder.create_tower(type_tower, self.__mediator.selected_tile)
            EventBus.publish('update_enemy')
            EventBus.publish('close_shop')
            EventBus.publish('remove_discount')
            self.__mediator.remove_money(round(self.__mediator.discount * TowerConfig.get_cost(type_tower)))
            self.__mediator.discount = 1
            EventBus.publish('using_tower', [tower, tower.level, tower.characteristic])

    def clear_towers(self):
        for tower in self.__towers_manager:
            tower.sprite.external_object = None

    def has_vision(self, enemy:Enemy)->None:
        if 'invisible' in enemy.characteristic:
            for tower in self.__towers_manager:
                if 'vision' in tower.characteristic and tower.is_target_in_radius(enemy.sprite):
                    enemy.visit(visitor=EnemyVisitor(invisible=False))
                    return
            enemy.visit(visitor=EnemyVisitor(invisible=True))

    def __upgrade_tower(self):
        tower = self.__mediator.selected_tile.tower
        if tower and tower.level < 2 and self.__mediator.money >= round(self.__mediator.discount * TowerConfig.get_improve_cost_array(tower.type_tower)[tower.level]):
            tower.upgrade()
            EventBus.publish('update_enemy')
            EventBus.publish('remove_discount')
            self.__mediator.remove_money(round(self.__mediator.discount * TowerConfig.get_improve_cost_array(tower.type_tower)[tower.level - 1]))
            self.__mediator.discount = 1
            EventBus.publish('using_tower', [tower, tower.level, tower.characteristic])

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
            tower.find_mouse(mouse_point)