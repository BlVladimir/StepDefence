from scripts.sprite.sprite3D import Sprite3D


class Tile:
    """Класс одного тайла"""
    def __init__(self, sprite:Sprite3D, effect:str):
        self._sprite = sprite
        self._effect = effect

    @property
    def effect(self):
        return self._effect

    @property
    def sprite(self):
        return self._sprite


