from breakout import BreakoutEnv
from montecarlo import MCModel as MC
import numpy as np
import time
import pickle

# the type of the game board
# can be triangle, single_row or stairs
# should be changed in the test file as well
type = 'triple_row'

env = BreakoutEnv(display=False, type=type)

eps = 1000
if type == 'single_row':
    S = (2**(5+4))
if type == 'triple_row':
    S = (2**(15+4))
elif type == 'stairs':
    S = (2**(6+4))
elif type == 'triangle':
    S = (2**(9+4))
A = 3
m = MC(S, A, epsilon=1)
for i in range(1, eps + 1):
    if i % 100 == 0:
        print("Episode {}".format(i))
    ep = []
    observation = env.reset()
    while True:
        # Choosing behavior policy
        action = m.choose_action(m.b, observation)

        # Run simulation
        next_observation, reward, done = env.step(action)
        ep.append((observation, action, reward))
        observation = next_observation
        if done:
            break

    m.update_Q(ep)
    # Decaying epsilon, reach optimal policy
    m.epsilon = max((eps - i) / eps, 0.1)

with open('enviroment.pickle', "wb") as file:
    pickle.dump(m, file)
    file.close()
'''
with open('enviroment.pickle', "rb") as file:
    test = pickle.load(file)
    file.close()

for i in range(1,  100):
    observation = env.reset()
    while True:
        # Choosing behavior policy
        action = test.choose_action(test.b, observation)
        time.sleep(0.01)
        # Run simulation
        next_observation, reward, done = env.step(action)
        observation = next_observation
        if done:
            break
'''

#print("Final expected returns : {}".format(m.score(env, m.pi, n_samples=10000)))# TODO throws an error bc of the return of _get_obs
