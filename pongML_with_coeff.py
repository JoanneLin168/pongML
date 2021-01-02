# Simple pygame program

# Import and initialize the pygame library
import pygame
import random
import math
import statistics
import Make_Graph
import Paddle
import Ball

### INITATION ###
# NOTE: There is no input verification
max_score = int(input("Enter the maximum score you want per generation: "))

### SETUP ###
# Score Counter
def show_score(screen, score):
    score_overlay = FONT.render('Score: '+str(score), True, FONT_COLOUR)
    screen.blit(score_overlay, (10, 5))

# FPS Counter
def show_fps(screen, clock):
    fps_overlay = FONT.render('FPS: '+str(int(clock.get_fps())), True, FONT_COLOUR)
    screen.blit(fps_overlay, (screen_width - 80, 5))

# Paddle Counter
def show_paddle_count(screen, paddles):
    paddle_overlay = FONT.render('Paddle Count: '+str(len(paddles)), True, FONT_COLOUR)
    screen.blit(paddle_overlay, (10, 30))

def calculateOutput(inputs, coefficients):
    outputs = []
    for i in range(len(inputs)):
        outputs.append(inputs[i] * coefficients[i])
    outputs_max = max(outputs)
    index_max = outputs.index(outputs_max)
    return index_max

# Setting up actual game
screen_width = 640
screen_height = 640

screen = pygame.display.set_mode([screen_width, screen_height])

# Set up ball
ball = Ball.Ball()
ball.x = screen_width/2
ball.y = ball.radius + 20

# Set up paddle
paddle = Paddle.Paddle()
paddle.x = screen_width/2 - paddle.width/2
paddle.y = screen_height - paddle.height - 20
paddle.coefficients[0] = float(input("Enter paddle x coefficient: "))
paddle.coefficients[1] = float(input("Enter ball x coefficient: "))
paddle.coefficients[2] = float(input("Enter ball y coefficient: "))
paddle.coefficients[3] = float(input("Enter ball speed coefficient: "))

### GAME ###
pygame.init()

clock = pygame.time.Clock()
FPS = 120
FONT = pygame.font.SysFont("Arial", 20)
FONT_COLOUR = pygame.Color("white")

# Colour
ball_colour = (254,74,73)
paddle_colour = (254,215,102)
bg_colour = (69, 69, 69)

running = True
score = 0
hit_buffer = 0

# Run this code constantly
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the background with white
    screen.fill(bg_colour)

    # Draw text
    show_fps(screen, clock)
    show_score(screen, score)

    # Draw a solid blue circle in the centre
    # Parameters: screen, colour, (pos x of centre, pos y of centre), radius
    pygame.draw.circle(screen, ball_colour, (ball.x, ball.y), ball.radius)

    # Draw a solid yellow rectangle from the top-left corner
    # Parameters: screen, colour, (pos x of corner, pos y of corner, width, height)
    pygame.draw.rect(screen, paddle_colour, (paddle.x, paddle.y, paddle.width, paddle.height))

    keys = pygame.key.get_pressed()

    # MACHINE LEARNING
    i = 0
    inputs = [paddle.x, ball.x, ball.y, ball.dx]
    paddle_move = calculateOutput(inputs, paddle.coefficients)

    if (paddle_move == 0):
        paddle.x -= 5
    elif (paddle_move == 1):
        paddle.x += 5

    hit_paddle = False
    if ((paddle.y-2 <= ball.y+ball.radius <= paddle.y+2) and (paddle.x <= ball.x <= paddle.x+paddle.width)):
        if (hit_buffer == 0):
            hit_paddle = True
            score += 1
            hit_buffer = 20

    ball.move(screen_width, screen_height, hit_paddle)

    if (hit_buffer > 0):
        hit_buffer -= 1

    if (ball.y > paddle.y or score == max_score):
        running = False
        score = 0
    
    clock.tick(FPS)
    # Flip the display
    pygame.display.flip()

# Done! Time to quit.
pygame.quit()