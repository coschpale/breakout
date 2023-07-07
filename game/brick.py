class Brick:
	def __init__(self, pos_x, pos_y, width, height):
		self.pos_x = pos_x
		self.pos_y = pos_y
		self.width = width
		self.height = height
		self.alive = True

	def kill(self):
		self.alive = False

