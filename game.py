import pygame
from sys import exit
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
        self.bgSprite = Background(self.scrollSpeed)
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

        self.player = Entity("player", pygame.Vector2(1920/2, 200))
        self.playerGS = pygame.sprite.GroupSingle(self.player)

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

                # Game
                self.bg.draw(self.screen)
                self.pickaxe.draw(self.screen)
                self.playerGS.draw(self.screen)


                self.bg.update()
                self.playerGS.update()
                
                if self.pickaxeClass is not None:
                    self.pickaxeClass.updatePlayerPos(self.player.rect.center)
                    
                self.pickaxe.update()

                if (self.ESC_KEY):
                    self.playing = False
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
