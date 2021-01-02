import random

class Paddle:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.speed = 10
        self.width = 100
        self.height = 10
        self.fitness = []
        self.coefficients = [0,0,0,0]
        for i in range(len(self.coefficients)):
            self.coefficients[i] = random.randint(0, 9999) / 10000