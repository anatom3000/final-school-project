from typing import Sequence

import numpy as np
import pygame


class Particle:
    def __init__(
            self,
            mass: float,
            position: np.array = np.zeros(2),
            velocity: np.array = np.zeros(2),
            color: Sequence = (255, 255, 255),
            radius: int = None
    ):

        # simulation related values
        self.mass = mass
        self.position = position
        self.velocity = velocity
        self.acceleration = np.zeros(2)
        self.resulting_force = np.zeros(2)
        self.radius = round(mass) if radius is None else radius

        # rendering related values
        self.color = color

    def __str__(self):
        return f"Particle(mass={self.mass}, position={self.position}, velocity={self.velocity}), acceleration={self.acceleration}, force={self.resulting_force}"

    def compute_state(self, dtime: float):
        self.acceleration = self.resulting_force / self.mass
        self.velocity = self.acceleration * dtime
        self.position += self.velocity * dtime

    def display(self, surface: pygame.Surface):
        pygame.draw.circle(surface, self.color, self.position, self.radius)
