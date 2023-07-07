import pygame
import time
from ball import Ball

pygame.init

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)


# Set the dimensions of the game board
board_width = 10
board_height = 15

window_width = board_width * 25
window_height = board_height * 25
window_size = (window_width, window_height)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("Game Board")
cell_size = 25
print(cell_size)

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

ball = Ball(window_width // 2, window_height-6, 5, 1, -1)

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

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
    ball.move()
    #print(ball.pos_x)
    pygame.draw.circle(screen, RED, (ball.pos_x, ball.pos_y), ball.radius)

    # Update the display
    pygame.display.flip()
    time.sleep(0.01)

# Quit Pygame
pygame.quit()