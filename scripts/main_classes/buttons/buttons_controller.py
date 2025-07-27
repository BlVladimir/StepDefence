from logging import debug

from direct.gui.DirectButton import DirectButton
from panda3d.core import LVecBase3f

from scripts.interface.i_button_controller import IButtonsController
from scripts.interface.i_context import IContext
from scripts.main_classes.interaction.render_manager import RenderManager
from scripts.main_classes.events.event_class import Event
from scripts.main_classes.buttons.buttons_group import ButtonsGroup

from scripts.sprite.rect import Rect2D


class ButtonsController(IButtonsController):
    """Класс всех кнопок на сцене"""
    def __init__(self, render:RenderManager, context:IContext):
        self.__buttons_node = render.main_node2d.attachNewNode('button_node')

        MMSC = 0.3

        main_menu_node = self.__buttons_node.attachNewNode('main_menu_buttons_node')

        buttons_main_menu = []
        coords = [LVecBase3f(MMSC*2.4, MMSC*1.2), LVecBase3f(MMSC*2.4, -MMSC*1.2), LVecBase3f(0, MMSC*1.2), LVecBase3f(0, -MMSC*1.2), LVecBase3f(-MMSC*2.4, MMSC*1.2), LVecBase3f(-MMSC*2.4, -MMSC*1.2)]
        for i, coord in enumerate(coords):
            buttons_main_menu.append(DirectButton(image = f'images2d/UI/lvl/lvl{i+1}.png',
                                        scale = MMSC,
                                        pos = coord,
                                        command = lambda lvl=i: context.send_event(Event('change_scene', scene=str(lvl))),
                                        pressEffect = False,
                                        frameColor=((0.5, 0.5, 0.5, 1),
                                                    (0.7, 0.7, 0.7, 1),
                                                    (0.3, 0.3, 0.3, 1))))
        self.__main_menu_group = ButtonsGroup(main_menu_node, init_list=buttons_main_menu)

        gameplay_buttons_node = render.main_node2d.attachNewNode('gameplay_buttons_node')
        # self.__gameplay_group = ButtonsGroup(gameplay_buttons_node, Button(Rect2D(x=width/40, y=width/40, width=width/15, height=width/15, convert=render.convert_coordinate), "images2d/UI/exit_in_main_menu.png", gameplay_buttons_node, render, Event('change_scene', scene='main_menu')))
        # self.__gameplay_group.hide()

    @staticmethod
    def click():
        print('click')

    def vision_control(self, context:IContext):
        match context.scene_controller.get_name_current_scene():
            case 'main_menu':
                self.__main_menu_group.show()
            case 'gameplay':
                self.__main_menu_group.hide()