import pygame
import sys
import os
from scripts.settings import load_settings, SettingsMenu
from level_1 import  start_level_1

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
# Устанавливаем разрешение окна
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
SCREEN_WIDTH, SCREEN_HEIGHT = screen.get_size()  # Получаем реальное разрешение экрана

# Расположение кнопок относительно центра экрана
def update_button_positions():
    global start_button, settings_button, quit_button
    button_width = SCREEN_WIDTH // 3
    button_height = SCREEN_HEIGHT // 10

    # Расчёт позиций кнопок относительно центра экрана
    center_x = SCREEN_WIDTH // 2
    center_y = SCREEN_HEIGHT // 2

    start_button = pygame.Rect(
        center_x - button_width // 2,  # Центрируем по горизонтали
        center_y - button_height * 1.5,  # Смещаем вверх
        button_width, button_height
    )
    settings_button = pygame.Rect(
        center_x - button_width // 2,  # Центрируем по горизонтали
        center_y - button_height // 2,  # Оставляем в центре
        button_width, button_height
    )
    quit_button = pygame.Rect(
        center_x - button_width // 2,  # Центрируем по горизонтали
        center_y + button_height * 0.5,  # Смещаем вниз
        button_width, button_height
    )

def draw_main_menu(screen):
    screen.fill(BACKGROUND_COLOR)

    # Кнопки
    pygame.draw.rect(screen, (255, 255, 255), start_button)
    pygame.draw.rect(screen, (255, 255, 255), settings_button)
    pygame.draw.rect(screen, (255, 255, 255), quit_button)

    # Тексты на кнопках
    start_text = font.render("Начать игру", True, (0, 0, 0))
    settings_text = font.render("Настройки", True, (0, 0, 0))
    quit_text = font.render("Выйти", True, (0, 0, 0))

    screen.blit(start_text, (
        start_button.centerx - start_text.get_width() // 2,
        start_button.centery - start_text.get_height() // 2
    ))
    screen.blit(settings_text, (
        settings_button.centerx - settings_text.get_width() // 2,
        settings_button.centery - settings_text.get_height() // 2
    ))
    screen.blit(quit_text, (
        quit_button.centerx - quit_text.get_width() // 2,
        quit_button.centery - quit_text.get_height() // 2
    ))

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
