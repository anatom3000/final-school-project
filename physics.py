import numpy as np

from utils import Stringable


def unit(a):
    return a / np.linalg.norm(a)


class Universe(Stringable):
    def __init__(self, particles: np.array, constant: float = 1):
        self.particles = particles
        self.constant = constant

    def tick(self, dtime: float):
        for particle in self.particles:
            particle.acceleration = np.zeros(2)
            for other_particle in self.particles[self.particles != particle]:
                distance = other_particle.position - particle.position
                partial_acceleration = other_particle.mass / (
                        np.linalg.norm(distance) ** 2
                )
                partial_acceleration *= unit(distance)
                particle.acceleration += partial_acceleration

            particle.acceleration *= self.constant
            particle.velocity = particle.acceleration * dtime
            particle.position += particle.velocity * dtime
            print(particle.position)

    def __iter__(self):
        return iter(self.particles)
