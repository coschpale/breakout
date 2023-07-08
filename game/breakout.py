import gym
from gym import spaces
import pygame
import numpy as np
from ball import Ball
from paddle import Paddle
from brick import Brick

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


class BreakoutEnv(gym.Env):
    metadata = {'render_modes': ['human']}

    def __init__(self):
        self.render_mode = "human"
        self.window = None
        self.size_height = 15
        self.size_width = 10
        self.cell_size = 15
        self.window_width = self.size_width * self.cell_size
        self.window_height = self.size_height * self.cell_size
        self.window_size = (self.window_width, self.window_height)

        self.brick_rows = 3
        self.brick_cols = 5
        self.terminal_reward = -(self.brick_rows * self.brick_cols)

        self.score = 0
        self.time = 0
        self.reward = 0

        # observation space - 15x10x3
        self.observation_space = spaces.Box(low=0, high=255, shape=(self.size_height, self.size_width, 3),
                                            dtype=np.uint8)

        # 5 actions - move left, move right, move left fast, move right fast, do nothing
        self.action_space = spaces.Discrete(5)

        self._action_to_key = {
            0: "stay",
            1: "left",
            2: "right",
            3: "up",
            4: "down"
        }

        self.ball = Ball(self.size_width // 2, self.size_height - 15, 7, 1, -1)
        self.ball._ball_position = self.ball.ball_location()
        self.ball._ball_velocity = self.ball.ball_velocity()
        self.paddle = Paddle(((self.window_width // 2) - 2) * self.cell_size, self.window_height - 5,
                             5 * self.cell_size, self.window_width)
        self._paddle_position = self.paddle.paddle_location()
        self.bricks = []

        for row in range(self.brick_rows):
            counter = 0
            while counter < self.window_width:
                self.bricks.append(
                    Brick(counter * self.cell_size, row * self.cell_size, 3 * self.cell_size, self.cell_size))
                counter += 3

    def _get_obs(self):
        # get the current state of the game
        return np.array(pygame.surfarray.array3d(pygame.display.get_surface()))

    def _get_info(self):
        return {"score": self.score, "time": self.time}

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self.score = 0
        self.time = 0
        self.ball = Ball(self.size_width // 2, self.size_height - 15, 7, 1, -1)
        self.ball._ball_position = self.ball.ball_location()
        self.ball._ball_velocity = self.ball.ball_velocity()
        self.paddle = Paddle(((self.window_width // 2) - 2) * self.cell_size, self.window_height - 5,
                             5 * self.cell_size, self.window_width)
        self._paddle_position = self.paddle.paddle_location()
        self.bricks = []

        for row in range(self.brick_rows):
            counter = 0
            while counter < self.window_width:
                self.bricks.append(
                    Brick(counter * self.cell_size, row * self.cell_size, 3 * self.cell_size, self.cell_size))
                counter += 3

        if self.render_mode == "human":
            self._render_frame()

        return self._get_obs(), self._get_info()

    def step(self, action):
        action_choice = self._action_to_key[action]
        if action_choice == 0:
            pass
        elif action_choice == 1:
            self._paddle_position = self.paddle.moveLeft()
        elif action_choice == 2:
            self._paddle_position = self.paddle.moveRight()
        elif action_choice == 3:
            self._paddle_position = self.paddle.moveRightFast()
        elif action_choice == 4:
            self._paddle_position = self.paddle.moveLeftFast()

        # episode is done iff the ball hits the bottom or all bricks are destroyed
        terminated = self._check_game_terminated()
        reward = 0
        if self._check_collision_bricks():
            reward = 1
        elif self._check_game_over():
            reward = -1000

        self._render_frame()

        return self._get_obs(), reward, terminated, False, self._get_info()

    def _render_frame(self):
        pygame.init()
        pygame.display.init()
        self.window = pygame.display.set_mode(self.window_size)

        # Fill the background
        self.window.fill(BLACK)

        # Draw the game board
        for row in range(self.window_height):
            for col in range(self.window_width):
                x = col * self.cell_size
                y = row * self.cell_size
                pygame.draw.rect(self.window, WHITE, (x, y, self.cell_size - 1, self.cell_size - 1))

        # Draw additional elements (e.g., game pieces)
        self.ball.move()

        self._check_collision_walls()
        self._check_collision_paddle()
        self._check_collision_bricks()

        # print(ball.pos_x)
        pygame.draw.circle(self.window, RED, (self.ball.pos_x, self.ball.pos_y), self.ball.radius)
        pygame.draw.rect(self.window, GREEN,
                         (self.paddle.pos_x, self.paddle.pos_y, self.paddle.paddle_width, self.cell_size))

        for brick in self.bricks:
            if brick.alive:
                pygame.draw.rect(self.window, BLUE, (brick.pos_x, brick.pos_y, brick.width - 1, brick.height - 1))

        # Update the display
        pygame.display.flip()

    def close(self):
        if self.window is not None:
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
        is_collided = False
        for brick in self.bricks:
            if brick.alive:
                # bottom
                if self.ball.pos_y - self.ball.radius == brick.pos_y + brick.height and self.ball.pos_x + self.ball.radius >= brick.pos_x and self.ball.pos_x - self.ball.radius <= brick.pos_x + brick.width:
                    brick.kill()
                    self.ball.bounce(x_bounce=True, y_bounce=False)
                    is_collided = True
                # top
                if self.ball.pos_y - self.ball.radius == brick.pos_y and self.ball.pos_x + self.ball.radius >= brick.pos_x and self.ball.pos_x - self.ball.radius <= brick.pos_x + brick.width:
                    brick.kill()
                    self.ball.bounce(x_bounce=True, y_bounce=False)
                    is_collided = True
                # right
                if self.ball.pos_x - self.ball.radius == brick.pos_x + brick.width and self.ball.pos_y + self.ball.radius >= brick.pos_y and self.ball.pos_y - self.ball.radius <= brick.pos_y + brick.height:
                    brick.kill()
                    self.ball.bounce(x_bounce=False, y_bounce=True)
                    is_collided = True
                # left
                if self.ball.pos_x + self.ball.radius == brick.pos_x and self.ball.pos_y + self.ball.radius >= brick.pos_y and self.ball.pos_y - self.ball.radius <= brick.pos_y + brick.height:
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
            if self.ball.pos_x + self.ball.radius >= self.paddle.pos_x and self.ball.pos_x < self.paddle.pos_x + (self.paddle.paddle_width // 5):
                self.ball.bounce_from_paddle(-2)
            elif self.paddle.pos_x + (self.paddle.paddle_width // 5) <= self.ball.pos_x < self.paddle.pos_x + 2 * (self.paddle.paddle_width // 5):
                self.ball.bounce_from_paddle(-1)
            elif self.paddle.pos_x + 2 * (self.paddle.paddle_width // 5) <= self.ball.pos_x < self.paddle.pos_x + 3 * (self.paddle.paddle_width // 5):
                self.ball.bounce_from_paddle(0)
            elif self.paddle.pos_x + 3 * (self.paddle.paddle_width // 5) <= self.ball.pos_x < self.paddle.pos_x + 4 * (self.paddle.paddle_width // 5):
                self.ball.bounce_from_paddle(1)
            elif self.ball.pos_x >= self.paddle.pos_x + 4 * (self.paddle.paddle_width // 5) and self.ball.pos_x - self.ball.radius < self.paddle.pos_x + self.paddle.paddle_width:
                self.ball.bounce_from_paddle(2)
