from typing import List

from direct.interval.LerpInterval import LerpPosInterval
from direct.interval.MetaInterval import Sequence
from panda3d.core import NodePath, Loader, Vec4, Vec3, Vec2

from scripts.sprite.rect import Rect3D
from scripts.sprite.sprite3D import Sprite3D


class EnemySprite(Sprite3D):
    def __init__(self, rect: Rect3D, path_image: str, parent: NodePath, name_group:str, loader: Loader, number: int, external_object: 'Enemy' = None, debug_mode: bool = True):
        super().__init__(rect, path_image, parent, loader, name_group, number, external_object, debug_mode)

        self.__select_frame = self.__wireframe(Vec4(0.5, 0, 0, 0.8))
        self.__select_frame.hide()
        self.__is_selected = False

        self.__special_select_frame = self.__wireframe(Vec4(0.8, 0.8, 1, 1))
        self.__special_select_frame.hide()
        self.__is_special_selected = False

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

    def move(self, movement_array: List[Vec3]) -> None:
        intervals = []
        for i in range(1, len(movement_array)):
            intervals.append(
                LerpPosInterval(
                    self._main_node,
                    duration=0.06,
                    pos=movement_array[i],
                    startPos=movement_array[i - 1]
                )
            )
        sequence = Sequence(*intervals)
        sequence.start()
        vec_move = movement_array[-1] - movement_array[0]
        self._rect.move(Vec2(vec_move.x, vec_move.y))

    @property
    def is_selected(self):
        return self.__is_selected

    @is_selected.setter
    def is_selected(self, value: bool):
        self.__is_selected = value and not self.__is_using
        self.is_special_selected = False
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
        self.is_special_selected = False
        if value:
            self.__use_frame.show()
        else:
            self.__use_frame.hide()

    @property
    def is_special_selected(self):
        return self.__is_special_selected

    @is_special_selected.setter
    def is_special_selected(self, value: bool):
        self.__is_special_selected = value and not self.__is_using
        if value:
            self.__special_select_frame.show()
        else:
            self.__special_select_frame.hide()