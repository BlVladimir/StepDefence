from logging import getLogger, info

from scripts.main_classes.interaction.event_bus import EventBus
from scripts.main_classes.scene.gameplay_scene import GameplayScene
from scripts.main_classes.scene.main_menu_scene import MainMenuScene
from scripts.main_classes.scene.scene import Scene
from scripts.sprite.sprites_factory import SpritesFactory


class SceneController:
    """Класс, обрабатывающий сцены"""
    def __init__(self, sprites_factory:SpritesFactory):

        self.__gameplay_scene = GameplayScene(sprites_factory)
        self.__settings_scene = Scene(sprites_factory, 'settings')
        self.__main_menu_scene = MainMenuScene(sprites_factory)
        self.__current_scene = self.__main_menu_scene

        EventBus.subscribe('change_scene', lambda event_type, data: self.__change_scene(data))

    def __change_scene(self, name_scene):
        """Меняет сцену"""
        match name_scene:
            case 'main_menu':
                self.__current_scene.hide()
                self.__current_scene = self.__main_menu_scene
                self.__current_scene.show()
                EventBus.publish('turn_off_gameplay_task')
                info(f'scene changed on {name_scene}')
            case 'settings':
                self.__current_scene.hide()
                self.__current_scene = self.__settings_scene
                self.__current_scene.show()
                EventBus.publish('turn_off_gameplay_task')
                info(f'scene changed on {name_scene}')
            case '0' | '1' | '2' | '3' | '4' | '5':
                self.__current_scene.hide()
                self.__current_scene = self.__gameplay_scene
                self.__current_scene.level = int(name_scene)
                self.__current_scene.show()
                EventBus.publish('turn_on_gameplay_task')
                info(f'scene changed on {name_scene}')
            case _:
                info('incorrect attributes')