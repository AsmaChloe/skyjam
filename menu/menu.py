from abc import abstractmethod

import pygame

from utils.CustomSprite import CustomSprite


class Menu():
    def __init__(self, game, state, previous_state=(None, None)):
        self.game = game
        self.position = game.WIDTH // 2, game.HEIGHT // 2
        self.offset = 20
        # Previous state of the menu, a tuple with the name of the state and the menu object
        self.previous_state = previous_state
        self.state = state

        pygame.font.init()
        self.title_font = pygame.font.Font("fonts/8bit-wonder/8-BIT WONDER.TTF", size=60)
        self.menu_fonts = pygame.font.Font("fonts/8bit-wonder/8-BIT WONDER.TTF", size=40)

        self.sprites = pygame.sprite.Group()

        self.create_sprites()

        self.position_sprites()

    @abstractmethod
    def create_sprites(self):
        """
        Create the sprites for the menu
        :return:
        """
        pass

    def position_sprites(self):
        """
        Compute the position of the sprites based on the position of the whole menu and the offset between each sprite
        :return:
        """
        total_height = sum(sprite.image.get_height() + self.offset for sprite in self.sprites)
        start_y = self.position[1] - total_height // 2

        for sprite in self.sprites:
            sprite.rect = sprite.image.get_rect(center=(self.position[0], start_y))
            start_y += sprite.image.get_height() + self.offset

    def back(self):
        """
        Go back to the previous menu
        :return:
        """
        if self.previous_state[0] is not None:
            self.game.current_menu = self.previous_state[1]


class MenuSubOptions(Menu):
    def __init__(self, game, state, main_text, menu_texts, previous_state=(None, None)):
        self.main_text = main_text
        self.menu_texts = menu_texts
        self.validate_button_sound = pygame.mixer.Sound("sound/Boutons_Menu.wav")
        Menu.__init__(self, game, state, previous_state)

    def create_sprites(self):
        """
        Create the sprites for the menu
        :return:
        """
        # Title
        title_sprite = CustomSprite(
            self.title_font.render(self.main_text, True, (255, 255, 255)),
            None
        )
        self.sprites.add(title_sprite)

        # Sub options
        for i, text in enumerate(self.menu_texts):
            option_sprite = CustomSprite(
                self.menu_fonts.render(f"{text}", True, (255, 255, 255)),
                text,
                callback=self.validate,
                clickable=True
            )
            self.sprites.add(option_sprite)

    @abstractmethod
    def validate(self, text):
        '''
        Validate the current option selected in the menu
        :return:
        '''
        pass
