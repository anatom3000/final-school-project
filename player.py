import numpy as np
import pygame

from constants import PLAYER_TRAIL_COLOR, PLAYER_TRAIL_LENGHT, PLAYER_TRAIL_DENSITY, MOUSE_CURSOR_COLOR
from particle import Particle
from utils import draw_circle_alpha


class Player(Particle):
    def __init__(self, position: np.array = np.array([0.0, 0.0]),
                 velocity: np.array = np.array([0.0, 0.0])):
        super().__init__(1e-16, position, radius=3.0, velocity=velocity)

        self.mouse_position = np.zeros(2)
        self.mouse_attraction = 0.0
        self.movement_cooldown = 0.0
        
        self.noclip = False

        self._colors = {
            "idle": np.array([255, 0, 0]),
            "disoriented": np.array([255, 0, 64])
        }

        self.last_positions = []

        self.last_trail_update = 0

    @property
    def color(self):
        if self.movement_cooldown > 0:
            return self._colors["disoriented"]
        else:
            return self._colors["idle"]

    @color.setter
    def color(self, value):
        pass  # control is an illusion

    def display(self, surface: pygame.Surface, camera, dt: float = 0.0):
        self.last_trail_update += dt
        for i, position in enumerate(self.last_positions):
            draw_circle_alpha(surface,
                              np.append(PLAYER_TRAIL_COLOR * self.color, (255 * (i + 1) / PLAYER_TRAIL_LENGHT)),
                              camera.convert_position(position), camera.convert_radius(self.radius))

        pygame.draw.circle(surface, self.color, camera.convert_position(self.position),
                           camera.convert_radius(self.radius))

        if self.last_trail_update > PLAYER_TRAIL_DENSITY:
            self.last_trail_update = 0.0  # we could just put a modulo but this can prevent potentail overflow errors if the game is running for too long
            self.last_positions.append(np.copy(self.position))
            self.last_positions = self.last_positions[-PLAYER_TRAIL_LENGHT:]

    def display_mouse(self, surface: pygame.Surface, camera):
        pygame.draw.circle(surface, MOUSE_CURSOR_COLOR, camera.convert_position(self.mouse_position),
                           self.mouse_attraction / 100, width=1)
