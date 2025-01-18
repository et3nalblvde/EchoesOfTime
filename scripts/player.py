import pygame
import os
import re


base_folder = os.path.dirname(os.path.abspath(__file__))
sprite_folder = os.path.join(base_folder, '..', 'assets', 'sprites')

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


animation_names = ["idle", "run", "jump", "fall", "death", "attack"]  
player_animations = load_animations(sprite_folder, animation_names)

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.x = x
        self.y = y
        self.state = "idle"
        self.animations = player_animations
        self.frame_index = 0
        self.image = self.animations[self.state][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)

        
        self.scale_factor = 2
        self.image = pygame.transform.scale(self.image, (
            self.image.get_width() * self.scale_factor, self.image.get_height() * self.scale_factor))
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)

        
        self.velocity_x = 0
        self.velocity_y = 0
        self.speed = 5
        self.gravity = 0.5
        self.jump_strength = -10
        self.on_ground = False

        
        self.animation_delays = {
            "idle": 100,
            "run": 4,
            "jump": 10,
            "fall": 10,
            "death": 10,
            "attack": 15
        }
        self.animation_counter = 0  

        
        self.facing_left = False

        
        self.health = 3  

    def update(self):
        
        if self.health <= 0:
            self.change_state("death")  
            self.frame_index = len(self.animations["death"]) - 1  
            self.image = self.animations["death"][self.frame_index]  
            self.rect = self.image.get_rect()
            self.rect.topleft = (self.x, self.y)
        else:
            
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

            
            self.velocity_y += self.gravity
            self.y += self.velocity_y
            if self.y >= 400:  
                self.y = 400
                self.velocity_y = 0
                self.on_ground = True
            else:
                self.on_ground = False

            
            self.x += self.velocity_x
            self.rect.topleft = (self.x, self.y)

    def take_damage(self, amount):
        
        self.health -= amount
        if self.health < 0:
            self.health = 0  

    def change_state(self, new_state):
        if new_state == "death" or (new_state != "idle" and new_state in self.animations and new_state != self.state):
            self.state = new_state
            self.frame_index = 0
            self.image = self.animations[self.state][self.frame_index]

            
            self.image = pygame.transform.scale(self.image, (
                self.image.get_width() * self.scale_factor, self.image.get_height() * self.scale_factor))

            
            if self.facing_left:
                self.image = pygame.transform.flip(self.image, True, False)

            self.rect = self.image.get_rect()
            self.rect.topleft = (self.x, self.y)

    def move_left(self):
        self.velocity_x = -self.speed
        self.change_state("run")
        self.facing_left = True  

    def move_right(self):
        self.velocity_x = self.speed
        self.change_state("run")
        self.facing_left = False  

    def jump(self):
        if self.on_ground:
            self.velocity_y = self.jump_strength
            self.change_state("jump")

    def stop(self):
        self.velocity_x = 0
        if self.on_ground:
            self.change_state("idle")

    def attack(self):
        self.change_state("attack")  
        

    def is_death_animation_finished(self):
        
        if self.state == "death" and self.frame_index == len(self.animations["death"]) - 1:
            return True
        return False
