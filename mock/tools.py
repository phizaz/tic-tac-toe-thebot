import json
from environment import Environment

__author__ = 'phizaz'


class Tools:
    invert_cache = {}
    filecache = {}

    @staticmethod
    def source_file_name(bot_desc):
        return 'results/' + \
               bot_desc['name'] \
               + '-' \
               + str(bot_desc['exploratory']) \
               + '-' \
               + str(bot_desc['rounds']) \
               + '.txt'

    @staticmethod
    def load_source(bot_desc):
        assert 'name' in bot_desc
        assert 'exploratory' in bot_desc
        assert 'rounds' in bot_desc
        bot_desc_idx = (bot_desc['name'], bot_desc['exploratory'], bot_desc['rounds'])
        if bot_desc_idx not in Tools.filecache:
            filename = Tools.source_file_name(bot_desc)
            result = Tools.filecache[bot_desc_idx] = json.load(open(filename, 'r'))
        else:
            result = Tools.filecache[bot_desc_idx]
        return result

        # filename = Tools.source_file_name(bot_desc)
        # return json.load(open(filename, 'r'))

    @staticmethod
    def invert(q_table, bot_desc=None):
        def do_invert():
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

        if bot_desc is not None:
            bot_desc_idx = (bot_desc['name'], bot_desc['exploratory'], bot_desc['rounds'])
            if bot_desc_idx not in Tools.invert_cache:
                result = Tools.invert_cache[bot_desc_idx] = do_invert()
            else:
                result = Tools.invert_cache[bot_desc_idx]
        else:
            result = do_invert()
        return result

    @staticmethod
    def cartesian_product(list_a, list_b):
        result = []
        for i in range(len(list_a)):
            for j in range(len(list_b)):
                result.append((list_a[i], list_b[j]))
        return result
