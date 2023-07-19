import pygame
import numpy as np
from ball import Ball
from paddle import Paddle
from brick import Brick
import time

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

class BreakoutEnv:

    def __init__(self, display):
        self.display = display
        self.board_height = 10
        self.board_width = 15
        self.cell_size = 15
        self.window_width = self.board_width * self.cell_size
        self.window_height = self.board_height * self.cell_size
        self.window_size = (self.window_width, self.window_height)
        self.brick_rows = 1
        self.brick_cols = 5
        self.terminal_reward = (self.brick_rows * self.brick_cols)

        self.window = None

        self.score = 0
        self.time = 0
        self.reward = 0

        # observation space - 15x10x3
        # self.observation_space = spaces.Box(low=0, high=255, shape=(self.size_height, self.size_width, 3), dtype=np.uint8)
        # self.observation_space = 15 * 10 * 3

        # 5 actions - move left, move right, move left fast, move right fast, do nothing
        # self.action_space = 5

        self._action_to_key = {
            "stay": 0,
            "left": 1,
            "right": 2,
            "up": 3,
            "down": 4
        }

        self.ball = Ball(self.window_width // 2, self.window_height - 15, 100, 1, -1)
        self.paddle = Paddle(((self.board_width // 2) - 2) * self.cell_size, self.window_height - 5, 5 * self.cell_size, self.window_width)
        self.bricks = []

        for row in range(self.brick_rows):
            counter = 0
            while counter < self.board_width:
                self.bricks.append(Brick(counter * self.cell_size, row * self.cell_size, 3 * self.cell_size, self.cell_size))
                counter += 3

    def _get_obs(self):
        # get the current state of the game
        # return np.array(pygame.surfarray.array3d(pygame.display.get_surface()))
        #paddle_pos = (self.paddle.pos_x, self.paddle.pos_y)
        #brick_positions = [(brick.pos_x, brick.pos_y, int(brick.alive)) for brick in self.bricks]
        brick_positions = [int(brick.alive) for brick in self.bricks]
        paddle_pos = self.paddle.pos_x // self.cell_size
        sum  = 0
        index = 0
        for i, val in enumerate(brick_positions):
            sum += val*(2**index)
            index += 1

        pad = self._decimal_to_binary(paddle_pos)
        pad.reverse()
        for bit in pad:
            if bit == '1':
                sum += (2**(index))
                index += 1
        return sum
    

    def _decimal_to_binary(self, decimal_number):
        if decimal_number == 0:
            return ['0']  # Special case for zero

        binary_digits = []
        while decimal_number > 0:
            binary_digits.append(str(decimal_number % 2))
            decimal_number //= 2

        binary_digits.reverse()
        return binary_digits
    def _get_info(self):
        return {"reward": self.reward, "time": self.time}

    def reset(self):
        self.score = 0
        self.time = 0
        self.ball = Ball(self.window_width // 2, self.window_height - 15, 7, 1, -1)
        self.paddle = Paddle(((self.board_width // 2) - 2) * self.cell_size, self.window_height - 5, 5 * self.cell_size,
                             self.window_width)
        self.bricks = []

        for row in range(self.brick_rows):
            counter = 0
            while counter < self.board_width:
                self.bricks.append(
                    Brick(counter * self.cell_size, row * self.cell_size, 3 * self.cell_size, self.cell_size))
                counter += 3

        if self.display:
            pygame.init()
            pygame.display.set_caption("Game Board")
            self.window = pygame.display.set_mode(self.window_size)

        return self._get_obs()

    def step(self, action):
        if action == 0:
            pass
        elif action == 1:
            self.paddle.moveLeft()
        elif action == 2:
            self.paddle.moveRight()
        elif action == 3:
            self.paddle.moveRightFast()
        elif action == 4:
            self.paddle.moveLeftFast()

        terminated, reward = self._render_frame()

        return self._get_obs(), reward, terminated

    def _render_frame(self):
        
        if self.display:
            self.window.fill(BLACK)

        # Draw the game board
        for row in range(self.board_height):
            for col in range(self.board_width):
                x = col * self.cell_size
                y = row * self.cell_size

                if self.display:
                    pygame.draw.rect(self.window, WHITE, (x, y, self.cell_size - 1, self.cell_size - 1))

        # Draw additional elements (e.g., game pieces)
        self.ball.move()

        terminated = self._check_game_terminated()

        reward = 0
        if self._check_collision_bricks():
            reward = 0
        elif self._check_game_won():
            # not sure if we really need this bc we only have 1 live, but if the reward overall is taken into account
            reward = 100
        elif self._check_game_over():
            # not sure if we really need this bc we only have 1 live, but if the reward overall is taken into account
            reward = -1000

        self._check_collision_walls()
        self._check_collision_paddle()


        if self.display:
            pygame.draw.circle(self.window, RED, (self.ball.pos_x, self.ball.pos_y), self.ball.radius)
            pygame.draw.rect(self.window, GREEN,
                            (self.paddle.pos_x, self.paddle.pos_y, self.paddle.paddle_width, self.cell_size))

            for brick in self.bricks:
                if brick.alive:
                    pygame.draw.rect(self.window, BLUE, (brick.pos_x, brick.pos_y, brick.width - 1, brick.height - 1))

            # Update the display
            pygame.display.flip()

        return terminated, reward

    def close(self):
        if self.window is not None and self.display:
            pygame.display.quit()
            pygame.quit()

    def _check_game_terminated(self):
        # check if the game is terminated
        if self._check_game_over():
            return True
        if self._check_game_won():
            return True
        return False

    def _check_game_over(self):
        if self.ball.pos_y >= self.window_height - self.ball.radius:
            return True
        else:
            return False

    def _check_game_won(self):
        for brick in self.bricks:
            if brick.alive:
                return False

        return True

    def _check_collision_bricks(self):
        is_collided = False  # if the ball collided with a brick return true to give reward
        for brick in self.bricks:
            if brick.alive:
                # bottom
                if self.ball.velocity_y < 0 and self.ball.pos_y - self.ball.radius == brick.pos_y + brick.height and self.ball.pos_x + self.ball.radius >= brick.pos_x and self.ball.pos_x - self.ball.radius <= brick.pos_x + brick.width:
                    brick.kill()
                    self.ball.bounce(x_bounce=True, y_bounce=False)
                    is_collided = True
                # top
                if self.ball.velocity_y > 0 and self.ball.pos_y + self.ball.radius == brick.pos_y and self.ball.pos_x + self.ball.radius >= brick.pos_x and self.ball.pos_x - self.ball.radius <= brick.pos_x + brick.width:
                    brick.kill()
                    self.ball.bounce(x_bounce=True, y_bounce=False)
                    is_collided = True
                # right
                if self.ball.velocity_x < 0 and self.ball.pos_x - self.ball.radius == brick.pos_x + brick.width and self.ball.pos_y + self.ball.radius >= brick.pos_y and self.ball.pos_y - self.ball.radius <= brick.pos_y + brick.height:
                    brick.kill()
                    self.ball.bounce(x_bounce=False, y_bounce=True)
                    is_collided = True
                # left
                if self.ball.velocity_x > 0 and self.ball.pos_x + self.ball.radius == brick.pos_x and self.ball.pos_y + self.ball.radius >= brick.pos_y and self.ball.pos_y - self.ball.radius <= brick.pos_y + brick.height:
                    brick.kill()
                    self.ball.bounce(x_bounce=False, y_bounce=True)
                    is_collided = True

        return is_collided

    def _check_collision_walls(self):
        if self.ball.pos_x <= self.ball.radius or self.ball.pos_x >= self.window_width - self.ball.radius:
            self.ball.bounce(x_bounce=False, y_bounce=True)

        if self.ball.pos_y <= self.ball.radius:
            self.ball.bounce(x_bounce=True, y_bounce=False)

    def _check_collision_paddle(self):
        if self.ball.pos_y == self.window_height - (self.ball.radius + 5):
            if self.ball.pos_x + self.ball.radius >= self.paddle.pos_x and self.ball.pos_x < self.paddle.pos_x + (
                    self.paddle.paddle_width // 5):
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
