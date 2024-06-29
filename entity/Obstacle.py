from random import randint
from typing import override

import pygame

from utils.CustomSprite import CustomSprite
from enum import Enum


class ObstacleType(Enum):
    """
    Enum class for the different types of obstacles.
    Contains the obstacle name, the image, and the probability of the obstacle to appear.
    """


    def __new__(cls, *args, **kwds):
        value = len(cls.__members__) + 1
        obj = object.__new__(cls)
        obj._value_ = value
        return obj

    def __init__(self, obstacle_name, direction, image_path, probability):
        self.obstacle_name = obstacle_name
        self.direction = direction
        if obstacle_name == "whole_beam":
           self.image = pygame.transform.rotozoom(pygame.image.load(image_path), 0, 0.5)
        else:
            self.image = pygame.image.load(image_path)
        self.probability = probability

    WHOLE_BEAM = ("whole_beam", "center", "img/obstacles/300x/Poutre_Metal-export.png", 0.6)
    LEFT_SMALL_BEAM = ("left_small_beam", "left", "img/obstacles/300x/Poutre_Metal_Incrustee_L.png", 0.1)
    RIGHT_SMALL_BEAM = ("right_small_beam", "right", "img/obstacles/300x/Poutre_Metal_Incrustee_R-export.png", 0.1)
    LEFT_SPIKE = ("left_spike", "left", "img/obstacles/300x/Pics_Pierres_L.png", 0.2)


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
        image = self.obs_type.image
        name = self.obs_type.obstacle_name
        CustomSprite.__init__(self, image, name)

        self.mid_top_position = mid_top_position
        self.speed = scroll_speed
        self.rect.midtop = self.mid_top_position

        self.mask = pygame.mask.from_surface(self.image)

    @override
    def update(self, events, scrollSpeed):
        self.rect.midtop = self.mid_top_position
        self.speed = scrollSpeed
        self.mid_top_position.y -= self.speed

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
    if(obstacle_type.obstacle_name == "left_spike"):
        offset = 75

    if (obstacle_type.direction == "left"):
        x_top_mid = game.LEFT_BORDER + obstacle_type.image.get_width() // 2 - offset
    elif (obstacle_type.direction == "right"):
        x_top_mid = game.RIGHT_BORDER - obstacle_type.image.get_width() // 2 + offset
    elif (obstacle_type.direction == "center"):
        x_top_mid = randint(game.LEFT_BORDER + obstacle_type.image.get_width() // 2,
                            game.RIGHT_BORDER - obstacle_type.image.get_width() // 2)

    y_top_mid = game.HEIGHT

    return Obstacle(pygame.Vector2(x_top_mid, y_top_mid), game.scrollSpeed, obstacle_type)