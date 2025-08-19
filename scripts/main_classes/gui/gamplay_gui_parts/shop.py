from direct.gui.DirectButton import DirectButton
from direct.gui.DirectFrame import DirectFrame
from panda3d.core import NodePath, TransparencyAttrib, Vec3, Texture, PNMImage, TextNode, Vec4D

from scripts.arrays_handlers.arrays_controllers.towers.tower_config import TowerConfig
from scripts.main_classes.gui.info.info_config import InfoConfig
from scripts.main_classes.interaction.event_bus import EventBus


class Shop:
    def __init__(self, relationship: float, buttons_node: NodePath):
        self.__shop_node = buttons_node.attachNewNode('shop_node')
        self.__shop_node.hide()
        self.__shop_frame = DirectFrame(parent=self.__shop_node,
                                        frameSize=(0.25, -0.25, 1, -1),
                                        frameColor=(0.5, 0.5, 0.5, 0),
                                        pos=Vec3(-relationship + 0.25, 0))

        START_Y = 0.87
        STEP = -0.25
        self.__products = set([self.__create_products(type_tower, Vec3(0, START_Y + STEP * i)) for i, type_tower in
                               enumerate(TowerConfig.get_all_towers_name())])

        EventBus.subscribe('open_shop', lambda event_type, data: self.__shop_node.show())
        EventBus.subscribe('close_shop', lambda event_type, data: self.__shop_node.hide())
        EventBus.subscribe('discount', lambda event_type, data: self.__update_discount(data))
        EventBus.subscribe('change_scene', lambda event_type, data: self.__shop_node.hide())

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
        SCALE: float = 0.09
        frame = DirectFrame(parent=self.__shop_frame,
                            frameSize=(0.25, -0.25, SCALE, -SCALE),
                            frameColor=(0.6, 0.6, 0.6, 1),
                            pos=pos,
                            text=f'x{TowerConfig.get_cost(type_tower)}',
                            text_fg=Vec4D(128 / 255, 64 / 255, 48 / 255, 1),
                            text_pos=(-0.25 + SCALE * 3, 0),
                            text_scale=SCALE / 1.2,
                            text_align=TextNode.ACenter,
                            image='images2d/UI/money.png',
                            image_pos=(-0.25 + SCALE * 3, 0, 0),
                            image_scale=(SCALE / 1.2, 0, SCALE / 1.2))
        InfoConfig.center_text(frame)
        first_path = TowerConfig.get_image_foundation(type_tower)
        second_path = TowerConfig.get_image_gun(type_tower)
        DirectButton(image=self.__create_texture(first_path, second_path) if second_path else first_path,
                     parent=frame,
                     scale=SCALE,
                     pos=Vec3(-0.25 + SCALE * 1.2, 0),
                     command=lambda: EventBus.publish('buy_tower', type_tower),
                     frameColor=((0.5, 0.5, 0.5, 1),
                                 (0.7, 0.7, 0.7, 1),
                                 (0.3, 0.3, 0.3, 1)))
        but_info = DirectButton(text='<i>',
                                text_fg=Vec4D(1, 1, 1, 1),
                                parent=frame,
                                scale=SCALE / 2,
                                pos=Vec3(0.25 - SCALE, 0),
                                command=lambda: EventBus.publish('open_info', ['tower', type_tower]),
                                text_align=TextNode.ACenter,
                                frameColor=((0.5, 0.5, 0.5, 1),
                                            (0.7, 0.7, 0.7, 1),
                                            (0.3, 0.3, 0.3, 1)),
                                frameSize=(-1, 1, -1, 1))
        InfoConfig.center_text(but_info)
        frame.setTransparency(TransparencyAttrib.MAlpha)
        frame.setPythonTag('cost', TowerConfig.get_cost(type_tower))
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