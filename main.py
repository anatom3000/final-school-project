import numpy as np

from sys import exit

import pygame
from pygame.locals import *

from physics import Universe
from camera import Camera
from particle import Particle
from player import Player

BLACK = (0, 0, 0)
LIGHT_BLUE = (0, 0, 16)
RESOLUTION = np.array([640, 480])
BASE_MASS = 1

pygame.init()

player = Player()

universe = Universe(
    np.array(
        [
            player,  # thanks, Python
            Particle(mass=BASE_MASS, position=np.array([5.0, 0.0])),
        ],
    ),
    constant=100
)

camera = Camera(RESOLUTION)

screen = pygame.display.set_mode(RESOLUTION)
clock = pygame.time.Clock()

tick_physics = False
running = True
while running:
    for ev in pygame.event.get():
        if ev.type == QUIT:
            pygame.quit()
            exit(0)
        if ev.type == KEYUP:
            if ev.key == K_SPACE:
                tick_physics = not tick_physics

        if ev.type == MOUSEBUTTONDOWN:
            # 1 = left click; 2 = middle click; 3 = right click; 4 = scroll up; 5 = scroll down
            if ev.button == 1:
                camera.moving = True

    dt = clock.tick(60) / 1000

    screen.fill(BLACK)

    if True:
        universe.tick(dt)
        screen.fill(LIGHT_BLUE)

    camera.follow(player, offset=np.array([0, 0]))

    for particle in universe:
        particle.display(screen, camera)
    player.display(screen, camera)

    pygame.draw.circle(screen, (0, 255, 0), camera.convert_position(np.array([0.0, 0.0])), 1)

    pygame.display.set_caption(f"FPS: {round(clock.get_fps(), 1)}")

    pygame.display.flip()
