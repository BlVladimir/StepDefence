from logging import getLogger

from scripts.main_classes.interaction.render import Render
from scripts.main_classes.events.event_class import Event
from scripts.scene.scene_classes.scenes.gameplay_scene import GameplayScene
from scripts.scene.scene_classes.scenes.main_menu_scene import MainMenuScene
from scripts.scene.scene_classes.scenes.settings_scene import SettingsScene


class SceneController:
    """Класс, обрабатывающий сцены"""
    def __init__(self, render:Render):
        self.__gameplay_scene = GameplayScene(render)
        self.__settings_scene = SettingsScene()
        self.__main_menu_scene = MainMenuScene()
        self.__current_scene = self.__main_menu_scene

        self.logger = getLogger(__name__)

    def change_scene(self, event:Event):
        """Меняет сцену"""
        if event.name:
            match event['scene']:
                case 'main_menu':
                    self.__current_scene = self.__main_menu_scene
                    self.__gameplay_scene.close_scene()
                    self.logger.info(f'scene changed on {event['scene']}')
                case 'settings':
                    self.__current_scene = self.__settings_scene
                    self.__gameplay_scene.close_scene()
                    self.logger.info(f'scene changed on {event['scene']}')
                case '1' | '2' | '3' | '4' | '5' | '6':
                    self.__current_scene.hide()
                    self.__current_scene = self.__gameplay_scene
                    self.__gameplay_scene.create_scene(int(event['scene'])-1)
                    self.logger.info(f'scene changed on {event['scene']}')
                case _:
                    self.logger.info('incorrect attributes')
        else:
            self.logger.error('incorrect event')

    def get_name_current_scene(self):
        return self.__current_scene.name()