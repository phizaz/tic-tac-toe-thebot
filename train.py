# this is a hack
# to import the tic-tac-toe game
import concurrent.futures
import sys
import multiprocessing
import os

sys.path.append(os.path.abspath('../tic-tac-toe-thegame'))
from tictactoe import TicTacToe
# import the game from another project
import json
import time
import tictactoebot
import environment
import player

name = 'BotSimpleRL'
rounds = 100000
# bot = tictactoebot.BotRLBetterDiscovery
bot = tictactoebot.BotSimpleRL
# exploratories = [1, 10, 100, 1000, 10000]
exploratories = [1.0, 0.8, 0.6, 0.4, 0.2, 0.1]
num_workers = max(multiprocessing.cpu_count() // 2, 1)

print('training ', name, ' with exploratories:', exploratories)


def instance(bot, exploratory):
    print('starting exploratory : ', exploratory)
    start_time = time.process_time()
    env = environment.Environment(discount=1.0, q_init=0.5)
    first_player = player.Player(
        name=1,
        exploratory=exploratory,
        environment=env)
    second_player = player.Player(
        name=2,
        exploratory=exploratory,
        environment=env)
    first_bot = bot(
        environment=env,
        player=first_player)
    second_bot = bot(
        environment=env,
        player=second_player)

    game = TicTacToe()
    # play the first bot against the second bot, self learning !!
    # the game should last .. long
    # report every 1000 rounds
    report = 1000
    # play until ends
    # the first bot makes move, alternate this afterwards
    start_turn = first_bot.player.name
    for round in range(rounds):
        # do the training
        # playing against each other
        # from the start
        # the players will alternatively begin
        game.restart(start=start_turn)
        whose_turn = start_turn
        start_turn = start_turn % 2 + 1
        first_bot.restart()
        second_bot.restart()
        while not game.is_end():
            # keep playing
            # the first bot makes move
            if first_bot.player.name is whose_turn:
                current_bot = first_bot
            else:
                current_bot = second_bot
            current_state = game.table
            action = current_bot.take_turn(current_state)
            # next player comes into play
            whose_turn = whose_turn % 2 + 1
            game.turn(action)

        # make the robot to learn something a bit
        # this will make the bots learn about the result of the game
        current_state = game.table
        first_bot.take_turn(current_state)
        second_bot.take_turn(current_state)

        if round % report is 0:
            # make report
            print('exploratory : ', exploratory, 'percent: ', round / rounds * 100)

    # write the q_table into a file
    # only the fist_bot is important
    filename = 'results/' + name + '-' + str(exploratory) + '-' + str(rounds) + '.txt'
    print('saving into file:', filename)
    json.dump(first_bot.q_table, open(filename, 'w'))
    print('finished exploratory: ', exploratory, ' time: ', time.process_time() - start_time)
    return 0

with concurrent.futures.ProcessPoolExecutor(max_workers=num_workers) as executor:
    jobs = {}
    for exploratory in exploratories:
        jobs[executor.submit(instance, bot, exploratory)] = exploratory
    for job in concurrent.futures.as_completed(jobs):
        exploratory = jobs[job]
        res = job.result()
        print('res:', res)
        print('job exploratory: ', exploratory, ' has been finished!')
