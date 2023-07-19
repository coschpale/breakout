import numpy as np
from copy import deepcopy


class MCModel:
    def __init__(self, state_space, action_space, gamma=1.0, epsilon=0.1):
        self.gamma = gamma
        self.epsilon = epsilon
        self.Q = None
        self.action_space = np.arange(action_space)
        actions = [0] * action_space
        # Action representation
        self.state_space = np.arange(state_space)
        self.Q = [deepcopy(actions) for _ in range(state_space)]
        # Frequency of state/action.
        self.Ql = deepcopy(self.Q)

    def pi(self, action, state):
        if action == np.argmax(self.Q[state]):
            return 1
        return 0

    def b(self, action, state):
        return self.epsilon / len(self.action_space) + (1 - self.epsilon) * self.pi(action, state)

    def generate_returns(self, ep):
        G = {}  # return on state
        C = 0  # cumulative reward
        for tpl in reversed(ep):
            observation, action, reward = tpl
            G[(observation, action)] = C = reward + self.gamma * C
        return G

    def choose_action(self, policy, state):
        probs = [policy(a, state) for a in self.action_space]
        return np.random.choice(self.action_space, p=probs)

    def update_Q(self, ep):
        G = self.generate_returns(ep)
        for s in G:
            state, action = s
            q = self.Q[state][action]
            self.Ql[state][action] += 1
            N = self.Ql[state][action]
            self.Q[state][action] = q * N / (N + 1) + G[s] / (N + 1)

