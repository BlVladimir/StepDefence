from scripts.main_classes.buttons.buttons_controller import ButtonsController
from scripts.sprite.sprites_factory import SpritesFactory


class Scene:
    """Стандартная сцена"""
    def __init__(self, sprites_factory:SpritesFactory, name:str):
        self._scene_node = sprites_factory.create3Dnode(name)
        self._name = name

        self._buttons_node = sprites_factory.create2Dnode(name + '_buttons')
        self.__buttons_controller = ButtonsController(sprites_factory.relationship, self._buttons_node)

    def hide(self)->None:
        """Скрывает сцену"""
        self._scene_node.hide()
        self._buttons_node.hide()

    def show(self)->None:
        """Показывает сцену"""
        self._scene_node.show()
        self._buttons_node.show()

    @property
    def name(self)->str:
        return self._name