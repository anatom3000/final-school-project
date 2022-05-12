from math import sqrt
from random import randint

import numpy as np
import pygame

from constants import PARTICLE_MASS_TO_RADIUS_FACTOR, MAX_PARTICLE_MASS
from utils import Stringable


class Particle(Stringable):
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
        self.radius = PARTICLE_MASS_TO_RADIUS_FACTOR * sqrt(self.mass) if radius is None else radius

        self.velocity = velocity
        self.acceleration = acceleration
        self.forces = np.array([])
        self.to_delete = False

        self.color = (randint(0, 255), randint(0, 255), randint(0, 255)) if color is None else color

    def display(self, surface: pygame.Surface, camera):
        pygame.draw.circle(surface, self.color, camera.convert_position(self.position),
                           camera.convert_radius(self.radius))

    def merge(self, other):
        new_mass = self.mass + other.mass
        self.position = (self.position * self.mass + other.position * other.mass) / new_mass
        self.velocity = (self.velocity * self.mass + other.velocity * other.mass) / new_mass
        self.mass = min(MAX_PARTICLE_MASS, new_mass)
        self.radius = PARTICLE_MASS_TO_RADIUS_FACTOR * sqrt(self.mass)
        return self
