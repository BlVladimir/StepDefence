from logging import debug
from typing import Callable

from direct.gui.DirectButton import DirectButton
from direct.gui.DirectFrame import DirectFrame
from panda3d.core import NodePath, Vec3, TextNode, Vec4

from scripts.main_classes.gui.info.info_config import InfoConfig


class ExtraInfo:
    def __init__(self, info_node:NodePath, info_frame:DirectFrame, set_close_button_func:Callable):
        self.__info_frame = info_frame
        self.__extra_info_frame = DirectFrame(parent=info_node,
                                              frameSize=(1, -1, 1, -1),
                                              frameColor=(0.5, 0.5, 0.5, 1),
                                              pos=Vec3(0, 0),
                                              text='',
                                              text_fg=(1, 1, 1, 1),
                                              text_pos=(0, 0),
                                              text_scale=0.1,
                                              text_align=TextNode.ACenter)
        self.__extra_info_frame.hide()

        self.__button_extra_info = DirectButton(text='<more_info>',
                                                text_fg=Vec4(1, 1, 1, 1),
                                                parent=info_frame,
                                                scale=0.1,
                                                pos=Vec3(0, 0, 0),
                                                command=lambda: self.__but_extra_info_command(),
                                                frameColor=((0.5, 0.5, 0.5, 1),
                                                           (0.7, 0.7, 0.7, 1),
                                                           (0.3, 0.3, 0.3, 1)),
                                                text_align=TextNode.ACenter,
                                                frameSize=(-3, 3, -0.5, 0.5))
        InfoConfig.center_text(self.__button_extra_info)
        self.__button_extra_info.setPythonTag('scale', (0.6, 0.1))
        self.__button_extra_info.hide()

        self.__set_close_button_func = set_close_button_func

    def show_button_extra_info(self, text:str):
        self.__button_extra_info.show()
        self.__extra_info_frame['text'] = f'{text}'

    def set_button_extra_info(self, min_pt, max_pt, xf, zf):
        scale_extra_info = self.__button_extra_info.getPythonTag('scale')
        self.__button_extra_info.setPos((min_pt.x + max_pt.x - 2 * xf) / 2, 0,
                                       min_pt.z - 0.15 - zf + scale_extra_info[1] / 2)

    def hide_extra_info(self):
        self.__button_extra_info.hide()
        self.__extra_info_frame.hide()

    def __but_extra_info_command(self) -> None:
        if self.__extra_info_frame.isHidden():
            InfoConfig.set_frame(self.__extra_info_frame)
            self.__extra_info_frame.show()
            min_pt, max_pt, xf, zf=InfoConfig.set_frame(self.__info_frame, Vec3(0, 0, 0.4), bottom=0.2)
            InfoConfig.set_frame(self.__extra_info_frame, Vec3(0, 0, -0.4))
            debug('show more info')
        else:
            self.__extra_info_frame.hide()
            min_pt, max_pt, xf, zf=InfoConfig.set_frame(self.__info_frame, bottom=0.2)
            debug('hide more info')

        self.set_button_extra_info(min_pt, max_pt, xf, zf)
        self.__set_close_button_func(max_pt, xf, zf)



