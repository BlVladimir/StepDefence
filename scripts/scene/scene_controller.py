from scripts.main_classes.events.event_class import Event
from scripts.scene.scene_classes.scenes.gameplay_scene import GameplayScene
from scripts.scene.scene_classes.scenes.main_menu_scene import MainMenuScene
from scripts.scene.scene_classes.scenes.settings_scene import SettingsScene


class SceneController:
    """Класс, обрабатывающий сцены"""
    def __init__(self):
        self.__gameplay_scene = GameplayScene()
        self.__settings_scene = SettingsScene()
        self.__main_menu_scene = MainMenuScene()
        self.__current_scene = self.__main_menu_scene

    def change_scene(self, event:Event):
        """Меняет сцену"""
        if event == 'change_scene':
            match event['scene']:
                case 'main_menu':
                    self.__current_scene.hide()
                    self.__current_scene = self.__main_menu_scene
                case 'settings':
                    self.__current_scene.hide()
                    self.__current_scene = self.__settings_scene
                case 'gameplay':
                    self.__current_scene.hide()
                    self.__current_scene = self.__gameplay_scene
                case _:
                    print('incorrect attributes')
        else:
            print('incorrect event')