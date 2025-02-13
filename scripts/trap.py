import pygame
import os

class NeedleTrap(pygame.sprite.Sprite):
    def __init__(self, x, y, frame_width, frame_height, scale_factor=1):
        super().__init__()
        self.frames = []
        self.current_frame = 0
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.image = None
        self.rect = None
        self.animation_speed = 0.8  # Скорость смены кадров
        self.time_since_last_frame = 0
        self.is_reverse = False  # Направление анимации
        self.x = x  # Сохраняем начальные координаты
        self.y = y
        self.scale_factor = scale_factor  # Фактор масштабирования
        self.load_frames()  # Загружаем кадры

    def load_frames(self):
        base_folder = os.path.dirname(os.path.abspath(__file__))
        needle_folder = os.path.join(base_folder, '..', 'assets', 'sprites', 'traps', 'needles')

        for filename in sorted(os.listdir(needle_folder)):
            if filename.endswith('.png'):
                image_path = os.path.join(needle_folder, filename)
                image = pygame.image.load(image_path).convert_alpha()
                image = pygame.transform.scale(image, (
                    int(self.frame_width * self.scale_factor),
                    int(self.frame_height * self.scale_factor)
                ))
                self.frames.append(image)

        if self.frames:
            self.image = self.frames[self.current_frame]
            self.rect = self.image.get_rect()
            self.rect.topleft = (self.x, self.y)

    def update(self, dt):
        if not self.frames:
            return

        self.time_since_last_frame += dt
        if self.time_since_last_frame >= self.animation_speed:
            self.time_since_last_frame = 0
            if self.is_reverse:
                self.current_frame -= 1
                if self.current_frame < 0:
                    self.current_frame = 1
                    self.is_reverse = False
            else:
                self.current_frame += 1
                if self.current_frame >= len(self.frames):
                    self.current_frame = len(self.frames) - 2
                    self.is_reverse = True

            self.image = self.frames[self.current_frame]
            self.rect.topleft = (self.x, self.y)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

import pygame
import os

class Fireball(pygame.sprite.Sprite):
    def __init__(self, x, y, image, speed):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = speed

    def update(self):
        self.rect.x -= self.speed
        if self.rect.x > 800:
            self.kill()

class SpittingHead(pygame.sprite.Sprite):
    def __init__(self, x, y, frame_width, frame_height, scale_factor=1):
        super().__init__()
        self.frames = []
        self.current_frame = 0
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.image = None
        self.rect = None
        self.animation_speed = 0.8
        self.time_since_last_frame = 0
        self.fireball_images = []
        self.fireballs = pygame.sprite.Group()
        self.fireball_speed = 5
        self.x = x
        self.y = y
        self.scale_factor = scale_factor
        self.fireball_interval = 1000
        self.last_fireball_time = 0
        self.load_frames()

    def load_frames(self):
        base_folder = os.path.dirname(os.path.abspath(__file__))
        head_folder = os.path.join(base_folder, '..', 'assets', 'sprites', 'traps', 'source')
        fireball_folder = os.path.join(base_folder, '..', 'assets', 'sprites', 'traps', 'fireballs')

        # Выводим путь к папке с огненными шарами
        print(f"Путь к папке с огненными шарами: {fireball_folder}")

        if os.path.exists(head_folder):
            for filename in sorted(os.listdir(head_folder)):
                if filename.endswith('.png'):
                    image_path = os.path.join(head_folder, filename)
                    image = pygame.image.load(image_path).convert_alpha()
                    image = pygame.transform.scale(image, (
                        int(self.frame_width * self.scale_factor),
                        int(self.frame_height * self.scale_factor)
                    ))
                    self.frames.append(image)
        else:
            print(f"Папка с изображениями головы не найдена: {head_folder}")

        if self.frames:
            self.image = self.frames[self.current_frame]
            self.rect = self.image.get_rect()
            self.rect.topleft = (self.x, self.y)

        if os.path.exists(fireball_folder):
            for filename in sorted(os.listdir(fireball_folder)):
                if filename.endswith('.png'):
                    image_path = os.path.join(fireball_folder, filename)
                    image = pygame.image.load(image_path).convert_alpha()
                    self.fireball_images.append(image)
            if self.fireball_images:
                print(f"Загружено {len(self.fireball_images)} кадров для огненных шаров.")
            else:
                print("Ошибка: изображения огненных шаров не загружены.")
        else:
            print(f"Папка с изображениями огненных шаров не найдена: {fireball_folder}")

    def update(self, dt, current_time):
        if not self.frames:
            return

        self.time_since_last_frame += dt
        if self.time_since_last_frame >= self.animation_speed:
            self.time_since_last_frame = 0
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.image = self.frames[self.current_frame]
            self.rect.topleft = (self.x, self.y)
            print(f"Проиграна анимация головы, текущий кадр: {self.current_frame + 1}")

        if current_time - self.last_fireball_time >= self.fireball_interval:
            self.last_fireball_time = current_time
            self.spit_fireball()

        self.fireballs.update()

        # Печатаем уникальные имена для каждого фаербола
        for idx, fireball in enumerate(self.fireballs):
            print(f"Проиграна анимация фаербола {idx + 1}")

    def spit_fireball(self):
        if self.fireball_images:
            fireball_image = self.fireball_images[0]  # Используем первый кадр
            if fireball_image is not None:
                fireball = Fireball(self.rect.centerx, self.rect.centery, fireball_image, self.fireball_speed)
                self.fireballs.add(fireball)
                print(f"Проиграна анимация фаербола {len(self.fireballs)}")  # Печатаем количество фаерболов
            else:
                print("Ошибка: изображение фаербола не загружено.")
        else:
            print("Ошибка: нет изображений фаерболов.")

    def draw_fireballs(self, screen):
        # Отрисовываем все фаерболы
        self.fireballs.draw(screen)

    def draw(self, screen):
        # Отрисовываем саму голову
        screen.blit(self.image, self.rect)