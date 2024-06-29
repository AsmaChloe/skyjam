import pygame

class Background(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.baseTexture = pygame.image.load("img/cailloux.png").convert()
        self.middleTexture = pygame.image.load("graphics/background/Fond_gros.png")
        self.image = pygame.Surface((4*288 + 1092, 500*288))
        self.rect = self.image.get_rect(midtop = (1920/2, 0))
        
        #le point de début de la zone est au pixel 414 et la fin au pixel 1506 et la zone fait 1092 pixels de large
        
        for i in range(5):
            for j in range(500):
                if i == 2  and j%4 == 0:
                    self.image.blit(self.middleTexture, (288*2, 288 * j))
                if i < 2:
                    self.image.blit(self.baseTexture, (288 * i, 288 * j))
                if i > 2:
                    self.image.blit(self.baseTexture, (288 * (i % 2) + 1668, 288 * j))
    
        
    def update(self):
        self.rect.top -= 15