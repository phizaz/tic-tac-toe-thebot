# this is a hack
# to import the tic-tac-toe game
import concurrent.futures
import sys
import multiprocessing
from mock.tools import Tools
import os

sys.path.append(os.path.abspath('../tic-tac-toe-thegame'))
from tictactoe import TicTacToe
# import the game from another project
import json
import time
import tictactoebot
import environment
import player

num_workers = max(multiprocessing.cpu_count() // 2, 1)

experiments = [
                  {
                      'name': 'BotSimpleRL',
                      'bot': tictactoebot.BotSimpleRL,
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
                      'bot': tictactoebot.BotRLBetterDiscovery,
                      'rounds': rounds,
                      'exploratory': exploratory
                  } for rounds, exploratory in
                  Tools.cartesian_product(
                      [3 ** power * 10000 for power in range(0, 6)],
                      [i / 10 for i in range(1, 10 + 1)]
                  )
              ]

def instance(name, bot, exploratory, rounds):
    print('task: name:', name, 'bot:', bot, 'exploratory:', exploratory, 'rounds:', rounds)
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
    for task in experiments:
        name = task['name']
        bot = task['bot']
        exploratory = task['exploratory']
        rounds = task['rounds']
        jobs[executor.submit(instance, name, bot, exploratory, rounds)] = \
            name, bot, exploratory, rounds
    for job in concurrent.futures.as_completed(jobs):
        task = jobs[job]
        res = job.result()
        print('res:', res)
        print('task:', task, 'has been finished!')
