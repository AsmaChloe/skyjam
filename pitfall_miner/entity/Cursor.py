import pygame
from pygame.sprite import Sprite


class Cursor(Sprite) :
    """
    Cursor class : used to display the cursor on the screen which is an animated sprite
    """
    def __init__(self, position):
        super().__init__()

        self.position = position

        # Frequency of the cursor animation
        self.frequency = 100
        self.latest_update = pygame.time.get_ticks()

        self.image_collection = []
        nb_images = 8
        for i in range(1,nb_images+1):
            self.image_collection.append(pygame.image.load(f"graphics/cursor/curseur{i}.png").convert_alpha())

        self.image_index = 0
        self.image = self.image_collection[self.image_index]
        self.rect = self.image.get_rect(center = (self.position[0], self.position[1]))

    def update(self):
        """
        Update the cursor
        :return:
        """
        self.rect.center = pygame.mouse.get_pos()
        if pygame.time.get_ticks() - self.latest_update < self.frequency:
            return
        self.latest_update = pygame.time.get_ticks()
        self.image_index = (self.image_index + 1) % 8
        self.image = self.image_collection[self.image_index]