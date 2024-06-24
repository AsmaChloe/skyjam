import pygame
from utils.CustomSprite import CustomSprite


class Entity(CustomSprite):
    def __init__(self, name, position):
        self.name = name
        self.position = position

        self.image_direction = {
            "up": [pygame.image.load("img/carrotFace.png").convert_alpha()],
            "down": [pygame.image.load("img/carrotFace.png").convert_alpha()],
            "left": [pygame.image.load("img/carrotWalkLeft.png").convert_alpha(), pygame.image.load("img/carrotWalkLeft2.png").convert_alpha()],
            "right": [pygame.image.load("img/carrotWalkRight1.png").convert_alpha(), pygame.image.load("img/carrotWalkRight2.png").convert_alpha()]
        }
        image = self.image_direction["up"][0]
        CustomSprite.__init__(self,image, name)

    def move(self, direction, dt, clock):
        img_nb = 0
        if direction == "up":
            self.position.y -= 300 * dt
        if direction == "down":
            self.position.y += 300 * dt
        if direction == "left":
            self.position.x -= 300 * dt
            img_nb = (int)(self.position.x % 2)
        if direction == "right":
            self.position.x += 300 * dt
            img_nb = (int)(self.position.x % 2)


        self.image = self.image_direction[direction][img_nb]