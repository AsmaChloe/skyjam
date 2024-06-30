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

    def __init__(self, obstacle_name, direction, image_path, probability, breakable):
        self.obstacle_name = obstacle_name
        self.direction = direction
        if obstacle_name == "whole_beam":
           self.image = pygame.transform.rotozoom(pygame.image.load(image_path), 0, 0.5)
        elif obstacle_name != "left_spike":
            self.image = pygame.transform.rotozoom(pygame.image.load(image_path), 0, 0.75)
        else:
            self.image = pygame.image.load(image_path)
        self.probability = probability
        self.breakable = breakable
        self.broken_img_collection = [pygame.image.load(f"img/ore/stone/explosion neutre{i}.png") for i in range(1, 4)]

    WHOLE_BEAM = ("whole_beam", "center", "img/obstacles/300x/Poutre_Metal-export.png", 0.6, False)
    LEFT_SMALL_BEAM = ("left_small_beam", "left", "img/obstacles/300x/Poutre_Metal_Incrustee_L.png", 0.1, False)
    RIGHT_SMALL_BEAM = ("right_small_beam", "right", "img/obstacles/300x/Poutre_Metal_Incrustee_R-export.png", 0.1, False)

    LEFT_SPIKE = ("left_spike", "left", "img/obstacles/300x/pierre_pics_L.png", 0.1, False)
    RIGHT_SPIKE = ("right_spike", "right", "img/obstacles/300x/pierre_pics_R.png", 0.1, False)

    ROCK_1 = ("rock_1", "center", "img/obstacles/300x/Roche_cassable.png", 0.2, True)
    ROCK_2 = ("rock_2", "center", "img/obstacles/300x/Roche_cassable_R.png", 0.2, True)


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

        self.breakable = self.obs_type.breakable
        self.broken = False
        self.broken_sound = pygame.mixer.Sound("sound/Minerai.wav")
        self.img_broken_index = 0

    @override
    def update(self, events, scrollSpeed):

        if(self.broken and self.img_broken_index < 3):
            self.image = self.obs_type.broken_img_collection[int(self.img_broken_index)]
            self.img_broken_index += 0.1

        self.rect.midtop = self.mid_top_position
        self.speed = scrollSpeed
        self.mid_top_position.y -= self.speed

        # if out of screen kill
        if self.rect.bottom < 0 or (self.broken and self.img_broken_index >= 3):
            self.kill()

def generate_obstacle(game, obstacle_type : ObstacleType):
    """
    Generates an obstacle based on the type
    :param obstacle_type:
    :return:
    """
    offset = 100
    if(obstacle_type.obstacle_name == "left_spike" or obstacle_type.obstacle_name == "right_spike"):
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