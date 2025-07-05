class Render:
    """Передает данные для отрисовки context"""
    def __init__(self, render, loader, render2d, set_window_size, win):
        self._render = render
        self._loader = loader
        self._render2d = render2d
        self._win = win
        self._set_window_size = set_window_size

    @property
    def render(self):
        return self._render

    @property
    def loader(self):
        return self._loader

    @property
    def render2d(self):
        return self._render2d

    @property
    def win(self):
        return self._win

    def set_window_size(self, width, height):
        """Меняет размер окна"""
        self._set_window_size(width, height)