from typing import Dict

from direct.gui.DirectButton import DirectButton
from direct.gui.DirectFrame import DirectFrame
from direct.p3d.pdeploy import value
from panda3d.core import NodePath, Vec3, TransparencyAttrib, TextNode

from scripts.main_classes.interaction.event_bus import EventBus


class UpgradeTable:
    def __init__(self, relationship:float, buttons_node:NodePath):
        self.__upgrade_table_node = buttons_node.attachNewNode('upgrade_table_node')
        self.__upgrade_table_node.hide()
        self.__upgrade_table_frame = DirectFrame(parent=self.__upgrade_table_node,
                                                 frameSize=(relationship * 0.25, -relationship * 0.25, 1, -1),
                                                 frameColor=(0.5, 0.5, 0.5, 1),
                                                 pos=Vec3(-relationship*0.75, 0))

        self.__button_upgrade = DirectButton(image='images2d/upgrade/1lvl.png',
                     parent=self.__upgrade_table_frame,
                     scale=0.15*relationship,
                     pos=Vec3(0, -0.65),
                     command=lambda: EventBus.publish('upgrade_tower'),
                     frameColor=((0.5, 0.5, 0.5, 1),
                                 (0.7, 0.7, 0.7, 1),
                                 (0.3, 0.3, 0.3, 1)))
        self.__button_upgrade.setTransparency(TransparencyAttrib.MAlpha)

        self.__images_list = ['images2d/upgrade/1lvl.png', 'images2d/upgrade/2lvl.png', 'images2d/upgrade/3lvl.png']
        self.__sequence_characteristic = ['basic_damage', 'radius', 'armor_piercing', 'poison', 'additional_money']
        self.__frame_char = DirectFrame(parent=self.__upgrade_table_frame,
                                 frameSize=(-0.25 * relationship,
                                            0.25 * relationship, -0.1, 0.1),
                                 frameColor=(0, 0, 0, 0),
                                 text='',
                                 text_fg=(1, 1, 1, 1),
                                 text_pos=(0, -0.035),
                                 text_scale=0.15,
                                 text_align=TextNode.ACenter)
        EventBus.subscribe('open_upgrade_table', lambda event_type, data: self.__show(data))
        EventBus.subscribe('close_upgrade_table', lambda event_type, data: self.__upgrade_table_node.hide())
        EventBus.subscribe('update_upgrade_table', lambda event_type, data: self.__update_level(data))

    def __show(self, level:int):
        self.__button_upgrade['image'] = self.__images_list[level]
        self.__upgrade_table_node.show()

    def __update_level(self, level:int):
        self.__button_upgrade['image'] = self.__images_list[level]

    def __redraw_characteristic(self, characteristic:Dict):
        sorted_characteristic = dict(sorted(characteristic.items(), key=lambda x: self.__sequence_characteristic.index(x[0])))
        len_char = len(sorted_characteristic)
        for i, (char, value_char) in enumerate(sorted_characteristic.items()):
            pass

    def __get_frame(self, text:str='how you see it?', pos:Vec3=Vec3(0, 0)):
        base_frame = self.__frame_char
        return DirectFrame(
            parent=self.__upgrade_table_frame,
            pos=pos,
            frameSize=base_frame['frameSize'],
            frameColor=base_frame['frameColor'],
            text = text,
            text_fg=base_frame['text_fg'],
            text_pos=base_frame['text_pos'],
            text_scale=base_frame['text_scale'],
            text_align=base_frame['text_align']
        )




