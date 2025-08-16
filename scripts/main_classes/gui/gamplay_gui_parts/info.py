from typing import Tuple

from direct.gui.DirectButton import DirectButton
from direct.gui.DirectFrame import DirectFrame
from panda3d.core import Vec3, NodePath, TextNode, Vec4D

from scripts.main_classes.gui.gamplay_gui_parts.info_config import InfoConfig
from scripts.main_classes.interaction.event_bus import EventBus


class Info:
    def __init__(self, buttons_node: NodePath):
        self.__info_node = buttons_node.attachNewNode('shop_node')
        self.__info_node.hide()
        self.__info_frame = DirectFrame(parent=self.__info_node,
                                        frameSize=(1, -1, 0.5, -0.5),
                                        frameColor=(0.5, 0.5, 0.5, 1),
                                        pos=Vec3(0, 0),
                                        text='',
                                        text_fg=(1, 1, 1, 1),
                                        text_pos=(0, 0.4),
                                        text_scale=0.1,
                                        text_align=TextNode.ACenter)

        DirectButton(text='<X>',
                     text_fg=Vec4D(1, 1, 1, 1),
                     parent=self.__info_frame,
                     scale=0.1,
                     pos=Vec3(0.9, 0.43),
                     command=lambda: self.__info_node.hide(),
                     frameColor=((0.5, 0.5, 0.5, 1),
                                 (0.7, 0.7, 0.7, 1),
                                 (0.3, 0.3, 0.3, 1)))
        EventBus.subscribe('open_info', lambda event_type, data:self.__show(InfoConfig.get_tower_info(data)))

    def __show(self, text: Tuple[str, str]) -> None:
        self.__info_frame['text'] = f'{text[0]}\nSpecific: {text[1]}'
        self.__info_node.show()




