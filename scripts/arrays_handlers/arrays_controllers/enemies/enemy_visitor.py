from logging import error
from typing import Dict


class EnemyVisitor:
    def __init__(self, **parameters):
        self._parameters = parameters

    def visit_damage_dict(self, characteristic_dict:Dict)->None:
        try:
            for parameter in self._parameters.keys():
                if self._parameters[parameter] > 0 or characteristic_dict[parameter] > 1:
                    characteristic_dict[parameter] += self._parameters[parameter]
        except KeyError:
            error('Parameter enemy visitor not in characteristic_dict')