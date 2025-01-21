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

# Названия анимаций для летучей мыши
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
        self.health = 3  # Количество жизней
        self.hits_taken = 0  # Количество полученных ударов
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

        # Параметры для движения между точками
        self.start_x = x
        self.start_y = y
        self.end_x = end_x
        self.end_y = end_y
        self.target_x = end_x
        self.target_y = end_y

    def update(self, hero_attack_rect=None, player=None):
        # Если летучая мышь мертва
        if self.health <= 0 and self.state != "die":
            self.change_state("die")
            self.frame_index = 0  # Начинаем анимацию смерти с первого кадра
            self.velocity_x = 0  # Останавливаем движение
            self.velocity_y = 0  # Останавливаем падение
            self.on_ground = True  # Заставляем стоять на месте

        if self.state == "die":
            self.animation_counter += 1
            if self.animation_counter >= self.animation_delays["die"]:
                self.frame_index += 1
                self.animation_counter = 0

                if self.frame_index >= len(self.animations["die"]):
                    self.frame_index = len(self.animations["die"]) - 1  # Останавливаем анимацию на последнем кадре
                    self.kill()  # Удаляем объект из всех групп

            self.image = self.animations["die"][self.frame_index]
            self.rect = self.image.get_rect()
            self.rect.topleft = (self.x, self.y)

            return  # Завершаем выполнение метода, объект больше не обновляется

        elif self.state == "hurt":
            self.animation_counter += 1
            if self.animation_counter >= self.animation_delays["hurt"]:
                self.frame_index += 1
                self.animation_counter = 0

                if self.frame_index >= len(self.animations["hurt"]):
                    self.change_state("run")  # После анимации боли возвращаемся в обычное состояние

            self.image = self.animations["hurt"][self.frame_index]
            self.rect = self.image.get_rect()
            self.rect.topleft = (self.x, self.y)

        else:
            # Обновление анимации
            self.animation_counter += 1
            if self.animation_counter >= self.animation_delays.get(self.state, 10):
                self.frame_index = (self.frame_index + 1) % len(self.animations[self.state])

                # Обновление изображения и позиции
                self.image = self.animations[self.state][self.frame_index]
                self.image = pygame.transform.scale(self.image, (
                    self.image.get_width() * self.scale_factor, self.image.get_height() * self.scale_factor))

                if self.facing_left:
                    self.image = pygame.transform.flip(self.image, True, False)

                self.rect = self.image.get_rect()
                self.rect.topleft = (self.x, self.y)
                self.animation_counter = 0

        # Если летучая мышь мертва, движение не обновляется
        if self.state != "die":
            # Дополнительная логика движения
            self.x += self.velocity_x
            self.y += self.velocity_y

            # Применение гравитации
            if not self.on_ground:
                self.velocity_y += self.gravity

            self.rect.topleft = (self.x, self.y)
            self.handle_collisions()

            # Логика движения между точками
            if self.x == self.target_x and self.y == self.target_y:
                # Меняем цель (обратное движение)
                if self.target_x == self.end_x:
                    self.target_x = self.start_x
                    self.target_y = self.start_y
                else:
                    self.target_x = self.end_x
                    self.target_y = self.end_y

            self.move_towards_target()

        # Проверка на столкновение с атакой героя
        if hero_attack_rect and player:
            if self.rect.colliderect(hero_attack_rect):
                if self.rect.colliderect(player.rect):
                    self.take_damage(1)
                    print("Player takes damage!")

    def handle_collisions(self):
        # Проверка на столкновения
        self.on_ground = self.collision.check_ground_collision(self)

        # Логика движения по оси X (для летучей мыши)
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
        # Рассчитываем направление и скорость движения
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
            self.change_state("die")  # Летучая мышь умирает
            self.frame_index = 0  # Начинаем анимацию смерти
            print("Bat is dead")
        else:
            self.change_state("hurt")  # Летучая мышь получает урон
            print(f"Bat took {amount} damage, remaining hits: {3 - self.hits_taken}")

    def attack(self, player):
        if not self.attacking:
            self.attacking = True
            player.take_damage(1)  # Игрок получает урон
            print("Bat attacks the player!")
            self.change_state("attack")
            # Запускаем анимацию атаки, которая закончится и вернется к обычному состоянию

