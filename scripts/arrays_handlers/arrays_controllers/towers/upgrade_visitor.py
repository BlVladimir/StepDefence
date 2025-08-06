from logging import error
from typing import Dict


class UpgradeVisitor:
    """Visitor для улучшения башен"""
    def __init__(self, **parameters):
        self._parameters = parameters

    def visit_damage_dict(self, damage_dict:Dict)->None:
        try:
            for parameter in self._parameters.keys():
                damage_dict[parameter] += self._parameters[parameter]
        except KeyError:
            error('Parameter upgrade visitor not in damage_dict')


    def visit_radius_state(self, radius_strategy: 'AbstractRadiusState')->None:
        radius_strategy.multiply_radius(self._parameters['radius'])