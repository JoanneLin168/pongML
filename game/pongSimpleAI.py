# Simple pygame program

# Import and initialize the pygame library
import pygame
import paddle
import ball

### SETUP ###

pygame.init()

def show_score(screen, score):
    score_overlay = FONT.render('Score: '+str(score), True, FONT_COLOUR)
    screen.blit(score_overlay, (10, 5))

# FPS Counter
def show_fps(screen, clock):
    fps_overlay = FONT.render('FPS: '+str(int(clock.get_fps())), True, FONT_COLOUR)
    screen.blit(fps_overlay, (screen_width - 80, 5))

clock = pygame.time.Clock()
FPS = 60
FONT = pygame.font.SysFont("Arial", 20)
FONT_COLOUR = pygame.Color("white")

screen_width = 640
screen_height = 640

# Set up the drawing window
screen = pygame.display.set_mode([screen_width, screen_height])

ball = ball.Ball()
ball.x = screen_width/2
ball.y = ball.radius + 20

paddle = paddle.Paddle()
paddle.x = screen_width/2 - paddle.width/2
paddle.y = screen_height - paddle.height - 20

# Colour
ball_colour = (254,74,73)
paddle_colour = (254,215,102)
bg_colour = (69, 69, 69)

### GAME ###

# Run until the user asks to quit
running = True
score = 0
hit_buffer = 0
while running:
    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the background with white
    screen.fill(bg_colour)

    # Draw text
    
    show_fps(screen, clock)
    show_score(screen, score)

    # Draw a solid blue circle in the center
    # Parameters: screen, colour, position, radius
    pygame.draw.circle(screen, ball_colour, (ball.x, ball.y), ball.radius)
    pygame.draw.rect(screen, paddle_colour, (paddle.x, paddle.y, paddle.width, paddle.height))

    keys = pygame.key.get_pressed()

    if (paddle.x+(paddle.width/2) > ball.x and paddle.x >= 0):
        paddle.x -= paddle.speed
    if (paddle.x+(paddle.width/2) < ball.x and paddle.x+paddle.width <= screen_width):
        paddle.x += paddle.speed
    
    hit_paddle = False
    if ((paddle.y-2 <= ball.y+ball.radius <= paddle.y+2) and (paddle.x <= ball.x <= paddle.x+paddle.width)):
        if (hit_buffer == 0):
            hit_paddle = True
            score += 1
            hit_buffer = 20

    ball.move(screen_width, screen_height, hit_paddle)

    if (hit_buffer > 0):
        hit_buffer -= 1
    
    if ball.dx == 0 and ball.dy == 0:
        running = False
    clock.tick(FPS)
    # Flip the display
    pygame.display.flip()

# Done! Time to quit.
pygame.quit()
