from typing import Dict

from direct.gui.DirectFrame import DirectFrame
from panda3d.core import NodePath, Vec3, TextNode, Vec4

from scripts.main_classes.interaction.event_bus import EventBus


class BugsList:
    def __init__(self, relationship:float, buttons_node:NodePath):
        self.__bugs_list = buttons_node.attachNewNode('bugs_list')
        self.__bugs_list_frame = DirectFrame(parent=self.__bugs_list,
                                                 frameSize=(0.25, -0.25, 1, -1),
                                                 frameColor=(0.5, 0.5, 0.5, 0),
                                                 pos=Vec3(relationship - 0.25, 0))

        self.__bugs_list_node = self.__bugs_list_frame.attachNewNode('bugs_list_node')
        self.__frame_bug = DirectFrame(parent=self.__bugs_list_node,
                                       frameSize=(-0.25, 0.25, -0.1, 0.1),
                                       frameColor=(0, 0, 0, 0),
                                       text='',
                                       text_fg=(1, 1, 1, 1),
                                       text_pos=(0, -0.035),
                                       text_scale=0.06,
                                       text_align=TextNode.ACenter)
        self.__bugs_array = []

        self.__enemies_char_node = self.__bugs_list_frame.attachNewNode('enemies_char_node')
        self.__frame_char = DirectFrame(parent=self.__enemies_char_node,
                                        frameSize=(-0.25, 0.25, -0.1, 0.1),
                                        frameColor=(0, 0, 0, 0),
                                        text='',
                                        text_fg=(1, 1, 1, 1),
                                        text_pos=(0, 0),
                                        text_scale=0.06,
                                        text_align=TextNode.ACenter)
        self.__sequence_characteristic = ['health', 'armor', 'regen', 'poison', 'invisible', 'laser']

        EventBus.subscribe('update_bugs_list', lambda event_type, data: self.__redraw_bugs_list(data[0], data[1]))
        EventBus.subscribe('change_scene', lambda event_type, data: self.__clear_bugs_list())
        EventBus.subscribe('draw_enemy_characteristic', lambda event_type, data: self.__draw_characteristic(data))
        EventBus.subscribe('close_enemy_characteristic', lambda event_type, data: self.__close_characteristic())
        EventBus.subscribe('remove_discount', lambda event_type, data: self.__remove_discount())

    def __draw_characteristic(self, characteristic:Dict)->None:
        sorted_characteristic = dict(sorted(characteristic.items(), key=lambda x: self.__sequence_characteristic.index(x[0])))
        self.__enemies_char_node.getChildren().detach()
        for i, (char, value_char) in enumerate(sorted_characteristic.items()):
            self.__get_frame(self.__enemies_char_node,
                             self.__frame_char,
                             Vec4(1, 1, 1, 1),
                             f'{char}: {value_char}',
                             Vec3(0, 0.6 - 0.15 * i))

    def __close_characteristic(self):
        self.__enemies_char_node.getChildren().detach()

    def __redraw_bugs_list(self, bug: str, luck: bool):
        # Удаляем 'price' из основного массива, если он уже присутствует
        if bug == 'price':
            if self.__bugs_array and self.__bugs_array[0][0] == 'price':
                self.__bugs_array[0][1].detachNode()
                self.__bugs_array.pop(0)
            self.__bugs_array.insert(0, (bug, self.__get_frame(self.__bugs_list_node, self.__frame_bug, Vec4(0, 1, 0, 1) if luck else Vec4(1, 0, 0, 1), self.__get_text(bug, luck))))
        else:
            index = 1 if self.__bugs_array and self.__bugs_array[0][0] == 'price' else 0
            self.__bugs_array.insert(index, (bug, self.__get_frame(self.__bugs_list_node, self.__frame_bug, Vec4(0, 1, 0, 1) if luck else Vec4(1, 0, 0, 1), self.__get_text(bug, luck))))

        # Если слишком много элементов, удаляем последний
        if len(self.__bugs_array) > 4:
            self.__bugs_array[-1][1].detachNode()
            self.__bugs_array.pop(-1)

        # Пересчитываем позиции (не трогаем 'price', он всегда на первом месте)
        for i, frame in enumerate(self.__bugs_array[1:], start=1):  # Пропускаем 'price'
            frame[1].setPos(0, 0, -0.15 * i)

    def __clear_bugs_list(self):
        self.__bugs_list_node.getChildren().detach()
        self.__enemies_char_node.getChildren().detach()
        self.__bugs_array.clear()

    @staticmethod
    def __get_text(bug:str, luck:bool)->str:
        match bug:
            case 'damage' | 'money':
                if luck:
                    return f'{bug} +1'
                else:
                    return f'{bug} -1'
            case 'health':
                if luck:
                    return f'{bug} -1'
                else:
                    return f'{bug} +1'
            case 'price':
                if luck:
                    return f'{bug} /2'
                else:
                    return f'{bug} x2'
            case _:
                return bug

    @staticmethod
    def __get_frame(parent_node:NodePath, parent:DirectFrame, color:Vec4, text:str= 'how you see it?', pos:Vec3=Vec3(0, 0)):
        bug_frame = parent
        return DirectFrame(
            parent=parent_node,
            pos=pos,
            frameSize=bug_frame['frameSize'],
            frameColor=bug_frame['frameColor'],
            text = text,
            text_fg=color,
            text_pos=bug_frame['text_pos'],
            text_scale=bug_frame['text_scale'],
            text_align=TextNode.ACenter
        )

    def __remove_discount(self):
        if self.__bugs_array and 'price' == self.__bugs_array[0][0]:
            self.__bugs_array[0][1].detachNode()
            self.__bugs_array.pop(0)