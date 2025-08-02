from scripts.main_classes.buttons.buttons_controller import ButtonsController
from scripts.main_classes.interaction.render_manager import RenderManager


class Scene:
    """Стандартная сцена"""
    def __init__(self, render_manager:RenderManager, name:str):
        self._scene_node = render_manager.main_node3d.attachNewNode(name)
        self._name = name

        self._buttons_node = render_manager.main_node2d.attachNewNode(name)
        self.__buttons_controller = ButtonsController(render_manager.win, self._buttons_node)

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