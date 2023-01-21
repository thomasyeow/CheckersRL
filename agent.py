import numpy as np
from collections import defaultdict
from gameLogic import *

class Agent:
    def __init__(
        self, game,
        learning_rate = 0.05,
        discount_factor = 0.9,
        epsilon_greedy = 0.9,
        epsilon_min = 0.1,
        epsilon_decay = 0.99
        ):
        self.game = game
        self.lr = learning_rate
        self.gamma = discount_factor
        self.epsilon = epsilon_greedy
        self.epsilon_min = epsilon_min
        self.epsilon_decay = epsilon_decay

        #Define the q-table
        self.q_table = defaultdict(lambda: np.zeros(self.game.nA))

    def get_state(self, game):
        gameState = [[EMPTY] * 8 for _ in range(8)]
        for x in range(8):
            for y in range(8):
                gameState[x][y] = game.boardArr[x][y]
        return gameState

    def learn(self, transition):
        s, a, r, next_s, done = transition
        q_val = self.q_table[s][a]
        if done:
            q_target = r
        else:
            q_target = r + self.gamma * np.max(self.q_table[next_s])

        self.q_table[s][a] += self.lr * (q_target - q_val)
        self._adjust_epsilon()

    #adjusts epsilon value
    def _adjust_epsilon(self):
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay
    #returns an action index(0 - 255) based on current game state
    def get_action(self):
        actionIndex = 0
        #should random action be taken?
        if np.random.uniform() < self.epsilon:
            actionIndex = np.random.choice(self.game.nA)
        else:
            #TODO the following line might be a problem
            q_vals = self.q_table[self.game.getStateCopy()]
            perm_actions = np.random.permutation(self.game.nA)
            q_vals = [q_vals[a] for a in perm_actions]
            perm_q_argmax = np.argmax(q_vals)
            actionIndex = perm_actions[perm_q_argmax]
        return actionIndex