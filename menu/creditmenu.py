from menu.menu import Menu

from utils.CustomSprite import CustomSprite


class CreditMenu(Menu):
    def __init__(self, game, state="Crédits", previous_state=None):
        self.main_text = "Crédits - Les Apéri'Cubes"
        self.credits_list = [
            "Alexandre Kraoul Riera - Concept Artist",
            "Asma-Chloë Farah - Développeuse",
            "Clément Chapelle - Concept Artist & Son",
            "Corentin Dupont - Développeur",
            "Hugo Delay - Développeur",
            "Louis Guernier - Musique",
            "Yoann Le Cras - Concept Artist"
        ]
        
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

        # Credits
        for name in self.credits_list:
            credit_sprite = CustomSprite(
                self.menu_fonts.render(name, True, (255, 255, 255)),
                None
            )
            self.sprites.add(credit_sprite)

        self.position_sprites()