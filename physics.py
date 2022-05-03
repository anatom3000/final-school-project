from math import sqrt
from random import uniform

import numpy as np
import pygame

from particle import Particle
from player import Player
from utils import Stringable, unit

CHUNK_SIZE = 64
COLISION_COOLDOWN = 3 # in frames
BOUNCYNESS = 2


class World(Stringable):
    def __init__(self, player: Player, particles: np.array, constant: float = 1):
        # self.player = player
        self.particles = particles
        self.constant = constant

    @classmethod
    def random(cls, player: Player, min_position: np.array, max_position: np.array, particle_number: int =10, min_mass: float = 0.2, max_mass: float = 5, constant: float = 1):
        particles = []
        for i in range(particle_number):
            particles.append(Particle(
                mass=uniform(min_mass, max_mass),
                position=np.array([uniform(min_position[0], max_position[0]), uniform(min_position[1], max_position[1])])
            ))
        return cls(player, np.array(particles), constant)


    def merge_bodies(a, b):
        name = a.name + " + " + b.name
        mass = a.m + b.m
        pos = [
            a.pos[0] * a.m / mass + b.pos[0] * b.m / mass,
            a.pos[1] * a.m / mass + b.pos[1] * b.m / mass
        ]
        velocity = [
            a.v[0] * a.m / mass + b.v[0] * b.m / mass,
            a.v[1] * a.m / mass + b.v[1] * b.m / mass
        ]

        radius = merge_radius(a, b)

        return Body(name, pos, acceleration, velocity, mass, color, radius)

    def tick(self, dtime: float):
        for particle in np.append(self.particles, []):
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
            if not particle.has_colisioned:
                for other_particle in self.particles[self.particles != particle]:
                    distance = other_particle.position - particle.position
                    if np.linalg.norm(distance) <= particle.radius + other_particle.radius:
                        self.particles.append()

            particle.position += particle.velocity * dtime

        for particle in np.append(self.particles, []):


    def __iter__(self):
        return iter(self.particles)
