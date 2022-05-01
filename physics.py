import numpy as np

N_DIM = 2


def unit(a):
    return a / np.linalg.norm(a)


class Particle:
    def __init__(
            self,
            mass: float,
            position: np.array = np.zeros(N_DIM),
            velocity: np.array = np.zeros(N_DIM),
    ):
        self.mass = mass
        self.position = position
        self.velocity = velocity
        self.acceleration = np.zeros(N_DIM)
        self.resulting_force = np.zeros(N_DIM)

    def __str__(self):
        return f"Particle(mass={self.mass}, position={self.position}, velocity={self.velocity}), acceleration={self.acceleration}, force={self.resulting_force}"

    def compute_state(self, dtime: float):
        self.acceleration = self.resulting_force / self.mass
        self.velocity = self.acceleration * dtime
        self.position += self.velocity * dtime


class Universe:
    def __init__(self, particles: np.array, constant: float = 1):
        self.particles = particles
        self.constant = constant

    @staticmethod
    def tick_two_by_two(particle1: Particle, particle2: Particle):
        distance = particle2.position - particle1.position
        force = particle1.mass * particle2.mass / (
                np.linalg.norm(distance) ** 2
        )

        a2b = unit(distance)
        print(a2b)
        return force * a2b

    def tick(self, dtime: float):
        for particle in self.particles:
            particle.force = np.zeros(N_DIM)
            for other_particle in self.particles[self.particles != particle]:
                particle.resulting_force += Universe.tick_two_by_two(particle, other_particle)

            particle.resulting_force *= self.constant
            particle.compute_state(dtime)
