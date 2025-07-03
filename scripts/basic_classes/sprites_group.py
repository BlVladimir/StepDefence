from scripts.basic_classes.sprite import Sprite

class SpritesGroup:
    """Группа спрайтов"""
    def __init__(self):
        self.__sprites = []

    def add(self, sprite:Sprite):
        """Добавляет спрайт в группу"""
        self.__sprites.append(sprite)

    def update(self, *args, **kwargs):
        """Вызывает update у каждого спрайта"""
        for sprite in self.__sprites:
            sprite.update(args, kwargs)

    def remove(self, sprite:Sprite):
        """Удаляет спрайт из группы"""
        if sprite in self.__sprites:
            sprite.node.removeNode()  # Удаляем из сцены
            self.__sprites.remove(sprite)

    def clear(self):
        """Очищает группу"""
        for sprite in self.__sprites:
            sprite.node.removeNode()
        self.__sprites.clear()