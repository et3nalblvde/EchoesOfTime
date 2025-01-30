import pygame
import os
import re

base_folder = os.path.dirname(os.path.abspath(__file__))
sprite_folder = os.path.join(base_folder, '..', 'assets', 'sprites', 'shadows')

def load_animations(folder, animation_names, scale_factor=2):
    animations = {}
    for anim in animation_names:
        anim_folder = os.path.join(folder, anim)
        files = sorted([f for f in os.listdir(anim_folder) if f.endswith(('.png', '.jpg', '.jpeg'))],
                       key=lambda f: int(re.search(r'(\d+)', f).group(1) if re.search(r'(\d+)', f) else -1))
        animations[anim] = []
        for file in files:
            image = pygame.image.load(os.path.join(anim_folder, file))
            scaled_image = pygame.transform.scale(image, (
                image.get_width() * scale_factor, image.get_height() * scale_factor))
            animations[anim].append(scaled_image)
    return animations


animation_names = ["idle", "run", "jump", "fall", "death"]
shadow_animations = load_animations(sprite_folder, animation_names)

class Shadow(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.x = x
        self.y = y
        self.state = "idle"  
        self.animations = shadow_animations  
        self.frame_index = 0
        self.image = self.animations[self.state][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)

        self.scale_factor = 2
        self.image = pygame.transform.scale(self.image, (
            self.image.get_width() * self.scale_factor, self.image.get_height() * self.scale_factor))
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)



        self.animation_delays = {
            "idle": 10,
            "run": 4,
            "jump": 10,
            "fall": 10,
            "death": 10,
        }
        self.animation_counter = 0
        self.facing_left = False

    def update(self,delta_time):
        
        self.animation_counter += 1
        if self.animation_counter >= self.animation_delays[self.state]:
            self.frame_index = (self.frame_index + 1) % len(self.animations[self.state])
            self.image = self.animations[self.state][self.frame_index]

            self.image = pygame.transform.scale(self.image, (
                self.image.get_width() * self.scale_factor, self.image.get_height() * self.scale_factor))

            if self.facing_left:
                self.image = pygame.transform.flip(self.image, True, False)

            self.rect = self.image.get_rect()
            self.rect.topleft = (self.x, self.y)
            self.animation_counter = 0

        


    def change_state(self, new_state):
        if new_state in self.animations and new_state != self.state:
            self.state = new_state
            self.frame_index = 0
            self.image = self.animations[self.state][self.frame_index]

            self.image = pygame.transform.scale(self.image, (
                self.image.get_width() * self.scale_factor, self.image.get_height() * self.scale_factor))

            if self.facing_left:
                self.image = pygame.transform.flip(self.image, True, False)

            self.rect = self.image.get_rect()
            self.rect.topleft = (self.x, self.y)

