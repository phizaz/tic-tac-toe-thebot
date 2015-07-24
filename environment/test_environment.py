from unittest import TestCase
from environment.environment import Environment
__author__ = 'phizaz'


class TestEnvironment(TestCase):
    def test_reward(self):
        assert 0

    def test_hasher(self):
        env = Environment()
        assert env.hasher([[0,1,2],
                           [0,0,0],
                           [0,0,1]]) == 6582
        # assert 0

    def test_dehasher(self):
        env = Environment()
        assert env.dehasher(6582) == ([[0,1,2],
                                       [0,0,0],
                                       [0,0,1]])
