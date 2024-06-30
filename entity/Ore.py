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

    def __init__(self, ore_name, direction, image_path, rarity, XP, filename):
        self.ore_name = ore_name
        self.direction = direction
        self.image = pygame.image.load(image_path)
        self.rarity = rarity
        self.XP = XP
        self.broken_img_collection = [pygame.image.load(f"img/ore/{ore_name}/{filename}{i}.png") for i in range(1, 4)]

    # 0.5
    STONE_LEFT = ("stone", "left", "img/ore/stone/Tas_Pierres_L.png", 0.5, 0, "explosion neutre")
    STONE_RIGHT = ("stone", "right", "img/ore/stone/Tas_Pierres_R.png", 0.5, 0, "explosion neutre")
    # 0.4
    IRON_LEFT = ("iron", "left", "img/ore/iron/Minerai_Fer_L.png", 0.25, 20,"explosion fert")
    IRON_RIGHT = ("iron", "right", "img/ore/iron/Minerai_Fer_R.png", 0.25, 20, "explosion fert")
    # 0.3
    GOLD_LEFT = ("gold", "left", "img/ore/gold/Minerai_Or_L.png", 0.15, 40, "explosion or")
    GOLD_RIGHT = ("gold", "right", "img/ore/gold/Minerai_Or_R.png", 0.15, 40 , "explosion or")
    # 0.2
    DIAMOND_LEFT = ("diamond", "left", "img/ore/diamond/Minerai_Diamant_L.png", 0.1, 80, "explosion diamant")
    DIAMOND_RIGHT = ("diamond", "right", "img/ore/diamond/Minerai_Diamant_R.png", 0.1, 80, "explosion diamant")


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

        self.broken_sound = pygame.mixer.Sound("sound/Minerai.wav")

        self.img_broken_index = 0
        self.broken = False

    def update(self, events, scrollSpeed):
        if(self.broken and self.img_broken_index < 3):
            self.image = self.ore_type.broken_img_collection[self.img_broken_index]
            self.img_broken_index += 1

        self.rect.midtop = self.mid_top_position
        self.speed = scrollSpeed
        self.mid_top_position.y -= self.speed

        if self.rect.bottom < 0 or (self.broken and self.img_broken_index >= 3):
            self.kill()

def generate_ore(game, ore_type : OreType):
    """
    Generates an ore based on the type
    :param ore_type:
    :return:
    """
    offset = 100
    if(ore_type.name == "stone"):
        offset = 0
    if(ore_type.direction == "left"):
        x_top_mid = game.LEFT_BORDER + ore_type.image.get_width() // 2 - offset
    elif(ore_type.direction == "right"):
        x_top_mid = game.RIGHT_BORDER - ore_type.image.get_width() // 2 + offset
    y_top_mid = game.HEIGHT

    return Ore(pygame.Vector2(x_top_mid, y_top_mid), game.scrollSpeed, ore_type)