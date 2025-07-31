from scripts.sprite.sprite3D import Sprite3D


class Tile:
    """Класс одного тайла"""
    def __init__(self, sprite:Sprite3D, effect:str):
        self._sprite = sprite
        self._effect = effect

        self._sprite.external_object = self

    @property
    def effect(self)->str:
        return self._effect

    @property
    def sprite(self)->Sprite3D:
        return self._sprite


