import asyncio
from asyncio import get_event_loop, get_running_loop, sleep
from logging import debug, error, info

from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from panda3d.core import WindowProperties, CollisionTraverser

from panda3d.core import LineSegs, TextNode

from scripts.arrays_handlers.arrays_controllers.enemies.enemies_config import EnemiesConfig
from scripts.arrays_handlers.arrays_controllers.maps.maps_config import MapsConfig
from scripts.main_classes.gui.info.info_config import InfoConfig
from scripts.main_classes.interaction.event_bus import EventBus
from scripts.main_classes.interaction.key_handler import KeyHandler
from scripts.main_classes.interaction.render_manager import RenderManager
from math import radians, sin, cos

from scripts.main_classes.interaction.selected_handler import SelectedHandler
from scripts.main_classes.interaction.task_manager import TaskManager
from scripts.main_classes.save_mng import SaveMng
from scripts.main_classes.scene.scene_controller import SceneController
from scripts.main_classes.settings import Settings
from scripts.sprite.sprites_factory import SpritesFactory


class StepDefence(ShowBase):
    """Главный класс, осуществляющий взаимодействие программы с пользователем"""
    def __init__(self):
        ShowBase.__init__(self)
        InfoConfig.load_config()
        MapsConfig.load_config()
        EnemiesConfig.load_config()
        SaveMng.load()

        self.__setup_fonts()
        self.cTrav = CollisionTraverser()

        self.__WIDTH = 1000
        self.__HEIGHT = 600
        self.__DEBUG_MODE = False

        self.setBackgroundColor(0, 0, 0, 1)


        # self._set_fullscreen(True)
        self._set_window_size(self.__WIDTH, self.__HEIGHT)

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

        self.__loop = asyncio.get_event_loop()
        EventBus.publish('append_task', ['update_async', self.__update_async])
        EventBus.subscribe('add_async_task', lambda event_type, data: self.__add_async_task(data))

    def __add_async_task(self, task):
        self.async_task = self.__loop.create_task(task)

    def __update_async(self, task):
        # Выполняем одну итерацию asyncio loop
        self.__loop.call_soon(self.__loop.stop)
        self.__loop.run_forever()
        return task.cont

    def __setup_fonts(self):
        """Настройка шрифта по умолчанию с поддержкой кириллицы."""
        font = None
        candidates = [
            'configs/ShareTechMono.otf',  # Пользовательский шрифт
            '/System/Library/Fonts/Supplemental/Arial Unicode.ttf',  # macOS
            '/Library/Fonts/Arial Unicode.ttf',  # macOS
            '/Library/Fonts/Arial.ttf',  # macOS
        ]

        for path in candidates:
            try:
                f = self.loader.loadFont(path)
                if f:
                    font = f
                    info(f'Successfully loaded font: {path}')
                    break
            except Exception:
                continue

        if font:
            TextNode.setDefaultFont(font)
        else:
            error('Warning: Unicode font not found')

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
        self.camera.setPos(0, 0, 16)
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