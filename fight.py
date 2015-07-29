import sys
import time
from mock.bot import Bot
from mock.tools import Tools
import os

sys.path.append(os.path.abspath('../tic-tac-toe-thegame'))
from tictactoe import TicTacToe

__author__ = 'phizaz'


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
    # this part shouldn't be reached
    return None


def timer(func, name='Unknown'):
    start_time = time.process_time()
    result = func()
    time_elapsed = time.process_time() - start_time
    print(name + 'time used:', time_elapsed)
    return result


def war(first_desc, second_desc, rounds=3):
    start_time = time.process_time()

    first_bot = Bot(name=1, q_table=Tools.load_source(first_desc))
    second_bot = Bot(name=2, q_table=Tools.invert(Tools.load_source(second_desc), second_desc))

    # this is for timing
    # def func():
    #     return Bot(name=1, q_table=Tools.load_source(first_desc))
    # first_bot = timer(func, 'first_bot')
    # def func():
    #     return Bot(name=2, q_table=Tools.invert(Tools.load_source(second_desc), second_desc))
    # second_bot = timer(func, 'second_bot')

    total = rounds * 2
    first_wins = 0
    draws = 0
    for i in range(rounds):
        print('game: ', i + 1, 'of', rounds)
        for bot_a, bot_b in (
                (first_bot, second_bot),
                (second_bot, first_bot)
        ):
            res = fight(bot_a, bot_b)
            if res is first_bot.name:
                first_wins += 1
            elif res is -1:
                draws += 1

    time_elapsed = time.process_time() - start_time
    print('war time used: ', time_elapsed)
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
    total_win_wars = [0 for i in range(bots_count)]
    total_lose_wars = [0 for i in range(bots_count)]
    total_wars = bots_count * (bots_count - 1) / 2
    total_fights = 3 * total_wars
    for j in range(bots_count):
        for i in range(j + 1, bots_count):
            print('bot', i, 'vs', j)
            result = war(bots[i], bots[j])
            total_wins[i] += result['first_wins']
            total_wins[j] += result['second_wins']
            if result['first_wins'] > result['second_wins']:
                score_board[i] += 3
                total_win_wars[i] += 1
                total_lose_wars[j] += 1
            elif result['second_wins'] < result['first_wins']:
                score_board[j] += 3
                total_win_wars[j] += 1
                total_lose_wars[i] += 1
            else:
                score_board[i] += 1
                score_board[j] += 1
    result = [{
                  'bot': bot,
                  'score': score_board[i],
                  'winning_rate': total_wins[i] / total_fights,
                  'total_win_wars': total_win_wars[i],
                  'total_lose_wars': total_lose_wars[i],
                  'total_draw_wars': total_wars - total_win_wars[i] - total_lose_wars[i],
              } for i, bot in enumerate(bots)]
    result.sort(key=lambda x: -x['score'])

    for rank, each in enumerate(result):
        print('rank: ', rank, 'score: ', each['score'])
        print('win_rate:', each['winning_rate'], 'won:', each['total_win_wars'], 'lost:', each['total_lose_wars'],
              'drew:', each['total_draw_wars'])
        print('bot: ', each['bot'])

    return result


bots = [
           {
               'name': 'BotSimpleRL',
               'rounds': rounds,
               'exploratory': exploratory
           } for rounds, exploratory in
           Tools.cartesian_product(
               [3 ** power * 10000 for power in range(0, 6)],
               [i / 10 for i in range(1, 10 + 1)]
           )
           ] + [
           {
               'name': 'BotRLBetterDiscovery',
               'rounds': rounds,
               'exploratory': exploratory
           } for rounds, exploratory in
           Tools.cartesian_product(
               [3 ** power * 10000 for power in range(0, 6)],
               [i / 10 for i in range(1, 10 + 1)]
           )
           ]

# print(war(first, second))
tournament(bots)
