import pygame


class Pickaxe(pygame.sprite.Sprite):
    def __init__(self, initPos, destination, speed):
        super().__init__()
        self.tickFrame = 0
        self.mvtDir = 1
        self.imageCollection = []
        self.maskCollection = []
        self.playerPosVector = initPos
        self.xMaxSpeed = speed
        self.xSpeed = 0
        self.topLimit = initPos.y
        
        self.directionVector = pygame.Vector2(destination - initPos).normalize()

        
        #self.turning = False
        
        for i in range(1, 9):
            self.imageCollection.append(pygame.image.load(f"graphics/wood_pickaxe/Animation_bois{i}.png").convert_alpha())
            self.maskCollection.append(pygame.mask.from_surface(self.imageCollection[-1]))
            
        self.image = self.imageCollection[0]
        self.mask = self.maskCollection[0]
        self.rect = self.image.get_rect(midtop = initPos)
        
        self.returnVector = pygame.Vector2(initPos - pygame.Vector2(self.rect.center))

    def switchDir(self):
        self.mvtDir = -1
    
    def animate(self):
        #durée de l'animation avec une vitesse de 20 pixels par frame : 65 frames (un peu plus d'une seconde)
        self.tickFrame = (self.tickFrame + 0.5) % 8
        self.image = self.imageCollection[int(self.tickFrame)]
        self.mask = self.maskCollection[int(self.tickFrame)]
        if self.rect.bottom > 1000:                                  #inversion du mvtDir quand on a atteind la portée maximale de la pioche
            self.switchDir()
            
        #self.rect.bottom += 20 * self.mvtDir                         #vitese de déplacement vertical * le mvtDir
        
        if self.mvtDir == 1:
            
            self.rect.centery += self.xMaxSpeed * self.directionVector.y
            if self.checkBound(self.directionVector.x):
                self.rect.centerx += self.xMaxSpeed * self.directionVector.x
        else:
            self.rect.centerx += self.xMaxSpeed * self.returnVector.x
            self.rect.centery += self.xMaxSpeed * self.returnVector.y
  
        
        if self.rect.centery - 10 <= self.topLimit:
            self.rect.centery = self.topLimit
            if self.rect.centerx < self.playerPosVector.x + 30 and self.rect.centerx > self.playerPosVector.x - 30:
                #kill() permet de supprimer le sprite de tous les groupes dans lequel il est présent
                self.kill()

    def checkBound(self, xSpeedThrow):
        if self.rect.left - xSpeedThrow <= 414 or self.rect.right + xSpeedThrow >= 1506:
            self.switchDir()
            return False
        return True
    
    def updatePlayerPos(self, positionJoueur):
        self.playerPosVector = positionJoueur
        self.returnVector = pygame.Vector2(self.playerPosVector - pygame.Vector2(self.rect.center)).normalize()
        
    
    def update(self):
        self.animate()

    def overlap(self, object_mask, object_rect):
        """
        Check if the pickaxe is overlapping with another object
        :param object_mask:
        :param object_rect:
        :return:
        """

        if self.mask.overlap(object_mask, (object_rect.x - self.rect.x, object_rect.y - self.rect.y)):
            return True
        return False