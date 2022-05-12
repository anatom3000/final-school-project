from math import tanh

import numpy as np

from constants import CAMERA_POSITION_SMOOTHING_SPEED, CAMERA_ZOOM_SMOOTHING_SPEED
from particle import Particle
from utils import Stringable, lerp


class Camera(Stringable):
    """
    pygame n'a pas de système de caméra par défaut
    Cette classe permet donc de émuler le déplacement d'une caméra.
    Le smoothing permet de rendre la caméra stable, faire un camera.position = [...] ne fera pas "sauter" la caméra
    instantanément, elle fera une transition entre sa position actuelle et la position voulue.
    Fonctionnalités:
        - déplacement interpolé de la caméra sur X et Y
        - zoom/dézoom interpolé
        - conversion des coordonnées dans le système physique (unité arbitraire) aux coordonnées sur l'écran (en pixels)
        - conversion des coordonnées sur l'écran (en pixels) aux coordonnées dans le système physique (unité arbitraire)
    Ressources:
        - https://fr.wikipedia.org/wiki/Interpolation_lin%C3%A9aire
    """
    def __init__(self, resolution: np.array, zoom: float = 2.0, position: np.array = None):
        self._position = np.array([0.0, 0.0]) if position is None else position
        self._zoom = zoom

        self._target_position = self._position
        self._target_zoom = self.zoom

        self.resolution = resolution

    @property
    def position(self):
        """
        Une property est un faux attribut, qui appelle une fonction pour renvoyer une valeur en fonction de self.
        """
        return self._position

    @position.setter
    def position(self, value: np.array):
        """
        <property>.setter permet de définir le comportement de <property> = value
        Ici on modifie en fait la position à atteindre par interpolation.
        """
        self._target_position = value

    @property
    def zoom(self):
        """Pareil à que la position, mais c'est le zoom"""
        return self._zoom

    @zoom.setter
    def zoom(self, value: float):
        """Pareil à que la position, mais c'est le zoom"""
        self._target_zoom = value

    def move(self, delta: np.array):
        """
        Déplace la caméra fluidement de delta.
        """
        self.position += delta

    def zoom_in(self, delta: float):
        """Zoom fluidement de delta"""
        self.zoom *= delta
        self.position *= delta

    def zoom_out(self, delta: float):
        """Dézoom fluidement de delta"""
        self.zoom /= delta
        self.position /= delta

    @staticmethod
    def _convert_velocity_to_zoom(velocity: np.array):
        """
        Une méthode statique est une méthode qui n'utilise pas les attributs de l'objet.
        Sorte de fonction fortement liée à la classe.
        Elle calcule le zoom en fonction de la vitesse (dézoom quand on accélère, zoom quand on ralentit)
        Fonction concue et ajustée avec Desmos
        voir https://www.desmos.com/calculator/w9ns72ijq1
        """

        x = np.linalg.norm(velocity)
        m = 0.5
        a = 50.0
        b = 0.2
        c = 0
        # return 5.0
        return 1 / (m * tanh(x / a + b)) + c

    def follow(self, particle: Particle, smoothing: bool = True):
        """
        Méthode permettant de bouger la caméra vers la position d'une particule.
        Utilisée pour le joueur
        """
        if smoothing:
            self.position = self.zoom * particle.position
            self.zoom = Camera._convert_velocity_to_zoom(particle.velocity)
        else:
            self._position = self.zoom * particle.position
            self._zoom = Camera._convert_velocity_to_zoom(particle.velocity)

    def convert_position(self, position: np.array):
        """
        Convertit des coordonnées dans le système physique aux coordonnées sur l'écran
        """
        return self.zoom * position + self.resolution / 2 - self.position

    def convert_radius(self, radius: float):
        """Convertit une distance (radius) dans le système physique à une distance sur l'écran"""
        return radius * self.zoom

    def real_position_from_screen(self, position: np.array):
        """
        Convertit des coordonnées sur l'écran (position) aux coordonnées dans le système physique (unité arbitraire)
        """
        return (position + self.position - self.resolution / 2) / self.zoom

    def tick(self, dt: float):
        """
        Appelé à chauque frame.
        Fait l'interpolation entre la position de la caméra et la position à atteindre en utilisant lerp (Linear intERPolation)
        dt est le temps en secondes depuis la dernière frame
        """
        self._position = lerp(self._position, self._target_position, dt * CAMERA_POSITION_SMOOTHING_SPEED)
        self._zoom = lerp(self._zoom, self._target_zoom, dt * CAMERA_ZOOM_SMOOTHING_SPEED)
