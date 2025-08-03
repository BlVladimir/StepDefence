from direct.gui.DirectButton import DirectButton
from panda3d.core import Vec3, NodePath

from scripts.main_classes.buttons.buttons_controller import ButtonsController
from scripts.main_classes.buttons.buttons_group import ButtonsGroup
from scripts.main_classes.interaction.event_bus import EventBus


class MainMenuButtonsController(ButtonsController):
    def __init__(self, relationship:float, buttons_node:NodePath):
        super().__init__(relationship , buttons_node)

        MMSC = 0.3

        buttons_main_menu = []
        coords = [Vec3(-MMSC*2.4, MMSC*1.2), Vec3(0, MMSC*1.2), Vec3(MMSC*2.4, MMSC*1.2), Vec3(-MMSC*2.4, -MMSC*1.2), Vec3(0, -MMSC*1.2), Vec3(MMSC*2.4, -MMSC*1.2)]
        for i, coord in enumerate(coords):
            buttons_main_menu.append(DirectButton(image=f'images2d/UI/lvl/lvl{i + 1}.png',
                                                  parent=self._buttons_node,
                                                  scale=MMSC,
                                                  pos=coord,
                                                  command=lambda lvl=i: EventBus.publish('change_scene', str(lvl)),
                                                  frameColor=((0.5, 0.5, 0.5, 1),
                                                              (0.7, 0.7, 0.7, 1),
                                                              (0.3, 0.3, 0.3, 1))))
        self.__main_menu_group = ButtonsGroup(self._buttons_node, init_list=buttons_main_menu)