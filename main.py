import numpy as np

np.seterr(all='raise')  # for debugging

import pygame
from pygame.locals import *

from sys import exit

import physics

<<<<<<< HEAD
RESOLUTION = (640, 480)

=======
window.title = "Yet another Gravit"  # The window title
window.borderless = False  # Show a border
window.fullscreen = False  # Do not go Fullscreen
window.aspect_ratio = 4 / 3

camera.orthographic = True

# window.exit_button.visible = False      # Do not show the in-game red X that loses the window
# window.fps_counter.enabled = True       # Show the FPS (Frames per second) counter

app = Ursina()

>>>>>>> parent of 75e08ca (refactored gravity but it doesn't work)
base_mass = 1
universe = physics.Universe(
    np.array(
        [
            physics.Particle(mass=base_mass, position=np.array([2.0, 2.0])),
            #    physics.Particle(mass=base_mass, position=np.array([+2.0, -2.0])),
            #    physics.Particle(mass=base_mass, position=np.array([-2.0, +2.0])),
            physics.Particle(mass=base_mass, position=np.array([0.0, 0.0])),
        ]
    ),
    constant=100,
)

pygame.init()

screen = pygame.display.set_mode(RESOLUTION)
clock = pygame.time.Clock()

running = True
while running:
    screen.fill((0,) * 3)
    for ev in pygame.event.get():
        if ev.type == QUIT:
            running = False

    pygame.display.flip()

    for particle in universe:
        particle.display(screen)

    dt = clock.tick() / 1000
    universe.tick(dt)

<<<<<<< HEAD
pygame.quit()
exit(0)
=======

def update():
    if started:
        universe.tick(time.dt)
    # print(np.dstack((universe.particles, particles)))
    # all_positions = np.empty((2, 2))
    for particle, entity_particle in zip(universe.particles, particles):
        entity_particle.position = particle.position
        print(particle)

    if mouse.left:
        camera.position -= mouse.velocity / (time.dt * 2) * camera.fov / 90


app.run()
>>>>>>> parent of 75e08ca (refactored gravity but it doesn't work)
