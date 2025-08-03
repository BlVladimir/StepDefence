from direct.gui.DirectButton import DirectButton
from direct.gui.DirectFrame import DirectFrame
from panda3d.core import Vec3, TransparencyAttrib, Texture, PNMImage, NodePath

from scripts.main_classes.buttons.buttons_controller import ButtonsController
from scripts.main_classes.buttons.buttons_group import ButtonsGroup
from scripts.main_classes.interaction.event_bus import EventBus


class GameplayButtonsController(ButtonsController):
    def __init__(self, relationship:float, buttons_node:NodePath):
        super().__init__(relationship , buttons_node)

        self.__gameplay_group = ButtonsGroup(self._buttons_node,
                                             DirectButton(image='images2d/UI/exit_in_main_menu.png',
                                                          parent=self._buttons_node,
                                                          scale=0.1,
                                                          pos=Vec3(-self._relationship + self._relationship * 0.075, 0.9),
                                                          command=lambda: EventBus.publish('change_scene', 'main_menu'),
                                                          frameColor=((0.5, 0.5, 0.5, 1),
                                                                      (0.7, 0.7, 0.7, 1),
                                                                      (0.3, 0.3, 0.3, 1))))
        self.__gameplay_group.hide()


        button_texture = self.__create_texture('images2d/tower/common_foundation.png', 'images2d/tower/common_gun.png')
        self.__shop_node = self._buttons_node.attachNewNode('shop_node')
        self.__shop_frame = DirectFrame(parent=self.__shop_node,
                                        frameSize=(0, self._relationship * 0.5, -2, 0),
                                        frameColor=(0.5, 0.5, 0.5, 1),
                                        pos=Vec3(-self._relationship, 1))
        button_tower = DirectButton(image=button_texture,
                                    parent=self.__shop_frame,
                                    scale=0.2,
                                    pos=Vec3(0.2, -0.2),
                                    command=lambda: EventBus.publish('buy_tower', 'basic'),
                                    frameColor=((0.5, 0.5, 0.5, 1),
                                                (0.7, 0.7, 0.7, 1),
                                                (0.3, 0.3, 0.3, 1)))
        button_tower.setTransparency(TransparencyAttrib.MAlpha)
        self.__shop_node.hide()

    def open_shop(self)->None:
        self.__shop_node.show()

    def close_shop(self)->None:
        self.__shop_node.hide()

    @staticmethod
    def __create_texture(first_path:str, second_path:str, xto:int=0, yto:int=0)->Texture:
        first_image = PNMImage(first_path)
        second_image = PNMImage(second_path)
        composed_image = PNMImage(first_image.getXSize(), first_image.getYSize())
        composed_image.copyFrom(first_image)

        for x in range(second_image.getXSize()):
            for y in range(second_image.getYSize()):
                r, g, b, a = second_image.getRed(x, y), second_image.getGreen(x, y), second_image.getBlue(x, y), second_image.getAlpha(x, y)
                if a > 0:
                    composed_image.setXelA(xto + x, yto + y, r, g, b, a)

        final_texture = Texture()
        final_texture.load(composed_image)
        return final_texture