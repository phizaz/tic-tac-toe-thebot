__author__ = 'phizaz'

class Environment:
    def __init__(self,
                 discount=0.99,
                 q_init=0):
        self.discount = discount
        self.q_init = q_init

    def states(self):
        # return state_count, init_state_idx
        return 3 ** 9, 0

    def hasher(self, state):
        # return the hashed int value
        hashed = 0
        power = 0
        for row in state:
            for each in row:
                hashed += each * 3 ** power
                power += 1
        return hashed

    def dehasher(self, hashed_state):
        state = [[0 for i in range(3)] for i in range(3)]
        for i in range(9):
            state[i//3][i%3] = hashed_state % 3
            hashed_state //= 3
        return state

