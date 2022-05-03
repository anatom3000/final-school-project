import numpy as np

from particle import Particle
from utils import Stringable

from math import tanh

VELOCITY_TO_ZOOM_FACTOR = 0.5


class Camera(Stringable):
    def __init__(self, resolution: np.array, zoom: float = 2.0, position: np.array = None):
        self.position = np.array([0.0, 0.0]) if position is None else position
        self.zoom = zoom
        self.resolution = resolution

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
        a = 20
        b = 0.47
        c = -1.7
        return 5.0
        #return 1 / (m * tanh(x / a + b)) + c

    # TODO: add smoothing. currently the camera is not smooth at all
    def follow(self, particle: Particle, offset: np.array = None):
        offset = self.resolution / 2 if offset is None else self.resolution / 2 + offset
        self.position = offset + self.zoom * particle.position - self.resolution / 2
        self.zoom = Camera._convert_velocity_to_zoom(particle.velocity)

    def convert_position(self, position: np.array):
        return self.zoom * position + self.resolution / 2 - self.position

    def convert_radius(self, radius: float):
        return radius * self.zoom
