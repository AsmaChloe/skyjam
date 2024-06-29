import pygame


class Pickaxe(pygame.sprite.Sprite):
    def __init__(self, initPos, destination):
        super().__init__()
        self.tickFrame = 0
        self.mvtDir = 1
        self.imageCollection = []
        self.initPos = initPos
        self.initX , self.initY = initPos
        self.destX, self.destY = destination
        self.playerX, self.playerY = initPos
        self.xSpeed = 0
        
        self.directionVector = pygame.Vector2((self.destX - self.initX, self.destY - self.initY)).normalize()
        self.posVector = pygame.Vector2((self.initX, self.initY))
        
        #self.turning = False
        
        for i in range(1, 9):
            self.imageCollection.append(pygame.image.load(f"graphics/wood_pickaxe/Animation_bois{i}.png").convert_alpha())
            
        self.image = self.imageCollection[0]
        self.rect = self.image.get_rect(midtop = initPos)

    def switchDir(self):
        self.mvtDir = -1
    
    def animate(self):
        #durée de l'animation avec une vitesse de 20 pixels par frame : 65 frames (un peu plus d'une seconde)
        self.tickFrame = (self.tickFrame + 0.5) % 8
        self.image = self.imageCollection[int(self.tickFrame)]
        if self.rect.bottom > 1000:                                  #inversion du mvtDir quand on a atteind la portée maximale de la pioche
            self.switchDir()
            
        #self.rect.bottom += 20 * self.mvtDir                         #vitese de déplacement vertical * le mvtDir
        
        if self.mvtDir == 1:
            #formule vitesse x => Vy * (dx/dy) => Vy fixe, dx distance entre xDestination et xDépart, dy la hauteur de travel (fixe, limite-centreDuPersonnage)
            #xSpeedThrow = ((self.destX - self.initX)*20)/740
            
            self.rect.centery += 20 * self.directionVector.y
            if self.checkBound(self.directionVector.x):
                self.rect.centerx += 20 * self.directionVector.x
        else:
            if self.playerX < self.rect.centerx:
                #effet progressif du changement de vitesse pour faire faire des petites courbes à la pioche (bien plus beau)
                if self.xSpeed != -20:
                    self.xSpeed -= 2

            elif self.playerX > self.rect.centerx:
                if self.xSpeed != 20:
                    self.xSpeed += 2
            self.rect.centery -= 20
  
                
            self.rect.centerx += self.xSpeed
        
        if self.rect.centery <= self.initY:
            self.rect.centery = self.initY
            if self.rect.centerx < self.playerX + 20 and self.rect.centerx > self.playerX - 20:
                #kill() permet de supprimer le sprite de tous les groupes dans lequel il est présent
                self.kill()

    def checkBound(self, xSpeedThrow):
        if self.rect.left - xSpeedThrow <= 414 or self.rect.right + xSpeedThrow >= 1506:
            self.switchDir()
            return False
        return True
    
    def updatePlayerPos(self, positionJoueur):
        self.playerX, self.playerY = positionJoueur
    
    def update(self):
        self.animate()