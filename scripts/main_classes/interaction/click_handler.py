from panda3d.core import CollisionTraverser, CollisionHandlerQueue, CollisionRay, CollisionNode, NodePath


class ClickHandler:
    """Обрабатывает клики в трехмерном пространстве"""

    def __init__(self, camera_node:NodePath, mouse_watcher:NodePath, render_root:NodePath):
        self.cam_node = camera_node
        self.mouse_watcher = mouse_watcher
        self.render_root = render_root

        self.picker = CollisionTraverser()
        self.picker_queue = CollisionHandlerQueue()
        self.picker_ray = CollisionRay()

        picker_node = CollisionNode('mouse_ray')
        picker_node.addSolid(self.picker_ray)
        self.picker_np = camera_node.get_parent().attachNewNode(picker_node)  # Прикрепляем к родителю камеры

        self.picker.addCollider(self.picker_np, self.picker_queue)

    def check_mouse_pick(self):
        if self.mouse_watcher.hasMouse():
            mpos = self.mouse_watcher.getMouse()
            self.picker_ray.setFromLens(self.cam_node, mpos.x, mpos.y)
            self.picker.traverse(self.render_root)

            if self.picker_queue.getNumEntries() > 0:
                self.picker_queue.sortEntries()
                entry = self.picker_queue.getEntry(0)
                return entry.getIntoNodePath().findNetTag('clickable')
        return None