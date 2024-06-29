from menu.menu import Menu
from utils.CustomSprite import CustomSprite
from utils.JsonUtils import JsonUtils
import pygame
import os

class OptionsMenu(Menu):
    def __init__(self, game, state="Options", previous_state="Main"):
        self.volume = game.MUSIC_VOLUME
        super().__init__(game, state, previous_state)
        self.update_volume_from_game()

    def create_sprites(self):
        self.sprites.add(
            self._create_sprite(self.title_font.render("Options", True, (255, 255, 255)), name="Title"),
            self._create_sprite(self.menu_fonts.render("Volume", True, (255, 255, 255)), name="Volume Text"),
            self._create_sprite(pygame.Surface((400, 40)), name="Volume Slider", clickable=True, callback=self.adjust_volume),
            self._create_sprite(self._render_volume_percentage(), name="Volume Percentage"),
            self._create_sprite(self.menu_fonts.render("Save", True, (255, 255, 255)), name="Save Button", clickable=True, callback=self.save_volume)
        )
        self.update_slider()
        self.position_sprites()

    def _create_sprite(self, image, name, clickable=False, callback=None):
        return CustomSprite(image, name=name, clickable=clickable, callback=callback)

    def _render_volume_percentage(self):
        
        return self.menu_fonts.render(f"{int(self.volume * 100)}%", True, (255, 255, 255))

    def position_sprites(self):
        positions = [
            ("Title", lambda s: (self.game.WIDTH // 2, self.game.HEIGHT // 4)),
            ("Volume Text", lambda s: (self.game.WIDTH // 2, self.get_sprite("Title").rect.bottom + 100)),
            ("Volume Slider", lambda s: (self.game.WIDTH // 2, self.get_sprite("Volume Text").rect.bottom + 30)),
            ("Volume Percentage", lambda s: (self.get_sprite("Volume Slider").rect.right + 10, self.get_sprite("Volume Slider").rect.centery)),
            ("Save Button", lambda s: (self.game.WIDTH // 2, self.get_sprite("Volume Slider").rect.bottom + 50))
        ]
        for name, pos_func in positions:
            sprite = self.get_sprite(name)
            sprite.rect.center = pos_func(sprite)
            if name == "Volume Percentage":
                sprite.rect.midleft = pos_func(sprite)
   
    def get_sprite(self, name):
        return next(s for s in self.sprites if s.name == name)

    def update_volume_from_game(self):
        self.volume = self.game.MUSIC_VOLUME
        pygame.mixer.music.set_volume(self.volume)
        if hasattr(self, 'sprites'):
            self.update_slider()
            self.update_percentage()

    def adjust_volume(self, name):
        slider = self.get_sprite("Volume Slider")
        self.volume = max(0, min(1, (pygame.mouse.get_pos()[0] - slider.rect.x) / slider.rect.width))
        self.game.MUSIC_VOLUME = self.volume
        pygame.mixer.music.set_volume(self.volume)
        self.update_slider()
        self.update_percentage()

    def update_slider(self):
        slider = self.get_sprite("Volume Slider")
        slider.image.fill((100, 100, 100))
        pygame.draw.rect(slider.image, (200, 200, 200), (0, 0, int(slider.rect.width * self.volume), slider.rect.height))

    def update_percentage(self):
        self.get_sprite("Volume Percentage").image = self._render_volume_percentage()

    def save_volume(self, name=None):
        data = {"volume": f"{self.volume:.2f}"}
        current_dir = os.path.dirname(os.path.abspath(__file__))
        config_file_path = os.path.join(current_dir, '..', 'options', 'options.json')
        JsonUtils.save_json(config_file_path, data)
        self.game.MUSIC_VOLUME = self.volume
        pygame.mixer.music.set_volume(self.volume)
        self.game.current_menu = self.game.main_menu
        self.game.current_menu.state = self.previous_state