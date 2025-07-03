from direct.showbase.ShowBase import ShowBase
from direct.task import Task

from scripts.sprite.rect import Rect
from scripts.sprite.sprite3D import Sprite3D
from scripts.main_classes.DTO.key_watcher import KeyWatcher
from scripts.main_classes.context import Context
from scripts.main_classes.DTO.render import Render
from math import radians, sin, cos



class StepDefence(ShowBase):
    """Главный класс, осуществляющий взаимодействие программы с пользователем"""
    def __init__(self):
        ShowBase.__init__(self)

        print(self.win.get_size())
        self.__context = Context(Render(self.render, self.loader, self.render2d), KeyWatcher(self.mouseWatcherNode))
        Sprite3D(Rect(0, 0, 2, 2), 'images2d/anty_invisibility_tower.png', Render(render=self.render, loader=self.loader, render2d=self.render2d))
        self.taskMgr.add(self.spinCameraTask, "SpinCameraTask")

    def spinCameraTask(self, task):
        angleDegrees = task.time * 100.0
        angleRadians = radians(angleDegrees)
        self.camera.setPos(20 * sin(angleRadians), -20 * cos(angleRadians), 8)
        self.camera.setHpr(angleDegrees, -15, 15)
        return Task.cont