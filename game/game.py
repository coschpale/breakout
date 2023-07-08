import pygame
import time
from ball import Ball
from paddle import Paddle
from brick import Brick
import numpy as np
import argparse

# parse if we want to use the agent or play by our own
parser = argparse.ArgumentParser()
parser.add_argument("-a", "--agent", help="use the agent to play the game", action="store_true")
args = parser.parse_args()

pygame.init()

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Set the dimensions of the game board
board_width = 15
board_height = 10
brick_rows = 3

cell_size = 15
window_width = board_width * cell_size
window_height = board_height * cell_size
window_size = (window_width, window_height)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("Game Board")


def adapter():
    # Here we should let the agent choose the action to take
    adapter_choice = np.random.choice([0, 1, 2, 3, 4])
    choice_string = "stay"

    # Map the action to arrow key presses
    if adapter_choice == 0:
        # Do nothing
        return choice_string, adapter_choice
    elif adapter_choice == 1:
        choice_string = "left"
    elif adapter_choice == 2:
        choice_string = "right"
    elif adapter_choice == 3:
        choice_string = "up"
    elif adapter_choice == 4:
        choice_string = "down"

    return choice_string, adapter_choice


def checkGameOver(ball):
    if ball.pos_y >= window_height - ball.radius:
        return True
    else:
        return False


def checkGameWon(bricks):
    for brick in bricks:
        if brick.alive:
            return False

    return True


def printStats(won, time, bricks):
    print(str(time))
    if won:
        print("Congrats you won in " + str(time) + "seconds!")
        return

    dead = 0
    alive = 0
    for brick in bricks:
        if brick.alive:
            alive += 1
        else:
            dead += 1

    print("Game over! Your score is " + str(dead) + "/" + str(dead + alive) + " in " + str(time) + " seconds")


def checkCollisionWithWalls(ball):
    if ball.pos_x <= ball.radius or ball.pos_x >= window_width - ball.radius:
        ball.bounce(x_bounce=False, y_bounce=True)

    if ball.pos_y <= ball.radius:
        ball.bounce(x_bounce=True, y_bounce=False)


def checkCollisionWithPaddle(paddle, ball):
    if ball.pos_y == window_height - (ball.radius + 5):
        if ball.pos_x + ball.radius >= paddle.pos_x and ball.pos_x < paddle.pos_x + (paddle.paddle_width // 5):
            ball.bounce_from_paddle(-2)
        elif paddle.pos_x + (paddle.paddle_width // 5) <= ball.pos_x < paddle.pos_x + 2 * (
                paddle.paddle_width // 5):
            ball.bounce_from_paddle(-1)
        elif paddle.pos_x + 2 * (paddle.paddle_width // 5) <= ball.pos_x < paddle.pos_x + 3 * (
                paddle.paddle_width // 5):
            ball.bounce_from_paddle(0)
        elif paddle.pos_x + 3 * (paddle.paddle_width // 5) <= ball.pos_x < paddle.pos_x + 4 * (
                paddle.paddle_width // 5):
            ball.bounce_from_paddle(1)
        elif ball.pos_x >= paddle.pos_x + 4 * (
                paddle.paddle_width // 5) and ball.pos_x - ball.radius < paddle.pos_x + paddle.paddle_width:
            ball.bounce_from_paddle(2)


def checkCollisionWithBricks(bricks, ball):
    for brick in bricks:
        if brick.alive:
            # bottom
            if ball.pos_y - ball.radius == brick.pos_y + brick.height and ball.pos_x + ball.radius >= brick.pos_x and ball.pos_x - ball.radius <= brick.pos_x + brick.width:
                brick.kill()
                ball.bounce(x_bounce=True, y_bounce=False)
            # top
            if ball.pos_y - ball.radius == brick.pos_y and ball.pos_x + ball.radius >= brick.pos_x and ball.pos_x - ball.radius <= brick.pos_x + brick.width:
                brick.kill()
                ball.bounce(x_bounce=True, y_bounce=False)
            # right
            if ball.pos_x - ball.radius == brick.pos_x + brick.width and ball.pos_y + ball.radius >= brick.pos_y \
                    and ball.pos_y - ball.radius <= brick.pos_y + brick.height:
                brick.kill()
                ball.bounce(x_bounce=False, y_bounce=True)
            # left
            if ball.pos_x + ball.radius == brick.pos_x and ball.pos_y + ball.radius >= brick.pos_y and \
                    ball.pos_y - ball.radius <= brick.pos_y + brick.height:
                brick.kill()
                ball.bounce(x_bounce=False, y_bounce=True)


ball = Ball(window_width // 2, window_height - 15, 7, 1, -1)
paddle = Paddle(((board_width // 2) - 2) * cell_size, window_height - 5, 5 * cell_size, window_width)
bricks = []

for row in range(brick_rows):
    counter = 0
    while counter < board_width:
        bricks.append(Brick(counter * cell_size, row * cell_size, 3 * cell_size, cell_size))
        counter += 3

# Game loop
running = True
start_time = time.time()
last_agent_call = time.time()
action_choice = 0
while running:

    # call the agent if passed as command line argument but only every second and not permanently for smooth gameplay
    if args.agent:
        if time.time() - last_agent_call >= 1:
            action_string, action_choice = adapter()
            print("action chosen by agent: " + str(action_string))
            last_agent_call = time.time()

            if action_choice == 0:
                pass
            elif action_choice == 1:
                paddle.moveLeft()
            elif action_choice == 2:
                paddle.moveRight()
            elif action_choice == 3:
                paddle.moveRightFast()
            elif action_choice == 4:
                paddle.moveLeftFast()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    if not args.agent:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and not args.agent:
                if event.key == pygame.K_LEFT:
                    paddle.moveLeft()
                elif event.key == pygame.K_RIGHT:
                    paddle.moveRight()
                elif event.key == pygame.K_UP:
                    paddle.moveRightFast()
                elif event.key == pygame.K_DOWN:
                    paddle.moveLeftFast()

    # Fill the background
    screen.fill(BLACK)

    # Draw the game board
    for row in range(board_height):
        for col in range(board_width):
            x = col * cell_size
            y = row * cell_size
            pygame.draw.rect(screen, WHITE, (x, y, cell_size - 1, cell_size - 1))

    # Draw additional elements (e.g., game pieces)
    ball.move()

    if checkGameWon(bricks=bricks):
        running = False
        printStats(won=True, time=time.time() - start_time, bricks=bricks)
    if checkGameOver(ball=ball):
        running = False
        printStats(won=False, time=time.time() - start_time, bricks=bricks)
    checkCollisionWithWalls(ball=ball)
    checkCollisionWithPaddle(paddle=paddle, ball=ball)
    checkCollisionWithBricks(bricks=bricks, ball=ball)

    # print(ball.pos_x)
    pygame.draw.circle(screen, RED, (ball.pos_x, ball.pos_y), ball.radius)
    pygame.draw.rect(screen, GREEN, (paddle.pos_x, paddle.pos_y, paddle.paddle_width, cell_size))

    for brick in bricks:
        if brick.alive:
            pygame.draw.rect(screen, BLUE, (brick.pos_x, brick.pos_y, brick.width - 1, brick.height - 1))

    # Update the display
    pygame.display.flip()
    time.sleep(0.01)

# Quit Pygame
pygame.quit()
