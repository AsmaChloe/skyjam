from abc import abstractmethod

import pygame

class Menu() :
    def __init__(self, game, previous_state=(None, None)):
        self.game = game
        self.position = game.WIDTH // 2, game.HEIGHT // 2
        pygame.font.init()
        self.title_font = pygame.font.Font("fonts/lemon_milk/LEMONMILK-MediumItalic.otf", size=60)
        self.menu_fonts = pygame.font.Font("fonts/lemon_milk/LEMONMILK-Light.otf", size=40)
        # self.title_font = pygame.font.Font(pygame.font.get_default_font(), size=60)
        # self.menu_fonts = pygame.font.Font(pygame.font.get_default_font(), size=40)
        self.offset = 60

        self.previous_state = previous_state

        # Parameters returned to the game loop
        self.text_surface = None
        self.text_rect = None

    def back(self):
        if self.previous_state[0] is not None:
            self.game.current_menu = self.previous_state[1]

    @abstractmethod
    def build_interface(self, surface, text_surfaces):
        pass

    def get_display(self):
        '''
        Return the text surface and the text rect
        :return:
        '''
        return self.text_surface, self.text_rect


class MenuSubOptions(Menu):
    def __init__(self, game, main_text, menu_texts, previous_state=(None, None)):
        Menu.__init__(self, game, previous_state)

        self.main_text = main_text
        self.menu_texts = menu_texts

        self.cursor = "*"
        self.cursor_position = 0
        self.cursor_max_position = len(self.menu_texts) - 1

        self.main_text_surface = self.title_font.render(self.main_text, True, (255, 255, 255))
        self.menu_text_surfaces = [self.menu_fonts.render(f"  {text}", True, (255, 255, 255)) if i != self.cursor_position
                                   else self.menu_fonts.render(f"{self.cursor} {text}", True, (255, 255, 255))
                                   for i, text in enumerate(self.menu_texts)]

        # Determine the width and height of the text surface based on the widest text surface
        self.text_block_width = max(self.main_text_surface.get_width(), max([text.get_width() for text in self.menu_text_surfaces]))
        self.text_block_height = self.main_text_surface.get_height() + sum([text.get_height() for text in self.menu_text_surfaces]) + self.offset

        self.text_surface = self.build_interface(self.main_text_surface, self.menu_text_surfaces)
        self.text_rect = self.text_surface.get_rect(center=self.position)

    def build_interface(self, main_test_surface, text_surfaces):
        text_surface = pygame.Surface((self.text_block_width, self.text_block_height))
        text_surface.fill((0, 0, 0))
        text_surface.blit(main_test_surface, (0, 0))
        for i, text in enumerate(text_surfaces):
            text_surface.blit(text, (0, (i+1) * self.offset))

        return text_surface

    def move_cursor(self, direction):
        '''
        Move the cursor up or down
        :param direction:
        :return:
        '''

        self.menu_text_surfaces[self.cursor_position] = self.menu_fonts.render(f"  {self.menu_texts[self.cursor_position]}", True, (255, 255, 255))

        if direction == "UP":
            if self.cursor_position == 0:
                self.cursor_position = self.cursor_max_position
            else:
                self.cursor_position -= 1
        elif direction == "DOWN":
            if self.cursor_position == self.cursor_max_position:
                self.cursor_position = 0
            else:
                self.cursor_position += 1

        self.menu_text_surfaces[self.cursor_position] = self.menu_fonts.render(f"{self.cursor} {self.menu_texts[self.cursor_position]}", True, (255, 255, 255))


        self.text_surface = self.build_interface(self.main_text_surface, self.menu_text_surfaces)
        self.text_rect = self.text_surface.get_rect(center=self.position)

    @abstractmethod
    def validate(self):
        '''
        Validate the current option
        :return:
        '''
        pass
