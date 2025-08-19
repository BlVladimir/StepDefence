from direct.gui.DirectButton import DirectButton
from direct.gui.DirectFrame import DirectFrame
from panda3d.core import Vec3, TransparencyAttrib, NodePath, TextNode

from scripts.main_classes.gui.buttons_controller import ButtonsController
from scripts.main_classes.gui.buttons_group import ButtonsGroup
from scripts.main_classes.gui.gamplay_gui_parts.bugs_list import BugsList
from scripts.main_classes.gui.gamplay_gui_parts.shop import Shop
from scripts.main_classes.gui.gamplay_gui_parts.upgrade_table import UpgradeTable
from scripts.main_classes.gui.info.info import NewInfo
from scripts.main_classes.gui.info.info_config import InfoConfig
from scripts.main_classes.interaction.event_bus import EventBus


class GameplayButtonsController(ButtonsController):
    def __init__(self, relationship: float, buttons_node: NodePath):
        super().__init__(relationship, buttons_node)

        self.__gameplay_group = ButtonsGroup(self._buttons_node,
                                             DirectButton(image='images2d/UI/exit_in_main_menu.png',
                                                          parent=self._buttons_node,
                                                          scale=0.1,
                                                          pos=Vec3(self._relationship - 0.1,
                                                                   0.9),
                                                          command=lambda: EventBus.publish('change_scene', 'main_menu'),
                                                          frameColor=((0.5, 0.5, 0.5, 1),
                                                                      (0.7, 0.7, 0.7, 1),
                                                                      (0.3, 0.3, 0.3, 1)),
                                                          frameSize=(-1, 1, -1, 1)))
        self.__gameplay_group.hide()

        self.__shop = Shop(self._relationship, self._buttons_node)
        self.__upgrade_tablet = UpgradeTable(self._relationship, self._buttons_node)
        self.__bugs_list = BugsList(self._relationship, self._buttons_node)
        self.__info = NewInfo(self._buttons_node)

        self.__counter_node = self._buttons_node.attachNewNode('counter_node')
        money_frame = DirectFrame(parent=self.__counter_node,
                                  pos=Vec3(-self._relationship + 0.85, 0, 0.9),
                                  frameSize=(-0.25, 0.25, -0.1, 0.1),
                                  frameColor=(0, 0, 0, 0),
                                  text='x4',
                                  text_fg=(1, 1, 1, 1),
                                  text_pos=(0.05, 0),
                                  text_scale=0.1,
                                  text_align=TextNode.ACenter,
                                  image='images2d/UI/money.png',
                                  image_pos=(-0.18, 0, 0),
                                  image_scale=(0.1, 0, 0.1))

        wave_frame = DirectFrame(parent=self.__counter_node,
                                 pos=Vec3(-self._relationship + 1.35, 0, 0.9),
                                 frameSize=(-0.25, 0.25, -0.1, 0.1),
                                 frameColor=(0, 0, 0, 0),
                                 text='wave: 1',
                                 text_fg=(1, 1, 1, 1),
                                 text_pos=(0, 0),
                                 text_scale=0.1,
                                 text_align=TextNode.ACenter)
        money_frame.setTransparency(TransparencyAttrib.MAlpha)
        InfoConfig.center_text(money_frame)
        InfoConfig.center_text(wave_frame)
        EventBus.subscribe('update_money', lambda event_type, data: money_frame.setText(f'x{data}'))
        EventBus.subscribe('update_wave', lambda event_type, data: wave_frame.setText(f'wave: {data+1}'))