from logging import getLogger

from scripts.main_classes.event_bus import EventBus
from scripts.main_classes.interaction.render_manager import RenderManager
from scripts.main_classes.settings import Settings
from scripts.scene.scene_classes.scenes.gameplay_scene import GameplayScene
from scripts.scene.scene_classes.scenes.main_menu_scene import MainMenuScene
from scripts.scene.scene_classes.scenes.settings_scene import SettingsScene


class SceneController:
    """Класс, обрабатывающий сцены"""
    def __init__(self, render:RenderManager, context:'IContext', settings:Settings):

        self.__gameplay_scene = GameplayScene(render, context, settings)
        self.__settings_scene = SettingsScene()
        self.__main_menu_scene = MainMenuScene()
        self.__current_scene = self.__main_menu_scene

        self.__context = context

        self.logger = getLogger(__name__)

        EventBus.subscribe('change_scene', lambda event_type, data: self.__change_scene(data))

    def __change_scene(self, name_scene):
        """Меняет сцену"""
        match name_scene:
            case 'main_menu':
                self.__current_scene = self.__main_menu_scene
                self.__gameplay_scene.close_scene()
                self.__context.task_mng.remove_task('check_tiles')
                self.__context.buttons_controller.vision_control(self.__context)
                self.logger.info(f'scene changed on {name_scene}')
            case 'settings':
                self.__current_scene = self.__settings_scene
                self.__gameplay_scene.close_scene()
                self.__context.buttons_controller.vision_control(self.__context)
                self.logger.info(f'scene changed on {name_scene}')
            case '0' | '1' | '2' | '3' | '4' | '5':
                self.__current_scene = self.__gameplay_scene
                self.__gameplay_scene.create_scene(int(name_scene))
                self.__context.task_mng.append_task('check_tiles', self.__context.key_watcher.click_handler.check_collision)
                self.__context.buttons_controller.vision_control(self.__context)
                self.logger.info(f'scene changed on {name_scene}')
            case _:
                self.logger.info('incorrect attributes')

    def get_name_current_scene(self):
        return self.__current_scene.name()