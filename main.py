import pygame
from typing import List
from math import hypot

from common import *
from particle import Particle

### Game Setup & Init
pygame.init()

# define screen
size = (WINDOW_WIDTH, WINDOW_WIDTH)
screen = pygame.display.set_mode(size)

# clock used to control how fast the game screen updates
clock = pygame.time.Clock()

positionClicked = (0, 0)
positionReleased = (0, 0)

particles: List[Particle] = []

### main game loop

carryOn = True
while carryOn:
    ## event loop & game logic
    for event in pygame.event.get():

        # exit the game
        if event.type == pygame.QUIT:
            carryOn = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == LEFT_MOUSE_BUTTON:
                positionClicked = (event.pos[0], event.pos[1])

        # create a particle
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == LEFT_MOUSE_BUTTON:
                positionReleased = (event.pos[0], event.pos[1])
                distance = min(max(hypot(abs(positionReleased[0] - positionClicked[0]), abs(positionReleased[1] - positionClicked[1])), 5), 100)
                particles.append(Particle(distance, positionReleased))

        elif event.type == pygame.MOUSEMOTION:
            pass

    # Update particle positions
    for particle in particles:
        particle.update(particles)

    # Clear the screen
    screen.fill(BLACK)

    # draw active pieces
    for particle in particles:
        particle.draw(screen)

    # update screen
    pygame.display.flip()

    # set clock rate
    clock.tick(TICKS_PER_SECOND)

pygame.quit()
