from math import pi, sin, cos

from direct.task import Task

from direct.showbase.ShowBase import ShowBase
from panda3d import core

from scripts.basic_classes.rect import Rect
from scripts.basic_classes.sprite import Sprite


class MyApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        Sprite(Rect(0, 0, 2, 2), 'images2d/anty_invisibility_tower.png', self)

        self.taskMgr.add(self.spinCameraTask, "SpinCameraTask")

    def spinCameraTask(self, task):
        angleDegrees = task.time * 100.0
        angleRadians = angleDegrees * (pi / 180.0)
        self.camera.setPos(20 * sin(angleRadians), -20 * cos(angleRadians), 8)
        self.camera.setHpr(angleDegrees, -15, 15)
        return Task.cont