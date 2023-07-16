class Ball:
    def __init__(self, pos_x, pos_y, radius, velocity_x, velocity_y):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.radius = radius
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y

    def move(self):
        self.pos_x += self.velocity_x
        self.pos_y += self.velocity_y

    def bounce(self, x_bounce, y_bounce):
        if x_bounce:
            self.velocity_y *= -1
        if y_bounce:
            self.velocity_x *= -1

    def bounce_from_paddle(self, velocity_x):
        self.velocity_y *= -1
        self.velocity_x = velocity_x

    def ball_location(self):
        return self.pos_x, self.pos_y

    def ball_velocity(self):
        return self.velocity_x, self.velocity_y
