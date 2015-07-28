from mock.bot import Bot
from mock.tools import Tools
import os
import sys

sys.path.append(os.path.abspath('../tic-tac-toe-thegame'))
from tictactoe import TicTacToe

__author__ = 'phizaz'

bot_desc = {
    'name': 'BotRLBetterDiscovery',
    'exploratory': 1,
    'rounds': 100000,
}

bot = Bot(name=1, q_table=Tools.load_source(bot_desc))
# bot starts first, but alternatively afterwards
start_turn = bot.name
while True:
    game = TicTacToe()
    game.restart(start=start_turn)
    whose_turn = start_turn
    start_turn = start_turn % 2 + 1
    print('game start : ')
    while True:
        if whose_turn is bot.name:
            # bot action
            action = bot.take_turn(game.table)
        else:
            # user action
            action = (int(input('row:')),
                      int(input('col:')))
        game.turn(action)
        game.display()
        whose_turn = whose_turn % 2 + 1
        winner = game.winner()
        if winner is not None:
            if winner is bot.name:
                print('bot won')
            else:
                print('you won')
            break
