import random
import os
import pygame
from sys import exit
from random import choices

from entity.Cursor import Cursor
from entity.Obstacle import ObstacleType, generate_obstacle
from entity.Ore import OreType, generate_ore
from entity.PickaxeHittingObstacleAnimation import PickaxeHittingObstacleAnimation
from menu.mainmenu import MainMenu
from menu.optionsmenu import OptionsMenu
from menu.creditmenu import CreditMenu
from menu.gameover import GameOver
from entity.Entity import Entity
from entity.background import Background
from utils.CustomSprite import CustomSprite
from utils.SoundPlayer import SoundPlayer
from entity.pickaxe import Pickaxe, PickaxeType
from entity.slowdown import Bat
from entity.protection import Protection
from entity.boom import Dynamite


class Game():
    def __init__(self):
        pygame.init()
        self.scrollSpeed = 10
        self.WIDTH, self.HEIGHT = 1920, 1080 #1280 , 720
        self.LEFT_BORDER, self.RIGHT_BORDER = 445, 1480
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        
        # Background
        self.bgSprite = Background(self.scrollSpeed, (1920/2, 0))
        self.bg = pygame.sprite.Group(self.bgSprite)
        self.newBg = None

        # Pickaxe
        self.pickaxe = None
        self.pickaxeGS = pygame.sprite.GroupSingle()
        self.pickaxe_Hitting_Animation = pygame.sprite.Group()
        self.pickaxe_type = PickaxeType.WOOD_PICKAXE
        self.max_XP = self.pickaxe_type.next_pickaxe_cost if self.pickaxe_type.next_pickaxe_cost is not None else 0

        # Music
        self.MUSIC_ON = True

        self.musics_filenames_dict = {'menu': 'music/menu_theme.mp3', 'game': 'music/game_theme.wav', 'gameover': 'music/son_fin_placeholder.wav'}
        self.sound_player = SoundPlayer(self.musics_filenames_dict, "menu")
        self.sound_player.load_and_play("menu", {"loops": -1}, self.MUSIC_ON)

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
        self.player = Entity(self,"player", pygame.Vector2(self.WIDTH / 2, 200))
        self.playerGS = pygame.sprite.GroupSingle(self.player)

        # XP bar images
        self.xp_bar_images = { i : pygame.image.load(f"img/xp/xp_bar_{i}.png").convert_alpha() for i in range(0,101,5)}
        self.image = self.xp_bar_images[0]
        self.xp_bar = CustomSprite(self.image, "xp_bar")
        self.xp_barGS = pygame.sprite.GroupSingle(self.xp_bar)
        self.update_xp_bar()

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
        
        #BigBuffs = Dynamite, canari
        self.big_buff_frequency = 5000 * (10/self.scrollSpeed)
        self.big_buffs = pygame.sprite.Group()
        self.latest_big_buff = pygame.time.get_ticks()
        self.dynamite_buff_timer = pygame.time.get_ticks()
        
        #Buff timer
        self.buff_begin = pygame.time.get_ticks()
        self.invicibilityBegin = pygame.time.get_ticks()

        #Custom userevent pickaxe hits walls
        self.WALLHITLEFT = pygame.USEREVENT + 1
        self.WALLHITRIGHT = pygame.USEREVENT + 2

    def game_loop(self):
        while self.running:
            events = pygame.event.get()

            self.screen.fill((0, 0, 0))
            self.check_events(events)

            if self.playing:
                if not self.gameOver:
                    # Music
                    if not self.sound_player.current_key == "game":
                        self.sound_player.stop()
                        self.sound_player.load_and_play("game", {"loops": -1}, self.MUSIC_ON)

                    # Generate environment : obstacles and ores
                    self.generate_environment()
                    self.manage_background()

                    self.bg.draw(self.screen)
                    self.pickaxeGS.draw(self.screen)
                    self.playerGS.draw(self.screen)
                    self.obstacles.draw(self.screen)
                    self.ores.draw(self.screen)
                    self.pickaxe_Hitting_Animation.draw(self.screen)
                    self.buffs.draw(self.screen)
                    self.xp_barGS.draw(self.screen)
                    self.big_buffs.draw(self.screen)

                    self.manageInvicibility()

                    # Pickaxe
                    if len(self.pickaxeGS):
                        self.pickaxe.updatePlayerPos(pygame.Vector2(self.player.rect.center))

                        #Collision pickaxe w/ anything
                        collided_obstacle = pygame.sprite.spritecollideany(self.pickaxe, self.obstacles, pygame.sprite.collide_mask)
                        collided_ore = pygame.sprite.spritecollideany(self.pickaxe, self.ores, pygame.sprite.collide_mask)
                        if collided_obstacle or collided_ore:

                            if not self.pickaxe.noHit:
                                if(collided_ore) :
                                    # Add XP
                                    self.player.XP += collided_ore.ore_type.XP

                                    # Remove ore
                                    self.sound_player.ore_channel.play(collided_ore.broken_sound)
                                    collided_ore.broken = True
                                    collided_ore.broken_sound.play()

                                    if self.pickaxe_type != PickaxeType.DIAMOND_PICKAXE and self.player.XP >= self.pickaxe_type.next_pickaxe_cost:
                                        self.player.XP -= self.pickaxe_type.next_pickaxe_cost
                                        self.pickaxe_type, self.max_XP = self.pickaxe.evolve()

                                    self.update_xp_bar()

                                if(collided_obstacle) :
                                    self.display_collision_animation(self.pickaxe.rect.midbottom)
                            self.pickaxe.switchDir()
                            
                            
                    collidedBuff = pygame.sprite.spritecollideany(self.player, self.buffs, pygame.sprite.collide_mask)
                    collidedBigBuff = pygame.sprite.spritecollideany(self.player, self.big_buffs, pygame.sprite.collide_mask)
                    
                    if collidedBigBuff is not None:
                        print(collidedBigBuff)
                        if isinstance(collidedBigBuff, Dynamite) and not self.player.isDynamite:
                            self.sound_player.player_channel.play(self.player.caughtDynamiteSound)
                            collidedBigBuff.kill()
                            self.player.isDynamite = True
                            self.player.isInvincible = True
                            self.dynamite_buff_timer = pygame.time.get_ticks()
                    else:
                        if collidedBuff is not None and not self.player.isDynamite:
                            if isinstance(collidedBuff, Bat):
                                self.player.touchBat(True)
                                self.sound_player.bat_channel.play(self.player.caughtBatSound)
                                self.buff_begin = pygame.time.get_ticks()
                                collidedBuff.kill()
                                self.scrollSpeed = 5
                                self.updateBackgroundScrollSpeed()
                                self.update_frequencies()
                            
                            if isinstance(collidedBuff, Protection):
                                self.player.protect(True)
                                self.player.caughtShieldSound.play()
                                collidedBuff.kill()
                    
                    # Collision player / obstacles
                    if pygame.sprite.spritecollide(self.player, self.obstacles, False, pygame.sprite.collide_mask):

                        # If the player has a bat
                        if self.player.isWithBat:
                            self.player.touchBat(False)
                            self.sound_player.bat_channel.stop()
                            self.scrollSpeed = 10
                            self.updateBackgroundScrollSpeed()
                            self.update_frequencies()
                            self.player.isInvincible = True
                            self.invicibilityBegin = pygame.time.get_ticks()
                        elif self.player.isProtected and not self.player.isInvincible:
                            self.player.protect(False)
                            self.player.isInvincible = True
                            self.invicibilityBegin = pygame.time.get_ticks()
                        elif not self.player.isInvincible and not self.player.isDynamiteDuring:
                            self.gameOver = True

                            self.sound_player.player_channel.play(self.player.hurt_sounds[random.randint(0, 2)])
                            self.sound_player.stop_sounds_at_game_over()
                
                            
                    if (pygame.time.get_ticks() - self.dynamite_buff_timer >= 3500) and self.player.isDynamite and not self.player.isDynamiteStarting and not self.player.isDynamiteDuring and not self.player.isDynamiteEnding:
                        self.scrollSpeed = 50
                        self.player.isProtected = False
                        self.player.isWithBat = False
                        self.player.isThrowing = False
                        self.player.isDynamiteStarting = True
                        if self.pickaxe is not None:
                            self.pickaxe.kill()
                        self.updateBackgroundScrollSpeed()
                        self.update_frequencies()
                    
                    if (pygame.time.get_ticks() - self.dynamite_buff_timer > 3500) and (pygame.time.get_ticks() - self.dynamite_buff_timer < 8500):
                        self.player.isInvincible = True
                        self.invicibilityBegin = pygame.time.get_ticks()
                        
                        
                    if (pygame.time.get_ticks() - self.dynamite_buff_timer >= 8500) and self.player.isDynamite:
                        self.scrollSpeed = 10
                        self.player.isDynamiteDuring = False
                        self.player.isDynamiteEnding = True
                        self.player.dynamiteTickFrame = 0
                        self.player.isDynamite = False
                        self.updateBackgroundScrollSpeed()
                        self.update_frequencies()
                            
                    if (pygame.time.get_ticks() - self.buff_begin) >= 10000 and self.player.isWithBat:
                        self.player.touchBat(False)
                        self.sound_player.bat_channel.stop()
                        self.scrollSpeed = 10
                        self.updateBackgroundScrollSpeed()
                        self.update_frequencies()

                    self.pickaxeGS.update()
                    self.playerGS.update()
                    self.obstacles.update(events, self.scrollSpeed)
                    self.ores.update(events, self.scrollSpeed)
                    self.pickaxe_Hitting_Animation.update(events)
                    self.buffs.update(self.scrollSpeed)
                    self.xp_barGS.update(events)
                    self.big_buffs.update(self.scrollSpeed)
                    self.bg.update()


                    if (self.ESC_KEY):
                        self.playing = False
                        self.reset_game()
                else:
                    pygame.surface.Surface.fill(self.screen, (0,0,0))

                    if not self.sound_player.current_key == "gameover":
                        self.sound_player.stop()
                        self.sound_player.load_and_play("gameover", {"loops": 0}, self.MUSIC_ON)

                    self.current_menu = self.gameover_menu

                    self.current_menu.sprites.update(self.MOUSE_EVENTS)
                    self.current_menu.sprites.draw(self.screen)

            else:
                # Music
                if not self.sound_player.current_key == "menu":
                    self.sound_player.stop()
                    self.sound_player.load_and_play("menu", {"loops": -1}, self.MUSIC_ON)

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
                        if not self.pickaxeGS.sprites():    #renvoie une liste des sprites. "not liste" fonctionne car une liste vide est implicitement un "False" en python
                            self.pickaxe = Pickaxe(pygame.Vector2(self.player.rect.center), pygame.Vector2(event.pos), 25, self.pickaxe_type, self.WALLHITLEFT, self.WALLHITRIGHT)
                            self.pickaxeGS.add(self.pickaxe)
                            self.player.throw()
                    else:
                        self.MOUSE_EVENTS.append(event)
                if event.type == self.WALLHITLEFT:
                    self.display_collision_animation(self.pickaxe.rect.bottomleft)

                if event.type == self.WALLHITRIGHT:
                    self.display_collision_animation(self.pickaxe.rect.bottomright)




    def reset_keys(self):
        self.UP_KEY, self.DOWN_KEY, self.ENTER_KEY, self.ESC_KEY = False, False, False, False
        self.MOUSE_EVENTS = []
    
    def update_frequencies(self):
        if self.scrollSpeed == 0:
            speed = 0.00001
        else:
            speed = self.scrollSpeed
        self.obstacle_frequency = 500 * (10/speed)
        # Ores
        self.ore_frequency = 2000 * (10/speed)
        
        #Buffs
        self.buff_frequency = 5000 * (10/speed)
        
        #Big buffs
        self.big_buff_frequency = 5000 * (10/speed)
        
    def manageInvicibility(self):
        if self.player.isInvincible and not self.player.isDynamiteDuring:
            if pygame.time.get_ticks() - self.invicibilityBegin >= 1000:
                self.player.isInvincible = False
    
    def reset_game(self):
        #screenreset
        self.screen.fill((0, 0, 0))

        #Player reset

        self.player.kill()
        self.player = Entity(self,"player", pygame.Vector2(self.WIDTH / 2, 200))
        self.playerGS.add(self.player)

        self.player.XP = 0
        self.update_xp_bar()

        #Pickaxe reset
        if self.pickaxe is not None:
            self.pickaxe.kill()
            self.pickaxe = None
        self.pickaxeGS.empty()
        self.pickaxe_type = PickaxeType.WOOD_PICKAXE

        #Obstacles reset
        self.obstacles.empty()
        self.latest_obstacle = pygame.time.get_ticks()

        #pickaxe reset
        if self.pickaxe is not None:
            self.pickaxe.kill()

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

            
            if random.choice(["Bat", "Protection"]) == "Bat":
                new_buff = Bat(self.scrollSpeed, self.sound_player).generate_buff(self)
            else:
                new_buff = Protection(self.scrollSpeed).generate_buff(self)
                
            if (not pygame.sprite.spritecollide(new_buff, self.buffs, False, None)
                    and not pygame.sprite.spritecollide(new_buff, self.obstacles, False, None)
                    and not pygame.sprite.spritecollide(new_buff, self.ores, False, None)):

                self.buffs.add(new_buff)
            else:
                new_buff.kill()
                del new_buff
        
            #Generate big buffs
            if current_time - self.latest_big_buff> self.big_buff_frequency:
                self.latest_big_buff = current_time

                new_big_buff = Dynamite(self.scrollSpeed).generate_buff(self)
                '''if random.choice(["Dynamite"]) == "Dynamite":
                    new_big_buff = Dynamite(self.scrollSpeed).generate_buff(self)
                else:
                    pass'''
                    
                if (not pygame.sprite.spritecollide(new_big_buff, self.buffs, False, None)
                        and not pygame.sprite.spritecollide(new_big_buff, self.obstacles, False, None)
                        and not pygame.sprite.spritecollide(new_big_buff, self.ores, False, None)
                        and not pygame.sprite.spritecollide(new_big_buff, self.big_buffs, False, None)):

                    self.big_buffs.add(new_big_buff)
                    print(self.big_buffs)
                else:
                    new_big_buff.kill()
                    del new_big_buff

                
    def manage_background(self):
        if self.bgSprite.rect.top <= 0 and self.newBg is None:
            self.newBg = Background(self.scrollSpeed, (1920/2, self.bgSprite.rect.bottom))
            self.bg.add(self.newBg)
        
        if self.bgSprite.rect.bottom <= 0:
            self.bgSprite.kill()
            del self.bgSprite
            self.bgSprite = self.newBg
            self.newBg = None

    def update_xp_bar(self):
        if self.max_XP == 0:
            xp_level = 100
        else :
            xp_level_percentage = (self.player.XP / self.max_XP) * 100
            xp_level = int(xp_level_percentage // 5 * 5)

        self.xp_bar.image = self.xp_bar_images[xp_level]
        self.xp_bar.rect.topleft = (self.WIDTH - self.xp_bar.rect.width - 70, 23)


    def display_collision_animation(self, position):
        self.pickaxe_Hitting_Animation.add(PickaxeHittingObstacleAnimation(self.sound_player, position, self.scrollSpeed))

    def updateBackgroundScrollSpeed(self):
        self.bgSprite.setScrollSpeed(self.scrollSpeed)
        if self.newBg is not None:
            self.newBg.setScrollSpeed(self.scrollSpeed)
    