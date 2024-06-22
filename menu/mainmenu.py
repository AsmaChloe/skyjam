import pygame
from menu.menu import MenuSubOptions

class MainMenu(MenuSubOptions):
    def __init__(self, game):
        MenuSubOptions.__init__(self, game, "Main Menu", ["Start Game", "Options", "Credits"])

    def validate(self):
        '''
        Validate the current option
        :return:
        '''
        if self.cursor_position == 0:
            self.game.playing = True
        elif self.cursor_position == 1:
            self.game.current_menu = self.game.options_menu
            self.game.current_menu.state = "Options"
            self.game.current_menu.cursor_position = 0
        elif self.cursor_position == 2:
            self.game.current_menu = self.game.credit_menu
            self.game.current_menu.state = "Credits"
            self.game.current_menu.cursor_position = 0
