from functools import partial
from typing import List

from direct.gui.DirectButton import DirectButton
from direct.gui.DirectFrame import DirectFrame
from panda3d.core import Vec4, Vec3, TextNode

from scripts.main_classes.gui.info.info_config import InfoConfig
from scripts.main_classes.interaction.event_bus import EventBus


class Links:
    def __init__(self, info_frame:DirectFrame):
        self.__info_frame = info_frame
        self.__buttons_link = [DirectButton(text='',
                                            text_fg=Vec4(1, 1, 1, 1),
                                            parent=self.__info_frame.parent,
                                            scale=0.1,
                                            pos=Vec3(i * 0.8, 0, -0.85),
                                            command=lambda: None,
                                            frameColor=((0.5, 0.5, 0.5, 1),
                                                        (0.7, 0.7, 0.7, 1),
                                                        (0.3, 0.3, 0.3, 1)),
                                            text_align=TextNode.ACenter,
                                            frameSize=(-2, 2, -0.5, 0.5)) for i in range(3)]
        for button in self.__buttons_link:
            button.hide()

    def add_links(self, links:List[str]):
        for i, button in enumerate(self.__buttons_link):
            if i < len(links):
                self.__set_button(self.__buttons_link[i], links[i])
            else:
                self.__buttons_link[i].hide()

    def clear_links(self):
        for button in self.__buttons_link:
            button.hide()

    @staticmethod
    def __set_button(button:DirectButton, texts:List[str]):
        button['text'] = ':\n'.join(texts)
        button['command'] = partial(EventBus.publish, 'open_info', texts)
        InfoConfig.center_text(button)

        text = button.component('text0')
        min_pt, max_pt = text.getTightBounds()

        width, height = (max_pt.x-min_pt.x)/2+0.1, (max_pt.z-min_pt.z)/2+0.1

        button['frameSize'] = (-width, width, -height, height)

        button.show()