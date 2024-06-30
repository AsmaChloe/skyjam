import pygame


class Entity(pygame.sprite.Sprite):
    def __init__(self, game, name, position):
        super().__init__()
        self.game = game
        self.name = name
        self.position = position
        self.side = True
        
        self.tickFrame = 0
        self.throwTickFrame = 0
        self.batTickFame = 0
        self.protectionTickFrame = 0
        
        self.isThrowing = False
        self.xSpeed = 10
        self.isWithBat = False
        self.caughtBatSound = pygame.mixer.Sound("sound/Chauve_souris.wav")
        self.caughtShieldSound = pygame.mixer.Sound("sound/Bouclier.wav")
        self.isInvincible = False
        self.isProtected = False
        self.isEvolvingPickaxe = False
        
        self.imageCollection = []

        
        self.imageCollectionThrowing = []

        
        self.imageCollectionBat = []

        
        self.imageCollectionBatThrowing = []

        
        self.imageCollectionProtected = []

        
        #collection image pour animation idle
        for i in range(1, 19):
            self.imageCollection.append(pygame.image.load(f"graphics/character/animation chute{i}.png").convert_alpha())
            
        
        #collection image pour animation lancé
        for i in range(1, 5):
            self.imageCollectionThrowing.append(pygame.image.load(f"graphics/character/hit/Lancé_pioche_animation{i}.png").convert_alpha())
            
        
        for i in range(1, 13):
            self.imageCollectionBat.append(pygame.image.load(f"graphics/character/avec_chauve_souris/Chauve souris qui se débat{i}.png").convert_alpha())
           
            
        for i in range(1, 3):
            self.imageCollectionBatThrowing.append(pygame.image.load(f"graphics/character/avec_chauve_souris/hit/Chauve souris qui se débat{i}.png").convert_alpha())
            
        
        for i in range(1, 19):
            self.imageCollectionProtected.append(pygame.image.load(f'graphics/character/protected/animation bouclier joueur{i}.png'))
            
        
        self.image = pygame.Surface((290, 320), pygame.SRCALPHA, 32).convert_alpha()
        self.rect = self.image.get_rect(center = (self.position.x, self.position.y))

        self.XP = 0

        self.throw_sound = pygame.mixer.Sound("sound/Lancer.wav")
        self.hurt_sounds = [pygame.mixer.Sound("sound/Aie_1.wav"), pygame.mixer.Sound("sound/Aie_2.wav"), pygame.mixer.Sound("sound/Aie_3.wav")]

    def animate(self):
        self.image = pygame.Surface((290, 320), pygame.SRCALPHA, 32).convert_alpha()
 
        if not self.isWithBat:
            #animation lancé
            if self.isThrowing:
                self.throwTickFrame = (self.throwTickFrame + 0.2)
                self.image.blit(self.imageCollectionThrowing[int(self.throwTickFrame)], self.imageCollectionThrowing[int(self.throwTickFrame)].get_rect(center = (290/2, 320/2)))
                
                #4 frames sur l'animation donc on limite l'index à 3
                if int(self.throwTickFrame) == 3:
                    self.throwTickFrame = 0
                    self.isThrowing = False
            else:
                #animation IDLE
                self.tickFrame = (self.tickFrame + 0.2) % 18
                self.image.blit(self.imageCollection[int(self.tickFrame)], self.imageCollection[int(self.tickFrame)].get_rect(center = (290/2, 320/2)))
        else:
            if self.isThrowing:
                self.throwTickFrame = (self.throwTickFrame + 0.5)
                self.batTickFame = (self.batTickFame + 0.2) % 12
                self.image.blit(self.imageCollectionBatThrowing[int(self.batTickFame)%2], self.imageCollectionBatThrowing[int(self.batTickFame)%2].get_rect(center = (290/2, 320/2)))
                if int(self.throwTickFrame) == 3:
                    self.throwTickFrame = 0
                    self.isThrowing = False
            else:
                self.batTickFame = (self.batTickFame + 0.2) % 12
                self.image.blit(self.imageCollectionBat[int(self.batTickFame)], self.imageCollectionBat[int(self.batTickFame)].get_rect(center = (290/2, 320/2)))
        
        if self.isProtected:
            self.protectionTickFrame = (self.protectionTickFrame + 0.15) % 18
            if self.isWithBat:
                shield = pygame.transform.rotozoom(self.imageCollectionProtected[int(self.protectionTickFrame)], 0, 1.5)
            else:
                shield = self.imageCollectionProtected[int(self.protectionTickFrame)]
            self.image.blit(shield, shield.get_rect(center = (290/2, 320/2))) 
        self.mask = pygame.mask.from_surface(self.image)
        
    def touchBat(self, isBatTouched):
        self.isWithBat = isBatTouched
        
    def flipAnimation(self, leftRight):
        #fonction qui flip tous les sprites sur l'axe x quand on appuie sur le bouton de coté opposé
        if self.side is not leftRight:
            for i, img in enumerate(self.imageCollection):
                self.imageCollection[i] = pygame.transform.flip(img, True, False)
                
            for i, img in enumerate(self.imageCollectionThrowing):
                self.imageCollectionThrowing[i] = pygame.transform.flip(img, True, False)
            
            for i, img in enumerate(self.imageCollectionBat):
                self.imageCollectionBat[i] = pygame.transform.flip(img, True, False)
            
            for i, img in enumerate(self.imageCollectionBatThrowing):
                self.imageCollectionBatThrowing[i] = pygame.transform.flip(img, True, False)
                
        self.side = leftRight
    
    def throw(self):
        self.throwTickFrame = 0
        self.isThrowing = True
        self.game.sound_player.pickaxe_channel.play(self.throw_sound)
    
    def checkBound(self, leftRight):
        leftBound = 365
        rightBound = 1570
        
        if self.isWithBat:
            leftBound = 395
            rightBound = 1545
        
        if self.isProtected:
            leftBound = 405
            rightBound = 1540
        
        if self.isProtected and self.isWithBat:
            leftBound = 447
            rightBound = 1498
        
        if leftRight:
            if self.rect.left - self.xSpeed <= leftBound:
                return False
            else:
                return True
        else:
            if self.rect.right + self.xSpeed >= rightBound:
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

    def overlap(self, object_mask, object_rect):
        """
        Check if an object is overlapping with the entity
        :param object_mask: mask of the object
        :param object_rect: rect of the object
        :return:
        """
        if self.mask.overlap(object_mask, (object_rect.x - self.rect.x, object_rect.y - self.rect.y)):
            return True

        return False

    def protect(self, newState):
        self.isProtected = newState