import pygame


class Entity(pygame.sprite.Sprite):
    def __init__(self, name, position):
        super().__init__()
        self.name = name
        self.position = position
        self.side = True
        self.tickFrame = 0

        '''self.image_direction = {
            "up": [pygame.image.load("img/carrotFace.png").convert_alpha()],
            "down": [pygame.image.load("img/carrotFace.png").convert_alpha()],
            "left": [pygame.image.load("img/carrotWalkLeft.png").convert_alpha(), pygame.image.load("img/carrotWalkLeft2.png").convert_alpha()],
            "right": [pygame.image.load("img/carrotWalkRight1.png").convert_alpha(), pygame.image.load("img/carrotWalkRight2.png").convert_alpha()]
        }'''
        
        self.imageCollection = []
        
        for i in range(1, 19):
            self.imageCollection.append(pygame.image.load(f"graphics/character/animation chute{i}.png").convert_alpha())
            
        self.image = self.imageCollection[0]
        self.rect = self.image.get_rect(center = (self.position.x, self.position.y))

    def animate(self):
        self.tickFrame = (self.tickFrame + 0.2) % 18
        self.image = self.imageCollection[int(self.tickFrame)]
        
    def flipAnimation(self, leftRight):
        if self.side is not leftRight:
            for i, img in enumerate(self.imageCollection):
                self.imageCollection[i] = pygame.transform.flip(img, True, False)
        self.side = leftRight
    
    def update(self):

        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_q]:
            '''left = self.image_direction["left"]
            if self.lastTickTime == 0:
                self.lastTickTime = pygame.time.get_ticks()
            elif pygame.time.get_ticks() - self.lastTickTime >= 350:
                self.tickFrame = not self.tickFrame
                self.lastTickTime = pygame.time.get_ticks()
            
            self.image = left[self.tickFrame]'''
            
            self.flipAnimation(True)
                
            self.rect.left -= 10
                
        if keys[pygame.K_d]:
            '''right = self.image_direction["right"]
            if self.lastTickTime == 0:
                self.lastTickTime = pygame.time.get_ticks()
            elif pygame.time.get_ticks() - self.lastTickTime >= 350:
                self.tickFrame = not self.tickFrame
                self.lastTickTime = pygame.time.get_ticks()
            
            self.image = right[self.tickFrame]'''
            self.flipAnimation(False)
            
            self.rect.right += 10
            
        self.animate()
        