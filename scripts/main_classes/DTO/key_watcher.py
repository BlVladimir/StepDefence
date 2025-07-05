class KeyWatcher:
    """Передает данные о клавиатуре и мышке context"""
    def __init__(self, mouse_watcher):
        self._mouse_watcher = mouse_watcher

    @property
    def mouse_watcher(self):
        return self._mouse_watcher