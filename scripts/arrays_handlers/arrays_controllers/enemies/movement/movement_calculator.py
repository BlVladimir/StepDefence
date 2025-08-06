from logging import debug
from typing import List

from panda3d.core import Vec2, NodePath, Vec3, LineSegs

from scripts.arrays_handlers.arrays_controllers.enemies.movement.bezier_curve_maker import BezierCurveMaker
from scripts.arrays_handlers.arrays_controllers.maps.creating_map.track import Track


class MovementCalculator:
    """Расчитывает траекторию движения"""
    def __init__(self, bezier_curve_maker:BezierCurveMaker, pos_on_tile:Vec2, started_division_vec:Vec2, track:Track):
        self.__bezier_curve_maker = bezier_curve_maker
        self.__pos_on_tile = pos_on_tile
        self.__previous_division_vec = started_division_vec

        self.__current_tile = 0
        self.__track = track

    def get_movement_array(self)->List[Vec3]:
        """Расчитывает массив точек"""
        points = self.__track.track[self.__current_tile]
        for i in (0, 1, 2, 3):
            points[i] += self.__pos_on_tile
        division_vec = self.__track.get_division_vec()
        movement_array = self.__bezier_curve_maker.generate_uniform_points(points[0] + self.__previous_division_vec,
                                                                           points[1] + self.__previous_division_vec,
                                                                           points[2] + division_vec,
                                                                           points[3] + division_vec)
        self.__previous_division_vec = division_vec

        for i in range(len(movement_array)):
            movement_array[i] = Vec3(movement_array[i].x, movement_array[i].y, 0)

        self.__current_tile += 1

        return movement_array



