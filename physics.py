import numpy as np


def unit(a):
    return a / np.linalg.norm(a)


class Particle:
    def __init__(
            self,
            mass: float,
            position: np.array = np.array([0.0, 0.0]),
            velocity: np.array = np.array([0.0, 0.0]),
            acceleration: np.array = np.array([0.0, 0.0])
    ):
        self.mass = mass
        self.position = position
        self.velocity = velocity
        self.acceleration = acceleration
        self.forces = np.array([])

    def __str__(self):
        return f"Particle(mass={self.mass}, position={self.position}, velocity={self.velocity}), acceleration={self.acceleration}"

class Universe:
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
