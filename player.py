import numpy as np

from particle import Particle


class Player(Particle):
    def __init__(self, position: np.array = np.array([0.0, 0.0])):
        super().__init__(2.0, position, radius=2.0, color=(255, 0, 0))
