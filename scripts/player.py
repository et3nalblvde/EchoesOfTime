import pygame
import os
import re

from collision import CollisionLevel1, CollisionLevel2
from settings import player_sounds

pygame.mixer.init()
base_folder = os.path.dirname(os.path.abspath(__file__))
sprite_folder = os.path.join(base_folder, '..', 'assets', 'sprites', 'player')


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
    def __init__(self, x, y, sounds, levelnum=None):
        super().__init__()
        self.attacking = False
        self.sounds = sounds
        self.x = x
        self.y = y
        self.state = "idle"
        self.animations = player_animations
        self.attacking = False
        self.frame_index = 0
        self.image = self.animations[self.state][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)
        self.on_platform = False
        self.scale_factor = 2
        self.velocity_x = 0
        self.velocity_y = 0
        self.speed = 7
        self.gravity = 0.5
        self.jump_strength = -12
        self.on_ground = False
        self.on_ladder = False
        self.animation_counter = 0
        self.facing_left = False
        self.health = 3
        self.last_direction = None
        self.last_jump_time = 0
        self.jump_delay = 500
        self.collision_type = 'none'
        self.on_box = False
        self.last_attack_time = 0
        self.attack_delay = 200
        self.animation_delays = {
            "idle": 10,
            "run": 4,
            "jump": 10,
            "fall": 10,
            "death": 10,
            "attack": 10
        }
        self.health = 3  # Здоровье игрока
        self.last_hit_time = 0  # Время последнего удара
        self.hit_delay = 1000

        if levelnum == 1:
            self.collision = CollisionLevel1()
        elif levelnum == 2:
            self.collision = CollisionLevel2()

    def update_sfx_volume(self, volume):
        for sound in self.sounds.values():
            sound.set_volume(volume)

    def update(self, delta_time):
        if self.health <= 0 and self.state != "death":
            self.change_state("death")
            self.frame_index = 0

        if self.state == "death":
            self.image = self.animations["death"][self.frame_index]
            self.rect = self.image.get_rect()
            self.rect.topleft = (self.x, self.y)
            if self.frame_index == len(self.animations["death"]) - 1:
                return
        else:
            self.animation_counter += 1
            if self.animation_counter >= self.animation_delays.get(self.state, 10):
                if self.state == "attack" and self.frame_index == len(self.animations["attack"]) - 1:
                    self.attacking = False  # Сбрасываем флаг атаки
                    self.change_state(self.previous_state)  # Возвращаемся к предыдущему состоянию
                else:
                    self.frame_index = (self.frame_index + 1) % len(self.animations[self.state])
                    self.image = self.animations[self.state][self.frame_index]
                    self.image = pygame.transform.scale(self.image, (
                        self.image.get_width() * self.scale_factor, self.image.get_height() * self.scale_factor))
                    if self.facing_left:
                        self.image = pygame.transform.flip(self.image, True, False)
                    self.rect = self.image.get_rect()
                    self.rect.topleft = (self.x, self.y)
                    self.animation_counter = 0

            # Обновление позиции игрока
            if self.on_ladder:
                self.velocity_y = 0
                keys = pygame.key.get_pressed()
                if keys[pygame.K_UP]:
                    self.y -= 10
                    self.change_state("idle")
                elif keys[pygame.K_DOWN]:
                    self.y += 10
                    self.change_state("idle")
            else:
                if not self.on_platform and not self.on_box:
                    self.velocity_y += self.gravity
                self.y += self.velocity_y
                if self.on_platform or self.on_box:
                    self.velocity_y = 0
                self.handle_collisions()



            self.x += self.velocity_x
            self.rect.topleft = (self.x, self.y)

    def handle_collisions(self):


        self.on_ladder = self.collision.check_ladder_collision(self)
        self.on_platform = self.collision.check_platform_collision(self)
        self.on_box = self.collision.check_box_collision(self)
        (self.collision_type)

        if self.on_ladder:
            self.collision_type = 'ladder'
            self.velocity_y = 0
        elif self.on_platform:
            self.collision_type = 'platform'
            self.velocity_y = 0
        elif self.on_box:
            self.collision_type = 'box'
            self.velocity_y = 0
        else:
            self.collision_type = 'none'

        if not self.collision.check_wall_collision(self):
            self.x += self.velocity_x
        else:
            if self.collision_type == 'wall':
                if self.velocity_x > 0:
                    if self.rect.right + 5 >= self.collision.walls[0].left:
                        self.rect.right = self.collision.walls[0].left - 5
                        self.velocity_x = 0
                    else:
                        self.x += self.velocity_x
                elif self.velocity_x < 0:
                    if self.rect.left - 5 <= self.collision.walls[0].right:
                        self.rect.left = self.collision.walls[0].right + 5
                        self.velocity_x = 0
                    else:
                        self.x += self.velocity_x

            elif self.collision_type == 'platform':
                if self.velocity_x > 0:
                    if self.rect.right + 5 >= self.collision.platforms[0].left:
                        self.rect.right = self.collision.platforms[0].left - 5
                        self.velocity_x = 0
                elif self.velocity_x < 0:
                    if self.rect.left - 5 <= self.collision.platforms[0].right:
                        self.rect.left = self.collision.platforms[0].right + 5
                        self.velocity_x = 0

            elif self.collision_type == 'box':
                if self.velocity_x > 0:
                    if self.rect.right + 5 >= self.collision.boxes[0].left:
                        self.rect.right = self.collision.boxes[0].left - 5
                        self.velocity_x = 0


            elif self.collision_type == 'ladder':

                if self.velocity_y != 0:
                    self.velocity_y = 0
                self.y += self.velocity_y

                if self.rect.colliderect(self.collision.ladders[0]):
                    self.y = self.collision.ladders[0].top - self.rect.height

        self.velocity_x = 0

    def take_damage(self, amount):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_hit_time >= self.hit_delay:
            self.health -= amount
            if self.health < 0:
                self.health = 0
            print(f"Player takes {amount} damage! Remaining health: {self.health}")
            self.last_hit_time = current_time

    def change_state(self, new_state):
        if new_state in self.animations and new_state != self.state:
            if new_state == "attack":
                self.attacking = True
                self.previous_state = self.state  # Сохраняем предыдущее состояние
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
        if self.state != "attack":
            self.velocity_x = -self.speed
            self.change_state("run")
            self.facing_left = True
            if self.on_ground:
                if not pygame.mixer.get_busy():
                    self.sounds["walk"].play()

    def move_right(self):
        if self.state != "attack":
            self.velocity_x = self.speed
            self.change_state("run")
            self.facing_left = False
            if self.on_ground:
                if not pygame.mixer.get_busy():
                    self.sounds["walk"].play()

    def jump(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_jump_time >= self.jump_delay and (
                self.on_ground or self.on_platform or self.on_ladder
        ):
            self.velocity_y = self.jump_strength
            self.change_state("jump")
            self.last_jump_time = current_time
            self.sounds["jump"].play()

    def stop(self):
        self.velocity_x = 0
        if self.on_ground and not self.on_ladder:
            self.change_state("idle")

    def attack(self, bats):
        current_time = pygame.time.get_ticks()
        if not self.attacking and current_time - self.last_attack_time >= self.attack_delay:
            self.change_state("attack")
            print('attack')
            self.sounds["attack"].play()
            self.attacking = True  # Устанавливаем флаг атаки
            self.last_attack_time = current_time

            for bat in bats:
                if self.rect.colliderect(bat.rect) and self.state == "attack":
                    bat.take_damage(1)
                else:
                    self.health -= 1

    def is_death_animation_finished(self):
        if self.state == "death" and self.frame_index == len(self.animations["death"]) - 1:
            return True
        return False

    def climb_ladder(self):
        self.on_ladder = True
        self.change_state("idle")
        self.velocity_y = 0
