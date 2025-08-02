from __future__ import annotations

from logging import debug

from panda3d.core import NodePath

from scripts.main_classes.buttons.buttons_controller import ButtonsController
from scripts.main_classes.interaction.key_watcher import KeyWatcher
from scripts.main_classes.interaction.selected_handler import SelectedHandler
from scripts.main_classes.settings import Settings
from scripts.main_classes.scene.scene_controller import SceneController


class Context:
    """Через этот класс осуществляются все взаимодействия в программе"""
    def __init__(self, render_manager:RenderManager, camera, taskMng:'TaskManager', mouse_watcher_node:NodePath, render):
        self._settings = Settings()
        self._taskMng = taskMng
        self._render_manager = render_manager
        debug(self._render_manager)
        click_handler = SelectedHandler(camera, mouse_watcher_node, render, self)
        self._key_watcher = KeyWatcher(mouse_watcher_node, click_handler)
        self._scene_controller = SceneController(self)

    @property
    def scene_controller(self)->'SceneController':
        return self._scene_controller

    @property
    def render_manager(self)->RenderManager:
        return self._render_manager

    @property
    def key_watcher(self)->'KeyWatcher':
        return self._key_watcher

    @property
    def settings(self)->'Settings':
        return self._settings

    @property
    def task_mng(self)->'TaskManager':
        return self._taskMng