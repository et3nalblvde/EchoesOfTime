import pygame
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.abspath(os.path.join(BASE_DIR, '..'))
sprites_path = os.path.join(PROJECT_DIR, 'assets', 'sprites', 'doors')


class Lever(pygame.sprite.Sprite):
    def __init__(self, x, y, sprites_path, frame_count):
        super().__init__()

        
        self.frames = [
            pygame.transform.scale(
                pygame.image.load(f"{sprites_path}/levers{i}.png").convert_alpha(),
                (pygame.image.load(f"{sprites_path}/levers{i}.png").get_width() * 2,
                 pygame.image.load(f"{sprites_path}/levers{i}.png").get_height() * 2)
            ) for i in range(1, frame_count + 1)  
        ]
        self.current_frame = 0
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect(topleft=(x, y))

        self.animation_speed = 0.1  
        self.time_since_last_frame = 0
        self.animation_playing = False  
    def deactivate(self):
        
        if self.animation_playing:  
            self.animation_playing = False
            self.current_frame = 0  
            self.image = self.frames[self.current_frame]
    def activate(self):
        
        if not self.animation_playing:  
            self.animation_playing = True
            self.current_frame = 0  

    def update(self, delta_time):
        
        if self.animation_playing:
            self.time_since_last_frame += delta_time
            if self.time_since_last_frame >= self.animation_speed:
                self.time_since_last_frame = 0
                self.current_frame += 1
                if self.current_frame >= len(self.frames):
                    self.current_frame = len(self.frames) - 1
                    self.animation_playing = False  
                self.image = self.frames[self.current_frame]
