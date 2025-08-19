from logging import debug
from typing import List, Optional, Dict

from direct.gui.DirectButton import DirectButton
from direct.gui.DirectFrame import DirectFrame
from panda3d.core import NodePath, Vec3, TextNode, Vec4

from scripts.main_classes.gui.info.extra_info import ExtraInfo
from scripts.main_classes.gui.info.info_config import InfoConfig
from scripts.main_classes.gui.info.links import Links
from scripts.main_classes.interaction.event_bus import EventBus


class NewInfo:
    __extra_info_text: Optional[str] = None

    def __init__(self, buttons_node: NodePath):
        self.__info_node = buttons_node.attachNewNode('info_node')
        self.__info_node.hide()
        self.__info_frame = DirectFrame(parent=self.__info_node,
                                        frameColor=(0.5, 0.5, 0.5, 1),
                                        frameSize=(-0.5, -0.5, -0.5, 0.5),
                                        pos=Vec3(0, 0),
                                        text='',
                                        text_fg=(1, 1, 1, 1),
                                        text_pos=(0, 0),
                                        text_scale=0.1,
                                        text_align=TextNode.ACenter)

        self.__button_close = DirectButton(text='<X>',
                                           text_fg=Vec4(1, 1, 1, 1),
                                           parent=self.__info_frame,
                                           scale=0.1,
                                           pos=Vec3(0, 0, 0),
                                           command=lambda: self.__close_info(),
                                           frameColor=((0.5, 0.5, 0.5, 1),
                                                       (0.7, 0.7, 0.7, 1),
                                                       (0.3, 0.3, 0.3, 1)),
                                           text_align=TextNode.ACenter,
                                           frameSize=(-1, 1, -0.5, 0.5))
        InfoConfig.center_text(self.__button_close)
        self.__button_close.setPythonTag('scale', (0.2, 0.1))

        self.__extra_info = ExtraInfo(self.__info_node, self.__info_frame, self.__set_close_button)
        self.__links = Links(self.__info_frame)

        EventBus.subscribe('open_info', lambda event_type, data: self.__show_info(InfoConfig.get_obj_info(data[0], data[1])))
        EventBus.subscribe('change_scene', lambda event_type, data: self.__info_node.hide())

    def __close_info(self) -> None:
        EventBus.publish('resume_game')
        self.__info_node.hide()

    def __show_info(self, text: Dict[str, List[str]]) -> None:
        EventBus.publish('pause_game')
        self.__info_frame['text'] = f'{text['info'][0]}'
        self.__extra_info.hide_extra_info()
        if len(text['info']) == 2:
            min_pt, max_pt, xf, zf=InfoConfig.set_frame(self.__info_frame, bottom=0.2)
            self.__extra_info.show_button_extra_info(text['info'][1])
            self.__extra_info.set_button_extra_info(min_pt, max_pt, xf, zf)
        else:
            min_pt, max_pt, xf, zf=InfoConfig.set_frame(self.__info_frame)
        if 'links' in text.keys():
            self.__links.add_links(text['links'])
        self.__info_node.show()

        self.__set_close_button(max_pt, xf, zf)

    def __set_close_button(self, max_pt, xf, zf):
        scale_close = self.__button_close.getPythonTag('scale')
        self.__button_close.setPos(max_pt.x + 0.1 - xf - scale_close[0] / 2, 0,
                                   max_pt.z + 0.1 - zf - scale_close[1] / 2)
