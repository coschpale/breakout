from game.breakout_game import Breakout_game

class Environment:
	def __init__(self, width, height, cell_size):
		self.width = width
		self.height = height
		self.cell_size = cell_size
		self.game = Breakout_game(self.widht, self.height, self.cell_size)

	def reset(self):
		self.game = Breakout_game(self.widht, self.height, self.cell_size)
		self.game.run()
		return self.game.get_obs()

	def step(self):
		
		