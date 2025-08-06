from logging import error
from typing import Dict


class EnemyVisitor:
    def __init__(self, **parameters):
        self._parameters = parameters

    def visit_damage_dict(self, characteristic_dict:Dict, health:int)->None:
        if 'health' in characteristic_dict.keys():
            health += self._parameters['health']
        try:
            for parameter in (key for key in self._parameters.keys() if key != 'health'):
                if self._parameters[parameter] > 0 or characteristic_dict[parameter] >1:
                    characteristic_dict[parameter] += self._parameters[parameter]
        except KeyError:
            error('Parameter enemy visitor not in characteristic_dict')