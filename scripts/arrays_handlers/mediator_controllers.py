from __future__ import annotations

from typing import Optional

from panda3d.core import NodePath, Loader

from scripts.arrays_handlers.arrays_controllers.enemies.enemies_controller import EnemiesController
from scripts.arrays_handlers.arrays_controllers.maps.maps_controllers import MapsController
from scripts.arrays_handlers.arrays_controllers.maps.tile import Tile
from scripts.arrays_handlers.arrays_controllers.towers.towers_controller import TowersController
from scripts.main_classes.interaction.event_bus import EventBus
from scripts.sprite.sprite3D import Sprite3D
from scripts.sprite.sprites_factory import SpritesFactory


class MediatorControllers:
    """Посредник между контроллерами основных классов"""
    def __init__(self, scene_gameplay_node:NodePath, sprites_factory:SpritesFactory):
        self.__towers_controller = TowersController(sprites_factory, self)
        self.__maps_controller = MapsController(scene_gameplay_node, sprites_factory)
        self.__enemies_controller = EnemiesController(scene_gameplay_node, sprites_factory, self.__maps_controller.track)

        self._current_wave = 0

        EventBus.subscribe('using_element', lambda event_type, data: self.__using_element())
        EventBus.subscribe('unselect_element', lambda event_type, data: self.__unselect_element(data))
        EventBus.subscribe('select_element', lambda event_type, data: self.__select_element(data))



    def create_scene(self, level):
        """Создание карты"""
        self.__maps_controller.create_map(level)
        self._current_wave = 0
        self.create_enemy(level, 0)

    def create_enemy(self, level:int, wave:int):
        self.__enemies_controller.create_enemies(wave, level, self.__maps_controller.first_tile_rect)

    def remove_scene(self):
        """Очистка карты"""
        self.__maps_controller.clear_map()
        self.__enemies_controller.clear_enemies()
        self.__towers_controller.clear_towers()
        self._current_wave = 0

    def __select_element(self, sprite:Sprite3D):
        """Выделить элемент"""
        match sprite.main_node.getName():
            case 'tile':
                self.__maps_controller.select_element(sprite)
            case 'enemy':
                self.__enemies_controller.handle_enemy_action('select', sprite)

    def __unselect_element(self, sprite:Sprite3D):
        """Снять выделение"""
        match sprite.main_node.getName():
            case 'tile':
                self.__maps_controller.unselect_element(sprite)
            case 'enemy':
                self.__enemies_controller.handle_enemy_action('unselect')

    def __using_element(self):
        """Назначить тайл активным"""
        self.__maps_controller.using_element()
        self.__enemies_controller.handle_enemy_action('using')

    @property
    def selected_tile(self)->Optional[Tile]:
        return self.__maps_controller.get_selected_tile()