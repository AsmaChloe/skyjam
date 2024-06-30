from menu.menu import MenuSubOptions

class MainMenu(MenuSubOptions):
    def __init__(self, game, state="Main"):
        MenuSubOptions.__init__(self, game, state, "Apericube", ["Jouer", "Options", "Crédits", "Quitter"])

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