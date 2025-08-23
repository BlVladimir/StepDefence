from copy import deepcopy
from random import random
from typing import List
from logging import error
from panda3d.core import Vec2, Mat3

from scripts.main_classes.interaction.event_bus import EventBus
from scripts.sprite.rect import Rect3D


class Track:
    """Класс пути врага"""
    def __init__(self):
        self._track = []
        self._first_tile_rect = None

    def get_track(self, tile:int)->List[Vec2]:
        if tile == len(self._track)-1:
            EventBus.publish('lose')
        return deepcopy(self._track[tile])

    def set_track(self, value:List[int]):
        pos = self._first_tile_rect.top_left
        scale = 1.2*self._first_tile_rect.width  # 1.2 от промежутка
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

    def get_division_vec(self)->Vec2:
        scale = min(self._first_tile_rect.width, self._first_tile_rect.height)
        return Vec2(1/6*scale*random(), 1/6*scale*random())

    def set_first_tile(self, value:Rect3D)->None:
        self._first_tile_rect = value