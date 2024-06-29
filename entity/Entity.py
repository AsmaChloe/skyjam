import pygame


class Entity(pygame.sprite.Sprite):
    def __init__(self, name, position):
        super().__init__()
        self.name = name
        self.position = position
        self.side = True
        
        self.tickFrame = 0
        self.throwTickFrame = 0
        self.batTickFame = 0
        
        self.isThrowing = False
        self.xSpeed = 10
        self.isWithBat = False
        self.caughtBatSound = pygame.mixer.Sound("sound/Chauve_souris.wav")
        self.isInvincible = False
        
        self.imageCollection = []
        self.maskCollection = []
        
        self.imageCollectionThrowing = []
        self.maskCollectionThrowing = []
        
        self.imageCollectionBat = []
        self.maskCollectionBat = []
        
        self.imageCollectionBatThrowing = []
        self.maskCollectionBatThrowing = []
        
        #collection image pour animation idle
        for i in range(1, 19):
            self.imageCollection.append(pygame.image.load(f"graphics/character/animation chute{i}.png").convert_alpha())
            self.maskCollection.append(pygame.mask.from_surface(self.imageCollection[-1]))
        
        #collection image pour animation lancé
        for i in range(1, 5):
            self.imageCollectionThrowing.append(pygame.image.load(f"graphics/character/hit/Lancé_pioche_animation{i}.png").convert_alpha())
            self.maskCollectionThrowing.append(pygame.mask.from_surface(self.imageCollectionThrowing[-1]))
        
        for i in range(1, 13):
            self.imageCollectionBat.append(pygame.image.load(f"graphics/character/avec_chauve_souris/Chauve souris qui se débat{i}.png").convert_alpha())
            self.maskCollectionBat.append(pygame.mask.from_surface(self.imageCollectionBat[-1]))
            
        for i in range(1, 3):
            self.imageCollectionBatThrowing.append(pygame.image.load(f"graphics/character/avec_chauve_souris/hit/Chauve souris qui se débat{i}.png").convert_alpha())
            self.maskCollectionBatThrowing.append(pygame.mask.from_surface(self.imageCollectionBatThrowing[-1]))
        
        self.image = self.imageCollection[0]
        self.mask = self.maskCollection[0]
        self.rect = self.image.get_rect(center = (self.position.x, self.position.y))

        self.XP = 0

        self.throw_sound = pygame.mixer.Sound("sound/Lancer.wav")
        self.hurt_sounds = [pygame.mixer.Sound("sound/Aie_1.wav"), pygame.mixer.Sound("sound/Aie_2.wav"), pygame.mixer.Sound("sound/Aie_3.wav")]

    def animate(self):
        if not self.isWithBat:
            #animation lancé
            if self.isThrowing:
                self.throwTickFrame = (self.throwTickFrame + 0.2)
                self.image = self.imageCollectionThrowing[int(self.throwTickFrame)]
                self.mask = self.maskCollectionThrowing[int(self.throwTickFrame)]
                
                #4 frames sur l'animation donc on limite l'index à 3
                if int(self.throwTickFrame) == 3:
                    self.throwTickFrame = 0
                    self.isThrowing = False
            else:
                #animation IDLE
                self.tickFrame = (self.tickFrame + 0.2) % 18
                self.image = self.imageCollection[int(self.tickFrame)]
                self.mask = self.maskCollection[int(self.tickFrame)]
        else:
            if self.isThrowing:
                self.throwTickFrame = (self.throwTickFrame + 0.5)
                self.batTickFame = (self.batTickFame + 0.2) % 12
                self.image = self.imageCollectionBatThrowing[int(self.batTickFame)%2]
                self.mask = self.maskCollectionBatThrowing[int(self.batTickFame)%2]
                if int(self.throwTickFrame) == 3:
                    self.throwTickFrame = 0
                    self.isThrowing = False
            else:
                self.batTickFame = (self.batTickFame + 0.2) % 12
                self.image = self.imageCollectionBat[int(self.batTickFame)]
                self.mask = self.maskCollectionBat[int(self.batTickFame)]
        
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
        self.throw_sound.play()
    
    def checkBound(self, leftRight):
        if leftRight:
            if self.rect.left - self.xSpeed <= 445:
                return False
            else:
                return True
        else:
            if self.rect.right + self.xSpeed >= 1480:
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