# from pygame.sprite import Group
#
# class ButtonsGroup:
#     def __init__(self, sprites = None):
#         self.__button_group = Group()
#         if sprites:
#             for i in sprites:
#                 self.__button_group.add(i)
#         self.__active = True
#
#     def draw(self, context):
#         if self.__active:
#             self.__button_group.draw(context.config_parameter_scene.get_screen())
#             self.__button_group.update(context=context)
#
#     def action(self):
#         if self.__active:
#             for i in self.__button_group.sprites():
#                 if i.is_pressed():
#                     return i.is_pressed()
#         return False
#
#     def update(self, context):
#         if self.__active:
#             self.__button_group.update(context = context)
#
#     @property
#     def active(self):
#         raise PermissionError('privet attribute')
#
#     @active.setter
#     def active(self, value):
#         self.__active = bool(value)
#
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