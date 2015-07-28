from unittest import TestCase
from environment import Environment
from player import Player
from tictactoebot import BotSimpleRL

__author__ = 'phizaz'


class TestBotSimpleRL(TestCase):
    env = Environment(q_init=0.1)
    player = Player(name=1, exploratory=0.9, environment=env)

    def test_init_q_state(self):
        bot = BotSimpleRL(self.env, self.player)
        bot.init_q_state(0)
        assert len(bot.q_table[0]) == len(self.player.actions(self.env.dehasher(0)))
        for each in bot.q_table[0]:
            assert each == self.env.q_init

    def test_take_turn(self):
        pass

    def test_test(self):
        pass

    def test_expected_reward(self):
        pass

    def test_current_policy(self):
        pass

    def test_alpha_fn_maker(self):
        bot = BotSimpleRL(self.env, self.player)
        fn = bot.alpha_fn_maker()
        assert abs(fn() - 1/2) < 0.00001
        assert abs(fn() - 1/3) < 0.00001

    def test_next_action(self):
        pass

    def test_binary_random(self):
        bot = BotSimpleRL(self.env, self.player)
        all = 1000
        trues = 0
        prob = 1.0
        for i in range(all):
            trues += 1 if bot.binary_random(prob) else 0
        experiment = trues / all
        assert abs((experiment - prob) / prob) < 0.0001

    def test_next_random_action(self):
        bot = BotSimpleRL(self.env, self.player)
        assert bot.next_random_action(bot.dehasher(0), 0) == 0
        assert 0

    def test_next_policy_action(self):
        bot = BotSimpleRL(self.env, self.player)
        bot.init_q_state(0)
        assert bot.next_policy_action(bot.dehasher(0), 0) == -1
        pass
