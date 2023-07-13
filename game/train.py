from breakout import BreakoutEnv
from montecarlo import MCModel as MC
import numpy as np

env = BreakoutEnv()


def choose_action():
    return np.random.choice(["stay", "left", "right", "up", "down"])


eps = 10
S = 15 * 10 * 3
A = 5
m = MC(S, A, epsilon=1)
for i in range(1, eps + 1):
    print("Episode {}".format(i))
    ep = []
    observation = env.reset()
    while True:
        # Choosing behavior policy
        action = choose_action()

        # Run simulation
        next_observation, reward, done, info = env.step(action)
        ep.append((observation, action, reward))
        observation = next_observation
        if done:
            break

    # m.update_Q(ep) TODO throws an error bc of the return of _get_obs
    # Decaying epsilon, reach optimal policy
    m.epsilon = max((eps - i) / eps, 0.1)

# print("Final expected returns : {}".format(m.score(env, m.pi, n_samples=10000))) TODO throws an error bc of the return of _get_obs
