from abc import ABC

from scripts.sprite.sprite3D import Sprite3D


class ExtObjOfSprite(ABC):
    _sprite:Sprite3D
    _type:str

    @property
    def sprite(self)->Sprite3D:
        return self._sprite

    @property
    def type_onj(self)->str:
        return self._type