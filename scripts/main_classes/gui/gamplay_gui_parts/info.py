from logging import error, debug
from typing import List

from direct.gui.DirectButton import DirectButton
from direct.gui.DirectFrame import DirectFrame
from panda3d.core import Vec3, NodePath, TextNode, Vec4D

from scripts.main_classes.gui.gamplay_gui_parts.info_config import InfoConfig
from scripts.main_classes.gui.text_func import center_text
from scripts.main_classes.interaction.event_bus import EventBus


class Info:
    def __init__(self, buttons_node: NodePath):
        self.__info_node = buttons_node.attachNewNode('shop_node')
        self.__info_node.hide()
        self.__info_frame = DirectFrame(parent=self.__info_node,
                                        frameSize=(1, -1, 1, -1),
                                        frameColor=(0.5, 0.5, 0.5, 1),
                                        pos=Vec3(0, 0),
                                        text='',
                                        text_fg=(1, 1, 1, 1),
                                        text_pos=(0, 0),
                                        text_scale=0.1,
                                        text_align=TextNode.ACenter)
        self.__more_info_frame = DirectFrame(parent=self.__info_node,
                                             frameSize=(1, -1, 1, -1),
                                             frameColor=(0.5, 0.5, 0.5, 1),
                                             pos=Vec3(0, 0),
                                             text='',
                                             text_fg=(1, 1, 1, 1),
                                             text_pos=(0, 0),
                                             text_scale=0.1,
                                             text_align=TextNode.ACenter)
        self.__more_info_frame.hide()

        self.__button_close = DirectButton(text='<X>',
                                           text_fg=Vec4D(1, 1, 1, 1),
                                           parent=self.__info_frame,
                                           scale=0.1,
                                           pos=Vec3(0, 0, 0),
                                           command=lambda: self.__close_info(),
                                           frameColor=((0.5, 0.5, 0.5, 1),
                                                       (0.7, 0.7, 0.7, 1),
                                                       (0.3, 0.3, 0.3, 1)),
                                           text_align=TextNode.ACenter,
                                           frameSize=(-1, 1, -0.5, 0.5))
        center_text(self.__button_close)
        self.__button_close.setPythonTag('scale', (0.2, 0.1))

        self.__button_more_info = DirectButton(text='<more_info>',
                                               text_fg=Vec4D(1, 1, 1, 1),
                                               parent=self.__info_frame,
                                               scale=0.1,
                                               pos=Vec3(0, 0, 0),
                                               command=lambda: self.__show_more_info(),
                                               frameColor=((0.5, 0.5, 0.5, 1),
                                                           (0.7, 0.7, 0.7, 1),
                                                           (0.3, 0.3, 0.3, 1)),
                                               text_align=TextNode.ACenter,
                                               frameSize=(-3, 3, -0.5, 0.5))
        center_text(self.__button_more_info)
        self.__button_more_info.setPythonTag('scale', (0.6, 0.1))
        self.__more_info_text:str = ''
        InfoConfig.load_config()

        EventBus.subscribe('open_info', lambda event_type, data:self.__show(InfoConfig.get_tower_info(data)))
        EventBus.subscribe('change_scene', lambda event_type, data:self.__info_node.hide())

    def __close_info(self) -> None:
        EventBus.publish('resume_game')
        self.__info_node.hide()

    def __show(self, text: List[str]) -> None:
        EventBus.publish('pause_game')
        self.__info_frame['text'] = f'{text[0]}'
        self.__more_info_text = text[1]
        self.__set_main_frame()
        self.__more_info_frame.hide()
        self.__info_node.show()

    def __show_more_info(self) -> None:
        if self.__more_info_frame.isHidden():
            self.__more_info_frame['text'] = f'{self.__more_info_text}'
            self.__more_info_frame.show()
            self.__set_main_frame(Vec3(0, 0, 0.4))
            self.__set_more_info(Vec3(0, 0, -0.4))
            debug('show more info')
        else:
            self.__more_info_frame.hide()
            self.__set_main_frame()
            debug('hide more info')
        
    @staticmethod
    def __set_frame(set_frame: DirectFrame, displacement_vec: Vec3 = Vec3(0, 0, 0), left=0.1, right=0.1, bottom=0.1, top=0.1):
        """
        Центрирует текст в measure_frame и устанавливает frameSize у set_frame
        по измеренным tight bounds. Возвращает (min_pt, max_pt, xf, zf).
        Логику расчётов не меняем: используем pos того фрейма, у которого берём bounds.
        """
        center_text(set_frame, displacement_vec)
        try:
            text = set_frame.component('text0')
        except KeyError:
            error('text not found')
            return None

        min_pt, max_pt = text.getTightBounds()
        vec_pos = set_frame['pos']
        xf, zf = vec_pos.x, vec_pos.z

        set_frame['frameSize'] = [
            min_pt.x - left - xf,
            max_pt.x + right - xf,
            min_pt.z - bottom - zf,
            max_pt.z + top - zf
        ]
        return min_pt, max_pt, xf, zf

    def __set_more_info(self, displacement_vec: Vec3 = Vec3(0, 0, 0)) -> None:
        self.__set_frame(self.__more_info_frame, displacement_vec)

    def __set_main_frame(self, displacement_vec: Vec3 = Vec3(0, 0, 0)) -> None:
        result = self.__set_frame(self.__info_frame, displacement_vec, bottom=0.2)
        if result is None:
            return
        min_pt, max_pt, xf, zf = result

        scale_close = self.__button_close.getPythonTag('scale')
        scale_more_info = self.__button_more_info.getPythonTag('scale')

        self.__button_close.setPos(max_pt.x + 0.1 - xf - scale_close[0] / 2, 0,
                                   max_pt.z + 0.1 - zf - scale_close[1] / 2)
        self.__button_more_info.setPos((min_pt.x + max_pt.x - 2 * xf) / 2, 0,
                                       min_pt.z - 0.15 - zf + scale_more_info[1] / 2)