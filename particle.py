import numpy as np
import pygame

from utils import Stringable


class Particle(Stringable):
    def __init__(
            self,
            mass: float,
            position: np.array = np.array([0.0, 0.0]),
            velocity: np.array = np.array([0.0, 0.0]),
            acceleration: np.array = np.array([0.0, 0.0]),
            radius: float = 1.0,
            color: tuple = (255, 255, 255)
    ):
        self.mass = mass
        self.position = position
        self.radius = radius

        self.velocity = velocity
        self.acceleration = acceleration
        self.forces = np.array([])

        self.color = color

    def display(self, surface: pygame.Surface, camera):
        pygame.draw.circle(surface, self.color, camera.convert_position(self.position),
                           camera.convert_radius(self.radius))
