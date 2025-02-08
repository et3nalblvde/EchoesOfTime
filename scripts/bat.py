import pygame
import os
import re
from math import sqrt
from collision import CollisionLevel1
from settings import player_sounds

pygame.mixer.init()

base_folder = os.path.dirname(os.path.abspath(__file__))
sprite_folder = os.path.join(base_folder, '..', 'assets', 'sprites', 'bat')

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

animation_names = ["attack", "die", "hurt", "run"]
bat_animations = load_animations(sprite_folder, animation_names)

class Bat(pygame.sprite.Sprite):
    def __init__(self, x, y, end_x, end_y):
        super().__init__()
        self.x = x
        self.y = y
        self.state = "run"
        self.animations = bat_animations
        self.attacking = False
        self.frame_index = 0
        self.image = self.animations[self.state][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)
        self.scale_factor = 2
        self.velocity_x = 0
        self.velocity_y = 0
        self.speed = 1
        self.gravity = 0.2
        self.on_ground = False
        self.health = 3
        self.hits_taken = 0
        self.animation_counter = 0
        self.facing_left = False
        self.last_direction = None
        self.collision_type = 'none'
        self.animation_delays = {
            "run": 4,
            "attack": 6,
            "die": 10,
            "hurt": 8,
        }
        self.collision = CollisionLevel1()
        self.start_x = x
        self.start_y = y
        self.end_x = end_x
        self.end_y = end_y
        self.target_x = end_x
        self.target_y = end_y
        self.last_attack_time = 0
        self.attack_delay = 1000
        self.attack_radius = 50
        self.last_attack_time = 0

    def update(self, hero_attack_rect=None, player=None):
        if self.health <= 0 and self.state != "die":
            self.change_state("die")
            self.frame_index = 0
            self.velocity_x = 0
            self.velocity_y = 0
            self.on_ground = True

        if self.state == "die":
            self.animation_counter += 1
            if self.animation_counter >= self.animation_delays["die"]:
                self.frame_index += 1
                self.animation_counter = 0
                if self.frame_index >= len(self.animations["die"]):
                    self.frame_index = len(self.animations["die"]) - 1
                    self.kill()
            self.image = self.animations["die"][self.frame_index]
            self.rect = self.image.get_rect()
            self.rect.topleft = (self.x, self.y)
            return

        elif self.state == "hurt":
            self.animation_counter += 1
            if self.animation_counter >= self.animation_delays["hurt"]:
                self.frame_index += 1
                self.animation_counter = 0
                if self.frame_index >= len(self.animations["hurt"]):
                    self.change_state("run")
            self.image = self.animations["hurt"][self.frame_index]
            self.rect = self.image.get_rect()
            self.rect.topleft = (self.x, self.y)

        else:
            self.animation_counter += 1
            if self.animation_counter >= self.animation_delays.get(self.state, 10):
                self.frame_index = (self.frame_index + 1) % len(self.animations[self.state])
                self.image = self.animations[self.state][self.frame_index]
                self.image = pygame.transform.scale(self.image, (
                    self.image.get_width() * self.scale_factor, self.image.get_height() * self.scale_factor))
                if self.facing_left:
                    self.image = pygame.transform.flip(self.image, True, False)
                self.rect = self.image.get_rect()
                self.rect.topleft = (self.x, self.y)
                self.animation_counter = 0

            if self.state != "die":
                self.x += self.velocity_x
                self.y += self.velocity_y
                if not self.on_ground:
                    self.velocity_y += self.gravity
                self.rect.topleft = (self.x, self.y)
                self.handle_collisions()

            if self.x == self.target_x and self.y == self.target_y:
                if self.target_x == self.end_x:
                    self.target_x = self.start_x
                    self.target_y = self.start_y
                else:
                    self.target_x = self.end_x
                    self.target_y = self.end_y

            self.move_towards_target()

            # Проверка столкновения с игроком
            if player:
                bat_center = pygame.Vector2(self.x + self.rect.width / 2, self.y + self.rect.height / 2)
                player_center = pygame.Vector2(player.x + player.rect.width / 2, player.y + player.rect.height / 2)
                distance = bat_center.distance_to(player_center)
                if distance <= self.attack_radius:
                    self.attack_player(player)

    def handle_collisions(self):
        self.on_ground = True
        if self.velocity_x != 0:
            if self.collision.check_wall_collision(self):
                self.velocity_x = 0

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

    def move_towards_target(self):
        if self.x < self.target_x:
            self.velocity_x = self.speed
            self.facing_left = True
        elif self.x > self.target_x:
            self.velocity_x = -self.speed
            self.facing_left = False
        else:
            self.velocity_x = 0

        if self.y < self.target_y:
            self.velocity_y = self.speed
        elif self.y > self.target_y:
            self.velocity_y = -self.speed
        else:
            self.velocity_y = 0

    def take_damage(self, amount):
        self.hits_taken += 1
        if self.hits_taken >= 3:
            self.change_state("die")
            self.frame_index = 0
            print("Bat is dead")
        else:
            self.change_state("hurt")
            print(f"Bat took {amount} damage, remaining hits: {3 - self.hits_taken}")

    def attack_player(self, player):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_attack_time >= self.attack_delay:
            bat_center = pygame.Vector2(self.x + self.rect.width / 2, self.y + self.rect.height / 2)
            player_center = pygame.Vector2(player.x + player.rect.width / 2, player.y + player.rect.height / 2)
            distance = bat_center.distance_to(player_center)

            if distance <= self.attack_radius:
                player.take_damage(1)
                print("Bat attacks the player!")
                self.change_state("attack")
                self.last_attack_time = current_time