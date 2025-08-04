class Effect:
    def __init__(self, damage: int, duration: int):
        self._damage = damage
        self._duration = duration

    @property
    def damage(self)->int:
        return self._damage

    def check_duration(self)->bool:
        return self._duration >0

    def decrease_duration(self)->None:
        self._duration -= 1

