from panda3d.core import NodePath

from scripts.interface.i_button_controller import IButtonsController
from scripts.interface.i_context import IContext
from scripts.interface.i_key_watcher import IKeyWatcher
from scripts.interface.i_render import IRenderManager
from scripts.interface.i_scene_controller import ISceneController
from scripts.interface.i_settings import ISettings
from scripts.interface.i_task_manager import ITaskManager
from scripts.main_classes.interaction.selected_handler import SelectedHandler
from scripts.main_classes.interaction.key_watcher import KeyWatcher
from scripts.main_classes.buttons.buttons_controller import ButtonsController
from scripts.main_classes.events.event_class import Event
from scripts.main_classes.events.event_handler import EventHandler
from scripts.main_classes.interaction.render_manager import RenderManager
from scripts.main_classes.settings import Settings
from scripts.scene.scene_controller import SceneController


class Context(IContext):
    """Через этот класс осуществляются все взаимодействия в программе"""
    def __init__(self, render_manager:RenderManager, camera, taskMng:ITaskManager, mouse_watcher_node:NodePath, render):
        self.__event_handler = EventHandler()
        self._scene_controller = SceneController(render_manager)
        self._render_manager = render_manager
        click_handler = SelectedHandler(camera, mouse_watcher_node, render, self)
        self._key_watcher = KeyWatcher(mouse_watcher_node, click_handler)
        self._settings = Settings()
        self._buttons_controller = ButtonsController(self._render_manager)
        self._taskMng = taskMng

    def send_event(self, event:Event):
        """Отправляет event на обработку"""
        if type(event) == Event:
            self.__event_handler.handle_event(event, self)

    @property
    def scene_controller(self)->ISceneController:
        return self._scene_controller

    @property
    def render_manager(self)->IRenderManager:
        return self._render_manager

    @property
    def key_watcher(self)->IKeyWatcher:
        return self._key_watcher

    @property
    def settings(self)->ISettings:
        return self._settings

    @property
    def buttons_controller(self)->IButtonsController:
        return self._buttons_controller

    @property
    def task_mng(self)->ITaskManager:
        return self._taskMng