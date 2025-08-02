from logging import debug

from direct.gui.DirectButton import DirectButton
from direct.gui.DirectFrame import DirectFrame
from panda3d.core import LVecBase3f, Texture, TransparencyAttrib, PNMImage

from scripts.interface.i_context import IContext
from scripts.main_classes.event_bus import EventBus
from scripts.main_classes.interaction.render_manager import RenderManager
from scripts.main_classes.buttons.buttons_group import ButtonsGroup


class ButtonsController:
    """Класс всех кнопок на сцене"""
    def __init__(self, render_manager:RenderManager, context:IContext):
        self.__buttons_node = render_manager.main_node2d.attachNewNode('button_node')

        w = render_manager.win.getXSize()
        h = render_manager.win.getYSize()

        MMSC = 0.3

        main_menu_node = self.__buttons_node.attachNewNode('main_menu_buttons_node')

        buttons_main_menu = []
        coords = [LVecBase3f(-MMSC*2.4, MMSC*1.2), LVecBase3f(0, MMSC*1.2), LVecBase3f(MMSC*2.4, MMSC*1.2), LVecBase3f(-MMSC*2.4, -MMSC*1.2), LVecBase3f(0, -MMSC*1.2), LVecBase3f(MMSC*2.4, -MMSC*1.2)]
        for i, coord in enumerate(coords):
            buttons_main_menu.append(DirectButton(image=f'images2d/UI/lvl/lvl{i + 1}.png',
                                                  parent=main_menu_node,
                                                  scale=MMSC,
                                                  pos=coord,
                                                  command=lambda lvl=i: EventBus.publish('change_scene', str(lvl)),
                                                  frameColor=((0.5, 0.5, 0.5, 1),
                                                              (0.7, 0.7, 0.7, 1),
                                                              (0.3, 0.3, 0.3, 1))))
        self.__main_menu_group = ButtonsGroup(main_menu_node, init_list=buttons_main_menu)

        gameplay_buttons_node = render_manager.main_node2d.attachNewNode('gameplay_buttons_node')
        self.__gameplay_group = ButtonsGroup(gameplay_buttons_node,
                                             DirectButton(image='images2d/UI/exit_in_main_menu.png',
                                                          parent=gameplay_buttons_node,
                                                          scale=0.1,
                                                          pos=LVecBase3f(-w / h + (w / h) * 0.075, 0.9),
                                                          command=lambda: EventBus.publish('change_scene', 'main_menu'),
                                                          frameColor=((0.5, 0.5, 0.5, 1),
                                                                      (0.7, 0.7, 0.7, 1),
                                                                      (0.3, 0.3, 0.3, 1))))
        self.__gameplay_group.hide()


        button_texture = self.__create_texture('images2d/tower/common_foundation.png', 'images2d/tower/common_gun.png')
        self.__shop_node = render_manager.main_node2d.attachNewNode('shop_node')
        self.__shop_frame = DirectFrame(parent=self.__shop_node,
                                        frameSize=(0, (w/h)*0.5, -2, 0),
                                        frameColor=(0.5, 0.5, 0.5, 1),
                                        pos=LVecBase3f(-w/h, 1))
        button_tower = DirectButton(image=button_texture,
                                    parent=self.__shop_frame,
                                    scale=0.2,
                                    pos=LVecBase3f(0.2, -0.2),
                                    command=lambda: EventBus.publish('buy_tower', 'basic'),
                                    frameColor=((0.5, 0.5, 0.5, 1),
                                                (0.7, 0.7, 0.7, 1),
                                                (0.3, 0.3, 0.3, 1)))
        button_tower.setTransparency(TransparencyAttrib.MAlpha)
        self.__shop_node.hide()

    def open_shop(self):
        self.__shop_node.show()

    def close_shop(self):
        self.__shop_node.hide()

    def vision_control(self, context:IContext):
        match context.scene_controller.get_name_current_scene():
            case 'main_menu':
                self.__main_menu_group.show()
                self.__gameplay_group.hide()
            case 'gameplay':
                self.__main_menu_group.hide()
                self.__gameplay_group.show()


    @staticmethod
    def __create_texture(first_path:str, second_path:str, xto:int=0, yto:int=0)->Texture:
        first_image = PNMImage(first_path)
        second_image = PNMImage(second_path)
        composed_image = PNMImage(first_image.getXSize(), first_image.getYSize())
        composed_image.copyFrom(first_image)

        for x in range(second_image.getXSize()):
            for y in range(second_image.getYSize()):
                r, g, b, a = second_image.getRed(x, y), second_image.getGreen(x, y), second_image.getBlue(x, y), second_image.getAlpha(x, y)
                if a > 0:
                    composed_image.setXelA(xto + x, yto + y, r, g, b, a)

        final_texture = Texture()
        final_texture.load(composed_image)
        return final_texture