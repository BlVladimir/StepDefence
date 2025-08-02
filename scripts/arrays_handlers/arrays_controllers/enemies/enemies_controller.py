from __future__ import annotations

from scripts.arrays_handlers.arrays_controllers.enemies.movement.group_enemies_builder import GroupEnemiesBuilder
from scripts.arrays_handlers.arrays_controllers.maps.creating_map.track import Track
from scripts.arrays_handlers.parts_handler.using_element_controller import UsingElementController
from scripts.main_classes.event_bus import EventBus
from scripts.main_classes.interaction.render_manager import RenderManager
from scripts.main_classes.settings import Settings
from scripts.sprite.rect import Rect3D
from scripts.sprite.sprite3D import Sprite3D


class EnemiesController:
    """Обработчик врагов"""
    def __init__(self, render:RenderManager, track:Track, settings:Settings):
        self._enemies_node = render.main_node3d.attachNewNode('enemy')
        self.__group_enemies_builder = GroupEnemiesBuilder(self._enemies_node, render, track)

        self._settings = settings

        self.__enemies_selector = UsingElementController()

        EventBus.subscribe('next_round', lambda event_type, data: self.__move_enemies())


    def clear_enemies(self)->None:
        """Удаоляет врагов"""
        self.__group_enemies_builder.clear_enemies()

    def create_enemies(self, wave:int, level:int, tile:Rect3D)->None:
        """Создает врагов"""
        self.__group_enemies_builder.create_enemies(wave, level, tile, self._settings)

    def __move_enemies(self)->None:
        enemies = self._enemies_node.getChildren()

        for i in range(len(enemies)):
            enemies[i].getPythonTag('sprite').external_object.move()

    def handle_enemy_action(self, action: str, enemy:Sprite3D = None) -> None:
        """Обрабатывает действия с врагами"""
        match action:
            case 'select':
                self.__enemies_selector.select_sprite(enemy)
            case 'unselect':
                self.__enemies_selector.unselect_sprite()
            case 'using':
                self.__enemies_selector.using_sprite()