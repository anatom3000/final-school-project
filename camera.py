import numpy as np


class Camera:
    def __init__(self, resolution: np.array, zoom: float = 2.0, position: np.array = None):
        self.position = None
        self.resolution = resolution

        self.default_zoom = zoom
        self.default_position = np.array([0.0, 0.0]) if position is None else position
        self.home()

        self.moving = False


    def home(self):
        self.position = self.default_position
        self.zoom = self.default_zoom

    def move(self, deplacement):
        self.position += deplacement

    def zoom_in(self, delta):
        self.zoom *= delta
        self.position *= delta

    def zoom_out(self, delta):
        self.zoom /= delta
        self.position /= delta

    def convert_position(self, position):
        return self.zoom * position + self.resolution / 2 - self.position

    def convert_radius(self, radius):
        return radius * self.zoom
