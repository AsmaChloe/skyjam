import pygame
from sys import exit
from random import randint, choices

from entity.Obstacle import Obstacle, ObstacleType

from menu.mainmenu import MainMenu
from menu.optionsmenu import OptionsMenu
from menu.creditmenu import CreditMenu
from menu.gameover import GameOver

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
        self.musics_filenames_dict = {'menu': 'music/menu_theme.mp3', 'game': 'music/groovy_ambient_funk.mp3', 'gameover': 'music/son_fin_placeholder.wav'}
        self.music_player = MusicPlayer(self.musics_filenames_dict, "menu")
        self.music_player.load_and_play("menu", {"loops": -1})

        self.clock = pygame.time.Clock()
        self.dt = 0

        self.running = True
        self.playing = False
        self.gameOver = False

        # Menus
        self.main_menu = MainMenu(self)
        self.options_menu = OptionsMenu(self, previous_state=("Main", self.main_menu))
        self.credit_menu = CreditMenu(self, previous_state=("Main", self.main_menu))
        self.gameover_menu = GameOver(self)
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

    def game_loop(self):
        while self.running:
            events = pygame.event.get()

            self.screen.fill((0, 0, 0))
            self.check_events(events)

            if self.playing:
                if not self.gameOver:
                # Music
                    if not self.music_player.current_key == "game":
                        self.music_player.stop()
                        self.music_player.load_and_play("game", {"loops": -1})

                    # Generate obstacles
                    current_time = pygame.time.get_ticks()
                    if current_time - self.latest_obstacle > self.obstacle_frequency:
                        self.latest_obstacle = current_time
                        obstacle_type = ObstacleType(choices(list(ObstacleType), weights=[ type.value[2] for type in ObstacleType], k=1)[0])
                        self.obstacles.add(self.generate_obstacle(obstacle_type))

                    self.bg.draw(self.screen)
                    self.pickaxe.draw(self.screen)
                    self.playerGS.draw(self.screen)
                    self.obstacles.draw(self.screen)

                    if self.pickaxeClass is not None:
                        self.pickaxeClass.updatePlayerPos(pygame.Vector2(self.player.rect.center))

                    # Collision player / obstacles
                    if pygame.sprite.spritecollide(self.player, self.obstacles, False, pygame.sprite.collide_mask):
                        print("Collision")
                        self.gameOver = True
                        #self.reset_game()

                    self.pickaxe.update()
                    self.bg.update()
                    self.playerGS.update()
                    self.obstacles.update(events)
                    


                    if (self.ESC_KEY):
                        self.playing = False
                        self.reset_game()
                else:
                    pygame.surface.Surface.fill(self.screen, (0,0,0))
                    
                    if not self.music_player.current_key == "gameover":
                        self.music_player.stop()
                        self.music_player.load_and_play("gameover", {"loops": 0})
                        
                    self.current_menu = self.gameover_menu
                    
                    self.current_menu.sprites.update(self.MOUSE_EVENTS)
                    self.current_menu.sprites.draw(self.screen)
                    
            else:
                # Music
                self.current_menu = self.main_menu
                
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

            if self.gameOver:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.reset_game()
                
                if event.type == pygame.MOUSEBUTTONUP:
                    self.MOUSE_EVENTS.append(event)
                    
            else:
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
                        if not self.pickaxe.sprites():    #renvoie une liste des sprites. "not liste" fonctionne car une liste vide est implicitement un "False" en python
                            self.pickaxeClass = Pickaxe(pygame.Vector2(self.player.rect.midbottom), pygame.Vector2(event.pos), 20)
                            self.pickaxe.add(self.pickaxeClass)
                            self.player.throw()
                    else:
                        self.MOUSE_EVENTS.append(event)

    def reset_keys(self):
        self.UP_KEY, self.DOWN_KEY, self.ENTER_KEY, self.ESC_KEY = False, False, False, False
        self.MOUSE_EVENTS = []

    def reset_game(self):
        #screenreset
        self.screen.fill((0, 0, 0))
        
        #Player reset
        self.player.position = pygame.Vector2(self.WIDTH / 2, 200)
        self.player.rect.center = self.player.position

        #Obstacles reset
        self.obstacles.empty()
        self.latest_obstacle = pygame.time.get_ticks()
        
        #pickaxe reset
        self.pickaxeClass.kill()
        
        #flag reset
        self.gameOver = False

    def quit(self):
        pygame.quit()
        exit()

    def generate_obstacle(self, obstacle_type):
        """
        Generates an obstacle based on the type
        :param obstacle_type:
        :return:
        """
        if (obstacle_type == ObstacleType.WHOLE_BEAM):
            x_top_mid = randint(self.LEFT_BORDER + obstacle_type.value[1].get_width() // 2,
                                self.RIGHT_BORDER - obstacle_type.value[1].get_width() // 2)
        elif (obstacle_type == ObstacleType.LEFT_SMALL_BEAM):
            x_top_mid = self.LEFT_BORDER + obstacle_type.value[1].get_width() // 2 - 100
        elif (obstacle_type == ObstacleType.RIGHT_SMALL_BEAM):
            x_top_mid = self.RIGHT_BORDER - obstacle_type.value[1].get_width() // 2 + 100

        y_top_mid = self.HEIGHT

        return Obstacle(pygame.Vector2(x_top_mid, y_top_mid), 15, obstacle_type)
