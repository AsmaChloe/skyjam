import pygame

class CustomSprite(pygame.sprite.Sprite):
	def __init__(self, image, name, clickable = False, callback = None):
		super().__init__()
		self.image = image
		self.rect = self.image.get_rect()
		self.name = name
		self.clickable = clickable
		self.callback = callback

	def update(self, events):
		for event in events:

			if self.clickable and event.type == pygame.MOUSEBUTTONUP:
				if self.rect.collidepoint(event.pos):
					if self.callback is not None:
						self.callback(self.name)

