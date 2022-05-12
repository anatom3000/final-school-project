from random import uniform

import numpy as np

from particle import Particle
from player import Player
from utils import Stringable, unit

CHUNK_SIZE = 64
COLISION_COOLDOWN = 3  # in frames
GLOBAL_SIMULATION_DISTANCE = 256
BOUNCYNESS = 2
MOVEMENT_COOLDOWN = 2.0
LOCAL_SIMULATION_DISTANCE = 64
RENDER_DISTANCE = 400  # valeur a ajuster car 100% random
MAX_ACCELERATION = 50


class World(Stringable):
    def __init__(self, player: Player, particles: np.array, constant: float = 1):
        self.player = player
        self.particles = particles
        self.constant = constant
        self.classified_particules = []

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

    def tick(self, dtime: float, tick_player: bool = True):
        self.particles = np.array(sorted(self.particles, key=lambda particule: particule.position[0]))
        all_particles = np.append(self.particles, [self.player]) if tick_player else self.particles
        for index_1, particle in enumerate(all_particles):
            particle.acceleration = np.zeros(2)
            for other_particle in self.particles[self.particles != particle]:
                particle_to_other_particle = other_particle.position - particle.position
                distance = np.linalg.norm(particle_to_other_particle)
                if particle.radius < distance < LOCAL_SIMULATION_DISTANCE:
                    partial_acceleration = other_particle.mass / (distance ** 2)
                    partial_acceleration *= unit(particle_to_other_particle)
                    particle.acceleration += partial_acceleration

            particle.acceleration = np.clip(particle.acceleration, -MAX_ACCELERATION * np.ones(2), MAX_ACCELERATION * np.ones(2))
            particle.acceleration *= self.constant

            if particle.is_player:
                distance = particle.mouse_position - particle.position
                if np.linalg.norm(distance) > (particle.radius + 0.5) and particle.movement_cooldown == 0:
                    particle.acceleration += particle.mouse_attraction * np.linalg.norm(distance) ** 0.5 * unit(
                        distance)

            particle.velocity = particle.acceleration * dtime

            if not (particle.merged or particle.is_player):
                for index_2, other_particle in enumerate(
                        self.particles[self.particles != particle][index_1 - 2: index_1 + 2]):
                    distance = other_particle.position - particle.position
                    if np.linalg.norm(distance) <= particle.radius + other_particle.radius:
                        particle.merge(other_particle)
                        other_particle.merged = True

            if particle.is_player:
                particle.movement_cooldown = max(0, particle.movement_cooldown - dtime)
                for index_2, other_particle in enumerate(self.particles[self.particles != particle]):
                    distance = other_particle.position - particle.position
                    if np.linalg.norm(distance) >= RENDER_DISTANCE:
                        other_particle.away_from_player = True
                    elif np.linalg.norm(distance) <= particle.radius + other_particle.radius:
                        particle.acceleration = np.array([0, 0])
                        particle.velocity = particle.velocity * -BOUNCYNESS
                        particle.movement_cooldown = MOVEMENT_COOLDOWN
                        other_particle.away_from_player = True

            particle.position += particle.velocity * dtime

        self.particles = self.particles[[not (p.merged or p.away_from_player) for p in self.particles]]

    def __iter__(self):
        return iter(self.particles)
