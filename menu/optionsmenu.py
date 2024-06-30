from menu.menu import Menu
from utils.CustomSprite import CustomSprite


class OptionsMenu(Menu):
    def __init__(self, game, state="Options", previous_state=(None, None)):

        self.main_text = "Options"
        self.sub_text = f"Musique * {'On' if game.MUSIC_ON else 'Off'}"

        self.title_sprite = None
        self.sub_title_sprite = None
        Menu.__init__(self, game, state, previous_state)

    def create_sprites(self):
        """
        Create the sprites for the menu
        :return:
        """
        # Title
        self.title_sprite = CustomSprite(
            self.title_font.render(self.main_text, True, (255, 255, 255)),
            None
        )
        self.sprites.add(self.title_sprite)

        # Sub title
        self.sub_title_sprite = CustomSprite(
            self.menu_fonts.render(self.sub_text, True, (255, 255, 255)),
            name = self.sub_text,
            clickable=True,
            callback=self.toggle_music
        )
        self.sprites.add(self.sub_title_sprite)

        self.position_sprites()

    def toggle_music(self, name):
        """
        Toggle the music on/off
        :return:
        """
        self.game.MUSIC_ON = not self.game.MUSIC_ON
        self.sub_text = f"Musique * {'On' if self.game.MUSIC_ON else 'Off'}"
        self.sub_title_sprite.image = self.menu_fonts.render(self.sub_text, True, (255, 255, 255))

        if self.game.sound_player.is_on() and not self.game.MUSIC_ON :
            self.game.sound_player.stop()
        elif not self.game.sound_player.is_on() and self.game.MUSIC_ON:
            self.game.sound_player.load_and_play("menu", {"loops": -1}, self.game.MUSIC_ON)