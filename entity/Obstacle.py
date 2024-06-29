from typing import override

import pygame

from utils.CustomSprite import CustomSprite
from enum import Enum


class ObstacleType(Enum):
    """
    Enum class for the different types of obstacles
    Contains the name of the obstacle, the image and the probability of the obstacle to appear
    """
    WHOLE_BEAM = ("whole_beam", pygame.image.load("img/obstacles/300x/Poutre_Metal-export.png"), 0.6)
    LEFT_SMALL_BEAM = ("left_small_beam", pygame.image.load("img/obstacles/300x/Poutre_Metal_Incrustee_L.png"), 0.2)
    RIGHT_SMALL_BEAM = ("right_small_beam", pygame.image.load("img/obstacles/300x/Poutre_Metal_Incrustee_R-export.png"), 0.2)


class Obstacle(CustomSprite):
    """
    Class for the obstacles
    """

    def __init__(self, mid_top_position, scroll_speed, obstacle_type: ObstacleType):
        """
        Constructor for the obstacle
        :param mid_top_position: position of the obstacle, top middle point
        :param scroll_speed: speed of which the obstacle will move
        :param obstacle_type: type of the obstacle
        """
        self.obs_type = obstacle_type
        image = self.obs_type.value[1]
        name = self.obs_type.value[0]
        CustomSprite.__init__(self, image, name)

        self.mid_top_position = mid_top_position
        self.speed = scroll_speed
        self.rect.midtop = self.mid_top_position

        self.mask = pygame.mask.from_surface(self.image)

    @override
    def update(self, events):
        self.mid_top_position.y -= self.speed
        self.rect.midtop = self.mid_top_position

        # if out of screen kill
        if self.rect.bottom < 0:
            self.kill()
