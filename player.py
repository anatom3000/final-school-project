import numpy as np
import pygame

from particle import Particle

TRAIL_COLOR = 0.5
TRAIL_LENGHT = 8
USE_TRAIL = False
TRAIL_FREQUENCY = 0.08

MOUSE_COLOR = (0, 0, 255)


def draw_circle_alpha(surface, color, center, radius):
    target_rect = pygame.Rect(center, (0, 0)).inflate((radius * 2, radius * 2))
    shape_surf = pygame.Surface(target_rect.size, pygame.SRCALPHA)
    pygame.draw.circle(shape_surf, color, (radius, radius), radius)
    surface.blit(shape_surf, target_rect)


class Player(Particle):
    is_player = True

    def __init__(self, screen_resolution: np.array, position: np.array = np.array([0.0, 0.0]),
                 velocity: np.array = np.array([0.0, 0.0])):
        super().__init__(1e-16, position, radius=2.0, velocity=velocity)

        self.mouse_position = np.zeros(2)
        self.mouse_attraction = 0.0
        self.movement_cooldown = 0.0

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
        pass

    def display(self, surface: pygame.Surface, camera, dt: float = 0.0):
        self.last_trail_update += dt
        for i, position in enumerate(self.last_positions):
            draw_circle_alpha(surface, np.append(TRAIL_COLOR * self.color, (255 * (i + 1) / TRAIL_LENGHT)),
                              camera.convert_position(position), camera.convert_radius(self.radius))

        pygame.draw.circle(surface, self.color, camera.convert_position(self.position),
                           camera.convert_radius(self.radius))

        if self.last_trail_update > TRAIL_FREQUENCY:
            self.last_trail_update = 0.0  # we could just put a modulo but this can prevent potentail overflow errors if the game is running for too long
            self.last_positions.append(np.copy(self.position))
            self.last_positions = self.last_positions[-TRAIL_LENGHT:]

    def display_mouse(self, surface: pygame.Surface, camera):
        pygame.draw.circle(surface, MOUSE_COLOR, camera.convert_position(self.mouse_position),
                           self.mouse_attraction / 100, width=1)
