from math import sqrt, pi

import numpy as np
import pygame

from utils import Stringable

RADIUS_FACTOR = pi


class Particle(Stringable):
    def __init__(
            self,
            mass: float,
            position: np.array = np.array([0.0, 0.0]),
            velocity: np.array = np.array([0.0, 0.0]),
            acceleration: np.array = np.array([0.0, 0.0]),
            radius: float = None,
            color: tuple = (255, 255, 255)
    ):
        self.mass = mass
        self.position = position
        self.radius = RADIUS_FACTOR * sqrt(self.mass) if radius is None else radius

        self.velocity = velocity
        self.acceleration = acceleration
        self.forces = np.array([])
        self.has_colisioned = False

        self.color = color

    def display(self, surface: pygame.Surface, camera):
        pygame.draw.circle(surface, self.color, camera.convert_position(self.position),
                           camera.convert_radius(self.radius))

    def get_rect(self):
        return pygame.Rect(center=self.position, width=self.radius, height=self.radius)
