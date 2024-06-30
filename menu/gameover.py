import os
from menu.menu import MenuSubOptions
from utils.JsonUtil import JsonUtil
from utils.CustomSprite import CustomSprite

class GameOver(MenuSubOptions):
    def __init__(self, game, state = "GameOver", previous_state=(None, None)):
        self.game = game
        MenuSubOptions.__init__(self, game, state, "Game Over", 
                                ["Rejouer", "Menu principal", "",""],
                                  previous_state=previous_state)

    def create_sprites(self):
        super().create_sprites()
        
        score_sprite = CustomSprite(
            self.menu_fonts.render(f"Score x {self.game.score} points", True, (255, 255, 255)),
            None
        )
        best_score_sprite = CustomSprite(
            self.menu_fonts.render(f"Meilleur score x {self.game.best_score} points", True, (255, 255, 255)),
            None
        )
        self.sprites.add(score_sprite)
        self.sprites.add(best_score_sprite)

    def validate(self, text):
        '''
        Validate the current option selected in the menu
        :return:
        '''
        self.game.sound_player.menu_button_channel.play(self.validate_button_sound)
        if text == "Rejouer":
            self.game.reset_game()
            self.game.playing = True
        elif text == "Menu principal":
            self.game.reset_game()
            self.game.playing = False
        self.game.current_menu = self.game.main_menu
        self.game.current_menu.state = "Main"