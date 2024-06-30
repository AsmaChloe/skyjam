from entity.buff import Buff
import pygame

from utils.CustomSprite import CustomSprite

class Protection(Buff):
    def __init__(self, scroll_speed):
        
        super().__init__(scroll_speed)
        
        for i in range(1, 13):
            self.imageCollection.append(pygame.image.load(f'graphics/protection/Bouclier{i}.png').convert_alpha())
        
        CustomSprite.__init__(self, self.imageCollection[0], "bouclier")

