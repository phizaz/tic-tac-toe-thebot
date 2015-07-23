import math
import random

__author__ = 'phizaz'
# this is a hack
import sys
import os

sys.path.append(os.path.abspath('../../tic-tac-toe-thegame'))
from tictactoe import TicTacToe

# this bot uses reinforcement learning with q-value
# with table lookup
# assumed that the agent is deterministic
class BotSimpleRL:
    def __init__(self):
        # list of states
        self.states = None
        # start state
        # index of self.states
        self.init_state_idx = None
        # function that maps s -> list( (a, next_state_idx) )
        # note that the action show tell us what is the next state as well
        # if there is no action means terminate, the game is end
        self.action_fn = None
        # function that maps s, a -> r
        # in this case, it's deterministic
        self.reward_fn = None
        # discount value (gamma)
        self.discount = None
        # randomness for epsilon-greedy
        self.epsilon = None
        # initial value of each state, default should be 0
        self.q_init = None
        # used in learning process
        self.q_table = [None for each in self.states]
        # result of the learning
        self.optimal_policy = None

    def init_state(self, state_idx):
        # init the q_table of this state if never been initiated
        possible_actions = self.action_fn(self.states[state_idx])
        self.q_table[state_idx] = [self.q_init for each in possible_actions]

    def train(self, iterations, report=1000):
        # report for every 1000 iterations
        # train the bot
        next_alpha_fn = self.alpha_fn_maker(iterations)
        current_state_idx = self.init_state_idx
        for itr in range(iterations):
            # update the q table
            current_state = self.states[current_state_idx]
            action, action_idx, next_state_idx = self.next_action(current_state)

            if self.q_table[current_state_idx] is None:
                self.init_state(current_state_idx)

            # what if the next state has not been initiated yet ? init it!
            # retrieve the q_value of the next state, in the past
            if self.q_table[next_state_idx] is None:
                self.init_state(next_state_idx)
            q_next_state = self.q_table[next_state_idx]
            next_state_q_value = max([each for each in q_next_state])

            # take action and update the q_table
            q_state = self.q_table[current_state_idx]
            alpha = next_alpha_fn()
            reward = self.reward_fn(current_state, action)
            # temporal difference
            # update the current q state
            q_state[action_idx] = (1 - alpha) * q_state[action_idx] \
                                  + alpha * (reward + self.discount * next_state_q_value)

            if itr % report is 0:
                # report the progress
                print('itr: ', itr, ' exected_reward: ', self.expected_reward())
        self.optimal_policy = self.current_policy()
        return self.optimal_policy

    def test(self, rounds=1):
        # play with the real game, with a given round count
        # the result will be averaged
        pass

    def expected_reward(self):
        # return the expected_reward if starts with init state
        # the value is max of every q_value in that state
        return max(self.q_state[self.init_state_idx])

    def current_policy(self):
        # return current policy according to the q_table
        # policy is a list of actions for each state
        policy = [None for each in self.states]
        for state_number, q_state in enumerate(self.q_table):
            best_action_number = 0
            for action_number, q_value in enumerate(q_state):
                if q_value > q_state[best_action_number]:
                    best_action_number = action_number
            policy[state_number] = best_action_number
        return policy

    def alpha_fn_maker(self, iterations=None):
        # return the alpha value
        # this value should eventually converge
        # high at first, low at the end
        # it should be a function of number of iterations
        # what is the function though ? google this topic
        count = 1

        # generator function
        # returns: 1 / count
        def generator():
            nonlocal count
            count += 1
            return 1 / count

        # return as a function
        return generator

    def next_action(self, state):
        # return the next action gonna take
        # also calculate the epsilon greedy
        # exploration vs exploitation
        is_explore = self.binary_randomn(self.epsilon)

        if is_explore:
            return self.next_random_action(state)
        else:
            return self.next_policy_action(state)

    def binary_random(self, probability):
        # return true with given probability
        power = 1
        while math.floor(probability) != math.ceil(probability):
            probability *= 10
            power *= 10
        rand = random.randrange(power)
        return rand <= probability

    def next_random_action(self, state):
        # next random action
        # just random
        actions = self.action_fn(state)
        action_idx = random.randrange(len(actions))
        # return a random action
        action, next_state_idx = actions[action_idx]
        return action, action_idx, next_state_idx

    def next_policy_action(self, state):
        # best action according to the current policy
        # not from optimal policy (because it's not determined yet)
        # use the value from q_value table
        best_action_number = 0
        q_state = self.q_table[state]
        for action_number, q_value in q_state:
            if q_value > q_state[action_number]:
                best_action_number = action_number
        # return the best action according to the policy
        action, next_state_idx = self.action_fn(state)[best_action_number]
        action_idx = best_action_number
        return action, action_idx, next_state_idx
