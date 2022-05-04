from random import uniform

import numpy as np

from particle import Particle
from player import Player
from utils import Stringable, unit

CHUNK_SIZE = 64
COLISION_COOLDOWN = 3  # in frames
BOUNCYNESS = 2
GLOBAL_SIMULATION_DISTANCE = 256
LOCAL_SIMULATION_DISTANCE = 64


class World(Stringable):
    def __init__(self, player: Player, particles: np.array, constant: float = 1):
        self.player = player
        self.particles = particles
        self.constant = constant

    @classmethod
    def random(cls, player: Player, min_position: np.array, max_position: np.array, particle_number: int = 10,
               min_mass: float = 0.2, max_mass: float = 5, constant: float = 1):
        particles = []
        for i in range(particle_number):
            particles.append(Particle(
                mass=uniform(min_mass, max_mass),
                position=np.array(
                    [uniform(min_position[0], max_position[0]), uniform(min_position[1], max_position[1])])
            ))
        return cls(player, np.array(particles), constant)

    def tick(self, dtime: float):
        all_particles = np.append(self.particles, [self.player])
        for particle in all_particles:
            particle.acceleration = np.zeros(2)
            for other_particle in self.particles[self.particles != particle]:
                particle_to_other_particle = other_particle.position - particle.position
                distance = np.linalg.norm(particle_to_other_particle)
                if particle.radius < distance < LOCAL_SIMULATION_DISTANCE:
                    partial_acceleration = other_particle.mass / (distance ** 2)
                    partial_acceleration *= unit(particle_to_other_particle)
                    particle.acceleration += partial_acceleration

            particle.acceleration *= self.constant
            particle.velocity = particle.acceleration * dtime
            if not particle.merged:
                for other_particle in self.particles[self.particles != particle]:
                    distance = other_particle.position - particle.position
                    if np.linalg.norm(distance) <= particle.radius + other_particle.radius:
                        particle.merge(other_particle)
                        other_particle.merged = True

            particle.position += particle.velocity * dtime

        self.particles = self.particles[[not p.merged for p in self.particles]]

    def __iter__(self):
        return iter(self.particles)
