from abc import ABC, abstractmethod

from scripts.main_classes.DTO.render import Render
from scripts.scene.buttons.buttons_controller import ButtonsController, NullButtonsController


class Scene(ABC):
    """Абстрактная сцена"""
    @abstractmethod
    def __init__(self, render:Render):
        self.__button_controller = NullButtonsController(render)


    def hide(self):
        """Скрывает сцену"""
        print('scene was hide')
        pass

    def action(self, context):
        return self.__button_controller.action(context)