from random import random
from typing import List
from logging import error
from panda3d.core import Vec2, Mat3

from scripts.arrays_handlers.arrays_controllers.maps.tile import Tile


class Track:
    def __init__(self):
        self._track = []
        self._first_tile = None

    @property
    def track(self)->List[Vec2]:
        return self._track

    @track.setter
    def track(self, value:List[int]):
        rect = self._first_tile.sprite.rect
        pos = Vec2(rect.x, rect.y)
        scale = 1.2*min(rect.width, rect.height)  # 1.2 от промежутка

        for i, rotate in enumerate(value):
            difference = value[i+1] - rotate if i+2 < len(value) else 0

            if difference == 3:
                difference = 1
            elif difference == -3:
                difference = -1

            if difference in (-1, 0, 1):
                self._track.append((pos,
                                    pos+Vec2(0, -scale*0.5 if difference!=0 else -1/3*scale),
                                    pos+Vec2(-scale*0.2*difference if difference!=0 else 1/3*scale, -1/3*scale if difference==0 else 0),
                                    pos+Vec2(0, -scale)))
            else:
                error(value)
                raise ValueError('tiles look at each other')

            rotation_matrix = Mat3.rotate_mat(rotate*90)
            for j in range(len(self._track)):
                self._track[j] = rotation_matrix.xform_vec(self._track[j])

    def get_division_vec(self)->Vec2:
        scale = min(self._first_tile.rect.width, self._first_tile.rect.height)
        return Vec2(1/6*scale*random(), 1/6*scale*random())

    def set_first_tile(self, value:Tile):
        self._first_tile = value