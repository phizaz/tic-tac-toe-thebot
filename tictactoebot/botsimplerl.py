import math
import random
from environment import Environment
from player import Player

__author__ = 'phizaz'

# this bot uses reinforcement learning with q-value
# with table lookup
# assumed that the agent is deterministic
class BotSimpleRL:
    def __init__(self,
                 environment,
                 player):
        assert isinstance(environment, Environment)
        assert isinstance(player, Player)
        # list of states, and start state
        self.state_count, self.init_state_idx = environment.states()
        assert isinstance(self.state_count, int)
        assert isinstance(self.init_state_idx, int)
        # hasher, encode state to int
        self.hasher = environment.hasher
        assert hasattr(self.hasher, '__call__')
        self.dehasher = environment.dehasher
        assert hasattr(self.dehasher, '__call__')
        # function that maps s -> list(a)
        # if there is no action means terminate, the game is end
        self.action_fn = player.actions
        assert hasattr(self.action_fn, '__call__')
        # function that maps s, a -> r
        # in this case, it's deterministic
        self.reward_fn = player.reward
        assert hasattr(self.reward_fn, '__call__')
        self.is_termination = player.is_termination
        assert hasattr(self.is_termination, '__call__')
        # discount value (gamma)
        self.discount = environment.discount
        assert isinstance(self.discount, float)
        # randomness for epsilon-greedy
        self.epsilon = player.epsilon
        assert isinstance(self.epsilon, float)
        # initial value of each state, default should be 0
        self.q_init = environment.q_init
        assert isinstance(float(self.q_init), float)
        # used in learning process
        self.q_table = [None for each in range(self.state_count)]
        # result of the learning
        self.optimal_policy = None
        self.alpha = self.alpha_fn_maker()

        # used in take_turn()
        self.first_turn = True
        self.last_state_idx = None
        self.last_action_idx = None
        self.last_reward = None
        self.last_alpha = None

    def restart(self):
        # the environment has been reset
        self.first_turn = True
        self.last_state_idx = None
        self.last_action_idx = None
        self.last_reward = None
        self.last_alpha = None

    def init_q_state(self, state_idx):
        assert isinstance(state_idx, int)
        # init the q_table of this state if never been initiated
        possible_actions = self.action_fn(self.dehasher(state_idx))
        self.q_table[state_idx] = [self.q_init for each in possible_actions]

    # return the optimal policy, actually it's not optimal but the best that can be achieved
    def take_turn(self, current_state):
        assert isinstance(current_state, list)

        # init_the current state if not
        current_state_idx = self.hasher(current_state)
        is_termination, termination_reward = self.is_termination(current_state)
        if is_termination:
            # this is a termination state
            # the reward is the state itself
            self.q_table[current_state_idx] = [termination_reward]

        if self.q_table[current_state_idx] is None:
            self.init_q_state(current_state_idx)

        # if this is the first turn, there's no need to update the q value
        if self.first_turn:
            self.first_turn = False
        else:
            # update the q_value
            # between the current state and the last state
            # temporal difference
            # update the current q state
            q_last_state = self.q_table[self.last_state_idx]
            # print('state: ', current_state_idx)
            # print('q_table: ', self.q_table[current_state_idx])
            q_current_state = self.q_table[current_state_idx]
            # if len(q_current_state) is 0:
            #     print('state: ', current_state)
            #     print('is_termination:', is_termination)
            q_current_value = max(q_current_state)
            q_last_state[self.last_action_idx] = (1 - self.last_alpha) * q_last_state[self.last_action_idx] \
                                            + self.last_alpha * (self.last_reward + self.discount * q_current_value)
            # print('q_last_state: ', q_last_state[self.last_action_idx], 'last_state_idx: ', self.last_state_idx)
            # print('last_reward: ', self.last_reward)

            if is_termination:
                # terminate state
                # should not do any action
                return None

        current_alpha = self.alpha()
        current_action, current_action_idx = self.next_action(current_state)
        current_reward = self.reward_fn(current_state, current_action)
        # print('current_reward: ', current_reward)
        # update the last state
        # put this at the end of function
        self.last_state_idx = current_state_idx
        self.last_action_idx = current_action_idx
        self.last_reward = current_reward
        self.last_alpha = current_alpha

        # the result will be fed up to the game (environment)
        return current_action

    def test(self, rounds=1):
        assert isinstance(rounds, int)
        # this is a hack
        # to import the tic-tac-toe game
        import sys
        import os
        # import the game from another project
        sys.path.append(os.path.abspath('../../tic-tac-toe-thegame'))
        from tictactoe import TicTacToe

        # play with the real game, with a given round count
        # the result will be averaged
        game = TicTacToe()

        pass

    def expected_reward(self):
        # return the expected_reward if starts with init state
        # the value is max of every q_value in that state
        return max(self.q_table[self.init_state_idx])

    def current_policy(self):
        # return current policy according to the q_table
        # policy is a list of actions for each state
        policy = [None for each in range(self.state_count)]
        for state_number, q_state in enumerate(self.q_table):
            best_action_number = 0
            for action_number, q_value in enumerate(q_state):
                if q_value > q_state[best_action_number]:
                    best_action_number = action_number
            policy[state_number] = best_action_number
        return policy

    def alpha_fn_maker(self):
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
            # return 1 / count
            return 0.3

        # return as a function
        return generator

    def next_action(self, state):
        assert isinstance(state, list)
        assert isinstance(state[0], list)
        # return the next action gonna take
        # also calculate the epsilon greedy
        # exploration vs exploitation
        is_explore = self.binary_random(self.epsilon)

        if is_explore:
            return self.next_random_action(state)
        else:
            return self.next_policy_action(state)

    def binary_random(self, probability):
        # return true with given probability
        assert isinstance(probability, float)
        if probability < 0.0001:
            return False

        power = 1
        while math.floor(probability) != math.ceil(probability):
            probability *= 10
            power *= 10
        rand = random.randrange(power)
        return rand <= probability

    def next_random_action(self, state):
        assert isinstance(state, list)
        assert isinstance(state[0], list)
        # next random action
        # just random
        actions = self.action_fn(state)
        action_idx = random.randrange(len(actions))
        # return a random action
        action = actions[action_idx]
        return action, action_idx

    def next_policy_action(self, state):
        assert isinstance(state, list)
        # best action according to the current policy
        # not from optimal policy (because it's not determined yet)
        # use the value from q_value table
        best_action_number = 0
        state_idx = self.hasher(state)
        q_state = self.q_table[state_idx]
        for action_number, q_value in enumerate(q_state):
            if q_value > q_state[action_number]:
                best_action_number = action_number
        # return the best action according to the policy
        action = self.action_fn(state)[best_action_number]
        action_idx = best_action_number
        return action, action_idx
