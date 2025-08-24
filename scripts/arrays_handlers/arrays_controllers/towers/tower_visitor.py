from logging import error
from typing import Dict


class TowerVisitor:
    """Visitor для улучшения башен"""
    def __init__(self, **parameters):
        self._parameters = parameters

    def visit_damage_dict(self, damage_dict:Dict, min_damage:int)->None:
        try:
            for parameter in (key for key in self._parameters.keys() if key not in ['radius', 'basic_damage']):
                if self._parameters[parameter] > 0 or damage_dict[parameter] >1:
                    damage_dict[parameter] += self._parameters[parameter]
            if self._parameters.get('basic_damage', 0) > 0 or damage_dict['basic_damage'] + self._parameters['basic_damage'] > min_damage:
                damage_dict['basic_damage'] += self._parameters.get('basic_damage', 0)
            else :
                damage_dict['basic_damage'] = min_damage
        except KeyError:
            error('Parameter tower visitor not in damage_dict')

    def visit_radius_state(self, radius_strategy: 'AbstractRadiusState')->None:
        if 'radius' in self._parameters.keys():
            radius_strategy.multiply_radius(self._parameters['radius'])

    def get_dmg_change(self)->int:
        return self._parameters.get('basic_damage', 0)