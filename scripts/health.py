import pygame
import os
import re


def load_heart_sprites():
    base_folder = os.path.dirname(os.path.abspath(__file__))
    sprite_folder = os.path.join(base_folder, '..', 'assets', 'sprites','player','heart')



    heart_full = None
    heart_empty = None
    heart_half = None

    
    for file in os.listdir(sprite_folder):
        if 'full' in file and file.endswith(('.png', '.jpg', '.jpeg')):  
            heart_full_path = os.path.join(sprite_folder, file)
            heart_full = pygame.image.load(heart_full_path)
            break

    
    for file in os.listdir(sprite_folder):
        if 'empty' in file and file.endswith(('.png', '.jpg', '.jpeg')):  
            heart_empty_path = os.path.join(sprite_folder, file)
            heart_empty = pygame.image.load(heart_empty_path)
            break

    
    for file in os.listdir(sprite_folder):
        if 'half' in file and file.endswith(('.png', '.jpg', '.jpeg')):  
            heart_half_path = os.path.join(sprite_folder, file)
            heart_half = pygame.image.load(heart_half_path)
            break

    
    if heart_full:
        heart_full = pygame.transform.scale(heart_full, (32, 32))
    if heart_empty:
        heart_empty = pygame.transform.scale(heart_empty, (32, 32))
    if heart_half:
        heart_half = pygame.transform.scale(heart_half, (32, 32))

    return heart_full, heart_empty, heart_half



class Health:
    def __init__(self, max_health, x, y, player):
        self.max_health = max_health
        self.current_health = max_health
        self.x = x
        self.y = y
        self.player = player
        self.heart_full, self.heart_empty, self.heart_half = load_heart_sprites()  

    def take_damage(self, amount):
        
        self.current_health -= amount
        if self.current_health < 0:
            self.current_health = 0

    def draw(self, screen):
        
        heart_width = 32  
        hearts_to_draw = int(self.current_health)  

        
        for i in range(hearts_to_draw):
            screen.blit(self.heart_full, (self.x + i * heart_width, self.y))

        
        for i in range(hearts_to_draw, self.max_health):
            screen.blit(self.heart_empty, (self.x + i * heart_width, self.y))

        
        if self.current_health % 1 != 0:
            screen.blit(self.heart_half, (self.x + hearts_to_draw * heart_width, self.y))

    def is_alive(self):
        
        return self.current_health > 0
