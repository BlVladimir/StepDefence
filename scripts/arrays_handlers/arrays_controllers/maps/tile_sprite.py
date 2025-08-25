from panda3d.core import NodePath, Loader, Vec4, Texture

from scripts.sprite.rect import Rect3D
from scripts.sprite.sprite3D import Sprite3D


class TileSprite(Sprite3D):
    def __init__(self, rect: Rect3D, texture: Texture, parent: NodePath, name_group: str, number: int, external_object=None, debug_mode: bool = True):
        super().__init__(rect, texture, parent, name_group, number, external_object, debug_mode)

        self.__select_frame = self.__wireframe(Vec4(0.5, 0, 0, 0.8))
        self.__select_frame.hide()
        self.__is_selected = False

        self.__use_frame = self.__wireframe()
        self.__use_frame.hide()
        self.__is_using = False

    def __wireframe(self, color: Vec4 = Vec4(1, 0, 0, 1)) -> NodePath:
        """Добавляет проволочную обводку вокруг объекта"""
        wireframe = self._texture_node.copyTo(self._main_node)

        wireframe.clearTexture()
        wireframe.setRenderModeWireframe()
        wireframe.setColor(color)
        wireframe.setLightOff()

        wireframe.setBin("fixed", 50)
        wireframe.setDepthTest(False)
        wireframe.setDepthWrite(False)

        return wireframe

    @property
    def is_selected(self):
        return self.__is_selected

    @is_selected.setter
    def is_selected(self, value: bool):
        self.__is_selected = value and not self.__is_using
        if value:
            self.__select_frame.show()
        else:
            self.__select_frame.hide()

    @property
    def is_using(self):
        return self.__is_using

    @is_using.setter
    def is_using(self, value: bool):
        self.__is_using = value
        self.is_selected = False
        if value:
            self.__use_frame.show()
        else:
            self.__use_frame.hide()