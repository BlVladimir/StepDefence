from direct.showbase.ShowBase import ShowBase
from direct.task import Task

from scripts.basic_classes.rect import Rect
from scripts.basic_classes.sprite3D import Sprite3D
from scripts.main_classes.context import Context
from scripts.main_classes.DTO.render import Render
from math import radians, sin, cos



class StepDefence(ShowBase):
    """Главный класс, осуществляющий взаимодействие программы с пользователем"""
    def __init__(self):
        ShowBase.__init__(self)
        self.__context = Context(Render(self.render, self.loader))

        Sprite3D(Rect(0, 0, 2, 2), 'images2d/anty_invisibility_tower.png', Render(self.render, self.loader, self.render2d))

        self.taskMgr.add(self.spinCameraTask, "SpinCameraTask")

    def spinCameraTask(self, task):
        angleDegrees = task.time * 100.0
        angleRadians = radians(angleDegrees)
        self.camera.setPos(20 * sin(angleRadians), -20 * cos(angleRadians), 8)
        self.camera.setHpr(angleDegrees, -15, 15)
        return Task.cont