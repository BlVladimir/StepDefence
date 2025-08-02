from logging import getLogger

from scripts.main_classes.interaction.event_bus import EventBus
from scripts.main_classes.scene.gameplay_scene import GameplayScene
from scripts.main_classes.scene.main_menu_scene import MainMenuScene
from scripts.main_classes.scene.scene import Scene

class SceneController:
    """Класс, обрабатывающий сцены"""
    def __init__(self, context:'Context'):

        self.__gameplay_scene = GameplayScene(context.render_manager, context)
        self.__settings_scene = Scene(context.render_manager, 'settings')
        self.__main_menu_scene = MainMenuScene(context.render_manager)
        self.__current_scene = self.__main_menu_scene

        self.__context = context

        self.logger = getLogger(__name__)

        EventBus.subscribe('change_scene', lambda event_type, data: self.__change_scene(data))

    def __change_scene(self, name_scene):
        """Меняет сцену"""
        match name_scene:
            case 'main_menu':
                self.__current_scene.hide()
                self.__current_scene = self.__main_menu_scene
                self.__current_scene.show()
                self.__context.task_mng.remove_task('check_tiles')
                self.logger.info(f'scene changed on {name_scene}')
            case 'settings':
                self.__current_scene.hide()
                self.__current_scene = self.__settings_scene
                self.__current_scene.show()
                self.__context.task_mng.remove_task('check_tiles')
                self.logger.info(f'scene changed on {name_scene}')
            case '0' | '1' | '2' | '3' | '4' | '5':
                self.__current_scene.hide()
                self.__current_scene = self.__gameplay_scene
                self.__current_scene.level = int(name_scene)
                self.__current_scene.show()
                self.__context.task_mng.append_task('check_tiles', self.__context.key_watcher.click_handler.check_collision)
                self.logger.info(f'scene changed on {name_scene}')
            case _:
                self.logger.info('incorrect attributes')

    def get_name_current_scene(self):
        return self.__current_scene.name