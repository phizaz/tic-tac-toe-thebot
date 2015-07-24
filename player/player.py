__author__ = 'phizaz'

from environment import Environment

class Player:
    def __init__(self,
                 name,
                 epsilon,
                 environment):
        assert isinstance(environment, Environment)
        # this will be used in reward function
        # used when comparing a state
        self.name = name
        self.epsilon = epsilon
        self.hasher = environment.hasher
        self.dehasher = environment.dehasher
        state_count = environment.states()[0]
        # init cache
        self.cache = [None for each in range(state_count)]

    def reward(self, state, action):
        # normally returns 0
        # except for the terminate states

        # no winner at first
        winner = None

        def is_identical(alist):
            return len(set(alist)) == 1

        def is_winning(alist):
            nonlocal winner
            if alist[0] is not 0 and is_identical(alist):
                winner = alist[0]
                return True
            else:
                return False

        for row in range(3):
            horizontal = [state[row][i] for i in range(3)]
            if is_winning(horizontal):
                break
        for col in range(3):
            vertical = [state[i][col] for i in range(3)]
            if is_winning(vertical):
                break

        diagonal_left = [state[i][i] for i in range(3)]
        is_winning(diagonal_left)

        diagonal_right = [state[i][3-i-1] for i in range(3)]
        is_winning(diagonal_right)

        # normally returns 0
        if winner is None:
            return 0
        else:
            # if wins return 100 otherwise -100 (punishment)
            if winner is self.name:
                return 100
            else:
                return -100

    def actions(self, state):
        # return list of actions for a given state,
        # action should be a list of functions ?
        hashed_state = self.hasher(state)
        if self.cache[hashed_state] is None:
            # calculate
            actions = []
            for i, row in enumerate(state):
                for j, col in enumerate(row):
                    if col is 0:
                        actions.append((i, j))
            self.cache[hashed_state] = actions
        # return the cached one
        return self.cache[hashed_state]