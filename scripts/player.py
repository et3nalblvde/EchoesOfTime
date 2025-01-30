import pygame
import os
import re
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
    def __init__(self, x, y, sounds):
        super().__init__()
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
        self.scale_factor = 2
        self.animation_counter = 0
        self.facing_left = False
        self.health = 3
        self.last_direction = None
        self.last_attack_time = 0
        self.attack_delay = 200
        self.velocity_x = 0
        self.velocity_y = 0
        self.on_ground = False
        self.gravity = 0.5
        self.jump_power = -15
        self.speed = 5
        self.animation_delays = {
            "idle": 10,
            "run": 4,
            "jump": 10,
            "fall": 10,
            "death": 10,
            "attack": 10
        }

    def handle_input(self, keys):
        if keys[pygame.K_a]:
            self.velocity_x = -self.speed
            self.facing_left = True
            self.change_state("left")
        elif keys[pygame.K_d]:
            self.velocity_x = self.speed
            self.facing_left = False
            self.change_state("right")
        else:
            self.velocity_x = 0
            if self.on_ground:
                self.change_state("idle")

        if keys[pygame.K_SPACE] and self.on_ground:
            self.velocity_y = self.jump_power
            self.on_ground = False
            self.change_state("jump")
            self.sounds["jump"].play()

    def apply_gravity(self):
        self.velocity_y += self.gravity
        self.y += self.velocity_y


        if self.y >= 1235:
            self.y = 1235
            self.velocity_y = 0
            self.on_ground = True
            if self.state == "jump":
                self.change_state("idle")

    def update_sfx_volume(self, volume):
        for sound in self.sounds.values():
            sound.set_volume(volume)

    def update(self, delta_time):
        keys = pygame.key.get_pressed()
        self.handle_input(keys)
        self.apply_gravity()



        # Обновление анимации
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
                    self.attacking = False
                    self.change_state(self.previous_state)
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



    def take_damage(self, amount, bats):
        self.health -= amount
        if self.health < 0:
            self.health = 0

    def change_state(self, new_state):
        # Проверяем, существует ли новое состояние в анимациях
        if new_state in self.animations and new_state != self.state:
            # Сохраняем предыдущее состояние перед атакой
            if new_state == "attack":
                self.attacking = True
                self.previous_state = self.state

            # Меняем состояние и сбрасываем счетчик кадров
            self.state = new_state
            self.frame_index = 0
            self.animation_counter = 0

            # Обновляем изображение игрока
            self.image = self.animations[self.state][self.frame_index]
            self.image = pygame.transform.scale(
                self.image,
                (self.image.get_width() * self.scale_factor, self.image.get_height() * self.scale_factor)
            )

            # Отражаем изображение, если игрок смотрит влево
            if self.facing_left:
                self.image = pygame.transform.flip(self.image, True, False)

            # Обновляем прямоугольник коллизии
            self.rect = self.image.get_rect()
            self.rect.topleft = (self.x, self.y)

    def attack(self, bats):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_attack_time >= self.attack_delay:
            self.change_state("attack")
            print('attack')
            self.sounds["attack"].play()

            # Проверяем столкновения с летучими мышами
            for bat in bats:
                if self.rect.colliderect(bat.rect) and self.state == "attack":
                    bat.take_damage(1)

            self.last_attack_time = current_time

    def is_death_animation_finished(self):
        if self.state == "death" and self.frame_index == len(self.animations["death"]) - 1:
            return True
        return False


