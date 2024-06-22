from menu.menu import Menu
import pygame

class CreditMenu(Menu):
    def __init__(self, game, previous_state):
        Menu.__init__(self, game, previous_state)

        self.main_text = "Credits"
        self.sub_text = "By Les apéricubes"

        self.main_text_surface = self.title_font.render(self.main_text, True, (255, 255, 255))
        self.sub_text_surface = self.menu_fonts.render(self.sub_text, True, (255, 255, 255))

        # Determine the width and height of the text surface based on the widest text surface
        self.text_block_width = max(self.main_text_surface.get_width(), self.sub_text_surface.get_width())
        self.text_block_height = self.main_text_surface.get_height() + self.sub_text_surface.get_height()

        self.text_surface, self.text_rect = self.build_interface()

    def build_interface(self):
        '''
        Build the interface
        :return:
        '''
        text_surface = pygame.Surface((self.text_block_width, self.text_block_height))
        text_surface.fill((0,0,0))

        # Calculate the positions to center the texts
        main_text_x = (self.text_block_width - self.main_text_surface.get_width()) // 2
        sub_text_x = (self.text_block_width - self.sub_text_surface.get_width()) // 2

        text_surface.blit(self.main_text_surface, (main_text_x, 0))
        text_surface.blit(self.sub_text_surface, (sub_text_x, self.main_text_surface.get_height()))

        return text_surface, text_surface.get_rect(center=self.position)