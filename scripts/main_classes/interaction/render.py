from scripts.sprite.convert_coordinate import ConvertCoordinate


class Render:
    """Передает данные для отрисовки context"""
    def __init__(self, main_node3d, loader, main_node2d, set_window_size, win):
        self._main_node3d = main_node3d
        self._loader = loader
        self._main_node2d = main_node2d
        self._win = win
        self._set_window_size = set_window_size
        self._convert_coordinate = ConvertCoordinate(self)

    @property
    def main_node3d(self):
        return self._main_node3d

    @property
    def loader(self):
        return self._loader

    @property
    def main_node2d(self):
        return self._main_node2d

    @property
    def win(self):
        return self._win

    @property
    def convert_coordinate(self):
        return self._convert_coordinate

    def set_window_size(self, width, height):
        """Меняет размер окна"""
        self._set_window_size(width, height)