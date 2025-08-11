from logging import warning
from typing import Any, Optional, List

from direct.gui.DirectButton import DirectButton
from panda3d.core import NodePath


class ButtonsGroup:
    def __init__(self, node: NodePath, *buttons:DirectButton, init_list:List[DirectButton] = None) -> None:
        """Группа кнопок"""
        self._node = node
        self.__buttons_array = []
        if buttons:
            self.__buttons_array = list(buttons)
        elif init_list:
            self.__buttons_array = init_list
        else:
            warning('no gui in group')

    def hide(self) -> None:
        self._node.hide()

    def show(self) -> None:
        self._node.show()