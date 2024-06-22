import pygame
from menu.menu import MenuSubOptions

class OptionsMenu(MenuSubOptions):
    def __init__(self, game, previous_state):
        MenuSubOptions.__init__(self, game, "Options", ["Sound", "Controls"], previous_state=previous_state)

    def validate(self):
        '''
        Validate the current option
        :return:
        '''
        if self.cursor_position == 0:
            print("Sound")
        elif self.cursor_position == 1:
            print("Controls")
        elif self.cursor_position == 2:
            self.game.current_menu = self.game.main_menu
            self.game.current_menu.state = "Main"
            self.game.current_menu.cursor_position = 0