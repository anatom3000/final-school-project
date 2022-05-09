import numpy as np

from particle import Particle


class Player(Particle):
    def __init__(self, position: np.array = np.array([0.0, 0.0]), velocity: np.array = np.array([0.0, 0.0])):
        super().__init__(1e-16, position, radius=2.0, color=(255, 0, 0), velocity=velocity, is_joueur=True)
        self.moteur = np.array([0, 0])