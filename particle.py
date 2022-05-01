import numpy as np
import pygame


class Particle:
    def __init__(
            self,
            mass: float,
            position: np.array = np.array([0.0, 0.0]),
            velocity: np.array = np.array([0.0, 0.0]),
            acceleration: np.array = np.array([0.0, 0.0])
    ):
        self.mass = mass
        self.position = position
        self.radius = 10

        self.velocity = velocity
        self.acceleration = acceleration
        self.forces = np.array([])

        self.color = (255, 255, 255)

    def __str__(self):
        return f"Particle(mass={self.mass}, position={self.position}, velocity={self.velocity}), acceleration={self.acceleration}"

    def display(self, surface, camera):
        pygame.draw.circle(surface, self.color, camera.convert_position(self.position),
                           camera.convert_radius(self.radius))
