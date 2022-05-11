import numpy as np
import pygame

from particle import Particle

TRAIL_COLOR = (0, 255, 0)
TRAIL_SIZE = 1.0
USE_TRAIL = False

MOUSE_COLOR = (0, 0, 255)


class Player(Particle):
    is_player = True

    def __init__(self, screen_resolution: np.array, position: np.array = np.array([0.0, 0.0]),
                 velocity: np.array = np.array([0.0, 0.0])):
        super().__init__(1e-16, position, radius=2.0, velocity=velocity)
        self.mouse_position = np.zeros(2)
        self.mouse_attraction = 0.0
        self.movement_cooldown = 0.0
        self._colors = {
            "idle": (255, 0, 0),
            "disoriented": (255, 0, 64)
        }

        self.transparent_surface = pygame.Surface(screen_resolution, pygame.SRCALPHA)

    @property
    def color(self):
        if self.movement_cooldown > 0:
            return self._colors["disoriented"]
        else:
            return self._colors["idle"]

    @color.setter
    def color(self, value):
        pass

    def display(self, surface: pygame.Surface, camera, background_color: tuple = (255, 255, 255)):
        self.transparent_surface.fill((255, 255, 255, 244), special_flags=pygame.BLEND_RGBA_MULT)

        on_screen_radius = camera.convert_radius(self.radius)
        particle_surface = pygame.Surface((on_screen_radius * 2, on_screen_radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(particle_surface, self.color, (on_screen_radius, on_screen_radius), on_screen_radius)

        if USE_TRAIL:
            trail_radius = on_screen_radius * TRAIL_SIZE
            trail_surface = pygame.Surface((2 * trail_radius, 2 * trail_radius), pygame.SRCALPHA)
            pygame.draw.circle(trail_surface, TRAIL_COLOR, (trail_radius, trail_radius), on_screen_radius * TRAIL_SIZE)
            self.transparent_surface.blit(trail_surface,
                                          trail_surface.get_rect(center=camera.convert_position(self.position)))

        self.transparent_surface.blit(particle_surface,
                                      particle_surface.get_rect(center=camera.convert_position(self.position)))

        surface.blit(self.transparent_surface, (0, 0))

    def display_mouse(self, surface: pygame.Surface, camera):
        pygame.draw.circle(surface, MOUSE_COLOR, camera.convert_position(self.mouse_position),
                           self.mouse_attraction * 5000, width=int(self.mouse_attraction * 200 + 1))
