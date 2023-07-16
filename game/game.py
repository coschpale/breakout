import pygame
import time
from ball import Ball
from paddle import Paddle
from brick import Brick

pygame.init

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
        elif ball.pos_x >= paddle.pos_x + (paddle.paddle_width // 5) and ball.pos_x < paddle.pos_x + 2 * (paddle.paddle_width // 5):
            ball.bounce_from_paddle(-1)
        elif ball.pos_x >= paddle.pos_x + 2 * (paddle.paddle_width // 5) and ball.pos_x < paddle.pos_x + 3 * (paddle.paddle_width // 5):
            ball.bounce_from_paddle(0)
        elif ball.pos_x >= paddle.pos_x + 3 * (paddle.paddle_width // 5) and ball.pos_x < paddle.pos_x + 4 * (paddle.paddle_width // 5):
            ball.bounce_from_paddle(1)
        elif ball.pos_x >= paddle.pos_x + 4 * (paddle.paddle_width // 5) and ball.pos_x - ball.radius < paddle.pos_x + paddle.paddle_width:
            ball.bounce_from_paddle(2)

def checkCollisionWithBricks(bricks, ball):
    for brick in bricks:
        if brick.alive:
            # bottom
            if ball.velocity_y < 0 and ball.pos_y - ball.radius == brick.pos_y + brick.height and ball.pos_x + ball.radius >= brick.pos_x and ball.pos_x - ball.radius <= brick.pos_x + brick.width:
                print("Hallo 1 " + str(ball.velocity_y))
                brick.kill()
                ball.bounce(x_bounce=True, y_bounce=False)
            # top
            elif ball.velocity_y > 0 and ball.pos_y + ball.radius == brick.pos_y and ball.pos_x + ball.radius >= brick.pos_x and ball.pos_x - ball.radius <= brick.pos_x + brick.width:
                print("Hallo 2 " + str(ball.velocity_y))
                brick.kill()
                ball.bounce(x_bounce=True, y_bounce=False)
            # right
            elif ball.velocity_x < 0 and ball.pos_x - ball.radius == brick.pos_x + brick.width and ball.pos_y + ball.radius >= brick.pos_y and ball.pos_y - ball.radius <= brick.pos_y + brick.height:
                print("Hallo 3 " + str(ball.velocity_y))
                brick.kill()
                ball.bounce(x_bounce=False, y_bounce=True)
            # left
            elif ball.velocity_x > 0 and ball.pos_x + ball.radius == brick.pos_x and ball.pos_y + ball.radius >= brick.pos_y and ball.pos_y - ball.radius <= brick.pos_y + brick.height:
                print("Hallo 4 " + str(ball.velocity_y))
                brick.kill()
                ball.bounce(x_bounce=False, y_bounce=True)

ball = Ball(window_width // 2, window_height-15, 7, 1, -1)
paddle = Paddle(((board_width // 2) -2)*cell_size, window_height-5, 5*cell_size, window_width)
bricks = []

for row in range(brick_rows):
    counter = 0
    while counter < board_width:
        bricks.append(Brick(counter * cell_size +1, row * cell_size +1, 3 * cell_size - 2, cell_size - 2))
        counter += 3

# Game loop
running = True
start_time = time.time()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                paddle.moveLeft()
            elif event.key == pygame.K_RIGHT:
                paddle.moveRight()

    # Fill the background
    screen.fill(BLACK)

    # Draw the game board
    for row in range(board_height):
        for col in range(board_width):
            x = col * cell_size
            y = row * cell_size
            pygame.draw.rect(screen, WHITE, (x, y, cell_size-1, cell_size-1))

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

    #print(ball.pos_x)
    pygame.draw.circle(screen, RED, (ball.pos_x, ball.pos_y), ball.radius)
    pygame.draw.rect(screen, GREEN, (paddle.pos_x, paddle.pos_y, paddle.paddle_width, cell_size))

    for brick in bricks:
        if brick.alive:
            pygame.draw.rect(screen, BLUE, (brick.pos_x, brick.pos_y, brick.width, brick.height))

    # Update the display
    pygame.display.flip()
    time.sleep(0.01)

# Quit Pygame
pygame.quit()