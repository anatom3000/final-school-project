import numpy as np

from constants import BLACK_HOLE_MASS_MULTIPLIER, BLACK_HOLE_RADIUS, BLACK_HOLE_COLOR
from particle import Particle


class BlackHole(Particle):
    def __init__(self, mass: float, position: np.array = np.zeros(2)):
        super().__init__(mass=mass * BLACK_HOLE_MASS_MULTIPLIER, position=position, radius=BLACK_HOLE_RADIUS)
        self.color = BLACK_HOLE_COLOR

    @property
    def velocity(self):
        return np.zeros(2)

    @velocity.setter
    def velocity(self, value):
        pass  # the matrix is everywhere
