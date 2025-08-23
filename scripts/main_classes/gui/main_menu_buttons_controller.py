from direct.gui.DirectButton import DirectButton
from direct.gui.DirectFrame import DirectFrame
from panda3d.core import Vec3, NodePath, Texture, PNMImage, TextNode

from scripts.main_classes.gui.buttons_controller import ButtonsController
from scripts.main_classes.interaction.event_bus import EventBus
from scripts.main_classes.save_mng import SaveMng


class MainMenuButtonsController(ButtonsController):
    def __init__(self, relationship:float, buttons_node:NodePath):
        super().__init__(relationship , buttons_node)

        MMSC = 0.3

        self.__buttons_main_menu = []
        coords = [Vec3(-MMSC*2.4, MMSC*1.2), Vec3(0, MMSC*1.2), Vec3(MMSC*2.4, MMSC*1.2), Vec3(-MMSC*2.4, -MMSC*1.2), Vec3(0, -MMSC*1.2), Vec3(MMSC*2.4, -MMSC*1.2)]
        level = SaveMng.get_level()
        info = DirectFrame(parent=self._buttons_node,
                           pos=Vec3(0, 0, -0.9),
                           frameSize=(-0.1, 0.1, -0.1, 0.1),
                           frameColor=(0, 0, 0, 0),
                           text='Чтобы разблокировать следующий уровень, доживите до 40 волны предыдущего',
                           text_fg=(1, 1, 1, 1),
                           text_pos=(0, 0),
                           text_scale=0.05,
                           text_align=TextNode.ACenter)
        info.hide()
        for i, coord in enumerate(coords):
            self.__buttons_main_menu.append(DirectButton(image=f'images2d/UI/lvl/lvl{i + 1}.png' if i <= level else self.__get_dark_texture(f'images2d/UI/lvl/lvl{i + 1}.png'),
                                                  parent=self._buttons_node,
                                                  scale=MMSC,
                                                  pos=coord,
                                                  command=lambda lvl=i: EventBus.publish('change_scene', str(lvl)) if lvl <= level else info.show(),
                                                  frameColor=((0.5, 0.5, 0.5, 1),
                                                              (0.7, 0.7, 0.7, 1),
                                                              (0.3, 0.3, 0.3, 1))))

        EventBus.subscribe('change_scene', lambda event_type, data: info.hide())
        EventBus.subscribe('win', lambda event_type, data: self.unlock_next_level(data))

    def unlock_next_level(self, level)->None:
        self.__buttons_main_menu[level]['image'] = f'images2d/UI/lvl/lvl{level + 1}.png'
        self.__buttons_main_menu[level]['command'] = lambda lvl=level: EventBus.publish('change_scene', str(lvl))
        SaveMng.save(level)


    @staticmethod
    def __get_dark_texture(path:str)->Texture:
        img = PNMImage(path)
        k=0.6

        for x in range(img.getXSize()):
            for y in range(img.getYSize()):
                r, g, b= img.getRed(x, y), img.getGreen(x, y), img.getBlue(x, y)
                img.setXelA(x, y, r*k, g*k, b*k, 1)

        final_texture = Texture()
        final_texture.load(img)
        return final_texture