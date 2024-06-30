from enum import Enum

import pygame

class PickaxeType(Enum):
    """
    Enum class for the different types of pickaxes.
    Contains the name of the pickaxe, the image, and the probability of the pickaxe to appear.
    """

    def __new__(cls, *args, **kwds):
        value = len(cls.__members__) + 1
        obj = object.__new__(cls)
        obj._value_ = value
        return obj

    def __init__(self, pickaxe_name, filename, next_pickaxe_cost, maxSpeed):
        self.pickaxe_name = pickaxe_name
        self.imageCollection = []
        self.maskCollection = []
        for i in range(1, 9):
            self.imageCollection.append(pygame.image.load(f"graphics/pickaxe/{pickaxe_name}/{filename}{i}.png"))
            self.maskCollection.append(pygame.mask.from_surface(self.imageCollection[-1]))
        self.next_pickaxe_cost = next_pickaxe_cost
        self.maxSpeed = maxSpeed

    WOOD_PICKAXE = ("wood_pickaxe", "Animation_bois", 100, 25)
    IRON_PICKAXE = ("iron_pickaxe", "Animation_fer", 200, 40)
    GOLD_PICKAXE = ("gold_pickaxe", "Animation_or", 300, 55)
    DIAMOND_PICKAXE = ("diamond_pickaxe", "Animation_diamant", None , 70)

class Pickaxe(pygame.sprite.Sprite):
    def __init__(self, initPos, destination, type):
        self.type = type
        super().__init__()
        self.tickFrame = 0
        self.mvtDir = 1
        self.imageCollection = self.type.imageCollection
        self.maskCollection = self.type.maskCollection
        self.playerPosVector = initPos
        self.maxSpeed = type.maxSpeed
        self.xSpeed = 0
        self.topLimit = initPos.y
        
        self.directionVector = pygame.Vector2(destination - initPos).normalize()

        self.image = self.imageCollection[0]
        self.mask = self.maskCollection[0]
        self.rect = self.image.get_rect(midtop = initPos)
        
        self.returnVector = pygame.Vector2(initPos - pygame.Vector2(self.rect.center))


    def switchDir(self):
        self.mvtDir = -1
    
    def animate(self):
        self.tickFrame = (self.tickFrame + 0.5) % 8
        self.image = self.imageCollection[int(self.tickFrame)]
        self.mask = self.maskCollection[int(self.tickFrame)]
        if self.rect.bottom > 1000:                                  #inversion du mvtDir quand on a atteind la portée maximale de la pioche
            self.switchDir()
            
        #self.rect.bottom += 20 * self.mvtDir                         #vitese de déplacement vertical * le mvtDir
        
        if self.mvtDir == 1:
            
            self.rect.centery += self.maxSpeed * self.directionVector.y
            if self.checkBound(self.directionVector.x):
                self.rect.centerx += self.maxSpeed * self.directionVector.x
        else:
            self.rect.centerx += self.maxSpeed * self.returnVector.x
            self.rect.centery += self.maxSpeed * self.returnVector.y
  
        
        if self.rect.centery - 10 <= self.topLimit:
            self.rect.centery = self.topLimit
            if self.rect.centerx < self.playerPosVector.x + 30 and self.rect.centerx > self.playerPosVector.x - 30:
                #kill() permet de supprimer le sprite de tous les groupes dans lequel il est présent
                self.kill()

    def checkBound(self, xSpeedThrow):
        if self.rect.left - xSpeedThrow <= 445 or self.rect.right + xSpeedThrow >= 1480:
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

    def evolve(self):
        """
        Evolve the pickaxe to the next level
        :return:
        """
        self.type = PickaxeType(self.type.value + 1)
        self.imageCollection = self.type.imageCollection
        self.maskCollection = self.type.maskCollection
        self.image = self.imageCollection[0]
        self.mask = self.maskCollection[0]
        self.rect = self.image.get_rect(midtop=self.rect.midtop)

        return self.type