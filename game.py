import pygame
from sys import exit
from random import randint, choice

from entity.Obstacle import Obstacle, ObstacleType
from menu.mainmenu import MainMenu
from menu.optionsmenu import OptionsMenu
from menu.creditmenu import CreditMenu
from entity.Entity import Entity
from entity.background import Background

class Game():
    def __init__(self):
        pygame.init()
        self.WIDTH, self.HEIGHT =1280 , 720 # 1920, 1080
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))

        # Background
        self.bgSprite = Background()
        self.bg = pygame.sprite.GroupSingle(self.bgSprite)

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

        # Player
        self.player = Entity("player", pygame.Vector2(1920/2, 200))
        self.playerGS = pygame.sprite.GroupSingle(self.player)

        #Obstacles
        self.obstacle_frequency = 1000
        self.obstacles = pygame.sprite.Group()
        self.obstacles.add(self.generate_obstacle(ObstacleType.WHOLE_BEAM))
        self.latest_obstacle = pygame.time.get_ticks()

    def game_loop(self):
        while self.running:

            events = pygame.event.get()

            self.screen.fill((0, 0, 0))

            
            self.check_events(events)

            if self.playing:

                # Generate obstacles
                current_time = pygame.time.get_ticks()
                if current_time - self.latest_obstacle > self.obstacle_frequency:
                    self.latest_obstacle = current_time
                    obstacle_type = ObstacleType(choice(list(ObstacleType)))
                    self.obstacles.add(self.generate_obstacle(obstacle_type))

                self.bg.draw(self.screen)
                self.playerGS.draw(self.screen)
                self.obstacles.draw(self.screen)

                # Game
                if (self.ESC_KEY):
                    self.playing = False
                # pygame.draw.circle(self.screen, "red", self.player.position, 40)

                self.bg.update()
                self.playerGS.update()
                self.obstacles.update(events)
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
        exit()

    def generate_obstacle(self, obstacle_type):
        x = randint(0, self.WIDTH)
        y = self.HEIGHT

        obstacle = Obstacle(pygame.Vector2(x, y), 5, obstacle_type)

        return obstacle