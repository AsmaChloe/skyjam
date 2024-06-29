import random

import pygame
from sys import exit
from random import choices

from entity.Cursor import Cursor
from entity.Obstacle import ObstacleType, generate_obstacle
from entity.Ore import OreType, generate_ore
from menu.mainmenu import MainMenu
from menu.optionsmenu import OptionsMenu
from menu.creditmenu import CreditMenu
from menu.gameover import GameOver
from entity.Entity import Entity
from entity.background import Background
from utils.CustomSprite import CustomSprite
from utils.MusicPlayer import MusicPlayer
from entity.pickaxe import Pickaxe
from entity.slowdown import Bat


class Game():
    def __init__(self):
        pygame.init()
        self.scrollSpeed = 10
        self.WIDTH, self.HEIGHT = 1920, 1080 #1280 , 720
        self.LEFT_BORDER, self.RIGHT_BORDER = 445, 1480
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        
        # Background
        self.bgSprite = Background(self.scrollSpeed)
        self.bg = pygame.sprite.GroupSingle(self.bgSprite)

        # Pickaxe
        self.pickaxe = pygame.sprite.GroupSingle()
        self.pickaxeClass = None

        # Music
        self.MUSIC_ON = True
        self.musics_filenames_dict = {'menu': 'music/menu_theme.mp3', 'game': 'music/groovy_ambient_funk.mp3', 'gameover': 'music/son_fin_placeholder.wav'}
        self.music_player = MusicPlayer(self.musics_filenames_dict, "menu")
        self.music_player.load_and_play("menu", {"loops": -1}, self.MUSIC_ON)

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

        #XP rectangle
        text = f"{self.player.XP} XP"
        self.XP_sprite = CustomSprite(
            pygame.font.Font("fonts/lemon_milk/LEMONMILK-Light.otf", size=30).render(text, True, (255, 255, 255)),
            "XP"
        )
        self.XP_sprite.rect.topleft = (20, 20)
        self.XPGS = pygame.sprite.GroupSingle(self.XP_sprite)

        # Cursor
        pygame.mouse.set_visible(False)
        self.cursor = Cursor(pygame.mouse.get_pos())
        self.cursorGS = pygame.sprite.GroupSingle(self.cursor)

        # Obstacles
        self.obstacle_frequency = 500 * (10/self.scrollSpeed)
        self.obstacles = pygame.sprite.Group()
        self.latest_obstacle = pygame.time.get_ticks()

        # Ores
        self.ore_frequency = 2000 * (10/self.scrollSpeed)
        self.ores = pygame.sprite.Group()
        self.latest_ore = pygame.time.get_ticks()
        
        #Buffs
        self.buff_frequency = 5000 * (10/self.scrollSpeed)
        self.buffs = pygame.sprite.Group()
        self.latest_buff = pygame.time.get_ticks()
        
        #Buff timer
        self.buff_begin = pygame.time.get_ticks()
        self.invicibilityBegin = pygame.time.get_ticks()

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
                        self.music_player.load_and_play("game", {"loops": -1}, self.MUSIC_ON)

                    # Generate environment : obstacles and ores
                    self.generate_environment()

                    self.bg.draw(self.screen)
                    self.pickaxe.draw(self.screen)
                    self.playerGS.draw(self.screen)
                    self.obstacles.draw(self.screen)
                    self.ores.draw(self.screen)

                    self.buffs.draw(self.screen)
                    self.manageInvicibility()

                    self.XPGS.draw(self.screen)


                    # Pickaxe
                    if self.pickaxeClass is not None and len(self.pickaxe):
                        self.pickaxeClass.updatePlayerPos(pygame.Vector2(self.player.rect.center))

                        #Collision pickaxe w/ anything
                        collided_obstacle = pygame.sprite.spritecollideany(self.pickaxeClass, self.obstacles, pygame.sprite.collide_mask)
                        collided_ore = pygame.sprite.spritecollideany(self.pickaxeClass, self.ores, pygame.sprite.collide_mask)
                        if collided_obstacle or collided_ore:
                            self.pickaxeClass.switchDir()

                            if(collided_ore) :
                                # Add XP
                                self.player.XP += collided_ore.ore_type.XP
                                self.XP_sprite.image = pygame.font.Font("fonts/lemon_milk/LEMONMILK-Light.otf", size=30).render(f"{self.player.XP} XP", True, (255, 255, 255))
                                # Remove ore
                                collided_ore.broken_sound.play()
                                collided_ore.kill()
                                del collided_ore
                            if(collided_obstacle) :
                                self.pickaxeClass.hitting_metal_sound.play()


                    # Collision player / obstacles
                    if pygame.sprite.spritecollide(self.player, self.obstacles, False, pygame.sprite.collide_mask):

                        # If the player has a bat
                        if self.player.isWithBat:
                            self.player.touchBat(False)
                            self.player.caughtBatSound.stop()
                            self.scrollSpeed = 10
                            self.bgSprite.setScrollSpeed(self.scrollSpeed)
                            self.update_frequencies()
                            self.player.isInvincible = True
                            self.invicibilityBegin = pygame.time.get_ticks()
                        elif not self.player.isInvincible:
                            self.gameOver = True
                            self.player.hurt_sounds[random.randint(0,2)].play()
                    
                    collidedBuff = pygame.sprite.spritecollideany(self.player, self.buffs)
                    
                    if collidedBuff is not None:
                        if isinstance(collidedBuff, Bat):
                            self.player.touchBat(True)
                            self.player.caughtBatSound.play()
                            self.buff_begin = pygame.time.get_ticks()
                            collidedBuff.kill()
                            self.scrollSpeed = 5
                            self.bgSprite.setScrollSpeed(self.scrollSpeed)
                            self.update_frequencies()
                            
                    if pygame.time.get_ticks() - self.buff_begin >= 10000:
                        self.player.touchBat(False)
                        self.player.caughtBatSound.stop()
                        self.scrollSpeed = 10
                        self.bgSprite.setScrollSpeed(self.scrollSpeed)
                        self.update_frequencies()



                    self.pickaxe.update()
                    self.bg.update()
                    self.playerGS.update()

                    self.obstacles.update(events, self.scrollSpeed)
                    self.ores.update(events, self.scrollSpeed)
                    self.buffs.update(self.scrollSpeed)
                    
                    self.XPGS.update(events)


                    if (self.ESC_KEY):
                        self.playing = False
                        self.reset_game()
                else:
                    pygame.surface.Surface.fill(self.screen, (0,0,0))

                    if not self.music_player.current_key == "gameover":
                        self.music_player.stop()
                        self.music_player.load_and_play("gameover", {"loops": 0}, self.MUSIC_ON)

                    self.current_menu = self.gameover_menu

                    self.current_menu.sprites.update(self.MOUSE_EVENTS)
                    self.current_menu.sprites.draw(self.screen)

            else:
                # Music

                if not self.music_player.current_key == "menu":
                    self.music_player.stop()
                    self.music_player.load_and_play("menu", {"loops": -1}, self.MUSIC_ON)

                self.current_menu.sprites.update(self.MOUSE_EVENTS)
                self.current_menu.sprites.draw(self.screen)

                if (self.ESC_KEY):
                    self.current_menu.back()

            self.cursorGS.draw(self.screen)
            self.cursorGS.update()

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
                            self.pickaxeClass = Pickaxe(pygame.Vector2(self.player.rect.midbottom), pygame.Vector2(event.pos), 25)
                            self.pickaxe.add(self.pickaxeClass)
                            self.player.throw()
                    else:
                        self.MOUSE_EVENTS.append(event)

    def reset_keys(self):
        self.UP_KEY, self.DOWN_KEY, self.ENTER_KEY, self.ESC_KEY = False, False, False, False
        self.MOUSE_EVENTS = []
    
    def update_frequencies(self):
        self.obstacle_frequency = 500 * (10/self.scrollSpeed)
        # Ores
        self.ore_frequency = 2000 * (10/self.scrollSpeed)
        
        #Buffs
        self.buff_frequency = 5000 * (10/self.scrollSpeed)
        
    def manageInvicibility(self):
        if self.player.isInvincible:
            if pygame.time.get_ticks() - self.invicibilityBegin >= 1000:
                self.player.isInvincible = False
    
    def reset_game(self):
        #screenreset
        self.screen.fill((0, 0, 0))

        #Player reset

        self.player.kill()
        self.player = Entity("player", pygame.Vector2(self.WIDTH / 2, 200))
        self.playerGS.add(self.player)

        self.player.XP = 0
        self.XP_sprite.image = pygame.font.Font("fonts/lemon_milk/LEMONMILK-Light.otf", size=30).render(f"{self.player.XP} XP", True, (255, 255, 255))

        #Obstacles reset
        self.obstacles.empty()
        self.latest_obstacle = pygame.time.get_ticks()

        #pickaxe reset
        if self.pickaxeClass is not None:
            self.pickaxeClass.kill()

        #Ores reset
        self.ores.empty()
        self.latest_ore = pygame.time.get_ticks()
        #flag reset
        self.gameOver = False

    def quit(self):
        pygame.quit()
        exit()

    def generate_environment(self) :
        # Generate obstacles
        current_time = pygame.time.get_ticks()
        if current_time - self.latest_obstacle > self.obstacle_frequency:
            self.latest_obstacle = current_time
            obstacle_type = ObstacleType(
                choices(list(ObstacleType), weights=[type.probability for type in ObstacleType], k=1)[0])
            self.obstacles.add(generate_obstacle(self, obstacle_type))

        # Generate ores
        if current_time - self.latest_ore > self.ore_frequency:
            self.latest_ore = current_time
            ore_type = choices(list(OreType), weights=[type.rarity for type in OreType], k=1)[0]
            new_ore = generate_ore(self, ore_type)
            #Check if the ore is not colliding with an obstacle
            if not pygame.sprite.spritecollide(new_ore, self.obstacles, False, None):
                self.ores.add(new_ore)
            else:
                new_ore.kill()
                del new_ore
        
        # Generate Buffs
        if current_time - self.latest_buff > self.buff_frequency:
            self.latest_buff = current_time
            new_buff = Bat(self.scrollSpeed).generate_buff(self)
            if not pygame.sprite.spritecollide(new_buff, self.buffs, False, None):
                self.buffs.add(new_buff)
            else:
                new_buff.kill()
                del new_buff
            
            