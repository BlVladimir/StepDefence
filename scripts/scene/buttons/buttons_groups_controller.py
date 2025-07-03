# from scripts.configs.buttons_group import *
# from math import ceil
# from scripts.classes_objects.button_class import *
# from scripts.classes_objects.event_class import ButtonEvent
#
# class ButtonGroupController:
#     def __init__(self, width, height, sound_controller, config_gameplay):
#         if height / 2.5 > width / 4:
#             button_level_scale = ceil(width / 4)
#         else:
#             button_level_scale = ceil(height / 2.5)
#         self.__main_menu_group = ButtonsGroup((Button(width / 2 - button_level_scale * 1.5 - height / 20, height / 2 - button_level_scale - height / 40, "images/UI/lvl/lvl1.png", button_level_scale,
#                                                       button_level_scale, ButtonEvent('change_scene', scene='1')),
#                                                Button(width / 2 - button_level_scale / 2, height / 2 - button_level_scale - height / 40, "images/UI/lvl/lvl2.png", button_level_scale,
#                                                       button_level_scale, ButtonEvent('change_scene', scene='2')),
#                                                Button(width / 2 + button_level_scale / 2 + height / 20, height / 2 - button_level_scale - height / 40, "images/UI/lvl/lvl3.png", button_level_scale,
#                                                       button_level_scale, ButtonEvent('change_scene', scene='3')),
#                                                Button(width / 2 - button_level_scale * 1.5 - height / 20, height / 2 + height / 40, "images/UI/lvl/lvl4.png", button_level_scale, button_level_scale,
#                                                       ButtonEvent('change_scene', scene='4')),
#                                                Button(width / 2 - button_level_scale / 2, height / 2 + height / 40, "images/UI/lvl/lvl5.png", button_level_scale, button_level_scale,
#                                                       ButtonEvent('change_scene', scene='5')),
#                                                Button(width / 2 + button_level_scale / 2 + height / 20, height / 2 + height / 40, "images/UI/lvl/lvl6.png", button_level_scale, button_level_scale,
#                                                       ButtonEvent('change_scene', scene='6'))))
#
#         self.__settings_group = TextButtonsGroup((ButtonWithText(width // 2 - height // 10, height // 2 - height // 10, 'images/UI/setting_button.png', height // 5, height // 5,
#                                                                  ButtonEvent('using_additional_parameter_setting'),
#                                                                  'Additional parameter:' + str(config_gameplay.get_always_use_additional_parameters()), 'additional_parameter'),
#                                                   ButtonWithText(width // 2 - 1.5 * height // 5 - height // 7, height // 2 - height // 10, 'images/UI/setting_button.png', height // 5, height // 5,
#                                                                  ButtonEvent('sound_setting'), 'Play sound:' + str(sound_controller.get_play_sound()), 'sound'),
#                                                   ButtonWithText(width // 2 + height // 10 + height // 7, height // 2 - height // 10, 'images/UI/setting_button.png', height // 5, height // 5,
#                                                                  ButtonEvent('music_setting'), 'Play music:' + str(sound_controller.get_play_music()), 'music')))
#         self.__products_group = ButtonsGroup(
#             (ButtonWithText(20, 150, "images/tower/common_foundation.png", height * 0.1, height * 0.1, ButtonEvent('buy_tower', type='common'), 'x 3', 'common', (100, 0)),  # coordinate = (20, 150 + i * 120)
#              ButtonWithText(20, 270, "images/tower/sniper_foundation.png", height * 0.1, height * 0.1, ButtonEvent('buy_tower', type='sniper'), 'x 5', 'sniper', (100, 0)),
#              ButtonWithText(20, 390, "images/tower/anty_shield.png", height * 0.1, height * 0.1, ButtonEvent('buy_tower', type='anty_shield'), 'x 4', 'anty_shield', (100, 0)),
#              ButtonWithText(20, 510, "images/tower/venom_foundation.png", height * 0.1, height * 0.1, ButtonEvent('buy_tower', type='venom'), 'x 5', 'venom_foundation', (100, 0))))
#         self.__general_group = ChangeableButtonGroup({Button(width - 170 - height * 0.4, 20, "images/UI/exit.png", 150, 75, ButtonEvent('exit')): [],
#                                                     Button(150, 20, "images/UI/exit_in_main_menu.png", 100, 100, ButtonEvent('change_scene', scene='main_menu')): ['main_menu'],
#                                                     Button(20, 20, "images/UI/settings.png", 100, 100, ButtonEvent('change_scene', scene='setting')):['setting']})
#         self.__upgrade_group = ChangeableButtonGroup({Button(height * 0.02, height - 37 * height / 150, 'images/upgrade/1lvl.png', 0.16 * height, 0.16 * height, ButtonEvent('upgrade')):[2, 3],
#                                                       Button(height * 0.02, height - 37 * height / 150, 'images/upgrade/2lvl.png', 0.16 * height, 0.16 * height, ButtonEvent('upgrade')):[1, 3]})
#
#     def action(self, context):
#         match context.config_parameter_scene.get_scene():
#             case 'main_menu':
#                 if self.__main_menu_group.action():
#                     return self.__main_menu_group.action()
#             case 'setting':
#                 if self.__settings_group.action():
#                     return self.__settings_group.action()
#             case '1' | '2' | '3' | '4' | '5' | '6':
#                 if self.__products_group.action():
#                     return self.__products_group.action()
#                 if context.towers_array_controller.get_current_tower()and self.__upgrade_group.action(context.towers_array_controller.get_current_tower().get_level()):
#                     return self.__upgrade_group.action(context.towers_array_controller.get_current_tower().get_level())
#         if self.__general_group.action(context.config_parameter_scene.get_scene()):
#             return self.__general_group.action(context.config_parameter_scene.get_scene())
#         return None
#
#     def draw(self, context):
#         for i in (self.__main_menu_group, self.__settings_group, self.__products_group):
#             i.draw(context)
#             i.update(context)
#         self.__general_group.draw(context, context.config_parameter_scene.get_scene())
#         if context.towers_array_controller.get_current_tower():
#             self.__upgrade_group.draw(context, context.towers_array_controller.get_current_tower().get_level())
#
#     def change_buttons_active(self, context):
#         match context.config_parameter_scene.get_scene():
#             case 'main_menu':
#                 self.__main_menu_group.active = True
#                 self.__settings_group.active = False
#                 self.__products_group.active = False
#             case 'setting':
#                 self.__main_menu_group.active = False
#                 self.__settings_group.active = True
#                 self.__products_group.active = False
#             case '1' | '2' | '3' | '4' | '5' | '6':
#                 self.__main_menu_group.active = False
#                 self.__settings_group.active = False
#                 self.__products_group.active = False
#
#     def update_state(self, context):
#         self.__settings_group.change_text(additional_parameter='Additional parameter:' + str(context.config_gameplay.get_always_use_additional_parameters()),
#                                           sound='Play sound:' + str(context.sound_controller.get_play_sound()),
#                                           music='Play music:' + str(context.sound_controller.get_play_music()))
#
#     def activate_products_group(self):
#         self.__products_group.active = True
#
#     def deactivate_products_group(self):
#         self.__products_group.active = False