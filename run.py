# this is a hack
# to import the tic-tac-toe game
import sys
import os
# import the game from another project
import tictactoebot
import environment
import player

sys.path.append(os.path.abspath('../../tic-tac-toe-thegame'))
from tictactoe import TicTacToe

environment = environment.Environment()
first_player = player.Player(name=1)
second_player = player.Player(name=2)
first_bot = tictactoebot.BotSimpleRL(environment=environment,
                                     player=first_player)
second_bot = tictactoebot.BotSimpleRL(environment=environment,
                                      player=second_player)

game = TicTacToe()


def game_state():
    # return the current game state
    state = []
    for row in game.table:
        for col in row:
            state.append(col)
    return state

# play the frist bot against the second bot, self learning !!
# the game should last .. long
# configurations
rounds = 1000
report = 100
# play until ends
# the first bot makes move
whose_turn = 0
for round in range(rounds):
    # do the training
    # playing against each other
    # from the start
    # the players will alternatively begin
    game.restart(start=whose_turn+1)
    while not game.is_end():
        # keep playing
        # the first bot makes move
        current_bot = (first_bot, second_bot)[whose_turn]
        current_state = game_state()
        action = current_bot.take_turn(current_state)
        # next player comes into play
        whose_turn = (whose_turn + 1) % 2
        assert len(action) is 2
        game.turn(action)

    # make the robot to learn something a bit
    # this will make the bots learn about the result of the game
    current_state = game_state()
    first_bot.take_turn(current_state)
    second_bot.take_turn(current_state)

    if round % report is 0:
        # make report
        print('round: ', round)
        print('bot 1: ', first_bot.expected_reward())
        print('bot 2: ', second_bot.expected_reward())
