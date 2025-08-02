from panda3d.core import MouseWatcher

from scripts.main_classes.interaction.selected_handler import SelectedHandler


class KeyWatcher:
    """Передает данные о клавиатуре и мышке context"""
    def __init__(self, mouse_watcher:MouseWatcher, click_handler:SelectedHandler):
        self._mouse_watcher = mouse_watcher
        self._click_handler = click_handler

    @property
    def mouse_watcher(self)->MouseWatcher:
        return self._mouse_watcher

    @property
    def click_handler(self)->SelectedHandler:
        return self._click_handler