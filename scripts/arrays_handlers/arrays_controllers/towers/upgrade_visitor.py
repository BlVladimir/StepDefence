
class UpgradeVisitor:
    """Visitor для улучшения башен"""
    def __init__(self, **parameters):
        self._parameters = parameters

    def visit_damage_state(self, damage_state:'DamageState')->None:
        for i in self._parameters.keys():
            damage_state.improve_damage(i, self._parameters[i])

    def visit_radius_strategy(self, radius_strategy:'AbstractRadiusState')->None:
        radius_strategy.multiply_radius(self._parameters['radius'])