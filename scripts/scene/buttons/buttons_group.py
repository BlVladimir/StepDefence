from typing import Tuple

from scripts.scene.buttons.button_class import Button
from scripts.sprite.sprites_group import SpritesGroup


class ButtonsGroup:
    def __init__(self, sprites:Tuple[Button]):
        self.__button_group = SpritesGroup()
        if sprites:
            for sprite in sprites:
                self.__button_group.add(sprite)

    def action(self, context):
        for i in self.__button_group.sprites():
            if i.is_pressed(context):
                return i.is_pressed(context)
        return False

# class TextButtonsGroup(ButtonsGroup):
#     def __init__(self, sprites = None):
#         super().__init__(sprites)
#         self.__button_group = Group()
#         if sprites:
#             for i in sprites:
#                 self.__button_group.add(i)
#
#     def change_text(self, **kwargs):
#         sprites = self.__button_group.sprites()
#         for i in range(len(sprites)):
#             if sprites[i].name in kwargs.keys():
#                 self.__button_group.sprites()[i].text = kwargs[sprites[i].name]
#
# class ChangeableButtonGroup:
#     def __init__(self, sprites_dict=None):
#         self.__button_group = Group()
#         self.__buttons_dict = sprites_dict  # объекты кнопок, встречающихся везде
#         for i in self.__buttons_dict.keys():
#             self.__button_group.add(i)
#
#     def __get_sprites(self, parameter):
#         returning_group = self.__button_group.copy()
#         for i in self.__buttons_dict.keys():
#             if parameter in self.__buttons_dict[i]:
#                 returning_group.remove(i)
#         return returning_group
#
#     def draw(self, context, parameter):
#         self.__get_sprites(parameter).draw(context.config_parameter_scene.get_screen())
#         self.__get_sprites(parameter).update(context)
#
#     def action(self, parameter):
#         for i in self.__get_sprites(parameter):
#             if i.is_pressed():
#                 return i.is_pressed()