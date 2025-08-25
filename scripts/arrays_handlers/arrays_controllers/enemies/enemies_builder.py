from random import randrange

from panda3d.core import NodePath, CullBinManager, Vec2

from scripts.arrays_handlers.arrays_controllers.enemies.damage.damage_calculater import DamageCalculater
from scripts.arrays_handlers.arrays_controllers.enemies.enemies_config import EnemiesConfig
from scripts.arrays_handlers.objects_manager import ObjectsManager
from scripts.arrays_handlers.arrays_controllers.enemies.movement.bezier_curve_maker import BezierCurveMaker
from scripts.arrays_handlers.arrays_controllers.enemies.enemy import Enemy
from scripts.arrays_handlers.arrays_controllers.enemies.movement.movement_calculator import MovementCalculator
from scripts.arrays_handlers.arrays_controllers.maps.creating_map.track import Track
from scripts.sprite.rect import Rect3D

from scripts.sprite.sprites_factory import SpritesFactory


class EnemiesBuilder:
    """Создает врагов"""
    def __init__(self, node:NodePath, sprites_factory:SpritesFactory, track:Track, enemies_manager:ObjectsManager):
        self.__enemies_node = node
        self.__enemies_manager = enemies_manager
        self.__sprites_factory = sprites_factory
        self.__bezier_curve_maker = BezierCurveMaker()

        self.__track = track

        CullBinManager.get_global_ptr().add_bin('enemy', CullBinManager.BT_fixed, 4)

        self.__damage_calculator = DamageCalculater()


    def create_enemy(self, wave:int, rect:Rect3D, type_enemy:str, pos_on_tile:Vec2, started_division_vec:Vec2, health_k)->None:
        parameters = EnemiesConfig.get_characteristic(type_enemy)
        parameters['health'] = round(parameters['health'] * health_k)
        sprite = self.__sprites_factory.create_sprite(rect, EnemiesConfig.get_textures(type_enemy)[0], self.__enemies_node,
                                                      'enemy', len(self.__enemies_manager))
        enemy = Enemy(type_enemy,
                      sprite,
                      parameters,
                      MovementCalculator(self.__bezier_curve_maker, pos_on_tile,
                                         started_division_vec, self.__track),
                      self.__damage_calculator, wave // 4 + 2, EnemiesConfig.get_textures(type_enemy))
        self.__enemies_manager + enemy

    def clear_enemies(self):
        self.__enemies_node.getChildren().detach()

    @staticmethod
    def __get_wave_health_modifier(wave:int)->float:
        if wave != 0:
            return 1 + (0.3 * (randrange(-1, 2)+wave//2))
        else:
            return 1