import pygame

class Background(pygame.sprite.Sprite):
    def __init__(self, scrollSpeed):
        super().__init__()
        self.baseTexture = pygame.image.load("img/cailloux.png").convert()
        self.middleTexture = pygame.image.load("graphics/background/Fond_gros.png").convert_alpha()
        self.leftWall = pygame.image.load('graphics/background/Mur_L.png').convert_alpha()
        self.rightWall = pygame.image.load('graphics/background/Mur_R.png').convert_alpha()
        self.image = pygame.Surface((2488, 500*1050))
        self.rect = self.image.get_rect(midtop = (1920/2, 0))
        self.scrollSpeed = scrollSpeed
        
        #le point de début de la zone est au pixel 414 et la fin au pixel 1506 et la zone fait 1092 pixels de large
        

        for i in range(500):
            #zone jouable
            self.image.blit(self.middleTexture, (650, 1050 * i))
        
        for j in range(1000):
            #mur de gauche
            self.image.blit(self.leftWall, (0, 525 * j))
            #mur de droite
            self.image.blit(self.rightWall, (1715, 525 * j))

            
            
                    
    
    def setScrollSpeed(self, scrollSpeed):
        self.scrollSpeed = scrollSpeed
        
    def update(self):
        self.rect.top -= self.scrollSpeed