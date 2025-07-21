from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from panda3d.core import WindowProperties

from panda3d.core import LineSegs, NodePath

from scripts.main_classes.DTO.key_handler import KeyHandler
from scripts.sprite.convert_coordinate import ConvertCoordinate
from scripts.sprite.rect import Rect2D, Rect3D
from scripts.main_classes.DTO.key_watcher import KeyWatcher
from scripts.main_classes.context import Context
from scripts.main_classes.DTO.render import Render
from math import radians, sin, cos



class StepDefence(ShowBase):
    """Главный класс, осуществляющий взаимодействие программы с пользователем"""
    def __init__(self):
        ShowBase.__init__(self)

        self._set_window_size(800, 600)
        render = Render(main_node3d=self.render, loader=self.loader, main_node2d=self.render2d, set_window_size=self._set_window_size, win=self.win)
        self.__context = Context(render, KeyWatcher(self.mouseWatcherNode))
        self.taskMgr.add(self.spinCameraTask, "SpinCameraTask")

        self.__key_handler = KeyHandler(self.accept, self.__context)

        self.__draw_basis()

    def _set_window_size(self, width, height):
        """Меняет размеры окна"""
        props = WindowProperties()
        props.set_title('Step defence')
        props.set_size(width, height)

        self.win.request_properties(props)

    def spinCameraTask(self, task):

        angleDegrees = task.time * 50.0
        angleRadians = radians(angleDegrees)
        self.camera.setPos(17 * sin(angleRadians), -17 * cos(angleRadians), 10)
        self.camera.setHpr(angleDegrees, -25, 0)
        """angleDegrees = 7
        angleRadians = radians(angleDegrees)
        self.camera.setPos(17 * sin(angleRadians), -17 * cos(angleRadians), 10)
        self.camera.setHpr(angleDegrees, -25, 0)"""
        return Task.cont

    def fixCameraTask(self, task):
        angleDegrees = 7
        angleRadians = radians(angleDegrees)
        self.camera.setPos(17 * sin(angleRadians), -17 * cos(angleRadians), 10)
        self.camera.setHpr(angleDegrees, -25, 0)
        return Task.cont

    def __draw_basis(self):
        """Рисует базис"""
        lines = LineSegs()
        lines.set_thickness(2)

        lines.set_color(1, 0, 0, 1)  # x - красный
        lines.move_to(0, 0, 0)
        lines.draw_to(1, 0, 0)

        lines.set_color(0, 1, 0, 1)  # y - зеленый
        lines.move_to(0, 0, 0)
        lines.draw_to(0, 1, 0)

        lines.set_color(0, 0, 1, 1)  # z - синий
        lines.move_to(0, 0, 0)
        lines.draw_to(0, 0, 1)

        self.render.attach_new_node(lines.create())