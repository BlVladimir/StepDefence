from panda3d.core import MouseWatcher

from scripts.main_classes.interaction.click_handler import ClickHandler
from scripts.interface.i_key_watcher import IKeyWatcher


class KeyWatcher(IKeyWatcher):
    """Передает данные о клавиатуре и мышке context"""
    def __init__(self, mouse_watcher:MouseWatcher, click_handler:ClickHandler):
        self._mouse_watcher = mouse_watcher
        self._click_handler = click_handler

    @property
    def mouse_watcher(self):
        return self._mouse_watcher

    @property
    def click_handler(self):
        return self._click_handler