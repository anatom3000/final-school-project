import numpy as np

"""
Contient toutes les constantes utilisées dans le jeu.
Permet d'être utilisé comme un fichier de configuration.
"""

# Configuration techniques/relatives à pygame
FPS_CAP = 120
RESOLUTION = np.array([960, 720])
DEBUGGING = False

# Couleurs
BACKGROUND_COLOR = (0, 0, 16)
MOUSE_CURSOR_COLOR = (0, 0, 255)

# Configuration de la physique du monde
G = 3e6
BOUNCYNESS = 2
MOVEMENT_COOLDOWN = 2.0
LOCAL_SIMULATION_DISTANCE = 64
SPAWNING_DISTANCE = 390
DESPAWNING_DISTANCE = 400
MAX_ACCELERATION = 50

# Configuration de la traction de la souris
MOUSE_PROPULSION_INIT = 2e2
MOUSE_PROPULSION_STEP = 2e2
MOUSE_PROPULSION_MAX = MOUSE_PROPULSION_STEP * 16

# Configuration des propriétés des particules
MAX_PARTICLE_MASS = 20.0
PARTICLE_MASS_TO_RADIUS_FACTOR = 10.0

# Configuration de la trainée du joueur
PLAYER_TRAIL_COLOR = 0.5
PLAYER_TRAIL_LENGHT = 16
PLAYER_TRAIL_DENSITY = 0.08

# Configuration de la caméra
CAMERA_POSITION_SMOOTHING_SPEED = 5.0
CAMERA_ZOOM_SMOOTHING_SPEED = 0.5
