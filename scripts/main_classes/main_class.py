import asyncio
from asyncio import get_event_loop, get_running_loop, sleep
from logging import debug

from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from panda3d.core import WindowProperties, CollisionTraverser

from panda3d.core import LineSegs

from scripts.main_classes.interaction.event_bus import EventBus
from scripts.main_classes.interaction.key_handler import KeyHandler
from scripts.main_classes.interaction.render_manager import RenderManager
from math import radians, sin, cos

from scripts.main_classes.interaction.selected_handler import SelectedHandler
from scripts.main_classes.interaction.task_manager import TaskManager
from scripts.main_classes.scene.scene_controller import SceneController
from scripts.main_classes.settings import Settings
from scripts.sprite.sprites_factory import SpritesFactory


class StepDefence(ShowBase):
    """Главный класс, осуществляющий взаимодействие программы с пользователем"""
    def __init__(self):
        ShowBase.__init__(self)
        self.cTrav = CollisionTraverser()

        self.__WIDTH = 1000
        self.__HEIGHT = 600
        self.__DEBUG_MODE = False

        self._set_fullscreen(True)
        # self._set_window_size(self.__WIDTH, self.__HEIGHT)

        render_manager = RenderManager(main_node3d=self.render, loader=self.loader, main_node2d=self.aspect2d, set_window_size=self._set_window_size, win=self.win)

        self.__settings = Settings(self.__DEBUG_MODE)
        self.__sprites_factory = SpritesFactory(self.__settings, render_manager, self.__WIDTH / self.__HEIGHT)

        self.__click_handler = SelectedHandler(self.cam, self.mouseWatcherNode, self.render)

        self.__taskMng = TaskManager(self.taskMgr)
        self.__scene_controller = SceneController(self.__sprites_factory)


        EventBus.publish('append_task', ['fix_camera_task', self.fixCameraTask])

        self.__key_handler = KeyHandler(self.accept)

        if self.__DEBUG_MODE:
            self.__draw_basis()

        self.loop = asyncio.get_event_loop()
        EventBus.publish('append_task', ['update_async', self.__update_async])
        EventBus.subscribe('add_async_task', lambda event_type, data: self.__add_async_task(data))

    def __add_async_task(self, task):
        self.async_task = self.loop.create_task(task)

    def __update_async(self, task):
        # Выполняем одну итерацию asyncio loop
        self.loop.call_soon(self.loop.stop)
        self.loop.run_forever()
        return task.cont

    @staticmethod
    def click():
        print('click')

    def _set_fullscreen(self, enabled: bool = True):
        """Включает/выключает полноэкранный режим"""
        props = WindowProperties()
        props.set_title('Step defence')
        props.set_fullscreen(enabled)
        self.win.request_properties(props)

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