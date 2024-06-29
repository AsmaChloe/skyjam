from enum import Enum

import pygame
import os
import random

class BackgroundType(Enum):
    def __new__(cls, *args, **kwds):
        value = len(cls.__members__) + 1
        obj = object.__new__(cls)
        obj._value_ = value
        return obj

    def __init__(self, direction, image_path, probability):
        self.direction = direction
        self.image = pygame.image.load(image_path)
        self.probability = probability

    #LEFT
    SIMPLE_WALL_LEFT = ("left", "graphics/background/Mur_L/Mur_L.png", 0.4)
    FERN_WALL_LEFT_1 = ("left", "graphics/background/Mur_L/Mur_L_Fougere_1.png", 0.1)
    FERN_WALL_LEFT_2 = ("left", "graphics/background/Mur_L/Mur_L_Fougere_2.png", 0.1)
    # GEODE_WALL_LEFT_1 = ("left", "graphics/background/Mur_L/Mur_L_Geode_1.png", 0.1)
    GEODE_WALL_LEFT_2 = ("left", "graphics/background/Mur_L/Mur_L_Geode_2.png", 0.1)
    CAVE_DYNAMITE_WALL_LEFT = ("left", "graphics/background/Mur_L/Mur_L_Grotte_dynamite.png", 0.01)
    # CAVE_GEODE_WALL_LEFT = ("left", "graphics/background/Mur_L/Mur_L_Grotte_geode.png", 0.01)
    # CAVE_GEODE_DYNAMITE_WALL_LEFT = ("left", "graphics/background/Mur_L/Mur_L_Grotte_geode_dynamite.png", 0.01)
    # CAVE_CHARACTER_WALL_LEFT = ("left", "graphics/background/Mur_L/Mur_L_Grotte_perso.png", 0.01)

    #RIGHT
    SIMPLE_WALL_RIGHT = ("right", "graphics/background/Mur_R/Mur_R.png", 0.4)
    FERN_WALL_RIGHT_1 = ("right", "graphics/background/Mur_R/Mur_R_Fougere_1.png", 0.1)
    FERN_WALL_RIGHT_2 = ("right", "graphics/background/Mur_R/Mur_R_Fougere_2.png", 0.1)
    # GEODE_WALL_RIGHT_1 = ("right", "graphics/background/Mur_R/Mur_R_Geode_1.png", 0.1)
    GEODE_WALL_RIGHT_2 = ("right", "graphics/background/Mur_R/Mur_R_Geode_2.png", 0.1)
    CAVE_DYNAMITE_WALL_RIGHT = ("right", "graphics/background/Mur_R/Mur_R_Grotte_dynamite.png", 0.01)
    # CAVE_GEODE_WALL_RIGHT = ("right", "graphics/background/Mur_R/Mur_R_Grotte_geode.png", 0.01)
    # CAVE_GEODE_DYNAMITE_WALL_RIGHT = ("right", "graphics/background/Mur_R/Mur_R_Grotte_geode_dynamite.png", 0.01)
    # CAVE_CHARACTER_WALL_RIGHT = ("right", "graphics/background/Mur_R/Mur_R_Grotte_perso.png", 0.01)


class Background(pygame.sprite.Sprite):
    def __init__(self, scrollSpeed):
        super().__init__()
        self.baseTexture = pygame.image.load("img/cailloux.png").convert()
        self.middleTexture = pygame.image.load("graphics/background/Fond_gros.png").convert_alpha()
        self.image = pygame.Surface((2488, 500*1050))
        self.rect = self.image.get_rect(midtop = (1920/2, 0))
        self.scrollSpeed = scrollSpeed
        
        #le point de début de la zone est au pixel 414 et la fin au pixel 1506 et la zone fait 1092 pixels de large
        

        for i in range(500):
            #zone jouable
            self.image.blit(self.middleTexture, (650, 1050 * i))
        
        for j in range(1000):
            #mur de gauche
            self.image.blit(self.randomWall("left"), (0, 525 * j))
            #mur de droite
            self.image.blit(self.randomWall("right"), (1715, 525 * j))
    
    def setScrollSpeed(self, scrollSpeed):
        self.scrollSpeed = scrollSpeed
        
    def update(self):
        self.rect.top -= self.scrollSpeed

    def randomWall(self, side):
        if side == "left":
            left_backgrounds = [bg for bg in BackgroundType if bg.direction == "left"]
            return random.choices(left_backgrounds, weights=[bg.probability for bg in left_backgrounds], k=1)[0].image
        else:
            right_backgrounds = [bg for bg in BackgroundType if bg.direction == "right"]
            return random.choices(right_backgrounds, weights=[bg.probability for bg in right_backgrounds], k=1)[0].image