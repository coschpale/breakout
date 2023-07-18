from game.breakout_game import Breakout_game
import pickle
import time
from game.breakout import BreakoutEnv
from breakout import BreakoutEnv
from montecarlo import MCModel as MC
import numpy as np
import time
import pickle
env = BreakoutEnv()

def main():
	with open('game/enviroment.pickle', "rb") as file:
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

def decimal_to_binary(decimal_number):
    if decimal_number == 0:
        return '0'  # Special case for zero

    binary_digits = []
    while decimal_number > 0:
        binary_digits.append(str(decimal_number % 2))
        decimal_number //= 2

    binary_digits.reverse()
    binary_string = ''.join(binary_digits)
    return binary_string

if __name__ == "__main__":
	decimal_to_binary(11)
    #main()
