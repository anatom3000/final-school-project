from math import tanh

import numpy as np

from particle import Particle
from utils import Stringable, lerp

POSITION_SMOOTHING_SPEED = 5.0
ZOOM_SMOOTHING_SPEED = 0.5


class Camera(Stringable):
    def __init__(self, resolution: np.array, zoom: float = 2.0, position: np.array = None):
        self._position = np.array([0.0, 0.0]) if position is None else position
        self._zoom = zoom

        self._target_position = self._position
        self._target_zoom = self.zoom

        self.resolution = resolution

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value):
        self._target_position = value

    @property
    def zoom(self):
        return self._zoom

    @zoom.setter
    def zoom(self, value):
        self._target_zoom = value

    def move(self, deplacement: np.array):
        self.position += deplacement

    def zoom_in(self, delta: float):
        self.zoom *= delta
        self.position *= delta

    def zoom_out(self, delta: float):
        self.zoom /= delta
        self.position /= delta

    @staticmethod
    def _convert_velocity_to_zoom(velocity: np.array):
        # function made in Desmos
        # https://www.desmos.com/calculator/w9ns72ijq1
        x = np.linalg.norm(velocity)
        m = 0.16
        a = 0.1
        b = 0.47
        c = 0
        # return 5.0
        return 1 / (m * tanh(x / a + b)) + c

    def follow(self, particle: Particle, smoothing=True):
        if smoothing:
            self.position = self.zoom * particle.position
            self.zoom = Camera._convert_velocity_to_zoom(particle.velocity)
        else:
            self._position = self.zoom * particle.position
            self._zoom = Camera._convert_velocity_to_zoom(particle.velocity)

    def convert_position(self, position: np.array):
        return self.zoom * position + self.resolution / 2 - self.position

    def convert_radius(self, radius: float):
        return radius * self.zoom

    def real_position_from_screen(self, position):
        """
        Inverse function of convert_position.
        """
        return (position + self.position - self.resolution / 2) / self.zoom

    def tick(self, dt):
        self._position = lerp(self._position, self._target_position, dt*POSITION_SMOOTHING_SPEED)

        self._zoom = lerp(self._zoom, self._target_zoom, dt*ZOOM_SMOOTHING_SPEED)
