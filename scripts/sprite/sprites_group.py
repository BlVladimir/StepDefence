from scripts.sprite.sprite3D import Sprite3D

class SpritesGroup:
    """Группа спрайтов"""
    def __init__(self):
        self.__sprites = []

    def add(self, sprite:Sprite3D):
        """Добавляет спрайт в группу"""
        self.__sprites.append(sprite)

    def update(self, *args, **kwargs):
        """Вызывает update у каждого спрайта"""
        for sprite in self.__sprites:
            sprite.update(args, kwargs)

    def remove(self, sprite:Sprite3D):
        """Удаляет спрайт из группы"""
        if sprite in self.__sprites:
            sprite.main_node.removeNode()  # Удаляем из сцены
            self.__sprites.remove(sprite)

    def clear(self):
        """Очищает группу"""
        for sprite in self.__sprites:
            sprite.main_node.removeNode()
        self.__sprites.clear()

    def sprites(self):
        return self.__sprites