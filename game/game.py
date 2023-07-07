import pygame
import time
from ball import Ball
from paddle import Paddle

pygame.init

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)


# Set the dimensions of the game board
board_width = 10
board_height = 15

cell_size = 25
window_width = board_width * cell_size
window_height = board_height * cell_size
window_size = (window_width, window_height)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("Game Board")

def checkCollisionWithWalls(ball):

    if ball.pos_x <= ball.radius or ball.pos_x >= window_width - ball.radius:
        ball.bounce(x_bounce=False, y_bounce=True)
    
    if ball.pos_y <= ball.radius:
        ball.bounce(x_bounce=True, y_bounce=False)

def checkGameOver(ball):
    if ball.pos_y >= window_height - ball.radius:
        return True
    else:
        return False
    
def checkCollisionWithPaddle(paddle, ball):
    if ball.pos_y == window_height - (ball.radius + 5):
        if ball.pos_x >= paddle.pos_x and ball.pos_x < paddle.pos_x + (paddle.paddle_width // 5):
            ball.bounce_from_paddle(-2)
        elif ball.pos_x >= paddle.pos_x + (paddle.paddle_width // 5) and ball.pos_x < paddle.pos_x + 2 * (paddle.paddle_width // 5):
            ball.bounce_from_paddle(-1)
        elif ball.pos_x >= paddle.pos_x + 2 * (paddle.paddle_width // 5) and ball.pos_x < paddle.pos_x + 3 * (paddle.paddle_width // 5):
            ball.bounce_from_paddle(0)
        elif ball.pos_x >= paddle.pos_x + 3 * (paddle.paddle_width // 5) and ball.pos_x < paddle.pos_x + 4 * (paddle.paddle_width // 5):
            ball.bounce_from_paddle(1)
        elif ball.pos_x >= paddle.pos_x + 4 * (paddle.paddle_width // 5) and ball.pos_x < paddle.pos_x + paddle.paddle_width:
            ball.bounce_from_paddle(2)
    

ball = Ball(window_width // 2, window_height-15, 5, 1, -1)
paddle = Paddle(((board_width // 2) -2)*25, window_height-5, 125, window_width)

# Game loop
running = True
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

    if checkGameOver(ball=ball):
        running = False
    checkCollisionWithWalls(ball=ball)
    checkCollisionWithPaddle(paddle=paddle, ball=ball)
    ball.move()
    #print(ball.pos_x)
    pygame.draw.circle(screen, RED, (ball.pos_x, ball.pos_y), ball.radius)
    pygame.draw.rect(screen, GREEN, (paddle.pos_x, paddle.pos_y, 125, 10))

    # Update the display
    pygame.display.flip()
    time.sleep(0.01)

# Quit Pygame
pygame.quit()