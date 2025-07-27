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

        w = render.win.getXSize()
        h = render.win.getYSize()

        MMSC = 0.3

        main_menu_node = self.__buttons_node.attachNewNode('main_menu_buttons_node')

        buttons_main_menu = []
        coords = [LVecBase3f(MMSC*2.4, MMSC*1.2), LVecBase3f(MMSC*2.4, -MMSC*1.2), LVecBase3f(0, MMSC*1.2), LVecBase3f(0, -MMSC*1.2), LVecBase3f(-MMSC*2.4, MMSC*1.2), LVecBase3f(-MMSC*2.4, -MMSC*1.2)]
        for i, coord in enumerate(coords):
            buttons_main_menu.append(DirectButton(image = f'images2d/UI/lvl/lvl{i+1}.png',
                                        parent=main_menu_node,
                                        scale = MMSC,
                                        pos = coord,
                                        command = lambda lvl=i: context.send_event(Event('change_scene', scene=str(lvl))),
                                        frameColor=((0.5, 0.5, 0.5, 1),
                                                    (0.7, 0.7, 0.7, 1),
                                                    (0.3, 0.3, 0.3, 1))))
        self.__main_menu_group = ButtonsGroup(main_menu_node, init_list=buttons_main_menu)

        gameplay_buttons_node = render.main_node2d.attachNewNode('gameplay_buttons_node')
        self.__gameplay_group = ButtonsGroup(gameplay_buttons_node, DirectButton(image = 'images2d/UI/exit_in_main_menu.png',
                                        parent=gameplay_buttons_node,
                                        scale = 0.1,
                                        pos = LVecBase3f(-w/h + (w/h)*0.075, 0.9),
                                        command = lambda: context.send_event(Event('change_scene', scene='main_menu')),
                                        frameColor=((0.5, 0.5, 0.5, 1),
                                        (0.7, 0.7, 0.7, 1),
                                        (0.3, 0.3, 0.3, 1))))
        self.__gameplay_group.hide()

    @staticmethod
    def click():
        print('click')

    def vision_control(self, context:IContext):
        match context.scene_controller.get_name_current_scene():
            case 'main_menu':
                self.__main_menu_group.show()
                self.__gameplay_group.hide()
            case 'gameplay':
                self.__main_menu_group.hide()
                self.__gameplay_group.show()