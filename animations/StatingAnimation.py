import pygame

from utils.CustomSprite import CustomSprite


class StartingAnimation(CustomSprite):
    def __init__(self, position):
        self.image_collection = [pygame.image.load(f"graphics/character/starting_animation/animation intro{i}.png") for i in range(1, 42)]
        self.img_index = 0
        image = self.image_collection[self.img_index]
        name = "StartingAnimation"
        super().__init__(image, name)

        self.rect.center = position

    def update(self, events):
        self.image = self.image_collection[(int)(self.img_index)]
        self.img_index += 0.2
        if self.img_index >= 41:
            self.kill()
        # self.rect.center = self.rect.center