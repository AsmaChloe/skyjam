from menu.menu import MenuSubOptions


class GameOver(MenuSubOptions):
    def __init__(self, game, state = "GameOver", previous_state=(None, None)):
        MenuSubOptions.__init__(self, game, state, "Game Over", ["Rejouer", "Menu principal"], previous_state=previous_state)
        
    def validate(self, text):
        '''
        Validate the current option selected in the menu
        :return:
        '''
        if text == "Restart":
            self.game.reset_game()
            self.game.playing = True
        elif text == "Main menu":
            self.game.reset_game()
            self.game.playing = False
        self.game.current_menu = self.game.main_menu
        self.game.current_menu.state = "Main"