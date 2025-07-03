from scripts.scene.buttons.battuns_controller import ButtonsController
from scripts.scene.scene_classes.scenes.abstract_scene import Scene


class GameplayScene(Scene):
    def __init__(self):
        super().__init__()
        self.__button_controller = ButtonsController()