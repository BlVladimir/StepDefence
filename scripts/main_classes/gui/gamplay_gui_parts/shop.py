from direct.gui.DirectButton import DirectButton
from direct.gui.DirectFrame import DirectFrame
from panda3d.core import NodePath, TransparencyAttrib, Vec3, Texture, PNMImage, TextNode, Vec4D

from scripts.arrays_handlers.arrays_controllers.towers.value_tower_config import ValueTowerConfig
from scripts.main_classes.interaction.event_bus import EventBus


class Shop:
    def __init__(self, relationship: float, buttons_node: NodePath):
        self.__shop_node = buttons_node.attachNewNode('shop_node')
        self.__shop_node.hide()
        self.__shop_frame = DirectFrame(parent=self.__shop_node,
                                        frameSize=(0.25, -0.25, 1, -1),
                                        frameColor=(0.5, 0.5, 0.5, 1),
                                        pos=Vec3(-relationship + 0.25, 0))
        self.__products = {self.__create_products('basic', Vec3(0, 0.8)),
                           self.__create_products('sniper', Vec3(0, 0.6)),
                           self.__create_products('anty_shield', Vec3(0, 0.4)),
                           self.__create_products('venom', Vec3(0, 0.2)),
                           self.__create_products('anty_invisible', Vec3(0, 0)),
                           self.__create_products('cutter', Vec3(0, -0.2)),
                           self.__create_products('laser', Vec3(0, -0.4)),
                           self.__create_products('cannon', Vec3(0, -0.6))}

        EventBus.subscribe('open_shop', lambda event_type, data: self.__shop_node.show())
        EventBus.subscribe('close_shop', lambda event_type, data: self.__shop_node.hide())
        EventBus.subscribe('discount', lambda event_type, data: self.__update_discount(data))

    def __update_discount(self, discount: float) -> None:
        if discount == 1:
            color = Vec4D(128 / 255, 64 / 255, 48 / 255, 1)
        elif discount < 1:
            color = Vec4D(128 / 255, 128 / 255, 48 / 255, 1)
        else:
            color = Vec4D(1, 64 / 255, 48 / 255, 1)
        for product in self.__products:
            product['text'] = f'x{round(product.getPythonTag("cost") * discount)}'
            product['text_fg'] = color

    def __create_products(self, type_tower: str, pos: Vec3) -> DirectFrame:
        SCALE: float = 0.075
        frame = DirectFrame(parent=self.__shop_frame,
                            frameSize=(0.25, -0.25, SCALE, -SCALE),
                            frameColor=(0.6, 0.6, 0.6, 1),
                            pos=pos,
                            text=f'x{ValueTowerConfig.get_products()[type_tower]['cost']}',
                            text_fg=Vec4D(128 / 255, 64 / 255, 48 / 255, 1),
                            text_pos=(0.25 - SCALE, -0.02),
                            text_scale=SCALE / 1.2,
                            text_align=TextNode.ACenter,
                            image='images2d/UI/money.png',
                            image_pos=(0.25 - SCALE, 0, 0),
                            image_scale=(SCALE / 1.2, 0, SCALE / 1.2))
        first_path = ValueTowerConfig.get_sprites_towers_foundations(type_tower)
        second_path = ValueTowerConfig.get_sprites_towers_guns(type_tower)
        DirectButton(image=self.__create_texture(first_path, second_path) if second_path else first_path,
                     parent=frame,
                     scale=SCALE,
                     pos=Vec3(-0.25 + SCALE * 1.2, 0),
                     command=lambda: EventBus.publish('buy_tower', type_tower),
                     frameColor=((0.5, 0.5, 0.5, 1),
                                 (0.7, 0.7, 0.7, 1),
                                 (0.3, 0.3, 0.3, 1)))
        frame.setTransparency(TransparencyAttrib.MAlpha)
        frame.setPythonTag('cost', ValueTowerConfig.get_products()[type_tower]['cost'])
        return frame

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