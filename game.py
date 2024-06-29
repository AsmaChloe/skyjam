import pygame
from sys import exit
from random import choices

from entity.Obstacle import Obstacle, ObstacleType, generate_obstacle
from entity.Ore import OreType, Ore, generate_ore
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
        self.scrollSpeed = 15
        self.WIDTH, self.HEIGHT = 1920, 1080 #1280 , 720
        self.LEFT_BORDER, self.RIGHT_BORDER = 414, 1506
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        
        # Background
        self.bgSprite = Background(self.scrollSpeed)
        
        self.bg = pygame.sprite.GroupSingle(self.bgSprite)

        # Pickaxe
        self.pickaxe = pygame.sprite.GroupSingle()
        self.pickaxeClass = None


        # Music
        self.musics_filenames_dict = {'menu': 'music/menu_theme.mp3', 'game': 'music/groovy_ambient_funk.mp3'}
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
        self.player = Entity("player", pygame.Vector2(self.WIDTH / 2, 200))
        self.playerGS = pygame.sprite.GroupSingle(self.player)

        # Obstacles
        self.obstacle_frequency = 500
        self.obstacles = pygame.sprite.Group()
        self.latest_obstacle = pygame.time.get_ticks()

        # Ores
        self.ore_frequency = 2000
        self.ores = pygame.sprite.Group()
        self.latest_ore = pygame.time.get_ticks()

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

                # Generate environment : obstacles and ores
                self.generate_environment()

                self.bg.draw(self.screen)
                self.pickaxe.draw(self.screen)
                self.playerGS.draw(self.screen)
                self.obstacles.draw(self.screen)
                self.ores.draw(self.screen)

                if self.pickaxeClass is not None:
                    self.pickaxeClass.updatePlayerPos(self.player.rect.center)

                # # Collision player / obstacles
                # if pygame.sprite.spritecollide(self.player, self.obstacles, False, pygame.sprite.collide_mask):
                #     print("Collision")
                #     self.playing = False
                #     self.reset_game()

                self.pickaxe.update()
                self.bg.update()
                self.playerGS.update()
                self.obstacles.update(events)
                self.ores.update(events)

                if (self.ESC_KEY):
                    self.playing = False
                    self.reset_game()
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

    def reset_game(self):
        #Player reset
        self.player.position = pygame.Vector2(self.WIDTH / 2, 200)
        self.player.rect.center = self.player.position

        #Obstacles reset
        self.obstacles.empty()
        self.latest_obstacle = pygame.time.get_ticks()

        #Ores reset
        self.ores.empty()
        self.latest_ore = pygame.time.get_ticks()

    def quit(self):
        pygame.quit()
        exit()

    def generate_environment(self) :
        # Generate obstacles
        current_time = pygame.time.get_ticks()
        if current_time - self.latest_obstacle > self.obstacle_frequency:
            self.latest_obstacle = current_time
            obstacle_type = ObstacleType(
                choices(list(ObstacleType), weights=[type.value[2] for type in ObstacleType], k=1)[0])
            self.obstacles.add(generate_obstacle(self, obstacle_type))

        # Generate ores
        if current_time - self.latest_ore > self.ore_frequency:
            self.latest_ore = current_time
            ore_type = choices(list(OreType), weights=[type.value[3] for type in OreType], k=1)[0]
            new_ore = generate_ore(self, ore_type)
            #Check if the ore is not colliding with an obstacle
            if not pygame.sprite.spritecollide(new_ore, self.obstacles, False, None):
                self.ores.add(new_ore)
            else:
                new_ore.kill()
                del new_ore
