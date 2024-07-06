import pygame

from utils.CustomSprite import CustomSprite


class PickaxeHittingObstacleAnimation(CustomSprite) :
    def __init__(self, sound_player, position, scroll_speed):
        self.image_collection = [
            pygame.image.load(f"graphics/obstacles/hitting_animation/Animation TING{i}.png").convert_alpha() for i in
            range(1, 5)]
        self.img_index = 0
        image = self.image_collection[self.img_index]
        name = "PickaxeHittingObstacleAnimation"
        super().__init__(image, name)

        self.rect.center = position

        self.hitting_metal_sound = pygame.mixer.Sound("sound/Impacte_Pioche_Metal.wav")
        sound_player.pickaxe_channel.play(self.hitting_metal_sound)

        self.scroll_speed = scroll_speed

    def update(self, events):
        self.img_index = (self.img_index + 0.4)
        if int(self.img_index) >= len(self.image_collection):
            self.kill()
        else:
            self.image = self.image_collection[int(self.img_index)]
            self.rect.top -= self.scroll_speed