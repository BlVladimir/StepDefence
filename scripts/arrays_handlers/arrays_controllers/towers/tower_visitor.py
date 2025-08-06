from logging import error
from typing import Dict


class TowerVisitor:
    """Visitor для улучшения башен"""
    def __init__(self, **parameters):
        self._parameters = parameters

    def visit_damage_dict(self, damage_dict:Dict)->None:
        try:
            for parameter in (key for key in self._parameters.keys() if key != 'radius'):
                if self._parameters[parameter] > 0 or damage_dict[parameter] >1:
                    damage_dict[parameter] += self._parameters[parameter]
        except KeyError:
            error('Parameter tower visitor not in damage_dict')


    def visit_radius_state(self, radius_strategy: 'AbstractRadiusState')->None:
        if 'radius' in self._parameters.keys():
            radius_strategy.multiply_radius(self._parameters['radius'])