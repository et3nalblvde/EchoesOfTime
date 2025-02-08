import pygame
import os
from game_over import GameOverScreen
from player import Player
from health import Health
from collision import CollisionLevel1, CollisionLevel2
from pause_menu import PauseMenu
from bat import Bat
from settings import load_sounds, load_settings

# Константы
WHITE = (255, 255, 255)

# Загрузка настроек
settings = load_settings()
MUSIC_VOLUME = settings["MUSIC_VOLUME"]
SFX_VOLUME = settings["SFX_VOLUME"]

# Инициализация Pygame
pygame.mixer.music.set_volume(MUSIC_VOLUME)

# Путь к изображению фона второго уровня
base_folder = os.path.dirname(os.path.abspath(__file__))
level_2_image_path = os.path.join(base_folder, '..', 'assets', 'sprites', 'maps', 'level_2.png')
level_2_image = pygame.image.load(level_2_image_path)

def scale_background(screen):
    """Масштабирование фона под размер экрана."""
    screen_width, screen_height = screen.get_size()
    return pygame.transform.scale(level_2_image, (screen_width, screen_height))

def draw_background(screen):
    """Отрисовка фона."""
    scaled_background = scale_background(screen).convert()
    screen.blit(scaled_background, (0, 0))

def start_level_2(screen, restart_main_menu, exit_to_main_menu):
    """Основная функция второго уровня."""
    # Загрузка звуков
    player_sounds = load_sounds(SFX_VOLUME)
    # Создание игрока
    player = Player(128, 1302, player_sounds, 2)
    health = Health(max_health=3, x=10, y=10, player=player)
    # Группы спрайтов
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)
    # Добавление врагов
    bats = pygame.sprite.Group()

    # Коллизии
    collision = CollisionLevel2()

    # Переменные для игрового цикла
    clock = pygame.time.Clock()
    running = True
    is_paused = False

    # Создаем объект PauseMenu один раз
    pause_menu = PauseMenu(screen)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Обработка паузы
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    is_paused = not is_paused  # Переключаем паузу
                    pause_menu.draw()


            if is_paused:
                result = pause_menu.handle_events(event)
                if result == "quit":
                    exit_to_main_menu()
                if result == "continue":
                    is_paused = False
                continue

        if is_paused:
            # Если игра на паузе, пропускаем основной игровой цикл
            continue

        # Отрисовка фона
        draw_background(screen)
        # Управление игроком
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            player.move_left()
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            player.move_right()
        else:
            player.stop()
        if keys[pygame.K_SPACE]:
            player.jump()
        if keys[pygame.K_f]:
            player.attack(bats)

        # Проверка здоровья игрока
        if not health.is_alive():
            game_over_screen = GameOverScreen(
                screen,
                lambda: start_level_2(screen, restart_main_menu, exit_to_main_menu),
                exit_to_main_menu
            )
            game_over_screen_loop(game_over_screen)
            running = False

        # Обновление коллизий
        collision.check_ladder_collision(player)
        collision.check_platform_collision(player)
        collision.check_wall_collision(player)
        collision.check_box_collision(player)
        collision.draw_collision_debug(screen)

        # Обновление спрайтов
        all_sprites.update(clock.get_time() / 1000)
        all_sprites.draw(screen)

        # Отрисовка здоровья
        health.draw(screen)

        # Отладочная информация (опционально)
        mouse_x, mouse_y = pygame.mouse.get_pos()
        font = pygame.font.Font(None, 36)
        coordinates_text = font.render(f"X: {mouse_x} Y: {mouse_y}", True, WHITE)
        screen.blit(coordinates_text, (10, 10))

        # Обновление экрана
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()