import pygame
import os

class MusicPlayer:
    def __init__(self, music_folder):
        pygame.mixer.init()
        self.music_folder = "music"
        self.playlist = [os.path.join(music_folder, f) for f in os.listdir(music_folder) if f.endswith((".mp3"))]
        self.current_index = 0
        self.is_playing = False

    def load_track(self):
        pygame.mixer.music.load(self.playlist[self.current_index])

    def play(self):
        if not self.is_playing:
            self.load_track()
            pygame.mixer.music.play()
            self.is_playing = True

    def stop(self):
        pygame.mixer.music.stop()
        self.is_playing = False

    def next_track(self):
        self.current_index = (self.current_index + 1) % len(self.playlist)
        self.playing_next()

    def prev_track(self):
        self.current_index = (self.current_index - 1) % len(self.playlist)
        self.playing_next()

    def playing_next(self):
        pygame.mixer.music.stop()
        self.load_track()
        pygame.mixer.music.play()
        self.is_playing = True

    def get_current_track_name(self):
        return os.path.basename(self.playlist[self.current_index])

    def get_position(self):
        return pygame.mixer.music.get_pos() / 1000
