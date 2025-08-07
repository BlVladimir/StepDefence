from direct.gui.DirectButton import DirectButton
from direct.gui.DirectFrame import DirectFrame
from panda3d.core import NodePath, Vec3, TransparencyAttrib

from scripts.main_classes.interaction.event_bus import EventBus


class UpgradeTable:
    def __init__(self, relationship:float, buttons_node:NodePath):
        self.__upgrade_table_node = buttons_node.attachNewNode('upgrade_table_node')
        self.__upgrade_table_node.hide()
        self.__upgrade_table_frame = DirectFrame(parent=self.__upgrade_table_node,
                                                 frameSize=(0, relationship * 0.5, -2, 0),
                                                 frameColor=(0.5, 0.5, 0.5, 1),
                                                 pos=Vec3(-relationship, 1))

        self.__button_upgrade = DirectButton(image='images2d/upgrade/1lvl.png',
                     parent=self.__upgrade_table_frame,
                     scale=0.2,
                     pos=Vec3(0.3, -1.7),
                     command=lambda: EventBus.publish('upgrade_tower'),
                     frameColor=((0.5, 0.5, 0.5, 1),
                                 (0.7, 0.7, 0.7, 1),
                                 (0.3, 0.3, 0.3, 1)))
        self.__button_upgrade.setTransparency(TransparencyAttrib.MAlpha)

        self.__images_list = ['images2d/upgrade/1lvl.png', 'images2d/upgrade/2lvl.png', 'images2d/upgrade/3lvl.png']

        EventBus.subscribe('open_upgrade_table', lambda event_type, data: self.__show(data))
        EventBus.subscribe('close_upgrade_table', lambda event_type, data: self.__upgrade_table_node.hide())
        EventBus.subscribe('update_upgrade_table', lambda event_type, data: self.__update_level(data))

    def __show(self, level:int):
        self.__button_upgrade['image'] = self.__images_list[level]
        self.__upgrade_table_node.show()

    def __update_level(self, level:int):
        self.__button_upgrade['image'] = self.__images_list[level]