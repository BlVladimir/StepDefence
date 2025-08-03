from panda3d.core import NodePath

class ButtonsController:
    """Класс всех кнопок на сцене"""
    def __init__(self, relationship:float, buttons_node:NodePath):
        self._buttons_node = buttons_node

        self._relationship = relationship