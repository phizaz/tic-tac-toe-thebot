from unittest import TestCase
from environment import Environment
from player import Player

__author__ = 'phizaz'


class TestPlayer(TestCase):
    def test_reward(self):
        env = Environment()
        player = Player(name=1,
                        epsilon=0.8,
                        environment=env)
        state = [
            [1, 2, 1],
            [2, 1, 2],
            [2, 1, 1],
        ]
        assert player.reward(state, None) is 100
        state = [
            [1, 2, 1],
            [2, 1, 2],
            [2, 1, 0],
        ]
        assert player.reward(state, None) is 0

    def test_actions(self):
        env = Environment()
        player = Player(name=1,
                        epsilon=0.8,
                        environment=env)
        state = [
            [1, 2, 1],
            [1, 2, 0],
            [2, 1, 0],
        ]
        actions = player.actions(state)
        assert actions == [(1, 2), (2, 2)]