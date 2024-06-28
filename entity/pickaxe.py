import pygame

class Pickaxe(pygame.sprite.Sprite):
    def __init__(self, initPos):
        super().__init__()
        self.tickFrame = 0
        self.mvtDir = 1
        self.imageCollection = []
        self.initPos = initPos
        
        for i in range(1, 9):
            self.imageCollection.append(pygame.image.load(f"graphics/wood_pickaxe/Animation_bois{i}.png").convert_alpha())
            
        self.image = self.imageCollection[0]
        self.rect = self.image.get_rect(midtop = initPos)

    def switchDir(self):
        self.mvtDir = -1
    
    def animate(self):
        self.tickFrame = (self.tickFrame + 0.5) % 8
        self.image = self.imageCollection[int(self.tickFrame)]
        if self.rect.bottom > 950:
            self.switchDir()
            
        self.rect.bottom += 20 * self.mvtDir
        
        if self.rect.midtop <= self.initPos:
            self.kill()
        
    def update(self):
        self.animate()