import json
from environment import Environment

__author__ = 'phizaz'

class Tools:
    @staticmethod
    def source_file_name(bot_desc):
        return 'results/' +\
               bot_desc['name'] \
               + '-' \
               + str(bot_desc['exploratory']) \
               + '-' \
               + str(bot_desc['rounds'])\
               + '.txt'
    @staticmethod
    def load_source(bot_desc):
        filename = Tools.source_file_name(bot_desc)
        return json.load(open(filename, 'r'))
    @staticmethod
    def invert(q_table):
        env = Environment()
        result = [None for each in q_table]
        for state_idx, q_state in enumerate(q_table):
            state = env.dehasher(state_idx)
            for i, row in enumerate(state):
                for j, col in enumerate(row):
                    if col is 1:
                        state[i][j] = 2
                    elif col is 2:
                        state[i][j] = 1
            inverted_state_idx = env.hasher(state)
            result[inverted_state_idx] = q_state
        return result
    @staticmethod
    def cartesian_product(list_a, list_b):
        result = []
        for i in range(len(list_a)):
            for j in range(len(list_b)):
                result.append((list_a[i], list_b[j]))
        return result