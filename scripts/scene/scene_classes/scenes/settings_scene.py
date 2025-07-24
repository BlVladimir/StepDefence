from scripts.scene.scene_classes.scenes.abstract_scene import Scene
from scripts.interface.i_settings_scene import ISettingsScene

class SettingsScene(Scene, ISettingsScene):
    """Сцена настроек"""
    @staticmethod
    def name():
        return 'settings'