import numpy as np
import pygame


class Stringable:
    # simple class that automatically generate a string representation
    # just subclass this class to add
    def __str__(self):
        return f"{self.__class__.__name__}({', '.join([f'{k}={repr(v)}' for k, v in vars(self).items()])})"

    def __repr__(self):
        return self.__str__()


def unit(a):
    return a / np.linalg.norm(a)


def lerp(a, b, x):
    """
    Basic linear interpolation.
    In:
        a is the starting point (float or vector/numpy array)
        b is the ending point (float or vector/numpy array)
        x is the interpolation amount
    Out:
        the lerp between a and b at x
    """
    return (1 - x) * a + x * b


def clamp(minimum, x, maximum):
    return min(max(x, minimum), maximum)


def draw_circle_alpha(surface, color, center, radius):
    target_rect = pygame.Rect(center, (0, 0)).inflate((radius * 2, radius * 2))
    shape_surf = pygame.Surface(target_rect.size, pygame.SRCALPHA)
    pygame.draw.circle(shape_surf, color, (radius, radius), radius)
    surface.blit(shape_surf, target_rect)
