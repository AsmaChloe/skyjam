import pygame

class MusicPlayer:
    def __init__(self, musics_filenames_dict, current_key):
        pygame.mixer.init()
        self.musics_filenames_dict = musics_filenames_dict
        self.current_key = current_key

    def load_and_play(self, music_filename_key, play_params, sound_on):
        if sound_on:
            pygame.mixer.music.load(self.musics_filenames_dict[music_filename_key])
            pygame.mixer.music.play(**play_params)
        self.current_key = music_filename_key

    def is_on(self):
        return pygame.mixer.music.get_busy()

    def stop(self):
        pygame.mixer.music.stop()
        self.current_key = None

    def load_and_play(self, key, params=None, music_on=True):
        if music_on:
            pygame.mixer.music.load(self.musics_filenames_dict[key])
            if params:
                pygame.mixer.music.play(**params)
            else:
                pygame.mixer.music.play()
        self.current_menu = key