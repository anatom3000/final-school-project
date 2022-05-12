# coding: utf-8
from random import uniform

import numpy as np

from constants import LOCAL_SIMULATION_DISTANCE, MAX_ACCELERATION, DESPAWNING_DISTANCE, BOUNCYNESS, MOVEMENT_COOLDOWN
from particle import Particle
from player import Player
from utils import Stringable, unit


class World(Stringable):
    """
    Classe représentant le système physique.
    Elle permet de simuler la gravité entre toutes les particules
    et gère tous les mouvements des particules, y compris le joueur.
    """

    def __init__(self, player: Player, particles: np.array, constant: float = 1):
        """
        Constructeur basique de la classe World
        player est le joueur
        particles est la liste des particules au début de la simulation
        constant est la constante gravitationnélle
        """
        self.player = player
        self.particles = particles
        self.constant = constant
        self.classified_particules = []

    @classmethod
    def random(cls, player: Player, min_position: np.array, max_position: np.array, particle_number: int = 10,
               min_mass: float = 0.2, max_mass: float = 5.0, constant: float = 1.0):
        """
        Contructeur alternatif de World
        Génère des particules aléatoirement en utilisant les paramètres
        particle_number est le nombre de particules à générer
        pour toutes les particules
            - min_mass < masse < max_mass
            - position dans le rectangle entre min_position et max_position
        player et constant: voir World.__init__
        """
        particles = []
        for i in range(particle_number):
            particles.append(Particle(
                mass=uniform(min_mass, max_mass),
                position=np.array(
                    [uniform(min_position[0], max_position[0]), uniform(min_position[1], max_position[1])])
            ))
        return cls(player, np.array(particles), constant)

    def tick(self, dtime: float, tick_player: bool = True):
        """
        Méthode calculant les déplacement de toutes particules.
        dtime: le temps depuis la dernière frame. Sert à "rythmer" la simulation : plus dtime est petit, plus la simulation sera précise.
        tick_player: détermine si le joueur est affecté par les changements (ignore le joueur si False)
        """
        self.particles = np.array(sorted(self.particles, key=lambda particule: particule.position[0]))
        # on inclut le joueur dans les calculs si tick_player
        all_particles = np.append(self.particles, [self.player]) if tick_player else self.particles
        for index_1, particle in enumerate(all_particles):
            particle.acceleration = np.zeros(2)
            # ∑Fg = -G * ∑ M*m / d² * u_A→B
            for other_particle in self.particles[self.particles != particle]:
                particle_to_other_particle = other_particle.position - particle.position
                distance = np.linalg.norm(particle_to_other_particle)
                # optimisation: si 2 particules sont trop éloignées, on néglige leur force d'attraction
                if particle.radius < distance < LOCAL_SIMULATION_DISTANCE:
                    # equivalent à F = Mm/d² * u_A→B
                    # on ne prends pas en compte la masse de la particule affectée car ne change pas l'acceleration (F = ma)
                    # on calcule alors directement l'accélération
                    partial_acceleration = other_particle.mass / (distance ** 2)
                    partial_acceleration *= unit(particle_to_other_particle)
                    particle.acceleration += partial_acceleration

            # on limite l'accélération pour éviter que la simulation ne s'effondre
            # (particules envoyées très loins car bug dans les lois de Newton pour d petit
            particle.acceleration = np.clip(particle.acceleration, -MAX_ACCELERATION * np.ones(2),
                                            MAX_ACCELERATION * np.ones(2))
            # on multiplie par G
            particle.acceleration *= self.constant

            # interaction spéciale pour le joueur
            # le joueur est attiré par la souris
            # a = "masse" souris * √d * u_a→b
            if isinstance(particle, Player):
                distance = particle.mouse_position - particle.position
                if np.linalg.norm(distance) > (particle.radius + 0.5) and particle.movement_cooldown <= 0:
                    particle.acceleration += particle.mouse_attraction * np.linalg.norm(distance) ** 0.5 * unit(distance)

            # v = ∫a dt
            particle.velocity = particle.acceleration * dtime

            if not (particle.to_delete or isinstance(particle, Player)):
                for index_2, other_particle in enumerate(
                        self.particles[self.particles != particle][index_1 - 2: index_1 + 2]):
                    distance = other_particle.position - particle.position
                    if np.linalg.norm(distance) <= particle.radius + other_particle.radius:
                        particle.merge(other_particle)
                        other_particle.to_delete = True

            if isinstance(particle, Player):
                particle.movement_cooldown = max(0, particle.movement_cooldown - dtime)
                for index_2, other_particle in enumerate(self.particles[self.particles != particle]):
                    distance = other_particle.position - particle.position
                    if np.linalg.norm(distance) >= DESPAWNING_DISTANCE:
                        other_particle.to_delete = True
                    elif np.linalg.norm(distance) <= particle.radius + other_particle.radius:
                        particle.acceleration = np.array([0, 0])
                        particle.velocity = particle.velocity * -BOUNCYNESS
                        particle.movement_cooldown = MOVEMENT_COOLDOWN
                        other_particle.to_delete = True

            particle.position += particle.velocity * dtime

        self.particles = self.particles[[(not p.to_delete) for p in self.particles]]

    def __iter__(self):
        return iter(self.particles)
