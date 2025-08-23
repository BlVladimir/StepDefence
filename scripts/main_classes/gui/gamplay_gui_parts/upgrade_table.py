from logging import debug
from typing import Dict

from direct.gui.DirectButton import DirectButton
from direct.gui.DirectFrame import DirectFrame
from panda3d.core import NodePath, Vec3, TransparencyAttrib, TextNode, Vec4D, Vec4

from scripts.arrays_handlers.arrays_controllers.towers.tower import Tower
from scripts.arrays_handlers.arrays_controllers.towers.tower_config import TowerConfig
from scripts.main_classes.gui.info.info_config import InfoConfig
from scripts.main_classes.interaction.event_bus import EventBus


class UpgradeTable:
    """Рамка с улучшениями и характеристиками башни"""
    def __init__(self, relationship:float, buttons_node:NodePath):
        self.__upgrade_table_node = buttons_node.attachNewNode('upgrade_table_node')
        self.__upgrade_table_node.hide()
        self.__upgrade_table_frame = DirectFrame(parent=self.__upgrade_table_node,
                                                 scale=1,
                                                 frameSize=(0.25, -0.25, 1, -1),
                                                 frameColor=(0.5, 0.5, 0.5, 0),
                                                 pos=Vec3(-relationship + 0.25, 0))

        self.__discount = 1
        self.__frame = DirectFrame(parent=self.__upgrade_table_frame,
                            frameSize=(-0.25, 0.25, -0.15, 0.15),
                            pos=(0, 0, -0.75),
                            frameColor=(0, 0, 0, 0),
                            text=f'x0',
                            text_fg=Vec4D(128 / 255, 64 / 255, 48 / 255, 1),
                            text_pos=(0.175, 0),
                            text_scale=0.075,
                            text_align=TextNode.ACenter,
                            image='images2d/UI/money.png',
                            image_pos=(0.175, 0, 0),
                            image_scale=(0.075, 0, 0.075))
        InfoConfig.center_text(self.__frame)
        self.__button_upgrade = DirectButton(image='images2d/upgrade/1lvl.png',
                                             parent=self.__frame,
                                             scale=0.15,
                                             pos=Vec3(-0.075, 0),
                                             command=lambda: EventBus.publish('upgrade_tower'),
                                             frameColor=((0.5, 0.5, 0.5, 1),
                                                         (0.7, 0.7, 0.7, 1),
                                                         (0.3, 0.3, 0.3, 1)))
        self.__frame.setTransparency(TransparencyAttrib.MAlpha)
        self.__frame.setPythonTag('price', 0)

        self.__images_list = ['images2d/upgrade/1lvl.png', 'images2d/upgrade/2lvl.png', 'images2d/upgrade/3lvl.png']
        self.__sequence_characteristic = ['basic_damage', 'radius', 'armor_piercing', 'poison', 'additional_money', 'vision', 'laser']
        self.__characteristic_node = self.__upgrade_table_frame.attachNewNode('characteristic_node')

        self.__char_frames = [DirectFrame(parent=self.__characteristic_node,
                                          text='',
                                          text_fg=Vec4(1, 1, 1, 1),
                                          text_align=TextNode.ALeft,
                                          scale=1,
                                          text_scale=0.1,
                                          pos=Vec3(-0.2, 0, 0.2 - 0.2 * i),
                                          frameSize=(0, 0.5, -0.1, 0.1),
                                          frameColor=Vec4(1, 0, 0, 0)) for i in range(6)]

        EventBus.subscribe('using_tower', lambda event_type, data: self.__show(data[0], data[1], data[2]))
        EventBus.subscribe('not_using_tower', lambda event_type, data: self.__upgrade_table_node.hide())
        EventBus.subscribe('change_scene', lambda event_type, data: self.__clear_characteristic())
        EventBus.subscribe('discount', lambda event_type, data: self.__update_discount(data))


    def __update_discount(self, discount: float) -> None:
        self.__discount = discount
        if discount == 1:
            color = Vec4D(128 / 255, 64 / 255, 48 / 255, 1)
        elif discount < 1:
            color = Vec4D(128 / 255, 128 / 255, 48 / 255, 1)
        else:
            color = Vec4D(1, 64 / 255, 48 / 255, 1)
        self.__frame['text_fg'] = color
        self.__frame['text'] = f'x{round(self.__frame.getPythonTag('price') * discount)}'


    def __clear_characteristic(self):
        """Очищает характеристики"""
        for frame in self.__char_frames:
            frame['text'] = ''

    def __show(self, tower:Tower, level:int, characteristic:Dict):
        """Открывает рамку"""
        type_tower = tower.type_tower
        self.__button_upgrade['image'] = self.__images_list[level]
        self.__redraw_characteristic(characteristic)
        if level < 2:
            price = TowerConfig.get_improve_cost_array(type_tower)[level]
            self.__frame.setPythonTag('price', price)
            self.__frame['text'] = f'x{round(price * self.__discount)}'
        else:
            self.__frame.setPythonTag('price', 0)
            self.__frame['text'] = ''

        self.__upgrade_table_node.show()

    def __redraw_characteristic(self, characteristic:Dict):
        """Создает объекты, отображающие характеристику башни"""
        debug(characteristic)
        sorted_characteristic = dict(sorted(characteristic.items(), key=lambda x: self.__sequence_characteristic.index(x[0])))
        self.__clear_characteristic()
        for i, (char, value_char) in enumerate(sorted_characteristic.items()):
            self.__char_frames[i]['text'] = f'{' '.join(char.split('_'))}:\n{value_char}'
            InfoConfig.center_text(self.__char_frames[i])