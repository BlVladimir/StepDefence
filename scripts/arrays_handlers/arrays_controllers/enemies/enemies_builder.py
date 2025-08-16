from random import randrange

from panda3d.core import NodePath, CullBinManager, Vec2

from scripts.arrays_handlers.arrays_controllers.enemies.damage.damage_calculater import DamageCalculater
from scripts.arrays_handlers.arrays_controllers.enemies.enemies_config_reader import EnemiesConfigReader, EnemiesConfig
from scripts.arrays_handlers.arrays_controllers.enemies.movement.bezier_curve_maker import BezierCurveMaker
from scripts.arrays_handlers.arrays_controllers.enemies.enemy import Enemy
from scripts.arrays_handlers.arrays_controllers.enemies.movement.movement_calculator import MovementCalculator
from scripts.arrays_handlers.arrays_controllers.maps.creating_map.track import Track
from scripts.sprite.rect import Rect3D

from scripts.sprite.sprites_factory import SpritesFactory


class EnemiesBuilder:
    """Создает врагов"""
    def __init__(self, node:NodePath, sprites_factory:SpritesFactory, track:Track):
        self.__enemies_node = node
        self.__sprites_factory = sprites_factory
        self.__bezier_curve_maker = BezierCurveMaker()
        self._counter = 0
        self.__track = track

        CullBinManager.get_global_ptr().add_bin('enemy', CullBinManager.BT_fixed, 4)

        self.__damage_calculator = DamageCalculater()

        self.__conf = EnemiesConfigReader()


    def create_enemy(self, wave:int, rect:Rect3D, type_enemy:str, pos_on_tile:Vec2, started_division_vec:Vec2)->None:
        parameters = self.__conf.get_characteristic(type_enemy)
        parameters['health'] = round(parameters['health'] * self.__get_wave_health_modifier(wave))
        sprite = self.__sprites_factory.create_sprite(rect, self.__conf.get_path_image(type_enemy), self.__enemies_node,
                                                      'enemy', self._counter)
        Enemy(sprite,
              parameters,
              MovementCalculator(self.__bezier_curve_maker, pos_on_tile, started_division_vec, self.__track),
              self.__damage_calculator, wave//4+2),
        self._counter += 1

    def clear_enemies(self):
        self._counter = 0
        self.__enemies_node.getChildren().detach()

    @staticmethod
    def __get_wave_health_modifier(wave:int)->float:
        if wave != 0:
            return 1 + (0.1 * (randrange(-1, 2)+wave//2))
        else:
            return 1