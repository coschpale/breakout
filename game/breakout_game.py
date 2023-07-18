import pygame
import time
from game.ball import Ball
from game.paddle import Paddle
from game.brick import Brick
import numpy as np
import argparse

class Breakout_game:
	def __init__(self, width, height, cell_size):
		self.width = width
		self.height = height
		self.cell_size = cell_size
		self.window_width = self.width * self.cell_size
		self.window_height = self.height * self.cell_size

		window_size = (self.window_width, self.window_height)
		self.screen = pygame.display.set_mode(window_size)

		self.ball = Ball(self.window_width // 2, self.window_height - 15, 7, 1, -1)
		self.paddle = Paddle(((self.width // 2) - 2) * cell_size, self.window_height - 5, 5 * cell_size, self.window_width)
		self.bricks = []

		for row in range(3):
			counter = 0
			while counter < self.width:
				self.bricks.append(Brick(counter * self.cell_size +1, row * self.cell_size +1, 3 * self.cell_size - 2, self.cell_size - 2))
				counter += 3

	def run(self):
		# Define colors
		BLACK = (0, 0, 0)
		WHITE = (255, 255, 255)
		RED = (255, 0, 0)
		GREEN = (0, 255, 0)
		BLUE = (0, 0, 255)

		# Game loop
		running = True
		start_time = time.time()
		last_agent_call = time.time()
		action_choice = 0
		while running:

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					running = False
				elif event.type == pygame.KEYDOWN:
					if event.key == pygame.K_LEFT:
						self.paddle.moveLeft()
					elif event.key == pygame.K_RIGHT:
						self.paddle.moveRight()
					elif event.key == pygame.K_UP:
						self.paddle.moveRightFast()
					elif event.key == pygame.K_DOWN:
						self.paddle.moveLeftFast()

			# Fill the background
			self.screen.fill(BLACK)

			# Draw the game board
			for row in range(self.height):
				for col in range(self.width):
					x = col * self.cell_size
					y = row * self.cell_size
					pygame.draw.rect(self.screen, WHITE, (x, y, self.cell_size - 1, self.cell_size - 1))

			# Draw additional elements (e.g., game pieces)
			self.ball.move()

			if self.checkGameWon():
				running = False
				self.printStats(won=True, time=time.time() - start_time)
			if self.checkGameOver():
				running = False
				self.printStats(won=False, time=time.time() - start_time)
			self.checkCollisionWithWalls()
			self.checkCollisionWithPaddle()
			self.checkCollisionWithBricks()

			# print(ball.pos_x)
			pygame.draw.circle(self.screen, RED, (self.ball.pos_x, self.ball.pos_y), self.ball.radius)
			pygame.draw.rect(self.screen, GREEN, (self.paddle.pos_x, self.paddle.pos_y, self.paddle.paddle_width, self.cell_size))

			for brick in self.bricks:
				if brick.alive:
					pygame.draw.rect(self.screen, BLUE, (brick.pos_x, brick.pos_y, brick.width, brick.height))

			# Update the display
			pygame.display.flip()
			time.sleep(0.01)

		# Quit Pygame
		pygame.quit()


	def checkGameOver(self):
		if self.ball.pos_y >= self.window_height - self.ball.radius:
			return True
		else:
			return False


	def checkGameWon(self):
		for brick in self.bricks:
			if brick.alive:
				return False

		return True


	def printStats(self, won, time):
		print(str(time))
		if won:
			print("Congrats you won in " + str(time) + "seconds!")
			return

		dead = 0
		alive = 0
		for brick in self.bricks:
			if brick.alive:
				alive += 1
			else:
				dead += 1

		print("Game over! Your score is " + str(dead) + "/" + str(dead + alive) + " in " + str(time) + " seconds")


	def checkCollisionWithWalls(self):
		if self.ball.pos_x <= self.ball.radius or self.ball.pos_x >= self.window_width - self.ball.radius:
			self.ball.bounce(x_bounce=False, y_bounce=True)

		if self.ball.pos_y <= self.ball.radius:
			self.ball.bounce(x_bounce=True, y_bounce=False)


	def checkCollisionWithPaddle(self):
		if self.ball.pos_y == self.window_height - (self.ball.radius + 5):
			if self.ball.pos_x + self.ball.radius >= self.paddle.pos_x and self.ball.pos_x < self.paddle.pos_x + (self.paddle.paddle_width // 5):
				self.ball.bounce_from_paddle(-2)
			elif self.paddle.pos_x + (self.paddle.paddle_width // 5) <= self.ball.pos_x < self.paddle.pos_x + 2 * (
					self.paddle.paddle_width // 5):
				self.ball.bounce_from_paddle(-1)
			elif self.paddle.pos_x + 2 * (self.paddle.paddle_width // 5) <= self.ball.pos_x < self.paddle.pos_x + 3 * (
					self.paddle.paddle_width // 5):
				self.ball.bounce_from_paddle(0)
			elif self.paddle.pos_x + 3 * (self.paddle.paddle_width // 5) <= self.ball.pos_x < self.paddle.pos_x + 4 * (
					self.paddle.paddle_width // 5):
				self.ball.bounce_from_paddle(1)
			elif self.ball.pos_x >= self.paddle.pos_x + 4 * (
					self.paddle.paddle_width // 5) and self.ball.pos_x - self.ball.radius < self.paddle.pos_x + self.paddle.paddle_width:
				self.ball.bounce_from_paddle(2)


	def checkCollisionWithBricks(self):
		for brick in self.bricks:
			if brick.alive:
				# bottom
				if self.ball.velocity_y < 0 and self.ball.pos_y - self.ball.radius == brick.pos_y + brick.height and self.ball.pos_x + self.ball.radius >= brick.pos_x and self.ball.pos_x - self.ball.radius <= brick.pos_x + brick.width:
					brick.kill()
					self.ball.bounce(x_bounce=True, y_bounce=False)
				# top
				elif self.ball.velocity_y > 0 and self.ball.pos_y + self.ball.radius == brick.pos_y and self.ball.pos_x + self.ball.radius >= brick.pos_x and self.ball.pos_x - self.ball.radius <= brick.pos_x + brick.width:
					brick.kill()
					self.ball.bounce(x_bounce=True, y_bounce=False)
				# right
				elif self.ball.velocity_x < 0 and self.ball.pos_x - self.ball.radius == brick.pos_x + brick.width and self.ball.pos_y + self.ball.radius >= brick.pos_y and self.ball.pos_y - self.ball.radius <= brick.pos_y + brick.height:
					brick.kill()
					self.ball.bounce(x_bounce=False, y_bounce=True)
				# left
				elif self.ball.velocity_x > 0 and self.ball.pos_x + self.ball.radius == brick.pos_x and self.ball.pos_y + self.ball.radius >= brick.pos_y and self.ball.pos_y - self.ball.radius <= brick.pos_y + brick.height:
					brick.kill()
					self.ball.bounce(x_bounce=False, y_bounce=True)