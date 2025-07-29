from scripts.sprite.sprite3D import Sprite3D


class GunState:
    """Состояние, влияющее на пушку башни"""
    def __init__(self, sprite:Sprite3D):
        self.__sprite = sprite

    def rotate_gun(self):  # поворачивает ствол в сторону мышки
        pass

    @property
    def gun_sprite(self):
        return self.__sprite