import numpy as np

from sys import exit

import pygame
from pygame.locals import *

import physics
from camera import Camera
from particle import Particle

BLACK = (0, 0, 0)
RESOLUTION = np.array([640, 480])
CAMERA_STEP = 1

pygame.init()

base_mass = 1
universe = physics.Universe(
    np.array(
        [
            Particle(mass=base_mass, position=np.array([100.0, 190.0])),
            Particle(mass=base_mass, position=np.array([100.0, 200.0])),
            Particle(mass=base_mass, position=np.array([0.0, 0.0])),
            Particle(mass=base_mass, position=np.array([200.0, 200.0])),
        ]
    ),
    constant=1e9
)

screen = pygame.display.set_mode(RESOLUTION)
camera = Camera(RESOLUTION)

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
            if ev.button == 4:
                camera.zoom_in(1.1)
            if ev.button == 5:
                camera.zoom_out(1.1)

        if ev.type == pygame.MOUSEBUTTONUP:
            camera.moving = False

        if ev.type == pygame.MOUSEMOTION:
            if camera.moving:
                camera.move(-np.array(ev.rel))
    dt = clock.tick() / 1000

    screen.fill(BLACK)

    if tick_physics:
        universe.tick(dt)

    for particle in universe:
        particle.display(screen, camera)

    pygame.display.flip()
