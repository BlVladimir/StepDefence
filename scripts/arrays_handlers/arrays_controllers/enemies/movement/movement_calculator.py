from logging import debug
from typing import List

from panda3d.core import Vec2, NodePath, Vec3, LineSegs

from scripts.arrays_handlers.arrays_controllers.enemies.movement.bezier_curve_maker import BezierCurveMaker
from scripts.arrays_handlers.arrays_controllers.maps.creating_map.track import Track


class MovementCalculator:
    """Расчитывает траекторию движения"""
    def __init__(self, bezier_curve_maker:BezierCurveMaker, pos_on_tile:Vec2, started_division_vec:Vec2, track:Track, track_node:NodePath, debug_mode:bool = True):
        self.__bezier_curve_maker = bezier_curve_maker
        self.__pos_on_tile = pos_on_tile
        self.__previous_division_vec = started_division_vec

        self.__current_tile = 0
        self.__track = track
        self._track_node = track_node
        if not debug_mode:
            self._track_node.hide()

    def get_movement_array(self, draw_track:bool)->List[Vec3]:
        """Расчитывает массив точек"""
        debug(self.__pos_on_tile)
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

        if draw_track:
            lines = LineSegs()
            lines.setColor(1, 1, 0, 1)
            lines.setThickness(2)
            lines.moveTo(movement_array[0])
            for i in range(1, len(movement_array)):
                lines.drawTo(movement_array[i])

            line_node = self._track_node.attachNewNode(lines.create())
            line_node.setBin('lines', 0)
            line_node.setDepthTest(False)
            line_node.setDepthWrite(False)

        return movement_array



