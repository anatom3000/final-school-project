from sys import exit

import numpy as np
import pygame
from pygame.locals import *

from camera import Camera
from physics import World
from player import Player
from utils import clamp

BLACK = (0, 0, 0)
LIGHT_BLUE = (0, 0, 16)
RESOLUTION = np.array([960, 720])
PROPULSION_INIT = 0.005
PROPULSION_STEP = 0.005
PROPULSION_MAX = 0.1
BASE_MASS = 1
G = 1e5

DEBUGGING = False

pygame.init()

player = Player(screen_resolution=RESOLUTION, velocity=np.array((100.0, 0.0)))

BOUND = 100.0

world = World.random(player, particle_number=100, constant=G, min_position=np.array([BOUND, BOUND]),
                     max_position=np.array([-BOUND, -BOUND]), max_mass=0.1)

camera = Camera(RESOLUTION)

screen = pygame.display.set_mode(RESOLUTION)
clock = pygame.time.Clock()

camera.follow(player, smoothing=False)
player.mouse_attraction = PROPULSION_INIT
player.movement_cooldown = 5.0

tick_physics = False
running = True
speed = 1

while running:
    for ev in pygame.event.get():
        if ev.type == QUIT:
            pygame.quit()
            exit(0)
        if ev.type == KEYUP:
            if ev.key == K_SPACE:
                tick_physics = not tick_physics

            if ev.key == K_DOWN:
                pass
            if ev.key == K_UP:
                pass
            if ev.key == K_LEFT:
                pass
            if ev.key == K_RIGHT:
                pass
        if ev.type == MOUSEBUTTONDOWN:
            # 1 = left click; 2 = middle click; 3 = right click; 4 = scroll up; 5 = scroll down
            if ev.button == 4:
                player.mouse_attraction = clamp(0, player.mouse_attraction + PROPULSION_STEP, PROPULSION_MAX)
            if ev.button == 5:
                player.mouse_attraction = clamp(0, player.mouse_attraction - PROPULSION_STEP, PROPULSION_MAX)

    dt = clock.tick(60) / 1000

    if tick_physics:
        screen.fill(LIGHT_BLUE)
        if player.movement_cooldown == 0:
            player.mouse_position = camera.real_position_from_screen(pygame.mouse.get_pos())

        world.tick(dt / speed)

        camera.follow(player)
        camera.tick(dt / speed)
    else:
        screen.fill(BLACK)

    player.display(screen, camera)
    for particle in world:
        particle.display(screen, camera)

    if DEBUGGING:
        # green dot at (O, O) in the coordinate plane for debugging purposes
        pygame.draw.circle(screen, (0, 255, 0), camera.convert_position(np.array([0.0, 0.0])), 1)

        # yellow dot at the center of the screen for debugging purposes
        pygame.draw.circle(screen, (255, 255, 0), RESOLUTION / 2, 1)

    pygame.display.set_caption(f"FPS: {round(clock.get_fps(), 1)} - Speed: {speed}")

    pygame.display.flip()
