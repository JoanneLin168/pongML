# Simple pygame program

# Import and initialize the pygame library
import random
import math
import statistics
import Make_Graph
import Paddle
import Ball

### INITATION ###
# NOTE: There is no input verification
gen = 0
num_of_gens = int(input("Enter the number of generations you want this program to run for (Minimum = 100): "))
max_score_per_gen = int(input("Enter the maximum score you want per generation: "))
create_file = True if (input("Do you want to save the results after the program has been run? Y/N").lower() == "y") else False
if create_file:
    filename = Make_Graph.create_file()

### SETUP ###
def reset(winners, gen_winners):
    new_paddles = []
    best = None
    prev_gen = False
    # If there is only one winner
    if len(winners) == 1:
        best = winners[0]
        gen_winners.append(best)
    # If there are several winners, use winner with highest fitness
    elif len(winners) > 1:
        best = winners[0]
        for winner in winners:
            winner_fitness = statistics.mean(winner.fitness)
            best_fitness = statistics.mean(best.fitness)
            if winner_fitness < best_fitness:
                best = winner
        gen_winners.append(best)
    # If there are no winners this generation, use previous winners coefficients
    elif (len(gen_winners) >= 1):
        best = gen_winners[-1:]
        prev_gen = True

    # If best is a paddle (retrieved from above code)
    if (best != None):
        for i in range(20):
            paddle = Paddle.Paddle()
            paddle.x = screen_width/2 - paddle.width/2
            paddle.y = screen_height - paddle.height - 20
            for j in range(len(paddle.coefficients)):
                mutation_chance = random.randint(1, 8) # 1 in 8 chance to mutate one coefficient
                if (mutation_chance == True):
                    paddle.coefficients[j] = round(best.coefficients[j] + (random.randint(-500, 500) / 10000), 4) # i.e. +- range 0.05
                else:
                    paddle.coefficients[j] = best.coefficients[j]
            new_paddles.append(paddle)
    # If the code above was unable to retrieve a paddle for best (i.e. when there have been zero winners)
    else:
        for i in range(20):
            paddle = Paddle.Paddle()
            paddle.x = screen_width/2 - paddle.width/2
            paddle.y = screen_height - paddle.height - 20
            new_paddles.append(paddle)

    if prev_gen:
        best = None
    return new_paddles, best

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

### GAME ###

running = True
score = 0
gen_winners = []
winners = []
hit_buffer = 0

# Run this code constantly
while running:
    # MACHINE LEARNING
    i = 0
    hit_paddle = False
    successful_paddles = []
    for paddle in paddles:
        inputs = [paddle.x, ball.x, ball.y]
        paddle_move = calculateOutput(inputs, paddle.coefficients)

        if (paddle_move == 0):
            paddle.x -= 5
        elif (paddle_move == 1):
            paddle.x += 5

        # Calculate distance to ball from paddle        
        distance_x = abs(paddle.x+(paddle.width)/2 - ball.x)
        distance_y = abs(paddle.y - ball.y)
        distance_to_ball = math.sqrt(distance_x**2 + distance_y**2)

        new_fitness = distance_to_ball
        paddle.fitness.append(new_fitness)
    
        if ((paddle.y-2 <= ball.y+ball.radius <= paddle.y+2) and (paddle.x <= ball.x <= paddle.x+paddle.width)):
            if (hit_buffer == 0):
                hit_paddle = True
                score += 1
                hit_buffer = 20
            if paddle not in successful_paddles:
                successful_paddles.append(paddle)

    ball.move(screen_width, screen_height, hit_paddle)

    if hit_paddle:
        winners = successful_paddles
        paddles = successful_paddles

    if (hit_buffer > 0):
        hit_buffer -= 1

    if (ball.y > paddle.y or score == max_score_per_gen):
        ball.x = screen_width/2
        ball.y = ball.radius + 20
        paddles, best = reset(winners, gen_winners)

        # Not using the best from this generation if none passed so that the next generation will use previously working genes (cheat method)
        if best == None:
            best = paddles[0]
            for paddle in paddles:
                paddle_fitness = statistics.mean(paddle.fitness)
                best_fitness = statistics.mean(best.fitness)
                if paddle_fitness < best_fitness:
                    best = paddle
        if create_file:
            Make_Graph.add_to_file(filename, best, score, len(winners))
        score = 0
        gen += 1
        if (gen <= num_of_gens):
            print("Progress: ", gen, "/", num_of_gens)

    if gen > num_of_gens:
        running = False
    

if create_file:
    Make_Graph.draw_graphs(filename)
