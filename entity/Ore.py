from enum import Enum

import pygame

from utils.CustomSprite import CustomSprite

class OreType(Enum):
    """
    Enum class for the different types of ores.
    Contains the name of the ore, the direction, the image, the rarity, and the probability of the ore to appear.
    """

    def __new__(cls, *args, **kwds):
        value = len(cls.__members__) + 1
        obj = object.__new__(cls)
        obj._value_ = value
        return obj

    def __init__(self, ore_name, direction, image_path, rarity, XP):
        self.ore_name = ore_name
        self.direction = direction
        self.image = pygame.image.load(image_path)
        self.rarity = rarity
        self.XP = XP

    # 0.5
    IRON_LEFT = ("iron", "left", "img/ore/iron/Minerai_Fer_L.png", 0.25, 2)
    IRON_RIGHT = ("iron", "right", "img/ore/iron/Minerai_Fer_R.png", 0.25, 2)
    # 0.3
    GOLD_LEFT = ("gold", "left", "img/ore/gold/Minerai_Or_L.png", 0.15, 4)
    GOLD_RIGHT = ("gold", "right", "img/ore/gold/Minerai_Or_R.png", 0.15, 4)
    # 0.2
    DIAMOND_LEFT = ("diamond", "left", "img/ore/diamond/Minerai_Diamant_L.png", 0.1, 6)
    DIAMOND_RIGHT = ("diamond", "right", "img/ore/diamond/Minerai_Diamant_R.png", 0.1, 6)


class Ore(CustomSprite):
    def __init__(self, mid_top_position, scroll_speed, ore_type: OreType):
        """
        Constructor for the ore
        :param mid_top_position:
        :param scroll_speed:
        :param ore_type:
        """
        self.ore_type = ore_type
        image = self.ore_type.image
        name = self.ore_type.ore_name
        CustomSprite.__init__(self, image, name)

        self.mid_top_position = mid_top_position
        self.speed = scroll_speed
        self.rect.midtop = self.mid_top_position

        self.mask = pygame.mask.from_surface(self.image)

    def update(self, events, scrollSpeed):
        self.mid_top_position.y -= self.speed
        self.rect.midtop = self.mid_top_position
        self.speed = scrollSpeed
        

        if self.rect.bottom < 0:
            self.kill()

def generate_ore(game, ore_type : OreType):
    """
    Generates an ore based on the type
    :param ore_type:
    :return:
    """
    if(ore_type.direction == "left"):
        x_top_mid = game.LEFT_BORDER + ore_type.image.get_width() // 2 - 70
    elif(ore_type.direction == "right"):
        x_top_mid = game.RIGHT_BORDER - ore_type.image.get_width() // 2 + 70
    y_top_mid = game.HEIGHT

    return Ore(pygame.Vector2(x_top_mid, y_top_mid), game.scrollSpeed, ore_type)