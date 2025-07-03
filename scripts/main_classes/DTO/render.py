class Render:
    """Передает данные для отрисовки context"""
    def __init__(self, render, loader, render2d):
        self.__render = render
        self.__loader = loader
        self.__render2d = render2d

    @property
    def render(self):
        return self.__render

    @property
    def loader(self):
        return self.__loader

    @property
    def render2d(self):
        return self.__render2d