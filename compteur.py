import numpy as np
import pygame as pygame

NB_REFRESH_FRAME = 10
POLICE = pygame.font.Font("assets/Computerfont.ttf", 72)


class Compteur:
    def __init__(self, pol=POLICE, pos=(10, 10), dim=(200, 50), label=""):
        self.position = pos
        self.dimension = np.array(dim)
        self.txt = "0"
        self.surface = pygame.Surface(dim)
        self.image = pygame.image.load('assets/compteur.png')
        self.police = pol
        self.label = label
        self.refresh = NB_REFRESH_FRAME
        self.count_frame = 0

    def update(self, texte):  # this function must be call once per frame
        if self.count_frame >= self.refresh:
            self.txt = self.label + str(texte).zfill(3)
            self.count_frame = 0
        else:
            self.count_frame += 1

    def display(self, ecran):
        self.surface.blit(pygame.transform.scale(self.image, self.dimension), (0, 0))
        img_txt = pygame.transform.scale(self.police.render(self.txt, True, pygame.Color("#01FDF7")), self.dimension)
        reduce_factor = self.dimension[0] / img_txt.get_size()[0] * 0.8
        self.surface.blit(pygame.transform.scale(img_txt, [int(img_txt.get_size()[0] * reduce_factor),
                                                           int(img_txt.get_size()[1] * reduce_factor)]), (20, 3))
        ecran.blit(self.surface, self.position)
