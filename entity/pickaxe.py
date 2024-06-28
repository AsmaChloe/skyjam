import pygame
import math

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
            
        self.rect.bottom += 20 * self.mvtDir                         #vitese de déplacement vertical * le mvtDir
        
        if self.mvtDir == 1:
            xSpeedThrow = ((self.destX - self.initX)*20)/740
            print(xSpeedThrow)
            self.rect.centerx += xSpeedThrow
        else:
            if self.playerX < self.rect.centerx:
                if self.xSpeed != -20:
                    self.xSpeed -= 2

            elif self.playerX > self.rect.centerx:
                if self.xSpeed != 20:
                    self.xSpeed += 2
  
                
            self.rect.centerx += self.xSpeed
        
        if self.rect.centery <= self.initY:
            self.rect.centery = self.initY
            if self.rect.centerx < self.playerX + 20 and self.rect.centerx > self.playerX - 20:
                self.kill()

    def updatePlayerPos(self, positionJoueur):
        self.playerX, self.playerY = positionJoueur
    
    def update(self):
        self.animate()