import pygame
from sys import exit
from random import randint, choice

from entity.Obstacle import Obstacle, ObstacleType
from menu.mainmenu import MainMenu
from menu.optionsmenu import OptionsMenu
from menu.creditmenu import CreditMenu
from entity.Entity import Entity
from entity.background import Background
from utils.MusicPlayer import MusicPlayer
from entity.pickaxe import Pickaxe


class Game():
    def __init__(self):
        pygame.init()
        self.WIDTH, self.HEIGHT = 1920, 1080 #1280 , 720
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))

        # Background
        self.bgSprite = Background()
        self.bg = pygame.sprite.GroupSingle(self.bgSprite)
        self.pickaxe = pygame.sprite.GroupSingle()
        self.pickaxeClass = None

        # Music
        self.musics_filenames_dict = { 'menu': 'music/menu_theme.mp3', 'game': 'music/groovy_ambient_funk.mp3'}
        self.music_player = MusicPlayer(self.musics_filenames_dict, "menu")
        self.music_player.load_and_play("menu", {"loops": -1})

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
                # Music
                if not self.music_player.current_key == "game":
                    self.music_player.stop()
                    self.music_player.load_and_play("game", {"loops": -1})



                # Generate obstacles
                current_time = pygame.time.get_ticks()
                if current_time - self.latest_obstacle > self.obstacle_frequency:
                    self.latest_obstacle = current_time
                    obstacle_type = ObstacleType(choice(list(ObstacleType)))
                    self.obstacles.add(self.generate_obstacle(obstacle_type))
                # Game
                self.bg.draw(self.screen)
                self.pickaxe.draw(self.screen)
                self.playerGS.draw(self.screen)
                self.obstacles.draw(self.screen)

                # Game


                self.bg.update()
                self.playerGS.update()

                if self.pickaxeClass is not None:
                    self.pickaxeClass.updatePlayerPos(self.player.rect.center)

                self.pickaxe.update()

                if (self.ESC_KEY):
                    self.playing = False
                # pygame.draw.circle(self.screen, "red", self.player.position, 40)

                self.bg.update()
                self.playerGS.update()
                self.obstacles.update(events)
            else:
                # Music
                if not self.music_player.current_key == "menu":
                    self.music_player.stop()
                    self.music_player.load_and_play("menu", {"loops": -1})

                self.current_menu.sprites.update(self.MOUSE_EVENTS)
                self.current_menu.sprites.draw(self.screen)

                if (self.ESC_KEY):
                    self.current_menu.back()

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
                if self.playing:
                    self.pickaxeClass = Pickaxe(self.player.rect.midbottom, event.pos)
                    self.pickaxe.add(self.pickaxeClass)
                    self.player.throw()
                else:
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