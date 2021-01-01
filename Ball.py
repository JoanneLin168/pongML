import math

class Ball:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.dx = 5
        self.dy = 5
        self.speed = math.sqrt(self.dx**2 + self.dy**2)
        self.radius = 10

    def move(self, screen_width, screen_height, hit_board):
        self.x += self.dx
        self.y += self.dy
        if (self.x <= 0+self.radius or self.x >= screen_width-self.radius): # accounts for the edge of the ball rather than the centre
            self.dx = -self.dx
        elif (self.y <= 0+self.radius or hit_board):
            self.dy = -self.dy
        elif (self.y >= screen_height-self.radius):
            self.dx = 0
            self.dy = 0