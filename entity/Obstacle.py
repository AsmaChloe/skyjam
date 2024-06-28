from typing import override

import pygame

from utils.CustomSprite import CustomSprite
from enum import Enum
class ObstacleType(Enum):
    WHOLE_BEAM = ("whole_beam", pygame.image.load("img/obstacles/Poutre_Metal-export.png"))
    LEFT_SMALL_BEAM = ("left_small_beam", pygame.image.load("img/obstacles/Poutre_Metal_Incrustee_L.png"))
    RIGHT_SMALL_BEAM = ("right_small_beam", pygame.image.load("img/obstacles/Poutre_Metal_Incrustee_R-export.png"))
    LEFT_LONG_BEAM = ("left_long_beam", pygame.image.load("img/obstacles/Poutre_Métal_Incrustee_Longue_L.png"))
    LEFT_MID_BEAM = ("left_mid_beam", pygame.image.load("img/obstacles/Poutre_Métal_Incrustee_Moyenne.png"))

class Obstacle(CustomSprite):
    def __init__(self, mid_top_position, scroll_speed, obstacle_type: ObstacleType):
        self.obs_type = obstacle_type
        image = self.obs_type.value[1]
        name = self.obs_type.value[0]
        CustomSprite.__init__(self, image, name)

        self.mid_top_position = mid_top_position
        self.speed = scroll_speed
        self.rect.midtop = self.mid_top_position


    @override
    def update(self, events):
        self.mid_top_position.y -= self.speed
        self.rect.midtop = self.mid_top_position

        # if out of screen kill
        if self.rect.bottom < 0:
            self.kill()
