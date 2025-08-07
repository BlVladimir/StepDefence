from logging import debug
from random import choice, getrandbits

from scripts.arrays_handlers.arrays_controllers.enemies.enemy_visitor import EnemyVisitor
from scripts.arrays_handlers.arrays_controllers.towers.tower_visitor import TowerVisitor


class RandomBug:
    def __init__(self, mediator:'MediatorControllers'):
        self.__bug_visitors = [TowerVisitor(basic_damage=1), TowerVisitor(basic_damage=-1),
                                  EnemyVisitor(health=1), EnemyVisitor(health=-1)]
        self.__bugs = {'damage', 'health', 'money', 'price'}
        self.__mediator = mediator

    def get_bug(self):
        type_bug = choice(list(self.__bugs))
        luck = getrandbits(1)
        debug(f'{type_bug}, {bool(luck)}')
        match type_bug:
            case 'damage':
                if luck:
                    self.__mediator.visit_all_towers(self.__bug_visitors[0])
                else:
                    self.__mediator.visit_all_towers(self.__bug_visitors[1])
            case 'health':
                if luck:
                    self.__mediator.visit_all_enemies(self.__bug_visitors[3])
                else:
                    self.__mediator.visit_all_enemies(self.__bug_visitors[2])
            case 'money':
                if luck:
                    self.__mediator.remove_money(-1)
                elif self.__mediator.money > 1:
                    self.__mediator.remove_money(1)
            case 'price':
                if luck:
                    self.__mediator.discount = 0.5
                else:
                    self.__mediator.discount = 2