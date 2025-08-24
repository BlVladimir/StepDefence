from logging import error

from panda3d.core import NodePath, Texture

from scripts.arrays_handlers.arrays_controllers.enemies.enemy_sprite import EnemySprite
from scripts.arrays_handlers.arrays_controllers.maps.tile_sprite import TileSprite
from scripts.main_classes.interaction.render_manager import RenderManager
from scripts.main_classes.settings import Settings
from scripts.sprite.rect import Rect3D
from scripts.sprite.sprite3D import Sprite3D


class SpritesFactory:
    def __init__(self, settings:Settings, render_manager:RenderManager, relationship:float):
        self.__settings = settings
        self.__render_manager = render_manager
        self._relationship = relationship

    def create_sprite(self, rect:Rect3D, path_image:str, parent:NodePath|Sprite3D, name_group:str, number:int)->Sprite3D:
        match name_group:
            case 'enemy':
                return EnemySprite(rect=rect, path_image=path_image, parent=parent, name_group=name_group, loader=self.__render_manager.loader, number=number, debug_mode=self.__settings.debug_mode)
            case 'tile':
                return TileSprite(rect = rect, path_image=path_image, parent=parent, loader=self.__render_manager.loader, name_group=name_group, number=number, debug_mode=self.__settings.debug_mode)
            case _:
                return Sprite3D(rect = rect, path_image=path_image, parent=parent, loader=self.__render_manager.loader, name_group=name_group, number=number, debug_mode=self.__settings.debug_mode)

    def get_texture(self, path_image: str)->Texture:

        try:
            texture = self.__render_manager.loader.loadTexture(path_image)
            return texture
        except Exception as e:
            error(f"❌ Failed to load texture: {e}")
            from panda3d.core import PNMImage
            fallback_texture = Texture("fallback")
            image = PNMImage(32, 32)
            image.fill(1, 0, 0)  # Красный цвет для заметности
            fallback_texture.load(image)
            return fallback_texture

    def create2Dnode(self, name:str)->NodePath:
        return self.__render_manager.main_node2d.attachNewNode(name)

    def create3Dnode(self, name:str)->NodePath:
        return self.__render_manager.main_node3d.attachNewNode(name)

    @property
    def relationship(self)->float:
        return self._relationship