from direct.gui.DirectButton import DirectButton
from direct.gui.DirectFrame import DirectFrame
from panda3d.core import Vec3, TransparencyAttrib, Texture, PNMImage, NodePath, TextNode

from scripts.main_classes.buttons.buttons_controller import ButtonsController
from scripts.main_classes.buttons.buttons_group import ButtonsGroup
from scripts.main_classes.buttons.gamplay_gui_parts.upgrade_table import UpgradeTable
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


        self.__shop_node = self._buttons_node.attachNewNode('shop_node')
        self.__shop_node.hide()
        self.__shop_frame = DirectFrame(parent=self.__shop_node,
                                        frameSize=(0, self._relationship * 0.5, -2, 0),
                                        frameColor=(0.5, 0.5, 0.5, 1),
                                        pos=Vec3(-self._relationship, 1))
        buttons_towers = {DirectButton(image=self.__create_texture('images2d/tower/common_foundation.png',
                                                                      'images2d/tower/common_gun.png'),
                                          parent=self.__shop_frame,
                                          scale=0.2,
                                          pos=Vec3(0.2, -0.2),
                                          command=lambda: EventBus.publish('buy_tower', 'basic'),
                                          frameColor=((0.5, 0.5, 0.5, 1),
                                                      (0.7, 0.7, 0.7, 1),
                                                      (0.3, 0.3, 0.3, 1))),
                          DirectButton(image=self.__create_texture('images2d/tower/sniper_foundation.png',
                                                                   'images2d/tower/sniper_gun.png'),
                                       parent=self.__shop_frame,
                                       scale=0.2,
                                       pos=Vec3(0.2, -0.5),
                                       command=lambda: EventBus.publish('buy_tower', 'sniper'),
                                       frameColor=((0.5, 0.5, 0.5, 1),
                                                   (0.7, 0.7, 0.7, 1),
                                                   (0.3, 0.3, 0.3, 1))),
                          DirectButton(image='images2d/tower/anty_shield.png',
                                       parent=self.__shop_frame,
                                       scale=0.2,
                                       pos=Vec3(0.2, -0.8),
                                       command=lambda: EventBus.publish('buy_tower', 'anty_shield'),
                                       frameColor=((0.5, 0.5, 0.5, 1),
                                                   (0.7, 0.7, 0.7, 1),
                                                   (0.3, 0.3, 0.3, 1))),
                          DirectButton(image=self.__create_texture('images2d/tower/venom_foundation.png',
                                                                   'images2d/tower/venom_gun.png'),
                                       parent=self.__shop_frame,
                                       scale=0.2,
                                       pos=Vec3(0.2, -1.1),
                                       command=lambda: EventBus.publish('buy_tower', 'venom'),
                                       frameColor=((0.5, 0.5, 0.5, 1),
                                                   (0.7, 0.7, 0.7, 1),
                                                   (0.3, 0.3, 0.3, 1)))

                          }

        for button in buttons_towers:
            button.setTransparency(TransparencyAttrib.MAlpha)
        EventBus.subscribe('open_shop', lambda event_type, data:  self.__shop_node.show())
        EventBus.subscribe('close_shop', lambda event_type, data: self.__shop_node.hide())

        self.__upgrade_tablet = UpgradeTable(self._relationship, self._buttons_node)

        self.__money_node = self._buttons_node.attachNewNode('money_node')
        frame = DirectFrame(parent=self.__money_node,
                            pos=Vec3(-self._relationship * 0.5, 0, 0.9),
                            frameSize=(-0.2 * self._relationship, 0.2 * self._relationship, -0.1, 0.1),
                            frameColor=(0, 0, 0, 0),
                            text='x4',
                            text_fg=(1, 1, 1, 1),
                            text_pos=(0.05 * self._relationship, -0.035),
                            text_scale=0.15,
                            text_align=TextNode.ACenter,
                            image='images2d/UI/money.png',
                            image_pos=(-0.125 * self._relationship, 0, 0),
                            image_scale=(0.1, 0, 0.1))
        frame.setTransparency(TransparencyAttrib.MAlpha)
        EventBus.subscribe('update_money', lambda event_type, data: frame.setText(f'x{data}'))

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