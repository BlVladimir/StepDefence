from direct.gui.DirectButton import DirectButton
from direct.gui.DirectFrame import DirectFrame
from panda3d.core import NodePath, Vec3, TextNode, Vec4

from scripts.main_classes.gui.info.info_config import InfoConfig


class ExtraInfo:
    def __init__(self, info_node:NodePath, info_frame:DirectFrame):
        self.__extra_info_frame = DirectFrame(parent=info_node,
                                              frameSize=(1, -1, 1, -1),
                                              frameColor=(0.5, 0.5, 0.5, 1),
                                              pos=Vec3(0, 0),
                                              text='',
                                              text_fg=(1, 1, 1, 1),
                                              text_pos=(0, 0),
                                              text_scale=0.1,
                                              text_align=TextNode.ACenter)

        self.__button_extra_info = DirectButton(text='<more_info>',
                                                text_fg=Vec4(1, 1, 1, 1),
                                                parent=info_frame,
                                                scale=0.1,
                                                pos=Vec3(0, 0, 0),
                                                command=lambda: self.__show_more_info(),
                                                frameColor=((0.5, 0.5, 0.5, 1),
                                                           (0.7, 0.7, 0.7, 1),
                                                           (0.3, 0.3, 0.3, 1)),
                                                text_align=TextNode.ACenter,
                                                frameSize=(-3, 3, -0.5, 0.5))
        InfoConfig.center_text(self.__button_extra_info)
        self.__button_extra_info.setPythonTag('scale', (0.6, 0.1))
        self.__button_extra_info.hide()
