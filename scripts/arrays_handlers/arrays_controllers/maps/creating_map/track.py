from copy import deepcopy
from random import random
from typing import List
from logging import error, debug
from panda3d.core import Vec2, Mat3

from scripts.arrays_handlers.arrays_controllers.maps.tile import Tile


class Track:
    def __init__(self):
        self._track = []
        self._first_tile = None

    @property
    def track(self)->List[Vec2]:
        return deepcopy(self._track)

    @track.setter
    def track(self, value:List[int]):
        rect = self._first_tile.sprite.rect
        pos = Vec2(0, 0)
        scale = 1.2*min(rect.width, rect.height)  # 1.2 от промежутка
        self._track = []
        for i, rotate in enumerate(value):
            difference = value[i+1] - rotate if i+1 < len(value) else 0
            if difference == 3:
                difference = -1
            elif difference == -3:
                difference = 1
            if difference in (-1, 0, 1):
                one_move = [Vec2(0, 0),
                             Vec2(0, scale * 0.5),
                             Vec2(-scale * 0.3 * difference if difference != 0 else 0,
                                        0.75 * scale if difference == 0 else scale),
                             Vec2(0, scale)]
            else:
                error(value)
                raise ValueError('tiles look at each other')
            rotation_matrix = Mat3.rotateMat(-rotate*90)
            for j in (range(len(one_move))):
                one_move[j] = rotation_matrix.xform_vec(one_move[j])
                one_move[j] += pos

            self._track.append(one_move)
            pos = one_move[3]
        debug(self._track)

    def get_division_vec(self)->Vec2:
        scale = min(self._first_tile.sprite.rect.width, self._first_tile.sprite.rect.height)
        return Vec2(1/6*scale*random(), 1/6*scale*random())

    def set_first_tile(self, value:Tile):
        self._first_tile = value