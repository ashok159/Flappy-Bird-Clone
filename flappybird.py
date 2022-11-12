# Ashok Surujdeo
# Flappy Bird Game in Python using Pygame

import pygame 
import random
import time
from settings import *
from pygame.locals import *

pygame.init()
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
framerate = pygame.time.Clock()

# Variables for the game
#sprites 
bg = pygame.image.load('media/background.png').convert_alpha()
ground = pygame.image.load('media/ground.png').convert_alpha()
bottom_pipe = pygame.image.load('media/pipe.png').convert_alpha()
top_pipe = pygame.transform.flip(bottom_pipe, False, True)
bird_sprite = pygame.image.load('media/bird.png').convert_alpha()
#sound effects
dead = pygame.mixer.Sound('media/dead.wav')
hit = pygame.mixer.Sound('media/hit.wav')
wing = pygame.mixer.Sound('media/wing.wav')
swoosh = pygame.mixer.Sound('media/swoosh.wav')
#font/pipe variables
font = pygame.font.SysFont('Arial', 30)
pipe_height = top_pipe.get_height()
pipe_width = top_pipe.get_width()
pipe_gap = 200
pipe_speed = 10

#game logic variables
done = False
jump = False
pipe = [500, 200]
bird_location = [50, WINDOW_HEIGHT/2.5]
bird_animation = 0
bird_velocity = 0
lives = 5
# Game loop
while not done:
    # Event loop
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                done = True
            if event.key == K_SPACE:
                jump = True
        if event.type == MOUSEBUTTONDOWN:
            jump = True
        if event.type == QUIT:
            done = True

    # Game logic
    #jumping logic
    if jump:
        bird_velocity = 20
        jump = False
        wing.play()
    bird_location[1] -= bird_velocity
    #gravity
    if bird_velocity > -10:
        bird_velocity -= 2
    pipe[0] -= pipe_speed
    #pipe reset, random pipe height/gaps
    if pipe[0] < -pipe_width:
        pipe[0] = WINDOW_WIDTH
        pipe[1] = random.randint(50, WINDOW_HEIGHT-150)
        pipe_gap = random.randint(100, 300)
    # Drawing
    window.fill((0, 0, 0))
    #background 
    window.blit(bg, (0, 0))
    #ground
    window.blit(ground, (0, 565))
    #lives counter
    label = font.render('Lives: ' + str(lives), 1, (255, 255, 255))
    window.blit(label, (5, 5))
    #pipes
    window.blit(top_pipe, (pipe[0], pipe[1] - pipe_height))
    window.blit(bottom_pipe, (pipe[0], pipe[1] + pipe_gap))
    #bird
    window.blit(bird_sprite, bird_location, (0, bird_animation*24, 34, 24))
    bird_animation = (bird_animation + 1) % 3
    #collision detection
    top_pipe_rect = top_pipe.get_rect(topleft=(pipe[0], pipe[1] - pipe_height))
    bottom_pipe_rect = bottom_pipe.get_rect(topleft=(pipe[0], pipe[1] + pipe_gap))
    bird_rect = Rect(bird_location[0], bird_location[1], 34, 24)
    if bird_rect.colliderect(top_pipe_rect) or bird_rect.colliderect(bottom_pipe_rect):
        lives -= 1
        bird_location = [50, WINDOW_HEIGHT/2.5]
        pipe[0] = WINDOW_WIDTH + pipe_speed*40
        pipe[1] = random.randint(50, WINDOW_HEIGHT-150)
        pipe_gap = random.randint(100, 300)
        if lives == 0:
            done = True
            dead.play()
        else:
            hit.play()
    # Update screen
    pygame.display.update()
    framerate.tick(55)

# Game over
time.sleep(1)
pygame.quit()
