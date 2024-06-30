from entity.buff import Buff
import pygame

from utils.CustomSprite import CustomSprite

class Dynamite(Buff):
    def __init__(self, scroll_speed, music_player):
        
        super().__init__(scroll_speed)

        
        for i in range(1, 9):
            self.imageCollection.append(pygame.image.load(f'graphics/dynamite/dynamite{i}.png').convert_alpha())
        
        CustomSprite.__init__(self, self.imageCollection[0], "dynamite")


        
