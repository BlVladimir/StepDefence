from math import ceil

from scripts.main_classes.DTO.render import Render
from scripts.main_classes.events.event_class import Event
from scripts.scene.buttons.button_class import Button
from scripts.scene.buttons.buttons_group import ButtonsGroup

from panda3d.core import WindowProperties


class ButtonsController:
    """Класс всех кнопок на сцене"""
    def __init__(self, render:Render):
        pass
        # props = WindowProperties.get_p
        # if height / 2.5 > width / 4:
        #     button_level_scale = ceil(width / 4)
        # else:
        #     button_level_scale = ceil(height / 2.5)
        # self.__main_menu_group = ButtonsGroup((Button(width / 2 - button_level_scale * 1.5 - height / 20, height / 2 - button_level_scale - height / 40, "images/UI/lvl/lvl1.png", button_level_scale,
        #                                               button_level_scale, Event('change_scene', scene='1')),
        #                                        Button(width / 2 - button_level_scale / 2, height / 2 - button_level_scale - height / 40, "images/UI/lvl/lvl2.png", button_level_scale,
        #                                               button_level_scale, Event('change_scene', scene='2')),
        #                                        Button(width / 2 + button_level_scale / 2 + height / 20, height / 2 - button_level_scale - height / 40, "images/UI/lvl/lvl3.png", button_level_scale,
        #                                               button_level_scale, Event('change_scene', scene='3')),
        #                                        Button(width / 2 - button_level_scale * 1.5 - height / 20, height / 2 + height / 40, "images/UI/lvl/lvl4.png", button_level_scale, button_level_scale,
        #                                               Event('change_scene', scene='4')),
        #                                        Button(width / 2 - button_level_scale / 2, height / 2 + height / 40, "images/UI/lvl/lvl5.png", button_level_scale, button_level_scale,
        #                                               Event('change_scene', scene='5')),
        #                                        Button(width / 2 + button_level_scale / 2 + height / 20, height / 2 + height / 40, "images/UI/lvl/lvl6.png", button_level_scale, button_level_scale,
        #                                               Event('change_scene', scene='6'))))


    def action(self, context):
        match 'main_menu':
            case 'main_menu':
                if self.__main_menu_group.action():
                    return self.__main_menu_group.action()
        return None

if __name__=='__main__':
    print(WindowProperties.size())
