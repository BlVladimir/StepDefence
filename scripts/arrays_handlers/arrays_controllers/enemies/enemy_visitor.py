from logging import error
from typing import Dict


class EnemyVisitor:
    """Меняет характеристики врага"""
    def __init__(self, **parameters):
        self._parameters = parameters

    def visit_characteristic_dict(self, characteristic_dict:Dict)->None:
        try:
            for parameter in [key for key in self._parameters.keys() if key != 'invisible']:
                if self._parameters[parameter] > 0 or characteristic_dict[parameter] > 1:
                    characteristic_dict[parameter] += self._parameters[parameter]
        except KeyError:
            error('Parameter enemy visitor not in characteristic_dict')

    def visit_invisible_value(self, characteristic_dict:Dict)->None:
        if 'invisible' in self._parameters.keys():
            characteristic_dict['invisible'] = self._parameters['invisible'] if self._parameters['invisible'] != 'delete' else characteristic_dict.pop('invisible')