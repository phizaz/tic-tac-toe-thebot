# this is a hack
# to import the tic-tac-toe game
import sys
import os
sys.path.append(os.path.abspath('../tic-tac-toe-thegame'))
from tictactoe import TicTacToe
# import the game from another project
import tictactoebot
import environment
import player

environment = environment.Environment(discount=0.5)
first_player = player.Player(name=1, epsilon=0.8, environment=environment)
second_player = player.Player(name=2, epsilon=0.8, environment=environment)
first_bot = tictactoebot.BotSimpleRL(environment=environment,
                                     player=first_player)
second_bot = tictactoebot.BotSimpleRL(environment=environment,
                                      player=second_player)

game = TicTacToe()


def game_state():
    # return the current game state
    state = [[None for i in range(3)] for i in range(3)]
    for i, row in enumerate(game.table):
        for j, col in enumerate(row):
            state[i][j] = col
    return state

# play the frist bot against the second bot, self learning !!
# the game should last .. long
# configurations
rounds = 100000
report = 1000
# play until ends
# the first bot makes move
whose_turn = 0
for round in range(rounds):
    # do the training
    # playing against each other
    # from the start
    # the players will alternatively begin
    game.restart(start=whose_turn+1)
    first_bot.restart()
    second_bot.restart()
    while not game.is_end():
        # keep playing
        # the first bot makes move
        current_bot = (first_bot, second_bot)[whose_turn]
        current_state = game_state()
        action = current_bot.take_turn(current_state)
        # next player comes into play
        whose_turn = (whose_turn + 1) % 2
        # if action is None:
        #     pass
        assert len(action) is 2
        game.turn(action)

        # game.display()

    # make the robot to learn something a bit
    # this will make the bots learn about the result of the game
    current_state = game_state()
    first_bot.take_turn(current_state)
    second_bot.take_turn(current_state)

    if round % report is 0:
        # make report
        print('round: ', round)
        print('bot 1: ', first_bot.expected_reward())
        print('tmp: ', first_bot.q_table[0])

# play with human
print('playing with human...')
game.restart(start=2)
first_bot.epsilon = 0.0
current_player = 1
while not game.is_end():
    if current_player is 1:
        # user
        action = (int(input('row: ')),
                  int(input('col: ')))
    else:
        # bot's turn
        current_state = game_state()
        action = first_bot.take_turn(current_state)
    game.turn(action)
    current_player = (current_player + 1) % 2
    # show the result
    game.display()
    pass
