import pygame


class Entity(pygame.sprite.Sprite):
    def __init__(self, name, position):
        super().__init__()
        self.name = name
        self.position = position
        self.lastTickTime = 0
        self.tickFrame = 0

        self.image_direction = {
            "up": [pygame.image.load("img/carrotFace.png").convert_alpha()],
            "down": [pygame.image.load("img/carrotFace.png").convert_alpha()],
            "left": [pygame.image.load("img/carrotWalkLeft.png").convert_alpha(), pygame.image.load("img/carrotWalkLeft2.png").convert_alpha()],
            "right": [pygame.image.load("img/carrotWalkRight1.png").convert_alpha(), pygame.image.load("img/carrotWalkRight2.png").convert_alpha()]
        }
        self.image = self.image_direction["up"][0]
        self.rect = self.image.get_rect(center = (self.position.x, self.position.y))

        
    def update(self):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_q]:
            left = self.image_direction["left"]
            if self.lastTickTime == 0:
                self.lastTickTime = pygame.time.get_ticks()
            elif pygame.time.get_ticks() - self.lastTickTime >= 350:
                self.tickFrame = not self.tickFrame
                self.lastTickTime = pygame.time.get_ticks()
            
            self.image = left[self.tickFrame]
                
            self.rect.left -= 5
                
        if keys[pygame.K_d]:
            right = self.image_direction["right"]
            if self.lastTickTime == 0:
                self.lastTickTime = pygame.time.get_ticks()
            elif pygame.time.get_ticks() - self.lastTickTime >= 350:
                self.tickFrame = not self.tickFrame
                self.lastTickTime = pygame.time.get_ticks()
            
            self.image = right[self.tickFrame]
            self.rect.right += 5
        