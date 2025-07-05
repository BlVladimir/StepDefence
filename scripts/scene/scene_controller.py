from scripts.main_classes.DTO.render import Render
from scripts.main_classes.events.event_class import Event
from scripts.scene.scene_classes.scenes.gameplay_scene import GameplayScene
from scripts.scene.scene_classes.scenes.main_menu_scene import MainMenuScene
from scripts.scene.scene_classes.scenes.settings_scene import SettingsScene


class SceneController:
    """Класс, обрабатывающий сцены"""
    def __init__(self, render:Render):
        self.__gameplay_scene = GameplayScene(render)
        self.__settings_scene = SettingsScene(render)
        self.__main_menu_scene = MainMenuScene(render)
        self.__current_scene = self.__main_menu_scene

    def change_scene(self, event:Event):
        """Меняет сцену"""
        if event.name:
            match event['scene']:
                case 'main_menu':
                    self.__current_scene.hide()
                    self.__current_scene = self.__main_menu_scene
                    print(f'scene changed on {event['scene']}')
                case 'settings':
                    self.__current_scene.hide()
                    self.__current_scene = self.__settings_scene
                    print(f'scene changed on {event['scene']}')
                case 'gameplay' | '1' | '2' | '3' | '4' | '5' | '6':
                    self.__current_scene.hide()
                    self.__current_scene = self.__gameplay_scene
                    print(f'scene changed on {event['scene']}')
                case _:
                    print('incorrect attributes')
        else:
            print('incorrect event')

    def action(self, context):
        return self.__current_scene.action(context)