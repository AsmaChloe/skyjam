from entity.buff import Buff
import pygame

from utils.CustomSprite import CustomSprite

class Bat(Buff):
    def __init__(self, scroll_speed, music_player):
        
        super().__init__(scroll_speed)
        self.music_player = music_player

        
        for i in range(1, 13):
            self.imageCollection.append(pygame.image.load(f'graphics/chauve_souris/animation_chauve_souris{i}.png').convert_alpha())
        
        CustomSprite.__init__(self, self.imageCollection[0], "chauve_souris")

        self.free_bat_sound = pygame.mixer.Sound("sound/Chauve_souris_Libre.wav")
        self.music_player.bat_channel.play(self.free_bat_sound)
        
