import numpy as np
from particle import Particle


class Player(Particle):
    is_player = True

    def __init__(self, position: np.array = np.array([0.0, 0.0]), velocity: np.array = np.array([0.0, 0.0])):
        super().__init__(1e-16, position, radius=2.0, velocity=velocity)
        self.mouse_position = np.zeros(2)
        self.mouse_attraction = 0.0
        self.movement_cooldown = 0.0
        self._colors = {
            "idle": (255, 0, 0),
            "disoriented": (255, 0, 64)
        }


    @property
    def color(self):
        if self.movement_cooldown > 0:
            return self._colors["disoriented"]
        else:
            return self._colors["idle"]

    @color.setter
    def color(self, value):
        pass
