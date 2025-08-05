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

    def __str__(self):
        return f'[Damage: {self._damage}, Duration: {self._duration}]'

    def __add__(self, other:int):
        return Effect(self._damage + other, self._duration)