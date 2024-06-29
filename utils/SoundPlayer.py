import pygame

class SoundPlayer() :
    def __init__(self, musics_filenames_dict, current_key) :
        self.nb_channels = 5

        pygame.mixer.pre_init(44100, -16, self.nb_channels, 2048)
        pygame.mixer.init()
        self.musics_filenames_dict = musics_filenames_dict
        self.current_key = current_key

        #Menu button channel
        self.menu_button_channel = pygame.mixer.Channel(0)
        #Pickaxe channel
        self.pickaxe_channel = pygame.mixer.Channel(1)
        #Ore channel
        self.ore_channel = pygame.mixer.Channel(2)
        #Bat channel
        self.bat_channel = pygame.mixer.Channel(3)
        #Player channel
        self.player_channel = pygame.mixer.Channel(4)

    def load_and_play(self, music_filename_key, play_params, sound_on) :
        if sound_on :
            pygame.mixer.music.load(self.musics_filenames_dict[music_filename_key])
            pygame.mixer.music.play(**play_params)
        self.current_key = music_filename_key

    def is_on(self) :
        return pygame.mixer.music.get_busy()

    def stop(self) :
        pygame.mixer.music.stop()
        self.current_key = None

    def stop_sounds_at_game_over(self) :
        self.menu_button_channel.stop()
        self.pickaxe_channel.stop()
        self.ore_channel.stop()
        self.bat_channel.stop()