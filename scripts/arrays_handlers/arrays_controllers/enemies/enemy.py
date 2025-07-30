from direct.interval.LerpInterval import LerpPosInterval
from direct.interval.MetaInterval import Sequence

from scripts.arrays_handlers.arrays_controllers.enemies.effects.bezier_curve_maker import BezierCurveMaker
from scripts.arrays_handlers.arrays_controllers.enemies.effects.effect_state import EffectState
from scripts.arrays_handlers.arrays_controllers.maps.creating_map.track import Track
from scripts.sprite.sprite3D import Sprite3D


class Enemy:
    """Класс врагов"""
    def __init__(self, sprite:Sprite3D, health:int, effect_state:EffectState, bezier_curve_maker:BezierCurveMaker, track:Track):
        self._sprite = sprite
        self._sprite.external_object = self

        self._health = health

        self._effect_state = effect_state

        self.__bezier_curve_maker = bezier_curve_maker

        self.__track = track

        self.__current_tile = 0

    def move(self):
        """Двигает всех врагов"""
        points = self.__track.track[self.__current_tile]
        for i in (0, 1, 2, 3):
            points[i] += self.__track.get_division_vec()
        movement_array = self.__bezier_curve_maker.generate_uniform_points(points[0], points[1], points[2], points[3])

        intervals = []
        for i in range(1, len(movement_array)):
            intervals.append(
                LerpPosInterval(
                    self._sprite.main_node,  # Ваша нода
                    duration=0.1,
                    pos=movement_array[i],
                    startPos=movement_array[i - 1]
                )
            )

        sequence = Sequence(*intervals)
        sequence.start()
