from math import ceil

from scripts.main_classes.DTO.render import Render
from scripts.main_classes.events.event_class import Event
from scripts.scene.buttons.button_class import Button
from scripts.scene.buttons.buttons_group import ButtonsGroup

from panda3d.core import WindowProperties

from scripts.sprite.rect import Rect


class ButtonsController:
    """Класс всех кнопок на сцене"""
    def __init__(self, render:Render):
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
        buttons = (Button(Rect(width / 2 - button_level_scale * 1.5 - height / 20, height / 2 - button_level_scale - height / 40, button_level_scale, button_level_scale, render.convert_coordinate), "images2d/UI/lvl/lvl1.png", render, Event(
                'change_scene', scene='1')),
            Button(Rect(width / 2 - button_level_scale / 2, height / 2 - button_level_scale - height / 40, button_level_scale, button_level_scale, render.convert_coordinate), "images2d/UI/lvl/lvl2.png", render, Event('change_scene', scene='2')),
            Button(Rect(width / 2 + button_level_scale / 2 + height / 20, height / 2 - button_level_scale - height / 40, button_level_scale, button_level_scale, render.convert_coordinate), "images2d/UI/lvl/lvl3.png", render, Event('change_scene', scene='3')),
            Button(Rect(width / 2 - button_level_scale * 1.5 - height / 20, height / 2 + height / 40, button_level_scale, button_level_scale, render.convert_coordinate), "images2d/UI/lvl/lvl4.png", render, Event('change_scene', scene='4')),
            Button(Rect(width / 2 - button_level_scale / 2, height / 2 + height / 40, button_level_scale, button_level_scale, render.convert_coordinate), "images2d/UI/lvl/lvl5.png", render, Event('change_scene', scene='5')),
            Button(Rect(width / 2 + button_level_scale / 2 + height / 20, height / 2 + height / 40, button_level_scale, button_level_scale, render.convert_coordinate), "images2d/UI/lvl/lvl6.png", render, Event('change_scene', scene='6')))
        self.__main_menu_group = ButtonsGroup(buttons)


    def action(self, context):
        match 'main_menu':
            case 'main_menu':
                if self.__main_menu_group.action(context):
                    return self.__main_menu_group.action(context)
        return None

