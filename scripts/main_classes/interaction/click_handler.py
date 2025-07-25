import logging

from panda3d.core import CollisionTraverser, CollisionHandlerQueue, CollisionRay, CollisionNode, NodePath

from logging import debug
from scripts.interface.i_click_handler import IClickHandler
from scripts.interface.i_context import IContext
from direct.task import Task


class ClickHandler(IClickHandler):
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

    def check_tiles(self, task):
        """Проверяет, на какой тайл наведена мышка"""
        if self.__mouse_watcher.hasMouse():
            mpos = self.__mouse_watcher.getMouse()
            self.__picker_ray.setFromLens(self.__cam_node.node(), mpos.x, mpos.y)
            self.__picker.traverse(self.__render_root)

            if self.__picker_queue.getNumEntries() > 0:
                self.__picker_queue.sortEntries()
                entry = self.__picker_queue.getEntry(0)
                collided_node = entry.getIntoNodePath().findNetTag('tile')
                sprite = collided_node.getPythonTag("sprite")
                dist_debug = logging.getLogger("dist_debug")
                dist_debug.debug(f"click on tile {sprite}")

                sprite.add_wireframe()
                return Task.cont
        return Task.cont