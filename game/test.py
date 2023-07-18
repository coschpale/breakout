from breakout import BreakoutEnv
from montecarlo import MCModel as MC
import numpy as np
import time
import pickle
env = BreakoutEnv(display=True)

def main():
	test = ''
	with open('enviroment.pickle', "rb") as file:
		test = pickle.load(file)
		file.close()
	print(test)
	for i in range(1,  100):	
		observation = env.reset()
		while True:
			# Choosing behavior policy
			action = test.choose_action(test.b, observation)
			# Run simulation
			next_observation, reward, done = env.step(action)
			observation = next_observation
			if done:
				break

			time.sleep(0.001)

if __name__ == "__main__":
	main()