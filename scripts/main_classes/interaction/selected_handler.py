from logging import debug

from panda3d.core import CollisionTraverser, CollisionHandlerQueue, CollisionRay, CollisionNode, NodePath

from scripts.interface.i_click_handler import ISelectedHandler
from scripts.interface.i_context import IContext
from direct.task import Task

from scripts.main_classes.event_bus import EventBus


class SelectedHandler(ISelectedHandler):
    """Обрабатывает клики в трехмерном пространстве"""

    def __init__(self, camera_node:NodePath, mouse_watcher:NodePath, render_root:NodePath, context:IContext):
        self.__cam_node = camera_node
        self.__mouse_watcher = mouse_watcher
        self.__render_root = render_root

        self.__picker = CollisionTraverser()
        self.__picker_queue = CollisionHandlerQueue()
        self.__picker_ray = CollisionRay()

        picker_node = CollisionNode('mouse_ray')
        picker_node.addSolid(self.__picker_ray)
        picker_np = camera_node.getParent().attachNewNode(picker_node)  # Прикрепляем к родителю камеры

        self.__picker.addCollider(picker_np, self.__picker_queue)

        self.__context = context

        self.__last_sprite = set()

    def check_collision(self, task):
        """Проверяет, на какой тайл наведена мышка"""
        if self.__mouse_watcher.hasMouse():
            mpos = self.__mouse_watcher.getMouse()
            self.__picker_ray.setFromLens(self.__cam_node.node(), mpos.x, mpos.y)
            self.__picker.traverse(self.__render_root)

            if self.__picker_queue.getNumEntries() > 0:
                self.__picker_queue.sortEntries()
                not_selected = self.__last_sprite.difference(self.__picker_queue.getEntries())
                for sprite in not_selected:
                    EventBus.publish('unselect_element', sprite)
                self.__last_sprite.difference_update(not_selected)
                for entry in self.__picker_queue.getEntries():
                    collided_node = entry.getIntoNodePath()

                    if collided_node.getName() == 'sprite_collision':
                        sprite = collided_node.getPythonTag('collision')
                        self.__last_sprite.add(sprite)
                        EventBus.publish('select_element', sprite)
                    elif collided_node.getName() == 'global_collision':
                        point = entry.getSurfacePoint(self.__render_root)
                        EventBus.publish('rotate_gun', point)
                return Task.cont
        if self.__last_sprite:
            for sprite in self.__last_sprite:
                EventBus.publish('unselect_element', sprite)
            self.__last_sprite.clear()
        return Task.cont