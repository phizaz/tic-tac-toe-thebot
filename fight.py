import json
import sys
import operator
import os
import environment
from player import Player
from tictactoebot import BotRLBetterDiscovery

sys.path.append(os.path.abspath('../tic-tac-toe-thegame'))
from tictactoe import TicTacToe

__author__ = 'phizaz'

def source_file_name(bot_desc):
    return 'results/' +\
           bot_desc['name'] \
           + '-' \
           + str(bot_desc['exploratory']) \
           + '-' \
           + str(bot_desc['rounds'])\
           + '.txt'

def load_source(bot_desc):
    filename = source_file_name(bot_desc)
    return json.load(open(filename, 'r'))

def invert(q_table):
    env = environment.Environment()
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

class Bot:
    def __init__(self, name, q_table):
        self.name = name
        self.q_table = q_table
        self.env = environment.Environment()
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

def fight(first_bot, second_bot):
    # the first bot begins
    game = TicTacToe()
    game.restart(start=first_bot.name)
    whose_turn = first_bot.name
    while True:
        if whose_turn is first_bot.name:
            action = first_bot.take_turn(game.table)
        else:
            action = second_bot.take_turn(game.table)
        game.turn(action)
        whose_turn = whose_turn % 2 + 1
        winner = game.winner()
        if winner is not None:
            return winner

def war(first_desc, second_desc, rounds=3):
    first_bot = Bot(name=1, q_table=load_source(first_desc))
    second_bot = Bot(name=2, q_table=invert(load_source(second_desc)))
    total = rounds * 2
    first_wins = 0
    draws = 0
    for i in range(rounds):
        print('game: ', i+1, 'of', rounds)
        for bot_a, bot_b in (
                (first_bot, second_bot),
                (second_bot, first_bot)
        ):
            res = fight(bot_a, bot_b)
            if res is first_bot.name:
                first_wins += 1
            elif res is -1:
                draws += 1
    return {
        'total': total,
        'first_wins': first_wins,
        'draws': draws,
        'second_wins': total - first_wins - draws
    }

def tournament(bots):
    bots_count = len(bots)
    score_board = [0 for i in range(bots_count)]
    total_wins = [0 for i in range(bots_count)]
    for i in range(bots_count):
        for j in range(i+1, bots_count):
            print('bot', i, 'vs', j)
            result = war(bots[i], bots[j])
            total_wins[i] += result['first_wins']
            total_wins[j] += result['second_wins']
            if result['first_wins'] > result['second_wins']:
                score_board[i] += 3
            elif result['second_wins'] < result['first_wins']:
                score_board[j] += 3
            else:
                score_board[i] += 1
                score_board[j] += 1
    result = [{'bot': bot, 'score': score_board[i], 'wins': total_wins[i]} for i, bot in enumerate(bots)]
    result.sort(key=lambda x: -x['score'])

    for rank, each in enumerate(result):
        print('rank: ', rank, 'score: ', each['score'], 'wins:', each['wins'])
        print('bot: ', each['bot'])

    return result

bots = (
    {
        'name': 'BotRLBetterDiscovery',
        'exploratory': 1,
        'rounds': 100000,
    }, {
        'name': 'BotRLBetterDiscovery',
        'exploratory': 10,
        'rounds': 100000,
    }, {
        'name': 'BotRLBetterDiscovery',
        'exploratory': 100,
        'rounds': 100000,
    }, {
        'name': 'BotRLBetterDiscovery',
        'exploratory': 1000,
        'rounds': 100000,
    },

    {
        'name': 'BotSimpleRL',
        'exploratory': 0.1,
        'rounds': 100000,
    }, {
        'name': 'BotSimpleRL',
        'exploratory': 0.2,
        'rounds': 100000,
    }, {
        'name': 'BotSimpleRL',
        'exploratory': 0.4,
        'rounds': 100000,
    }, {
        'name': 'BotSimpleRL',
        'exploratory': 0.6,
        'rounds': 100000,
    }, {
        'name': 'BotSimpleRL',
        'exploratory': 0.8,
        'rounds': 100000,
    }, {
        'name': 'BotSimpleRL',
        'exploratory': 1.0,
        'rounds': 100000,
    }
)

# print(war(first, second))
tournament(bots)