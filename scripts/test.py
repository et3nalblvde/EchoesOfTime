import pygame
import time
from player import Player  # Предполагается, что класс Player находится в файле player.py

# Инициализация Pygame
pygame.init()

# Параметры экрана
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Тест анимации игрока")

# Цвет фона
BG_COLOR = (0, 0, 0)

# Создаем игрока
player = Player(100, 150)

# Главный игровой цикл
running = True
clock = pygame.time.Clock()

while running:
    screen.fill(BG_COLOR)  # Очистить экран

    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Обновление состояния анимации
    player.update()

    # Временно изменяем состояния для теста
    player.change_state("idle")
    time.sleep(1)
    player.change_state("run")
    time.sleep(1)
    player.change_state("jump")
    time.sleep(1)
    player.change_state("fall")
    time.sleep(1)
    player.change_state("attack")
    time.sleep(1)
    player.change_state("take_damage")
    time.sleep(1)
    player.change_state("dead")
    time.sleep(1)

    # Отображаем игрока
    player.draw(screen)

    pygame.display.flip()  # Обновить экран
    clock.tick(30)  # Устанавливаем FPS (кадры в секунду)

pygame.quit()
