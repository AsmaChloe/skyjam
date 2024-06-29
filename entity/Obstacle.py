from random import randint
from typing import override

import pygame

from utils.CustomSprite import CustomSprite
from enum import Enum


class ObstacleType(Enum):
    """
    Enum class for the different types of obstacles
    Contains the name of the obstacle, the image and the probability of the obstacle to appear
    """
    WHOLE_BEAM = ("whole_beam", "center", pygame.transform.rotozoom(pygame.image.load("img/obstacles/300x/Poutre_Metal-export.png"), 0, 0.5), 0.6)
    LEFT_SMALL_BEAM = ("left_small_beam", "left", pygame.image.load("img/obstacles/300x/Poutre_Metal_Incrustee_L.png"), 0.1)
    RIGHT_SMALL_BEAM = ("right_small_beam", "right", pygame.image.load("img/obstacles/300x/Poutre_Metal_Incrustee_R-export.png"), 0.1)
    LEFT_SPIKE = ("left_spike", "left", pygame.image.load("img/obstacles/300x/Pics_Pierres_L.png"), 0.2)

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
        image = self.obs_type.value[2]
        name = self.obs_type.value[0]
        CustomSprite.__init__(self, image, name)

        self.mid_top_position = mid_top_position
        self.speed = scroll_speed
        self.rect.midtop = self.mid_top_position

        self.mask = pygame.mask.from_surface(self.image)

    @override
    def update(self, events, scrollSpeed):
        self.mid_top_position.y -= self.speed
        self.rect.midtop = self.mid_top_position
        self.speed = scrollSpeed

        # if out of screen kill
        if self.rect.bottom < 0:
            self.kill()
def generate_obstacle(game, obstacle_type : ObstacleType):
    """
    Generates an obstacle based on the type
    :param obstacle_type:
    :return:
    """
    offset = 100
    if(obstacle_type.value[0] == "left_spike"):
        offset = 75

    if (obstacle_type.value[1] == "left"):
        x_top_mid = game.LEFT_BORDER + obstacle_type.value[2].get_width() // 2 - offset
    elif (obstacle_type.value[1] == "right"):
        x_top_mid = game.RIGHT_BORDER - obstacle_type.value[2].get_width() // 2 + offset
    elif (obstacle_type.value[1] == "center"):
        x_top_mid = randint(game.LEFT_BORDER + obstacle_type.value[2].get_width() // 2,
                            game.RIGHT_BORDER - obstacle_type.value[2].get_width() // 2)

    y_top_mid = game.HEIGHT

    return Obstacle(pygame.Vector2(x_top_mid, y_top_mid), game.scrollSpeed, obstacle_type)