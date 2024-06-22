import pygame
from menu.mainmenu import MainMenu
from menu.menu import MenuSubOptions
from menu.optionsmenu import OptionsMenu
from menu.creditmenu import CreditMenu


class Game():
    def __init__(self):
        pygame.init()
        self.WIDTH, self.HEIGHT = 1280, 720
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))

        self.clock = pygame.time.Clock()
        self.dt = 0

        self.running = True
        self.playing = False

        self.main_menu = MainMenu(self)
        self.options_menu = OptionsMenu(self, previous_state=("Main", self.main_menu))
        self.credit_menu = CreditMenu(self, previous_state=("Main", self.main_menu))
        self.current_menu = self.main_menu

        # keys
        self.UP_KEY, self.DOWN_KEY, self.ENTER_KEY, self.ESC_KEY = False, False, False, False

        self.player_pos = pygame.Vector2(self.WIDTH / 2, self.HEIGHT / 2)

    def game_loop(self):
        while self.running:
            self.screen.fill((0, 0, 0))

            if self.playing:
                # Game
                self.check_events()
                if (self.ESC_KEY):
                    self.playing = False
                pygame.draw.circle(self.screen, "red", self.player_pos, 40)

                keys = pygame.key.get_pressed()
                if keys[pygame.K_z]:
                    self.player_pos.y -= 300 * self.dt
                if keys[pygame.K_s]:
                    self.player_pos.y += 300 * self.dt
                if keys[pygame.K_q]:
                    self.player_pos.x -= 300 * self.dt
                if keys[pygame.K_d]:
                    self.player_pos.x += 300 * self.dt

                self.dt = self.clock.tick(60) / 1000
            else:
                # Menus
                text_surface, text_rect = self.current_menu.get_display()
                self.screen.blit(text_surface, text_rect)

                self.check_events()

                if (isinstance(self.current_menu, MenuSubOptions)):
                    if (self.UP_KEY):
                        self.current_menu.move_cursor("UP")
                    if (self.DOWN_KEY):
                        self.current_menu.move_cursor("DOWN")
                    if (self.ENTER_KEY):
                        self.current_menu.validate()
                if (self.ESC_KEY):
                    self.current_menu.back()

            # flip() the display to put your work on screen
            pygame.display.flip()

            self.clock.tick(60)  # limits FPS to 60

            self.reset_keys()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                # Arrow keys
                if event.key == pygame.K_UP:
                    self.UP_KEY = True
                if event.key == pygame.K_DOWN:
                    self.DOWN_KEY = True

                # Validate
                if event.key == pygame.K_RETURN:
                    self.ENTER_KEY = True

                # Back
                if event.key == pygame.K_ESCAPE:
                    self.ESC_KEY = True

    def reset_keys(self):
        self.UP_KEY, self.DOWN_KEY, self.ENTER_KEY, self.ESC_KEY = False, False, False, False

    def quit(self):
        pygame.quit()
