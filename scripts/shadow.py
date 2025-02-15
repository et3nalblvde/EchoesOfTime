import pygame
import os
import re
from collision import CollisionLevel1, CollisionLevel2
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
    def __init__(self, x, y, levelnum=None):
        super().__init__()
        self.attacking = False
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

        self.velocity_x = 0
        self.velocity_y = 0
        self.speed = 7
        self.gravity = 0.5
        self.jump_strength = -17
        self.on_ground = False
        self.on_ladder = False

        self.animation_delays = {
            "idle": 10,
            "run": 4,
            "jump": 10,
            "fall": 10,
            "death": 10,
        }
        self.animation_counter = 0
        self.facing_left = False

        self.last_jump_time = 0
        self.jump_delay = 1000
        if levelnum == 1:
            self.collision = CollisionLevel1()
        elif levelnum == 2:
            self.collision = CollisionLevel2()

    def update(self, delta_time):
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

        keys = pygame.key.get_pressed()
        if keys[pygame.K_e]:
            self.stop()

        if self.on_ladder:
            self.velocity_y = 0
            if keys[pygame.K_UP]:
                self.y -= 10
                self.change_state("idle")
            elif keys[pygame.K_DOWN]:
                self.y += 10
                self.change_state("idle")
            else:
                self.change_state("idle")

        else:
            self.velocity_y += self.gravity
            self.y += self.velocity_y

        self.x += self.velocity_x
        self.rect.topleft = (self.x, self.y)

    def change_state(self, new_state):
        if new_state in self.animations and new_state != self.state:
            if new_state == "attack":
                self.attacking = True
                self.previous_state = self.state
                self.frame_index = 0
                self.state = new_state
                self.image = self.animations[self.state][self.frame_index]
                self.image = pygame.transform.scale(self.image, (
                    self.image.get_width() * self.scale_factor, self.image.get_height() * self.scale_factor))
                if self.facing_left:
                    self.image = pygame.transform.flip(self.image, True, False)
                self.rect = self.image.get_rect()
                self.rect.topleft = (self.x, self.y)
                return
            if new_state == "idle" and not self.attacking:
                self.state = new_state
                self.frame_index = 0
                self.image = self.animations[self.state][self.frame_index]
                self.image = pygame.transform.scale(self.image, (
                    self.image.get_width() * self.scale_factor, self.image.get_height() * self.scale_factor))
                if self.facing_left:
                    self.image = pygame.transform.flip(self.image, True, False)
                self.rect = self.image.get_rect()
                self.rect.topleft = (self.x, self.y)
            elif new_state != "idle":
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
        current_time = pygame.time.get_ticks()
        if current_time - self.last_jump_time >= self.jump_delay:
            self.velocity_y = self.jump_strength
            self.change_state("jump")
            self.last_jump_time = current_time

    def stop(self):
        self.velocity_x = 0
        if self.on_ground:
            self.change_state("idle")

    def climb_ladder(self):
        self.on_ladder = True
        self.change_state("idle")
        self.velocity_y = 0
