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
from entity.pickaxe import Pickaxe
from entity.slowdown import Bat
from utils.JsonUtil import JsonUtil

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
        self.pickaxe_Hitting_Animation = pygame.sprite.Group()
        self.pickaxeClass = None

        # Music
        self.MUSIC_ON = True
        self.musics_filenames_dict = {'menu': 'music/menu_theme.mp3', 'game': 'music/groovy_ambient_funk.mp3', 'gameover': 'music/son_fin_placeholder.wav'}
        self.sound_player = SoundPlayer(self.musics_filenames_dict, "menu")
        self.sound_player.load_and_play("menu", {"loops": -1}, self.MUSIC_ON)

        self.clock = pygame.time.Clock()
        self.dt = 0

        # Score that depends on time spent in game
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.scoring_json_file_path = os.path.join(current_dir, 'save', 'scoring.json')

        self.scoring_json_file = JsonUtil.load_json(self.scoring_json_file_path)

        self.score_tick = 0
        self.score = 0
        self.best_score = self.scoring_json_file.get("best")
        
        self.score_sprite = CustomSprite(
            pygame.font.Font("fonts/8bit-wonder/8-BIT WONDER.TTF", size=30).render(f"Score * {self.score}", True, (255, 255, 255)),
            "score"
        )
        self.score_GS = pygame.sprite.GroupSingle()
        self.score_sprite.rect.topleft = (20, 20)
        self.score_GS.add(self.score_sprite)

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

        self.load_xp_bar_images()
        # XP bar image
        self.image = pygame.image.load("img/xp/xp_bar_0.png").convert_alpha()
        self.custom_sprite = CustomSprite(self.image, "xp_bar")
        self.sprite_group = pygame.sprite.GroupSingle(self.custom_sprite)
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
                    if not self.sound_player.current_key == "game":
                        self.sound_player.stop()
                        self.sound_player.load_and_play("game", {"loops": -1}, self.MUSIC_ON)

                    # Generate environment : obstacles and ores
                    self.generate_environment()

                    self.bg.draw(self.screen)
                    self.pickaxe.draw(self.screen)
                    self.playerGS.draw(self.screen)
                    self.obstacles.draw(self.screen)
                    self.ores.draw(self.screen)
                    self.pickaxe_Hitting_Animation.draw(self.screen)
                    self.buffs.draw(self.screen)

                    self.manageInvicibility()

                    self.sprite_group.draw(self.screen)
                    self.score_GS.draw(self.screen)

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
                                self.update_xp_bar()

                                # Remove ore
                                self.sound_player.ore_channel.play(collided_ore.broken_sound)
                                collided_ore.broken = True
                                collided_ore.broken_sound.play()
                            if(collided_obstacle) :
                                print(f"Collided obstacle mask pos: {collided_obstacle.mask.get_bounding_rects()}")
                                self.display_collision_animation(collided_obstacle)



                    # Collision player / obstacles
                    if pygame.sprite.spritecollide(self.player, self.obstacles, False, pygame.sprite.collide_mask):

                        # If the player has a bat
                        if self.player.isWithBat:
                            self.player.touchBat(False)
                            self.sound_player.bat_channel.stop()
                            self.scrollSpeed = 10
                            self.bgSprite.setScrollSpeed(self.scrollSpeed)
                            self.update_frequencies()
                            self.player.isInvincible = True
                            self.invicibilityBegin = pygame.time.get_ticks()
                        elif not self.player.isInvincible:
                            self.gameOver = True
                            self.sound_player.player_channel.play(self.player.hurt_sounds[random.randint(0, 2)])
                            self.sound_player.stop_sounds_at_game_over()

                            if self.score > self.best_score:
                                self.best_score = self.score
                                self.scoring_json_file["best"] = self.best_score
                                JsonUtil.save_json(self.scoring_json_file_path, self.scoring_json_file)
                            self.gameover_menu.update() 
                            self.main_menu.update()    

                    collidedBuff = pygame.sprite.spritecollideany(self.player, self.buffs)
                    
                    if collidedBuff is not None:
                        if isinstance(collidedBuff, Bat):
                            self.player.touchBat(True)
                            self.sound_player.bat_channel.play(self.player.caughtBatSound)
                            self.buff_begin = pygame.time.get_ticks()
                            collidedBuff.kill()
                            self.scrollSpeed = 5
                            self.bgSprite.setScrollSpeed(self.scrollSpeed)
                            self.update_frequencies()
                            
                    if pygame.time.get_ticks() - self.buff_begin >= 10000:
                        self.player.touchBat(False)
                        self.sound_player.bat_channel.stop()
                        self.scrollSpeed = 10
                        self.bgSprite.setScrollSpeed(self.scrollSpeed)
                        self.update_frequencies()


                    #Score update every second
                    if pygame.time.get_ticks() - self.score_tick >= 1000:
                        self.score += self.scrollSpeed
                        self.score_sprite.image = pygame.font.Font("fonts/8bit-wonder/8-BIT WONDER.TTF", size=30).render(f"Score * {self.score}", True, (255, 255, 255))
                        self.score_tick = pygame.time.get_ticks()

                    self.pickaxe.update()
                    self.bg.update()
                    self.playerGS.update()
                    self.obstacles.update(events, self.scrollSpeed)
                    self.ores.update(events, self.scrollSpeed)
                    self.pickaxe_Hitting_Animation.update(events)
                    self.buffs.update(self.scrollSpeed)
                    self.score_GS.update(events)

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
        self.player = Entity(self,"player", pygame.Vector2(self.WIDTH / 2, 200))
        self.playerGS.add(self.player)

        self.player.XP = 0
        self.update_xp_bar()

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

        #Score reset
        self.score = 0
        self.score_sprite.image = pygame.font.Font("fonts/8bit-wonder/8-BIT WONDER.TTF", size=30).render(f"{self.score}", True, (255, 255, 255))
        self.score_tick = pygame.time.get_ticks()

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
            new_buff = Bat(self.sound_player, self.scrollSpeed).generate_buff(self)
            if (not pygame.sprite.spritecollide(new_buff, self.buffs, False, None)
                    and not pygame.sprite.spritecollide(new_buff, self.obstacles, False, None)
                    and not pygame.sprite.spritecollide(new_buff, self.ores, False, None)):
                self.buffs.add(new_buff)
            else:
                new_buff.kill()
                del new_buff

    def load_xp_bar_images(self):
        self.xp_bar_images = {}
        xp_folder = "img/xp/"
        for filename in os.listdir(xp_folder):
            if filename.startswith("xp_bar_") and filename.endswith(".png"):
                xp_value = int(filename[7:-4])
                self.xp_bar_images[xp_value] = pygame.image.load(os.path.join(xp_folder, filename)).convert_alpha()

        self.xp_levels = sorted(self.xp_bar_images.keys())

    def update_xp_bar(self):
        xp_level = (self.player.XP // 5) * 5

        if (xp_level >= 100):
            self.reset_xp_bar()

        available_levels = [level for level in self.xp_levels if level <= xp_level]

        if available_levels:
            appropriate_level = max(available_levels)
        else:
            appropriate_level = min(self.xp_levels)

        self.custom_sprite.image = self.xp_bar_images[appropriate_level]
        self.custom_sprite.rect.topleft = (self.WIDTH - self.custom_sprite.rect.width - 70, 18)

    def reset_xp_bar(self):
        initial_xp_image = pygame.image.load("img/xp/xp_bar_0.png").convert_alpha()
        self.current_xp_image = initial_xp_image


    def display_collision_animation(self, collided_obstacle):
        x_collision, y_collision = pygame.sprite.collide_mask(self.pickaxe.sprite, collided_obstacle)
        print(f"Collision at {x_collision}, {y_collision}")

        self.pickaxe_Hitting_Animation.add(PickaxeHittingObstacleAnimation(self.sound_player, (x_collision, y_collision), self.scrollSpeed))