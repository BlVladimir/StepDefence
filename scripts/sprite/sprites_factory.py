from panda3d.core import NodePath

from scripts.main_classes.interaction.render_manager import RenderManager
from scripts.main_classes.settings import Settings
from scripts.sprite.rect import Rect3D
from scripts.sprite.sprite3D import Sprite3D


class SpritesFactory:
    def __init__(self, settings:Settings, render_manager:RenderManager):
        self.__settings = settings
        self.__render_manager = render_manager

    def create_sprite(self, rect:Rect3D, path_image:str, parent:NodePath|Sprite3D, name_group:str, number:int)->Sprite3D:
        return Sprite3D(rect = rect, path_image=path_image, parent=parent, loader=self.__render_manager.loader, name_group=name_group, number=number, debug_mode=self.__settings.debug_mode)

    def create2Dnode(self, name:str)->NodePath:
        return self.__render_manager.main_node2d.attachNewNode(name)

    def create3Dnode(self, name:str)->NodePath:
        return self.__render_manager.main_node3d.attachNewNode(name)

    @property
    def relationship(self)->float:
        win = self.__render_manager.win
        return win.getXSize() / win.getYSize()