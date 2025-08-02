from scripts.scene.scene_classes.scenes.abstract_scene import Scene


class MainMenuScene(Scene):
    """Сцена главного меню"""
    @staticmethod
    def name():
        return 'main_menu'