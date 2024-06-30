import os
from menu.menu import MenuSubOptions
from utils.JsonUtil import JsonUtil
from utils.CustomSprite import CustomSprite


class MainMenu(MenuSubOptions):
    def __init__(self, game, state="Main"):
        self.game = game
        MenuSubOptions.__init__(self, game, state, "Apericube", ["Jouer", "Options", "Crédits", "Quitter", ""])

    def create_sprites(self):
        super().create_sprites()

        best_score_sprite = CustomSprite(
            self.menu_fonts.render(f"Meilleur score : {self.game.best_score} points", True, (255, 255, 255)),
            None
        )
        self.sprites.add(best_score_sprite)

    def update(self):
        super().update()

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