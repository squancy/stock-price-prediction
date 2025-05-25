import gym
import numpy as np
from gym import spaces
import consts

class TradingEnv(gym.Env):
    def __init__(self, prices, window_size=10, initial_cash=consts.INIT_CASH):
        super().__init__()
        self.prices = prices
        self.window_size = window_size
        self.initial_cash = initial_cash
        self.action_space = spaces.Discrete(3)
        self.observation_space = spaces.Box(low=0, high=np.inf, shape=(window_size,), dtype=np.float32)
        self.reset()

    def reset(self):
        self.cash = self.initial_cash
        self.shares = 0
        self.current_step = self.window_size
        self.done = False
        self.initial_cash_val = self.initial_cash
        return self._get_state()

    def _get_state(self):
        return self.prices[self.current_step - self.window_size:self.current_step]

    def step(self, action):
        prev_price = self.prices[self.current_step]
        prev_value = self.cash + self.shares * prev_price

        if action == 1:
            shares_to_buy = int(self.cash / prev_price)
            self.cash -= shares_to_buy * prev_price
            self.shares += shares_to_buy
        elif action == 2 and self.shares > 0:
            self.cash += self.shares * prev_price
            self.shares = 0

        self.current_step += 1
        if self.current_step >= len(self.prices):
            self.done = True

        price = self.prices[self.current_step - 1]
        total_value = self.cash + self.shares * price
        reward = total_value - prev_value  # dense reward
        return self._get_state(), reward, self.done, {}


    def get_value(self):
        return self.cash + self.shares * self.prices[self.current_step-1]