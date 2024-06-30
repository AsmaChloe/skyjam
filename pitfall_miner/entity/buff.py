from random import randint
import pygame

from utils.CustomSprite import CustomSprite

class Buff(CustomSprite):
    def __init__(self, scroll_speed):
        
        self.scroll_speed = scroll_speed
        self.imageCollection = []
        self.tickFrame = 0

        
    def animate(self):
        self.tickFrame = (self.tickFrame + 0.2) % len(self.imageCollection)
        self.image = self.imageCollection[int(self.tickFrame)]
        self.rect.top -= self.scroll_speed
    
    def update(self, scrollSpeed):
        self.animate()
        self.scroll_speed = scrollSpeed
        
        if self.rect.bottom < 0:
            self.kill()
    
    def generate_buff(self, game):

        x_top_mid = randint(game.LEFT_BORDER + self.rect.width // 2,
                                game.RIGHT_BORDER - self.rect.width // 2)

        y_top_mid = game.HEIGHT
        
        self.rect.midtop = (x_top_mid, y_top_mid)
        

        return self