import pygame
import os
import re

from numba.core.typing.builtins import Print

from collision import CollisionLevel1  # Импортируем класс для обработки коллизий с уровнями


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

        # Инициализация других параметров
        self.x = x
        self.y = y
        self.state = "idle"
        self.animations = player_animations
        self.frame_index = 0
        self.image = self.animations[self.state][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)

        # Другие параметры
        self.scale_factor = 2
        self.velocity_x = 0
        self.velocity_y = 0
        self.speed = 5
        self.gravity = 0.5
        self.jump_strength = -12
        self.on_ground = False
        self.on_ladder = False
        self.animation_counter = 0
        self.facing_left = False
        self.health = 3
        self.last_direction = None
        # Время последнего прыжка
        self.last_jump_time = 0
        self.jump_delay = 500  # Задержка в 1 секунду (1000 миллисекунд)
        self.collision_type = 'none'
        # Добавляем атрибуты для задержек анимации
        self.animation_delays = {
            "idle": 200,
            "run": 4,
            "jump": 10,
            "fall": 10,
            "death": 10,
            "attack": 10
        }

        # Создаем объект для обработки коллизий
        self.collision = CollisionLevel1()

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

            if self.on_ladder:
                self.velocity_y = 0  # Не поддается гравитации, когда на лестнице

                keys = pygame.key.get_pressed()
                if keys[pygame.K_UP]:
                    self.y -= 10  # Двигаемся вверх по лестнице
                    self.change_state("idle")  # Состояние "idle" при карабкании
                elif keys[pygame.K_DOWN]:
                    self.y += 10  # Двигаемся вниз по лестнице
                    self.change_state("idle")
            else:
                # Применяем гравитацию, если игрок не на лестнице
                self.velocity_y += self.gravity
                self.y += self.velocity_y

            # Обрабатываем столкновения с окружающими стенами и платформами
            self.handle_collisions()

            # Проверка на землю
            if self.y >= 1228:
                self.y = 1228
                self.velocity_y = 0
                self.on_ground = True
            else:
                self.on_ground = False

            # Обновляем позицию по X
            self.x += self.velocity_x
            self.rect.topleft = (self.x, self.y)

    def handle_collisions(self):
        # Проверка столкновения с платформами
        if not self.collision.check_platform_collision(self):  # Если нет коллизии с платформой
            self.x += self.velocity_x  # Продолжаем движение по X

        # Проверяем столкновение с walls
        if not self.collision.check_wall_collision(self):  # Нет столкновения с стеной
            self.x += self.velocity_x  # Продолжаем движение, если нет коллизии с стенами
        else:
            if self.collision_type == 'wall':
                # Логика, если столкновение с стеной
                if self.velocity_x > 0:  # Двигаемся вправо
                    # Проверяем, если игрок слишком близко к стене
                    if self.rect.right + 5 >= self.collision.walls[0].left:
                        self.rect.right = self.collision.walls[0].left - 5  # Останавливаем игрока
                        self.velocity_x = 0  # Останавливаем движение по оси X
                    else:
                        self.x += self.velocity_x  # Иначе продолжаем движение

                elif self.velocity_x < 0:  # Двигаемся влево
                    # Проверяем, если игрок слишком близко к стене
                    if self.rect.left - 5 <= self.collision.walls[0].right:
                        self.rect.left = self.collision.walls[0].right + 5  # Останавливаем игрока
                        self.velocity_x = 0  # Останавливаем движение по оси X
                    else:
                        self.x += self.velocity_x  # Иначе продолжаем движение

            # Проверка для медленного движения или постоянных столкновений
            if abs(self.velocity_x) > 0:
                if self.rect.colliderect(self.collision.walls[0]):
                    if self.velocity_x > 0:  # При движении вправо
                        while self.rect.colliderect(self.collision.walls[0]):
                            self.rect.x -= 1  # Откатываем по 1 пикселю назад
                        self.velocity_x = 0  # Останавливаем движение по оси X
                    elif self.velocity_x < 0:  # При движении влево
                        while self.rect.colliderect(self.collision.walls[0]):
                            self.rect.x += 1  # Откатываем по 1 пикселю вперед
                        self.velocity_x = 0  # Останавливаем движение по оси X

        self.velocity_x = 0  # После проверки коллизий, останавливаем движение по оси X

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
        # Проверяем, прошло ли достаточно времени с последнего прыжка
        current_time = pygame.time.get_ticks()
        if current_time - self.last_jump_time >= self.jump_delay and self.on_ground and not self.on_ladder:
            self.velocity_y = self.jump_strength
            self.change_state("jump")


    def stop(self):
        self.velocity_x = 0
        if self.on_ground and not self.on_ladder:  # Остановить движение, если не на лестнице
            self.change_state("idle")

    def attack(self):
        self.change_state("attack")  # Атака происходит независимо от положения игрока

    def is_death_animation_finished(self):
        if self.state == "death" and self.frame_index == len(self.animations["death"]) - 1:
            return True
        return False

    def climb_ladder(self):
        self.on_ladder = True
        self.change_state("idle")  # Лестница = состояние idle
        self.velocity_y = 0  # Когда на лестнице, гравитация не действует

