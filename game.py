import pygame
from menu.mainmenu import MainMenu
from menu.optionsmenu import OptionsMenu
from menu.creditmenu import CreditMenu
from entity.Entity import Entity

class Game():
    def __init__(self):
        pygame.init()
        self.WIDTH, self.HEIGHT = 1280, 720
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))

        self.clock = pygame.time.Clock()
        self.dt = 0

        self.running = True
        self.playing = False

        # Menus
        self.main_menu = MainMenu(self)
        self.options_menu = OptionsMenu(self, previous_state=("Main", self.main_menu))
        self.credit_menu = CreditMenu(self, previous_state=("Main", self.main_menu))
        self.current_menu = self.main_menu

        # Events
        self.UP_KEY, self.DOWN_KEY, self.ENTER_KEY, self.ESC_KEY = False, False, False, False
        self.MOUSE_EVENTS = []

        self.player = Entity("player", pygame.Vector2(self.WIDTH / 2, self.HEIGHT / 2))

    def game_loop(self):
        while self.running:
            events = pygame.event.get()

            self.screen.fill((0, 0, 0))
            self.check_events(events)

            if self.playing:
                # Game
                if (self.ESC_KEY):
                    self.playing = False
                # pygame.draw.circle(self.screen, "red", self.player.position, 40)
                self.screen.blit(self.player.image, self.player.position)

                keys = pygame.key.get_pressed()
                if keys[pygame.K_z]:
                    self.player.move("up", self.dt, self.clock)
                if keys[pygame.K_s]:
                    self.player.move("down", self.dt, self.clock)
                if keys[pygame.K_q]:
                    self.player.move("left", self.dt, self.clock)
                if keys[pygame.K_d]:
                    self.player.move("right", self.dt, self.clock)

                self.dt = self.clock.tick(60) / 1000
            else:
                # Menus
                self.current_menu.sprites.update(self.MOUSE_EVENTS)
                self.current_menu.sprites.draw(self.screen)

                if (self.ESC_KEY):
                    self.current_menu.back()

            # flip() the display to put your work on screen
            pygame.display.flip()

            self.clock.tick(60)  # limits FPS to 60

            self.reset_keys()

    def check_events(self, events):
        for event in events:
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

            if event.type == pygame.MOUSEBUTTONUP:
                self.MOUSE_EVENTS.append(event)

    def reset_keys(self):
        self.UP_KEY, self.DOWN_KEY, self.ENTER_KEY, self.ESC_KEY = False, False, False, False
        self.MOUSE_EVENTS = []

    def quit(self):
        pygame.quit()
