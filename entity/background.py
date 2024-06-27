import pygame

class Background(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.baseTexture = pygame.image.load("img/cailloux.png").convert()
        self.image = pygame.Surface((10*288, 10*288))
        self.rect = self.image.get_rect(midtop = (1920/2, 0))
        
        for i in range(10):
            for j in range(10):
                self.image.blit(self.baseTexture, (288 * i, 288 * j))
    
        
    def update(self):
        self.rect.top -= 5