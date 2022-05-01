import numpy as np

from ursina import *

import physics

window.title = "Yet another Gravit"  # The window title
window.borderless = False  # Show a border
window.fullscreen = False  # Do not go Fullscreen
window.aspect_ratio = 4 / 3
window.vsync = False

camera.orthographic = False

# window.exit_button.visible = False      # Do not show the in-game red X that loses the window
# window.fps_counter.enabled = True       # Show the FPS (Frames per second) counter

app = Ursina()

base_mass = 1e-12
universe = physics.Universe(
    np.array(
        [
            physics.Particle(mass=base_mass, position=np.array([+2.0, +2.0])),
            #    physics.Particle(mass=base_mass, position=np.array([+2.0, -2.0])),
            #    physics.Particle(mass=base_mass, position=np.array([-2.0, +2.0])),
            physics.Particle(mass=base_mass, position=np.array([-2.0, -2.0])),
        ]
    ),
    constant=2,
)

particles = np.array(
    [
        Entity(model="sphere", color=color.orange, scale=2, position=p.position)
        for p in universe.particles
    ]
)

started = False
ZOOM_MULTIPLIER = 1.1


def input(key):
    global started

    if key == "space":
        started = not started

    if key == "scroll up":
        camera.fov = max(5.0, camera.fov / ZOOM_MULTIPLIER)
    if key == "scroll down":
        camera.fov = min(150.0, camera.fov * ZOOM_MULTIPLIER)


def update():
    if started:
        universe.tick(time.dt)
    # print(np.dstack((universe.particles, particles)))
    # all_positions = np.empty((2, 2))
    for particle, entity_particle in zip(universe.particles, particles):
        entity_particle.position = particle.position
        if started:
            print(particle)

    if mouse.left:
        camera.position -= mouse.velocity / (time.dt * 2) * camera.fov / 90


app.run()
