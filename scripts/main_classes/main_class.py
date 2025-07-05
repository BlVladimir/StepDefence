from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from panda3d.core import WindowProperties

from scripts.main_classes.DTO.key_handler import KeyHandler
from scripts.sprite.rect import Rect
from scripts.sprite.sprite2D import Sprite2D
from scripts.sprite.sprite3D import Sprite3D
from scripts.main_classes.DTO.key_watcher import KeyWatcher
from scripts.main_classes.context import Context
from scripts.main_classes.DTO.render import Render
from math import radians, sin, cos



class StepDefence(ShowBase):
    """Главный класс, осуществляющий взаимодействие программы с пользователем"""
    def __init__(self):
        ShowBase.__init__(self)

        self._set_window_size(800, 600)
        self.__context = Context(Render(render=self.render, loader=self.loader, render2d=self.render2d, set_window_size=self._set_window_size, win=self.win), KeyWatcher(self.mouseWatcherNode))
        Sprite3D(Rect(-1, -1, 1, 1), 'images2d/button_image_1.png', Render(render=self.render, loader=self.loader, render2d=self.render2d, set_window_size=self._set_window_size, win=self.win))
        self.taskMgr.add(self.spinCameraTask, "SpinCameraTask")

        self.__key_handler = KeyHandler(self.accept, self.__context)

    def _set_window_size(self, width, height):
        """Меняет размеры окна"""
        props = WindowProperties()
        props.set_title('Step defence')
        props.set_size(width, height)

        self.win.request_properties(props)

    def spinCameraTask(self, task):
        angleDegrees = task.time * 100.0
        angleRadians = radians(angleDegrees)
        self.camera.setPos(20 * sin(angleRadians), -20 * cos(angleRadians), 8)
        self.camera.setHpr(angleDegrees, -15, 15)
        return Task.cont