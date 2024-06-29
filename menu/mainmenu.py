from menu.menu import MenuSubOptions

import sys
import pygame

class MainMenu(MenuSubOptions):
    def __init__(self, game, state="Main"):
        MenuSubOptions.__init__(self, game, state, "Main Menu", ["Start Game", "Options", "Credits", "Exit"])

    def validate(self, text):
        '''
        Validate the current option selected in the menu
        :return:
        '''
        self.validate_button_sound.play()
        if text == "Start Game":
            self.game.playing = True
        elif text == "Options":
            self.game.current_menu = self.game.options_menu
            self.game.current_menu.state = "Options"
        elif text == "Credits":
            self.game.current_menu = self.game.credit_menu
            self.game.current_menu.state = "Credits"
        elif text == "Exit":
            self.game.quit()
