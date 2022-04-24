import numpy as np


def unit(a):
    return a / np.linalg.norm(a)


class Particle:
    def __init__(
        self,
        mass: float,
        position: np.array = np.array([0.0, 0.0]),
        velocity: np.array = np.array([0.0, 0.0]),
    ):
        self.mass = mass
        self.position = position
        self.velocity = velocity


class Universe:
    def __init__(self, particles: np.array, constant: float = 1):
        self.particles = particles
        self.constant = constant

    def tick(self, dtime: float):
        for particle in self.particles:
            acceleration = np.zeros(2)
            for other_particle in self.particles[self.particles != particle]:
                distance = other_particle.position - particle.position
                partial_acceleration = other_particle.mass / (
                    np.linalg.norm(distance) ** 2
                )
                partial_acceleration *= unit(distance)
                acceleration += partial_acceleration

            acceleration *= self.constant
            particle.velocity += acceleration * dtime
            particle.position += particle.velocity * dtime
