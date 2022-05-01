import numpy as np

<<<<<<< HEAD
from particle import Particle

=======
>>>>>>> parent of 75e08ca (refactored gravity but it doesn't work)

def unit(a: np.array):
    return a / np.linalg.norm(a)


<<<<<<< HEAD
=======
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

class

>>>>>>> parent of 75e08ca (refactored gravity but it doesn't work)
class Universe:
    def __init__(self, particles: np.array, constant: float = 1):
        self.particles = particles
        self.constant = constant

<<<<<<< HEAD
    @staticmethod
    def tick_two_by_two(particle1: Particle, particle2: Particle):
        distance = particle2.position - particle1.position
        force = particle1.mass * particle2.mass / (
                np.sum(np.square(distance))
        )

        a2b = unit(distance)
        return force * a2b

    def tick(self, dtime: float):
        for particle in self.particles:
            particle.force = np.zeros(2)
=======
    def tick(self, dtime: float):
        for particle in self.particles:
            particle.acceleration = np.zeros(2)
>>>>>>> parent of 75e08ca (refactored gravity but it doesn't work)
            for other_particle in self.particles[self.particles != particle]:
                distance = other_particle.position - particle.position
                partial_acceleration = other_particle.mass / (
                        np.linalg.norm(distance) ** 2
                )
                partial_acceleration *= unit(distance)
                particle.acceleration += partial_acceleration

<<<<<<< HEAD
            particle.resulting_force *= self.constant
            particle.compute_state(dtime)

    def __iter__(self):
        return iter(self.particles)
=======
            particle.acceleration *= self.constant
            particle.velocity = particle.acceleration * dtime
            particle.position += particle.velocity * dtime
>>>>>>> parent of 75e08ca (refactored gravity but it doesn't work)
