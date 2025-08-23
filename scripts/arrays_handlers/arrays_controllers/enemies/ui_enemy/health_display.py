from logging import debug

from panda3d.core import NodePath, TextNode


class HealthDisplay:
    def __init__(self, parent_node:NodePath, health:int):
        self.__SCALE = 0.4
        self.__text_node = TextNode('health_node')
        self.__text_node.setText(str(health))  # Задаем начальное значение текста
        self.__text_node.setTextColor(1, 1, 1, 1)  # Цвет текста (красный)
        self.__text_node.setAlign(TextNode.ACenter)

        self.__node_path = parent_node.attachNewNode(self.__text_node)  # Создаем ноду в сцене
        self.__node_path.setScale(self.__SCALE)  # Устанавливаем начальный масштаб
        min_pt, max_pt = self.__node_path.getTightBounds()

        debug(f'health_display: min_pt={min_pt}, max_pt={max_pt}, {-(max_pt.z - min_pt.z) * 0.5}')

        self.__node_path.setPos(0, -(max_pt.z + min_pt.z) * 0.5, 0)
        self.__node_path.setBillboardPointEye()  # Включаем биллбординг

    def update_health(self, health:int):
        self.__text_node.setText(str(health))


