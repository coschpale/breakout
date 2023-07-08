DISTANCE = 5


class Paddle:
    def __init__(self, pos_x, pos_y, paddle_width, window_width):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.paddle_width = paddle_width
        self.max_width = window_width

    def moveRight(self):
        if self.pos_x + DISTANCE + self.paddle_width <= self.max_width:
            self.pos_x += DISTANCE

        return self.pos_x

    def moveLeft(self):
        if self.pos_x - DISTANCE >= 0:
            self.pos_x -= DISTANCE

        return self.pos_x

    def moveRightFast(self):
        if self.pos_x + DISTANCE*2 + self.paddle_width <= self.max_width:
            self.pos_x += DISTANCE*2

        return self.pos_x

    def moveLeftFast(self):
        if self.pos_x - DISTANCE*2 >= 0:
            self.pos_x -= DISTANCE*2

        return self.pos_x

    def paddle_location(self):
        return self.pos_x
