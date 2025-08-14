from logging import debug, error
from typing import Set, Optional

from panda3d.core import NodePath, CollisionTraverser, CollisionHandlerQueue, CollisionRay, CollisionNode, Point3, \
    BitMask32

from scripts.arrays_handlers.arrays_controllers.enemies.enemy import Enemy
from scripts.arrays_handlers.arrays_controllers.towers.states.select_for_attack_state.abstract_targets_state import \
    AbstractTargetsState
from scripts.arrays_handlers.arrays_controllers.towers.tower import Tower
from scripts.main_classes.interaction.event_bus import EventBus
from scripts.sprite.sprite3D import Sprite3D


class RayState(AbstractTargetsState):
    def __init__(self, render_root:NodePath):
        super().__init__()
        self.__render_root = render_root

        self.__picker = CollisionTraverser()
        self.__picker_queue = CollisionHandlerQueue()
        self.__ray = CollisionRay()

        ray_node = CollisionNode('mouse_ray')
        ray_node.addSolid(self.__ray)

        ray_node.setFromCollideMask(BitMask32.bit(1))  # луч "излучает" по биту 1
        ray_node.setIntoCollideMask(BitMask32.allOff())
        picker_np = render_root.attachNewNode(ray_node)
        picker_np.show()

        self.__picker.addCollider(picker_np, self.__picker_queue)

        EventBus.subscribe('change_scene', lambda event_type, data: picker_np.hide())
        EventBus.subscribe('using_tower', lambda event_type, data: picker_np.show() if data[0].type_target_state == 'ray' else None)


    def determine_set(self, enemies_set:Set[Enemy], tower:Tower, **kwargs)->Set[Sprite3D]:
        """Как определить множество врагов для выстрела"""
        mouse_pos: Optional[Point3] = kwargs.get('mouse_pos')

        # Обновляем начало и направление луча
        tower_pos = tower.sprite.main_node.getPos(self.__render_root)
        self.__ray.setOrigin(tower_pos)
        try:
            self.__ray.setDirection(mouse_pos - tower_pos)
        except TypeError:
            error('TypeError: mouse_pos is None')
            return set()

        # Трассируем сцену
        self.__picker.traverse(self.__render_root)

        targets_set: Set[Sprite3D] = set()
        if self.__picker_queue.getNumEntries() > 0:
            self.__picker_queue.sortEntries()
            # debug('has queue')
            for entry in self.__picker_queue.getEntries():
                collided_node = entry.getIntoNodePath()
                # Фильтруем только коллайдеры спрайтов
                # debug(collided_node)
                if collided_node.getName() == 'sprite_collision':
                    sprite: Sprite3D = collided_node.getPythonTag('collision')
                    # И только врагов
                    if sprite.main_node.getName() == 'enemy':
                        sprite.is_special_selected = True
                        targets_set.add(sprite)
        # debug(f'targets_set: {len(targets_set)}')
        return targets_set

    def hit(self, tower:Tower, **kwargs)->Optional[Sprite3D]:
        """В каких врагов стрелять"""
        if kwargs['targets_set']:
            if self.__hit_condition(tower, **kwargs):
                for enemy in kwargs['targets_set']:
                    enemy.external_object.hit(tower.damage_dict(enemy.external_object))
        elif kwargs['main_sprite']:
            return kwargs['main_sprite']
        return None

    @staticmethod
    def __hit_condition(tower:Tower, **kwargs)->bool:
        return tower.is_charge

    def __str__(self):
        return 'ray'