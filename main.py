from sys import exit

import numpy as np
import pygame
from pygame.locals import *

from camera import Camera
from constants import G, RESOLUTION, MOUSE_PROPULSION_INIT, MOUSE_PROPULSION_STEP, MOUSE_PROPULSION_MAX, FPS_CAP, BACKGROUND_COLOR, DEBUGGING
from physics import World
from player import Player
from utils import clamp

# initialisation des modules pygame
pygame.init()

# creation du joueur
player = Player()

# creation du monde
BOUND = 100.0
world = World.random(player, particle_number=100, constant=G, min_position=np.array([BOUND, BOUND]),
                     max_position=np.array([-BOUND, -BOUND]), max_mass=0.1)

# creation de la caméra
camera = Camera(RESOLUTION)

# initialisation de la fenetre
screen = pygame.display.set_mode(RESOLUTION)
clock = pygame.time.Clock()

# on cache la souris (curseur custom)
pygame.mouse.set_visible(False)

# on place la caméra à la position du joueur (instantanément, pas de smoothing)
camera.follow(player, smoothing=False)
player.mouse_attraction = MOUSE_PROPULSION_INIT

tick_physics = True
running = True
speed = 1
tick_player = False

while running:
    for ev in pygame.event.get():
        if ev.type == QUIT:
            pygame.quit()
            exit(0)
        if ev.type == KEYUP:
            if ev.key == K_SPACE:
                tick_physics = not tick_physics

        if ev.type == MOUSEBUTTONDOWN:
            if ev.button == 1:
                tick_player = True
            # 1 = left click; 2 = middle click; 3 = right click; 4 = scroll up; 5 = scroll down
            if ev.button == 4:
                player.mouse_attraction = clamp(0, player.mouse_attraction + MOUSE_PROPULSION_STEP, MOUSE_PROPULSION_MAX)
            if ev.button == 5:
                player.mouse_attraction = clamp(0, player.mouse_attraction - MOUSE_PROPULSION_STEP, MOUSE_PROPULSION_MAX)

    dt = clock.tick(FPS_CAP) / 1000

    player.mouse_position = camera.real_position_from_screen(pygame.mouse.get_pos())

    if tick_physics:
        screen.fill(BACKGROUND_COLOR)

        world.tick(dt / speed, tick_player)

        camera.follow(player)
        camera.tick(dt / speed)
    else:
        screen.fill(BACKGROUND_COLOR)

    player.display(screen, camera, dt)
    for particle in world:
        particle.display(screen, camera)
    player.display_mouse(screen, camera)

    if DEBUGGING:
        # green dot at (O, O) in the coordinate plane for debugging purposes
        pygame.draw.circle(screen, (0, 255, 0), camera.convert_position(np.array([0.0, 0.0])), 1)

        # yellow dot at the center of the screen for debugging purposes
        pygame.draw.circle(screen, (255, 255, 0), RESOLUTION / 2, 1)

    pygame.display.set_caption(f"FPS: {round(clock.get_fps(), 1)} - Speed: {player.velocity}")

    pygame.display.flip()
