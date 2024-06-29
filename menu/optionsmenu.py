from menu.menu import Menu
from utils.CustomSprite import CustomSprite


class OptionsMenu(Menu):
    def __init__(self, game, state="Options", previous_state=(None, None)):

        self.main_text = "Options"
        self.sub_text = "Music volume"

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

        # Sub title
        sub_title_sprite = CustomSprite(
            self.menu_fonts.render(self.sub_text, True, (255, 255, 255)),
            None
        )
        self.sprites.add(sub_title_sprite)

        self.position_sprites()
