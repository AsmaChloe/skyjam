import pygame

class MusicPlayer() :
    def __init__(self, musics_filenames_dict, current_key) :
        pygame.mixer.init()
        self.musics_filenames_dict = musics_filenames_dict
        self.current_key = current_key

    def load_and_play(self, music_filename_key, play_params) :
        pygame.mixer.music.load(self.musics_filenames_dict[music_filename_key])
        pygame.mixer.music.play(**play_params)
        self.current_key = music_filename_key

    def stop(self) :
        pygame.mixer.music.stop()
        self.current_key = None
