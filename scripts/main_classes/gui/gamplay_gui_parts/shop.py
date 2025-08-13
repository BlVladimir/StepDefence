from direct.gui.DirectButton import DirectButton
from direct.gui.DirectFrame import DirectFrame
from panda3d.core import NodePath, TransparencyAttrib, Vec3, Texture, PNMImage

from scripts.main_classes.interaction.event_bus import EventBus


class Shop:
    def __init__(self, relationship:float, buttons_node:NodePath):
        self.__shop_node = buttons_node.attachNewNode('shop_node')
        self.__shop_node.hide()
        self.__shop_frame = DirectFrame(parent=self.__shop_node,
                                        frameSize=(0.25, -0.25, 1, -1),
                                        frameColor=(0.5, 0.5, 0.5, 1),
                                        pos=Vec3(-relationship + 0.25, 0))

        buttons_towers = {DirectButton(image=self.__create_texture('images2d/tower/common_foundation.png',
                                                                   'images2d/tower/common_gun.png'),
                                       parent=self.__shop_frame,
                                       scale=0.075,
                                       pos=Vec3(0, 0.8),
                                       command=lambda: EventBus.publish('buy_tower', 'basic'),
                                       frameColor=((0.5, 0.5, 0.5, 1),
                                                   (0.7, 0.7, 0.7, 1),
                                                   (0.3, 0.3, 0.3, 1))),
                          DirectButton(image=self.__create_texture('images2d/tower/sniper_foundation.png',
                                                                   'images2d/tower/sniper_gun.png'),
                                       parent=self.__shop_frame,
                                       scale=0.075,
                                       pos=Vec3(0, 0.6),
                                       command=lambda: EventBus.publish('buy_tower', 'sniper'),
                                       frameColor=((0.5, 0.5, 0.5, 1),
                                                   (0.7, 0.7, 0.7, 1),
                                                   (0.3, 0.3, 0.3, 1))),
                          DirectButton(image='images2d/tower/anty_shield.png',
                                       parent=self.__shop_frame,
                                       scale=0.075,
                                       pos=Vec3(0, 0.4),
                                       command=lambda: EventBus.publish('buy_tower', 'anty_shield'),
                                       frameColor=((0.5, 0.5, 0.5, 1),
                                                   (0.7, 0.7, 0.7, 1),
                                                   (0.3, 0.3, 0.3, 1))),
                          DirectButton(image=self.__create_texture('images2d/tower/venom_foundation.png',
                                                                   'images2d/tower/venom_gun.png'),
                                       parent=self.__shop_frame,
                                       scale=0.075,
                                       pos=Vec3(0, 0.2),
                                       command=lambda: EventBus.publish('buy_tower', 'venom'),
                                       frameColor=((0.5, 0.5, 0.5, 1),
                                                   (0.7, 0.7, 0.7, 1),
                                                   (0.3, 0.3, 0.3, 1))),
                          DirectButton(image='images2d/tower/anty_invisibility_tower.png',
                                       parent=self.__shop_frame,
                                       scale=0.075,
                                       pos=Vec3(0, 0),
                                       command=lambda: EventBus.publish('buy_tower', 'anty_invisible'),
                                       frameColor=((0.5, 0.5, 0.5, 1),
                                                   (0.7, 0.7, 0.7, 1),
                                                   (0.3, 0.3, 0.3, 1))),
                          DirectButton(image='images2d/tower/cannon.png',
                                       parent=self.__shop_frame,
                                       scale=0.075,
                                       pos=Vec3(0, -0.6),
                                       command=lambda: EventBus.publish('buy_tower', 'cannon'),
                                       frameColor=((0.5, 0.5, 0.5, 1),
                                                   (0.7, 0.7, 0.7, 1),
                                                   (0.3, 0.3, 0.3, 1)))

                          }


        for button in buttons_towers:
            button.setTransparency(TransparencyAttrib.MAlpha)
        EventBus.subscribe('open_shop', lambda event_type, data: self.__shop_node.show())
        EventBus.subscribe('close_shop', lambda event_type, data: self.__shop_node.hide())

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