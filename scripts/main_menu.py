import pygame
import sys
import os
from scripts.settings import load_settings, SettingsMenu
from level_1 import start_level_1

pygame.init()
settings = load_settings()
SCREEN_WIDTH = settings["SCREEN_WIDTH"]
SCREEN_HEIGHT = settings["SCREEN_HEIGHT"]
FPS = settings["FPS"]
BACKGROUND_COLOR = settings["BACKGROUND_COLOR"]
MUSIC_VOLUME = settings["MUSIC_VOLUME"]
pygame.mixer.music.set_volume(MUSIC_VOLUME)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.join(BASE_DIR, '..')
ASSETS_DIR = os.path.join(PROJECT_DIR, 'assets')
FONTS_DIR = os.path.join(ASSETS_DIR, 'fonts')
FONT_PATH = os.path.join(FONTS_DIR, 'PressStart2P.ttf')

# Инициализируем шрифт
base_font_size = 25
font = pygame.font.Font(FONT_PATH, base_font_size)

# Устанавливаем разрешение окна
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
SCREEN_WIDTH, SCREEN_HEIGHT = screen.get_size()  # Получаем реальное разрешение экрана


# Кнопки
def update_button_positions():
    global start_button, settings_button, quit_button
    button_width = SCREEN_WIDTH // 3
    button_height = SCREEN_HEIGHT // 10

    # Центрирование кнопок
    center_x = SCREEN_WIDTH // 2
    center_y = SCREEN_HEIGHT // 2

    start_button = pygame.Rect(
        center_x - button_width // 2,
        center_y - button_height * 1.5,
        button_width, button_height
    )
    settings_button = pygame.Rect(
        center_x - button_width // 2,
        center_y - button_height // 2,
        button_width, button_height
    )
    quit_button = pygame.Rect(
        center_x - button_width // 2,
        center_y + button_height * 0.5,
        button_width, button_height
    )


# Градиентный фон
def draw_gradient_background(surface):
    top_color = pygame.Color(0, 0, 0)
    bottom_color = pygame.Color(0, 0, 100)
    for y in range(SCREEN_HEIGHT):
        color = pygame.Color(
            int(top_color.r + (bottom_color.r - top_color.r) * y / SCREEN_HEIGHT),
            int(top_color.g + (bottom_color.g - top_color.g) * y / SCREEN_HEIGHT),
            int(top_color.b + (bottom_color.b - top_color.b) * y / SCREEN_HEIGHT)
        )
        pygame.draw.line(surface, color, (0, y), (SCREEN_WIDTH, y))


# Эффекты кнопок
def draw_button(surface, button, text, is_hovered):
    color = (255, 255, 255)
    if is_hovered:
        pygame.draw.rect(surface, (255, 255, 0), button)  # Подсветка
        text_surface = font.render(text, True, (0, 0, 0))
    else:
        pygame.draw.rect(surface, color, button)
        text_surface = font.render(text, True, (0, 0, 0))

    surface.blit(text_surface, (
        button.centerx - text_surface.get_width() // 2,
        button.centery - text_surface.get_height() // 2
    ))


def draw_main_menu(screen):
    draw_gradient_background(screen)

    # Переменные для наведения
    mouse_x, mouse_y = pygame.mouse.get_pos()

    # Кнопки с эффектами
    is_start_hovered = start_button.collidepoint(mouse_x, mouse_y)
    is_settings_hovered = settings_button.collidepoint(mouse_x, mouse_y)
    is_quit_hovered = quit_button.collidepoint(mouse_x, mouse_y)

    draw_button(screen, start_button, "Начать игру", is_start_hovered)
    draw_button(screen, settings_button, "Настройки", is_settings_hovered)
    draw_button(screen, quit_button, "Выйти", is_quit_hovered)


def main_menu(screen):
    running = True
    clock = pygame.time.Clock()
    settings_menu = None

    # Обновляем кнопки в зависимости от разрешения
    update_button_positions()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if settings_menu:
                if not settings_menu.handle_events(event):
                    settings_menu = None
                continue
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):
                    start_level_1(screen)  # Запуск первого уровня
                    print("Запуск игры...")
                elif settings_button.collidepoint(event.pos):
                    print("Открытие настроек...")
                    settings_menu = SettingsMenu(screen, settings)
                elif quit_button.collidepoint(event.pos):
                    running = False

        if settings_menu:
            settings_menu.draw()
        else:
            draw_main_menu(screen)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    # Убедимся, что разрешение обновлено перед запуском меню
    SCREEN_WIDTH, SCREEN_HEIGHT = screen.get_size()
    update_button_positions()  # Пересчёт позиций кнопок
    main_menu(screen)
