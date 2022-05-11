from math import sqrt

import numpy as np
import pygame

from utils import Stringable

from random import randint

RADIUS_FACTOR = np.pi
MAX_MASS = 20.0


class Particle(Stringable):
    is_player = False

    def __init__(
            self,
            mass: float,
            position: np.array = np.zeros(2),
            velocity: np.array = np.zeros(2),
            acceleration: np.array = np.zeros(2),
            radius: float = None,
            color: tuple = None
    ):
        self.mass = mass
        self.position = position
        self.radius = RADIUS_FACTOR * sqrt(self.mass) if radius is None else radius

        self.velocity = velocity
        self.acceleration = acceleration
        self.forces = np.array([])
        self.merged = False
        self.away_from_player = False

        self.color = (randint(0, 255), randint(0, 255), randint(0, 255)) if color is None else color

    def display(self, surface: pygame.Surface, camera):

        pygame.draw.circle(surface, self.color, camera.convert_position(self.position),
                           camera.convert_radius(self.radius))

    def get_rect(self):
        return pygame.Rect(center=self.position, width=self.radius, height=self.radius)

    def merge(self, other):
        new_mass = self.mass + other.mass
        self.position = (self.position * self.mass + other.position * other.mass) / new_mass
        self.velocity = (self.velocity * self.mass + other.velocity * other.mass) / new_mass
        self.mass = min(MAX_MASS, new_mass)
        self.radius = RADIUS_FACTOR * sqrt(self.mass)
        return self
