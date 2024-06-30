import os

import pygame

from animations.MenuAnimation import MenuAnimation
from menu.menu import MenuSubOptions, Menu
from utils.JsonUtil import JsonUtil
from utils.CustomSprite import CustomSprite

class MainMenu(Menu):
    def __init__(self, game, state, logo_path, previous_state=(None, None)):
        menu_texts = ["Jouer", "Options", "Crédits", "Quitter", ""]
        self.logo_path = logo_path
        self.menu_texts = menu_texts
        self.validate_button_sound = pygame.mixer.Sound("sound/Boutons_Menu.wav")
        Menu.__init__(self, game, state, previous_state)

        self.animation = MenuAnimation((self.game.WIDTH * 1/5, self.game.HEIGHT * 3/4))
        self.sprites.add(self.animation)

    def create_sprites(self):
        """
        Create the sprites for the menu
        :return:
        """
        self.sprites = pygame.sprite.Group()
        # Title
        title_sprite = CustomSprite(
            pygame.image.load(self.logo_path),
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

        best_score_sprite = CustomSprite(
            self.menu_fonts.render(f"Meilleur score : {self.game.best_score} points", True, (255, 255, 255)),
            None
        )
        self.sprites.add(best_score_sprite)



    def validate(self, text):
        '''
        Validate the current option selected in the menu
        :return:
        '''
        self.game.sound_player.menu_button_channel.play(self.validate_button_sound)
        if text == "Jouer":
            self.game.playing = True
        elif text == "Options":
            self.game.current_menu = self.game.options_menu
            self.game.current_menu.state = "Options"
        elif text == "Crédits":
            self.game.current_menu = self.game.credit_menu
            self.game.current_menu.state = "Crédits"
        elif text == "Quitter":
            self.game.quit()