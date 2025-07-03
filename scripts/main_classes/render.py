class Render:
    """Инкапсулирует отрисовку от context"""
    def __init__(self, render, loader):
        self.__render = render
        self.__loader = loader

    @property
    def render(self):
        return self.__render

    @property
    def loader(self):
        return self.__loader