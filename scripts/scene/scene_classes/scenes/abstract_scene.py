from abc import ABC, abstractmethod
from scripts.scene.buttons.buttons_controller import ButtonsController


class Scene(ABC):
    """Абстрактная сцена"""
    @abstractmethod
    def __init__(self):
        self.__button_controller = ButtonsController()


    def hide(self):
        """Скрывает сцену"""
        print('scene was hid')
        pass