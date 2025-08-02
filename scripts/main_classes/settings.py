
class Settings:
    """Содержит поля для глобальных настроек игры"""
    def __init__(self):
        self._debug_mode = True

    @property
    def debug_mode(self)->bool:
        return self._debug_mode

    @debug_mode.setter
    def debug_mode(self, value:bool):
        self._debug_mode = value