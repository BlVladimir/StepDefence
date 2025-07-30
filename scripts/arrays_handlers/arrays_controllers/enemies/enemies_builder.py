from panda3d.core import NodePath, CullBinManager

from scripts.arrays_handlers.arrays_controllers.enemies.effects.bezier_curve_maker import BezierCurveMaker
from scripts.arrays_handlers.arrays_controllers.enemies.effects.effect_state import EffectState
from scripts.arrays_handlers.arrays_controllers.enemies.enemies_config import EnemiesConfig
from scripts.arrays_handlers.arrays_controllers.enemies.enemy import Enemy
from scripts.arrays_handlers.arrays_controllers.maps.creating_map.track import Track
from scripts.sprite.rect import Rect3D
from scripts.sprite.sprite3D import Sprite3D
from panda3d.core import Loader


class EnemiesBuilder:
    """Создает врагов"""
    def __init__(self, node:NodePath, loader:Loader, track:Track):
        self.__config = EnemiesConfig()
        self.__enemies_node = node
        self.__loader = loader
        self.__bezier_curve_maker = BezierCurveMaker()
        self._counter = 0
        self.__track = track

        CullBinManager.get_global_ptr().add_bin('enemy', CullBinManager.BT_fixed, 4)


    def create_enemy(self, wave:int, rect:Rect3D, type_enemy:str)->None:
        parameters = self.__config.get_started_characteristic(type_enemy)
        effects = parameters.copy()
        effects.pop('health')
        Enemy(Sprite3D(rect=rect, path_image=self.__config.get_image_enemy(type_enemy), parent=self.__enemies_node,
                       loader=self.__loader, name_group='enemy', number=self._counter),
              parameters['health'] + self.__config.get_wave_health_modifier(wave),
              EffectState(effects),
              self.__bezier_curve_maker)
        self._counter += 1

    def clear_enemies(self):
        self._counter = 0
        self.__enemies_node.getChildren().detach()