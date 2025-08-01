from panda3d.core import NodePath, CullBinManager, Vec2

from scripts.arrays_handlers.arrays_controllers.enemies.movement.bezier_curve_maker import BezierCurveMaker
from scripts.arrays_handlers.arrays_controllers.enemies.movement.effect_state import EffectState
from scripts.arrays_handlers.arrays_controllers.enemies.enemies_config import EnemiesConfig
from scripts.arrays_handlers.arrays_controllers.enemies.enemy import Enemy
from scripts.arrays_handlers.arrays_controllers.enemies.movement.movement_calculator import MovementCalculator
from scripts.arrays_handlers.arrays_controllers.maps.creating_map.track import Track
from scripts.main_classes.settings import Settings
from scripts.sprite.rect import Rect3D
from scripts.sprite.sprite3D import Sprite3D
from panda3d.core import Loader


class EnemiesBuilder:
    """Создает врагов"""
    def __init__(self, node:NodePath, loader:Loader, track:Track, track_node:NodePath):
        self.__config = EnemiesConfig()
        self.__enemies_node = node
        self.__loader = loader
        self.__bezier_curve_maker = BezierCurveMaker()
        self._counter = 0
        self.__track = track

        self._track_node = track_node

        CullBinManager.get_global_ptr().add_bin('enemy', CullBinManager.BT_fixed, 4)
        CullBinManager.get_global_ptr().add_bin('lines', CullBinManager.BT_fixed, 50)


    def create_enemy(self, wave:int, rect:Rect3D, type_enemy:str, pos_on_tile:Vec2, started_division_vec:Vec2, settings:Settings)->None:
        parameters = self.__config.get_started_characteristic(type_enemy)
        effects = parameters.copy()
        effects.pop('health')
        Enemy(Sprite3D(rect=rect, path_image=self.__config.get_image_enemy(type_enemy), parent=self.__enemies_node,
                       loader=self.__loader, name_group='enemy', number=self._counter, debug_mode=settings.debug_mode),
              parameters['health'] + self.__config.get_wave_health_modifier(wave),
              EffectState(effects),
              MovementCalculator(self.__bezier_curve_maker, pos_on_tile, started_division_vec, self.__track, self._track_node, settings.debug_mode))
        self._counter += 1

    def clear_enemies(self):
        self._counter = 0
        self.__enemies_node.getChildren().detach()