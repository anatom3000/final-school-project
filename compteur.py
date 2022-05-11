import numpy as np
import pygame as pygame

pygame.init()

NB_REFRESH_FRAME = 10
POLICE = pygame.font.Font("Computerfont.ttf", 72)


class Compteur():
    def __init__(self, img, pol=POLICE, pos=(10, 10), dim=(200, 50), label=""):
        self.position = pos
        self.dimenssion = np.array(dim)
        self.txt = "0"
        self.surface = pygame.Surface(dim)
        self.image = img
        self.police = pol
        self.label = label
        self.refresh = NB_REFRESH_FRAME
        self.count_frame = 0

    def update(self, texte):  # this function must be call once per frame
        print(self.count_frame, self.refresh)
        if self.count_frame >= self.refresh:
            self.txt = self.label + str(texte)
            self.count_frame = 0
        else:
            self.count_frame += 1

    def display(self, ecran):
        self.surface.blit(pygame.transform.scale(self.image, self.dimenssion), (0, 0))
        img_txt = pygame.transform.scale(self.police.render(self.txt, True, pygame.Color("#01FDF7")), self.dimenssion)
        reduce_factor = self.dimenssion[0] / img_txt.get_size()[0] * 0.8
        self.surface.blit(pygame.transform.scale(img_txt, [int(img_txt.get_size()[0] * reduce_factor),
                                                       int(img_txt.get_size()[1] * reduce_factor)]), (20, 3))
        ecran.blit(self.surface, self.position)


fond_velocity = pygame.image.load('vitesse.png')
compteur_vitesse = Compteur(fond_velocity, label="vitesse :")