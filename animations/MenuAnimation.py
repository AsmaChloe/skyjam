import pygame.image

from utils.CustomSprite import CustomSprite


class MenuAnimation(CustomSprite) :
    def __init__(self, position):
        self.img_index = 0
        self.image_collection = [pygame.image.load(f"graphics/character/menu/animation marche{i}.png") for i in range(1,7)]
        name = "MenuAnimation"
        image = self.image_collection[self.img_index]

        super().__init__(image, name, position)

        self.rect.center = position

    def update(self, events):
        self.img_index += 0.1
        self.image = self.image_collection[int(self.img_index) % len(self.image_collection)]
        super().update(events)