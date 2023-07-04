from turtle import Turtle


MOVE_DIST = 40


class Paddle(Turtle):
	def __init__(self):
		super().__init__()
		self.color('steel blue')
		self.shape('square')
		self.penup()
		self.shapesize(stretch_wid=1, stretch_len=10)
		self.goto(x=0, y=-280)

	def move_left(self, fast=False):
		if fast:
			self.backward(2*MOVE_DIST)
			print("fastLeft")
		else:
			self.backward(MOVE_DIST)
			print("slowLeft")

	def move_right(self, fast=False):
		if fast:
			self.forward(2*MOVE_DIST)
		else:
			self.forward(MOVE_DIST)
