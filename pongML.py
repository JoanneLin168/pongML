# Simple pygame program

# Import and initialize the pygame library
import pygame
import random
import math
import Make_Graph
import Paddle
import Ball

### SETUP ###
pygame.init()
filename = Make_Graph.create_file()

clock = pygame.time.Clock()
FPS = 2000
FONT = pygame.font.SysFont("Arial", 20)
BLACK = pygame.Color("black")

# Score Counter
def show_score(screen, score):
    score_overlay = FONT.render('Score: '+str(score), True, BLACK)
    screen.blit(score_overlay, (10, 5))

# FPS Counter
def show_fps(screen, clock):
    fps_overlay = FONT.render('FPS: '+str(int(clock.get_fps())), True, BLACK)
    screen.blit(fps_overlay, (screen_width - 80, 5))

# Paddle Counter
def show_paddle_count(screen, paddles):
    paddle_overlay = FONT.render('Paddle Count: '+str(len(paddles)), True, BLACK)
    screen.blit(paddle_overlay, (10, 30))

# Generation Counter
def show_generation(screen, gen_winners):
    paddle_overlay = FONT.render('Generation: '+str(len(gen_winners)+1), True, BLACK)
    screen.blit(paddle_overlay, (10, 55))

def reset(winners, gen_winners):
    new_paddles = []
    best = None
    # If there is only one winner
    if len(winners) == 1:
        best = winners[0]
        gen_winners.append(best)
    # If there are several winners, use winner with highest fitness
    elif len(winners) > 1:
        best = winners[0]
        for winner in winners:
            if winner.fitness > best.fitness:
                best = winner
        gen_winners.append(best)
    # If there are no winners this generation, use previous winners coefficients
    elif (len(gen_winners) >= 1):
        best = gen_winners[-1:]

    # If best is a paddle (retrieved from above code)
    if (best != None):
        for i in range(20):
            paddle = Paddle.Paddle()
            paddle.x = screen_width/2 - paddle.width/2
            paddle.y = screen_height - paddle.height - 20
            for j in range(len(paddle.coefficients)):
                paddle.coefficients[j] = round(best.coefficients[j] + (random.randint(-2000, 2000) / 10000), 4)
            new_paddles.append(paddle)
    # If the code above was unable to retrieve a paddle for best (i.e. when there have been zero winners)
    else:
        for i in range(20):
            paddle = Paddle.Paddle()
            paddle.x = screen_width/2 - paddle.width/2
            paddle.y = screen_height - paddle.height - 20
            new_paddles.append(paddle)
    return new_paddles, best

def calculateOutput(inputs, coefficients):
    outputs = []
    for i in range(len(inputs)):
        outputs.append(inputs[i] * coefficients[i])
    outputs_max = max(outputs)
    index_max = outputs.index(outputs_max)
    return index_max

### GAME ###
screen_width = 640
screen_height = 640

screen = pygame.display.set_mode([screen_width, screen_height])

# Set up ball
ball = Ball.Ball()
ball.x = screen_width/2
ball.y = ball.radius + 20

# Set up paddles
paddles = []
for i in range(20):
    paddle = Paddle.Paddle()
    paddle.x = screen_width/2 - paddle.width/2
    paddle.y = screen_height - paddle.height - 20
    paddles.append(paddle)

running = True
score = 0
gen_winners = []
winners = []
hit_buffer = 0

# Run this code constantly
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the background with white
    screen.fill((255, 255, 255))

    # Draw text
    show_fps(screen, clock)
    show_score(screen, score)
    show_paddle_count(screen, paddles)
    show_generation(screen, gen_winners)

    # Draw a solid blue circle in the center
    # Parameters: screen, colour, position, radius
    pygame.draw.circle(screen, (255, 0, 0), (ball.x, ball.y), ball.radius)
    for i in range(len(paddles)):
        pygame.draw.rect(screen, (255,255,0), (paddles[i].x, paddles[i].y, paddles[i].width, paddles[i].height))

    keys = pygame.key.get_pressed()

    # MACHINE LEARNING
    i = 0
    hit_paddle = False
    successful_paddles = []
    for paddle in paddles:
        inputs = [paddle.x, ball.x, ball.y, ball.dx]
        paddle_move = calculateOutput(inputs, paddle.coefficients)

        if (paddle_move == 0):
            paddle.x -= 5
        elif (paddle_move == 1):
            paddle.x += 5
    
        if ((paddle.y-2 <= ball.y+ball.radius <= paddle.y+2) and (paddle.x <= ball.x <= paddle.x+paddle.width)):
            if (hit_buffer == 0):
                hit_paddle = True
                score += 1
                hit_buffer = 20
            if paddle not in successful_paddles:
                distance_x = abs(paddle.x+(paddle.width)/2 - ball.x)
                distance_y = abs(paddle.y - ball.y)
                distance_to_ball = math.sqrt(distance_x**2 + distance_y**2)
                paddle.fitness = 100 - distance_to_ball
                successful_paddles.append(paddle)

    ball.move(screen_width, screen_height, hit_paddle)

    if hit_paddle:
        winners = successful_paddles
        paddles = successful_paddles

    if (hit_buffer > 0):
        hit_buffer -= 1

    if (ball.y > paddle.y or score == 10):
        ball.x = screen_width/2
        ball.y = ball.radius + 20
        paddles, best = reset(winners, gen_winners)
        Make_Graph.add_to_file(filename, best, score, len(winners))
        score = 0

    if len(gen_winners) >= 1000:
        running = False
    
    clock.tick(FPS)
    # Flip the display
    pygame.display.flip()

# Done! Time to quit.
pygame.quit()

Make_Graph.draw_graphs(filename)