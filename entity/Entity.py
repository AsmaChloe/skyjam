import pygame


class Entity(pygame.sprite.Sprite):
    def __init__(self, name, position):
        super().__init__()
        self.name = name
        self.position = position
        self.side = True
        self.tickFrame = 0
        self.throwTickFrame = 0
        self.isThrowing = False
        self.xSpeed = 10
        
        self.imageCollection = []
        self.imageCollectionThrowing = []
        
        #collection image pour animation idle
        for i in range(1, 19):
            self.imageCollection.append(pygame.image.load(f"graphics/character/animation chute{i}.png").convert_alpha())
        
        #collection image pour animation lancé
        for i in range(1, 5):
            self.imageCollectionThrowing.append(pygame.image.load(f"graphics/character/hit/Lancé_pioche_animation{i}.png").convert_alpha())
        
        self.image = self.imageCollection[0]
        self.rect = self.image.get_rect(center = (self.position.x, self.position.y))

    def animate(self):
        #animation lancé
        if self.isThrowing:
            self.throwTickFrame = (self.throwTickFrame + 0.2)
            self.image = self.imageCollectionThrowing[int(self.throwTickFrame)]
            
            #4 frames sur l'animation donc on limite l'index à 3
            if int(self.throwTickFrame) == 3:
                self.throwTickFrame = 0
                self.isThrowing = False
        else:
            #animation IDLE
            self.tickFrame = (self.tickFrame + 0.2) % 18
            self.image = self.imageCollection[int(self.tickFrame)]
        
    def flipAnimation(self, leftRight):
        #fonction qui flip tous les sprites sur l'axe x quand on appuie sur le bouton de coté opposé
        if self.side is not leftRight:
            for i, img in enumerate(self.imageCollection):
                self.imageCollection[i] = pygame.transform.flip(img, True, False)
                
            for i, img in enumerate(self.imageCollectionThrowing):
                self.imageCollectionThrowing[i] = pygame.transform.flip(img, True, False)
        self.side = leftRight
    
    def throw(self):
        self.throwTickFrame = 0
        self.isThrowing = True
    
    def checkBound(self, leftRight):
        if leftRight:
            if self.rect.left - self.xSpeed <= 414:
                return False
            else:
                return True
        else:
            if self.rect.right + self.xSpeed >= 1506:
                return False
            else:
                return True
    
    def update(self):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_q] and self.checkBound(True):
            self.flipAnimation(True)
            self.rect.left -= self.xSpeed
                
        if keys[pygame.K_d] and self.checkBound(False):
            self.flipAnimation(False)
            self.rect.right += self.xSpeed
            
        self.animate()
        