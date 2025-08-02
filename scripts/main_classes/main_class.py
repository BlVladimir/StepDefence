from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from panda3d.core import WindowProperties, CollisionTraverser

from panda3d.core import LineSegs

from scripts.main_classes.interaction.key_handler import KeyHandler
from scripts.main_classes.context import Context
from scripts.main_classes.interaction.render_manager import RenderManager
from math import radians, sin, cos
from scripts.main_classes.interaction.task_manager import TaskManager


class StepDefence(ShowBase):
    """Главный класс, осуществляющий взаимодействие программы с пользователем"""
    def __init__(self):
        ShowBase.__init__(self)
        self.cTrav = CollisionTraverser()

        # self.cTrav.showCollisions(self.render)

        self._set_window_size(800, 600)
        render_manager = RenderManager(main_node3d=self.render, loader=self.loader, main_node2d=self.aspect2d, set_window_size=self._set_window_size, win=self.win)

        self.__context = Context(render_manager, self.cam, TaskManager(self.taskMgr), self.mouseWatcherNode, self.render)

        self.__context.task_mng.append_task("SpinCameraTask", self.fixCameraTask)

        self.__key_handler = KeyHandler(self.accept)

        self.__draw_basis()


    @staticmethod
    def click():
        print('click')

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
        return Task.cont

    def fixCameraTask(self, task):
        self.camera.setPos(0, 0, 13)
        self.camera.setHpr(0, -90, 0)
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