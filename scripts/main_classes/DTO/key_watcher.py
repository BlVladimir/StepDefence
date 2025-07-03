class KeyWatcher:
    """Передает данные о клавиатуре и мышке context"""
    def __init__(self, mouse_watcher):
        self.__mouse_watcher = mouse_watcher

    @property
    def mouse_watcher(self):
        return self.__mouse_watcher