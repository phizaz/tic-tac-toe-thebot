from environment import Environment
import operator
from player import Player

__author__ = 'phizaz'

class Bot:
    def __init__(self, name, q_table):
        self.name = name
        self.q_table = q_table
        self.env = Environment()
        self.player = Player(name=name,
                             exploratory=0.0,
                             environment=self.env)

    def take_turn(self, state):
        state_idx = self.env.hasher(state)
        actions = self.player.actions(state)
        # print('state_idx: ', state_idx, 'state: ', state)
        # print('q_table: ', self.q_table[state_idx])
        best_action_idx, _ = max(enumerate(self.q_table[state_idx]), key=operator.itemgetter(1))
        # if best_action_idx >= len(actions):
        #     print('problem state: ', state, 'action_idx: ', best_action_idx, 'actions: ', actions)
        return actions[best_action_idx]