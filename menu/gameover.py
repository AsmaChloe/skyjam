from menu.menu import MenuSubOptions


class GameOver(MenuSubOptions):
    def __init__(self, game, state = "GameOver"):
        MenuSubOptions.__init__(self, game, state, "Game Over", ["Rejouer", "Menu principal"])
        
    def validate(self, text):
        '''
        Validate the current option selected in the menu
        :return:
        '''
        if text == "Rejouer":
            self.game.reset_game()
        elif text == "Menu principal":
            self.game.playing = False
            self.game.reset_game()
