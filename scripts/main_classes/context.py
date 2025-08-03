from __future__ import annotations

from logging import debug

from panda3d.core import NodePath

from scripts.main_classes.interaction.selected_handler import SelectedHandler
from scripts.main_classes.settings import Settings
from scripts.main_classes.scene.scene_controller import SceneController


class Context:
    """Через этот класс осуществляются все взаимодействия в программе"""
    def __init__(self, render_manager:RenderManager, camera, taskMng:'TaskManager', mouse_watcher_node:NodePath, render):
        self._settings = Settings()
        self._render_manager = render_manager
        debug(self._render_manager)
        self._click_handler = SelectedHandler(camera, mouse_watcher_node, render, self)

        self.__taskMng = taskMng
        self.__scene_controller = SceneController(self)

    @property
    def render_manager(self)->RenderManager:
        return self._render_manager

    @property
    def click_handler(self)->'SelectedHandler':
        return self._click_handler

    @property
    def settings(self)->'Settings':
        return self._settings