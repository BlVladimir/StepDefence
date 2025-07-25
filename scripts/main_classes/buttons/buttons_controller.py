from scripts.interface.i_button_controller import IButtonsController
from scripts.interface.i_context import IContext
from scripts.main_classes.interaction.render_manager import RenderManager
from scripts.main_classes.events.event_class import Event
from scripts.main_classes.buttons.button_class import Button
from scripts.main_classes.buttons.buttons_group import ButtonsGroup

from scripts.sprite.rect import Rect2D


class ButtonsController(IButtonsController):
    """Класс всех кнопок на сцене"""
    def __init__(self, render:RenderManager):
        height = render.win.get_y_size()
        width = render.win.get_x_size()
        if height / 2.5 > width / 4:
            button_level_scale = 1 / 4
            height /= width
            width = 1
        else:
            button_level_scale = 1 / 2.5
            width /= height
            height = 1
        self.__buttons_node = render.main_node2d.attachNewNode('button_node')

        main_menu_node = self.__buttons_node.attachNewNode('main_menu_buttons_node')
        self.__main_menu_group = ButtonsGroup(main_menu_node, Button(Rect2D(width / 2 - button_level_scale * 1.5 - height / 20, height / 2 - button_level_scale - height / 40, button_level_scale, button_level_scale, render.convert_coordinate), "images2d/UI/lvl/lvl1.png", main_menu_node, render, Event('change_scene', scene='1')),
            Button(Rect2D(width / 2 - button_level_scale / 2, height / 2 - button_level_scale - height / 40, button_level_scale, button_level_scale, render.convert_coordinate), "images2d/UI/lvl/lvl2.png", main_menu_node, render, Event('change_scene', scene='2')),
            Button(Rect2D(width / 2 + button_level_scale / 2 + height / 20, height / 2 - button_level_scale - height / 40, button_level_scale, button_level_scale, render.convert_coordinate), "images2d/UI/lvl/lvl3.png", main_menu_node, render, Event('change_scene', scene='3')),
            Button(Rect2D(width / 2 - button_level_scale * 1.5 - height / 20, height / 2 + height / 40, button_level_scale, button_level_scale, render.convert_coordinate), "images2d/UI/lvl/lvl4.png", main_menu_node, render, Event('change_scene', scene='4')),
            Button(Rect2D(width / 2 - button_level_scale / 2, height / 2 + height / 40, button_level_scale, button_level_scale, render.convert_coordinate), "images2d/UI/lvl/lvl5.png", main_menu_node, render, Event('change_scene', scene='5')),
            Button(Rect2D(width / 2 + button_level_scale / 2 + height / 20, height / 2 + height / 40, button_level_scale, button_level_scale, render.convert_coordinate), "images2d/UI/lvl/lvl6.png", main_menu_node, render, Event('change_scene', scene='6')))

        gameplay_buttons_node = render.main_node2d.attachNewNode('gameplay_buttons_node')
        self.__gameplay_group = ButtonsGroup(gameplay_buttons_node, Button(Rect2D(x=width/40, y=width/40, width=width/15, height=width/15, convert=render.convert_coordinate), "images2d/UI/exit_in_main_menu.png", gameplay_buttons_node, render, Event('change_scene', scene='main_menu')))
        self.__gameplay_group.hide()


    def action(self, context:IContext):
        match context.scene_controller.get_name_current_scene():
            case 'main_menu':
                if self.__main_menu_group.action(context):
                    return self.__main_menu_group.action(context)
            case 'gameplay':
                if self.__gameplay_group.action(context):
                    return self.__gameplay_group.action(context)
        return None

    def vision_control(self, context:IContext):
        match context.scene_controller.get_name_current_scene():
            case 'main_menu':
                self.__main_menu_group.show()
                self.__gameplay_group.hide()
            case 'gameplay':
                self.__main_menu_group.hide()
                self.__gameplay_group.show()