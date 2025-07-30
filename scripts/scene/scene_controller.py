from logging import getLogger, warning

from scripts.arrays_handlers.arrays_controllers.maps.tile import Tile
from scripts.interface.i_context import IContext
from scripts.main_classes.interaction.render_manager import RenderManager
from scripts.main_classes.events.event_class import Event
from scripts.scene.scene_classes.scenes.gameplay_scene import GameplayScene
from scripts.scene.scene_classes.scenes.main_menu_scene import MainMenuScene
from scripts.scene.scene_classes.scenes.settings_scene import SettingsScene
from scripts.interface.i_scene_controller import ISceneController
from scripts.sprite.sprite3D import Sprite3D


class SceneController(ISceneController):
    """Класс, обрабатывающий сцены"""
    def __init__(self, render:RenderManager, context:IContext):
        self.__gameplay_scene = GameplayScene(render, context)
        self.__settings_scene = SettingsScene()
        self.__main_menu_scene = MainMenuScene()
        self.__current_scene = self.__main_menu_scene

        self.logger = getLogger(__name__)

    def change_scene(self, event:Event, context:IContext):
        """Меняет сцену"""
        if event.name:
            match event['scene']:
                case 'main_menu':
                    self.__current_scene = self.__main_menu_scene
                    self.__gameplay_scene.close_scene()
                    self.logger.info(f'scene changed on {event['scene']}')
                    context.task_mng.remove_task('check_tiles')
                case 'settings':
                    self.__current_scene = self.__settings_scene
                    self.__gameplay_scene.close_scene()
                    self.logger.info(f'scene changed on {event['scene']}')
                case '0' | '1' | '2' | '3' | '4' | '5':
                    self.__current_scene.hide()
                    self.__current_scene = self.__gameplay_scene
                    self.__gameplay_scene.create_scene(int(event['scene']))
                    context.task_mng.append_task('check_tiles', context.key_watcher.click_handler.check_tiles)
                    self.logger.info(f'scene changed on {event['scene']}')
                case _:
                    self.logger.info('incorrect attributes')
        else:
            self.logger.error('incorrect event')

    def get_name_current_scene(self):
        return self.__current_scene.name()

    def send_sprite_to_selected(self, sprite:Sprite3D):
        if self.__current_scene == self.__gameplay_scene:
            self.__gameplay_scene.gameplay_handler.mediator_controllers.select_element(sprite)

    def send_sprite_to_unselected(self, sprite:Sprite3D):
        if self.__current_scene == self.__gameplay_scene:
            self.__gameplay_scene.gameplay_handler.mediator_controllers.unselect_element(sprite)

    def send_using_selected_element(self):
        if self.__current_scene == self.__gameplay_scene:
            self.__gameplay_scene.gameplay_handler.mediator_controllers.using_element()

    def create_tower_on_current_tile(self, tower_type:str):
        if self.__current_scene == self.__gameplay_scene:
            self.__gameplay_scene.gameplay_handler.mediator_controllers.create_tower(tower_type)

    def next_round(self):
        if self.__current_scene == self.__gameplay_scene:
            self.__gameplay_scene.gameplay_handler.mediator_controllers.next_round()