from sys import exit

import numpy as np
import pygame
from pygame.locals import *

from camera import Camera
from physics import World
from player import Player

BLACK = (0, 0, 0)
LIGHT_BLUE = (0, 0, 16)
RESOLUTION = np.array([960, 720])
BASE_MASS = 1
G = 1e2m

pygame.init()

player = Player(velocity=np.array((100.0, 0.0)))

BOUND = 100.0

world = World.random(player, particle_number=50, constant=G, min_position=np.array([BOUND, BOUND]),
                     max_position=np.array([-BOUND, -BOUND]), max_mass=0.1)

camera = Camera(RESOLUTION)
camera.zoom = 2.0

screen = pygame.display.set_mode(RESOLUTION)
clock = pygame.time.Clock()

tick_physics = False
running = True
speed = 1
while running:
    for ev in pygame.event.get():
        if ev.type == QUIT:
            pygame.quit()
            exit(0)
        if ev.type == KEYUP:
            if ev.key == K_SPACE: tick_physics = not tick_physics
            if ev.key == K_DOWN:
                speed -= 1
                if speed == 0: speed = -1
            if ev.key == K_UP:
                speed += 1
                if speed == 0: speed = 1

        if ev.type == MOUSEBUTTONDOWN:
            # 1 = left click; 2 = middle click; 3 = right click; 4 = scroll up; 5 = scroll down
            pass  # (for now)

    dt = clock.tick(60) / 1000

    screen.fill(BLACK)

    if tick_physics:
        world.tick(dt / speed)
        screen.fill(LIGHT_BLUE)

    camera.follow(player, offset=np.array([0, 0]))

    player.display(screen, camera)
    for particle in world:
        particle.display(screen, camera)

    # green dot at (O, O) for debugging purposes
    pygame.draw.circle(screen, (0, 255, 0), camera.convert_position(np.array([0.0, 0.0])), 1)

    pygame.display.set_caption(f"FPS: {round(clock.get_fps(), 1)} - Speed: {speed}")

    pygame.display.flip()
