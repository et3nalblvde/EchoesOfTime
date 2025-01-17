import pygame
from player import Player  # Импортируем класс Player
from shadow import Shadow  # Импортируем класс Shadow

# Цвета
WHITE = (255, 255, 255)
DARK_GREEN = (34, 139, 34)
BROWN = (139, 69, 19)
GREY = (169, 169, 169)
BLACK = (0, 0, 0)

# Загрузка изображений для ассетов
column_image = pygame.Surface((50, 200))  # Пример разрушенной колонны
column_image.fill(GREY)
moss_image = pygame.Surface((50, 50))  # Мох
moss_image.fill(DARK_GREEN)
vine_image = pygame.Surface((30, 200))  # Лианы
vine_image.fill(BROWN)

# Функция для отрисовки фона и уровня (без анимаций)
def draw_background(screen):
    screen.fill(WHITE)

    # Рисуем разрушенные колонны (статично)
    for i in range(0, screen.get_width(), 100):
        screen.blit(column_image, (i, screen.get_height() - 200))

    # Рисуем мох (статично)
    for i in range(0, screen.get_width(), 150):
        screen.blit(moss_image, (i, screen.get_height() - 220))

    # Рисуем лианы (статично)
    for i in range(0, screen.get_width(), 150):
        screen.blit(vine_image, (i, screen.get_height() - 200))

    # Легкие лучи света (статичные)
    pygame.draw.rect(screen, (255, 255, 200), pygame.Rect(100, 50, 200, 100), 2)

# Функция для старта уровня 1
# Функция для старта уровня 1
def start_level_1(screen):
    # Создаем объекты игрока и тени
    player = Player(100, 400)  # Начальная позиция игрока
    shadow = Shadow(100, 400)  # Начальная позиция тени

    # Группировка спрайтов
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)
    all_sprites.add(shadow)  # Добавляем тень в группу спрайтов

    # Флаг для отслеживания, кто управляется (True - игрок, False - тень)
    controlling_player = True

    # Создаем объект для управления частотой кадров
    clock = pygame.time.Clock()

    # Основной цикл уровня 1
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Обработка ввода с клавиатуры
        keys = pygame.key.get_pressed()

        # Переключаем управление при нажатии клавиши 'E'
        if keys[pygame.K_e]:
            # Останавливаем текущего контролируемого персонажа
            if controlling_player:
                player.stop()  # Останавливаем игрока
            else:
                shadow.stop()  # Останавливаем тень

            controlling_player = not controlling_player  # Переключаем управление
            pygame.time.wait(200)  # Небольшая задержка, чтобы избежать многократного переключения

        # Управляем текущим объектом
        if controlling_player:
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                player.move_left()
            elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                player.move_right()
            else:
                player.stop()

            if keys[pygame.K_SPACE]:
                player.jump()

        else:
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                shadow.move_left()
            elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                shadow.move_right()
            else:
                shadow.stop()

            if keys[pygame.K_SPACE]:
                shadow.jump()

        # Отрисовываем обновленный уровень
        draw_background(screen)

        # Обновляем все спрайты (игрок или тень)
        all_sprites.update()

        # Отрисовываем все спрайты
        all_sprites.draw(screen)  # Используем стандартный метод draw

        # Обновление экрана
        pygame.display.flip()

        # Ограничиваем FPS (например, до 60 кадров в секунду)
        clock.tick(60)  # Здесь 60 — это количество кадров в секунду

    pygame.quit()



