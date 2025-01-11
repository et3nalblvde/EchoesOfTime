import pygame
import sys
import os
from scripts.settings import load_settings, SettingsMenu

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
font = pygame.font.Font(FONT_PATH, 25)
start_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50, 200, 50)
settings_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 20, 200, 50)
quit_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 90, 200, 50)


def draw_main_menu(screen):
    screen.fill(BACKGROUND_COLOR)
    pygame.draw.rect(screen, (255, 255, 255), start_button)
    pygame.draw.rect(screen, (255, 255, 255), settings_button)
    pygame.draw.rect(screen, (255, 255, 255), quit_button)
    start_text = font.render("Начать игру", True, (0, 0, 0))
    settings_text = font.render("Настройки", True, (0, 0, 0))
    quit_text = font.render("Выйти", True, (0, 0, 0))
    screen.blit(start_text, (SCREEN_WIDTH // 2 - start_text.get_width() // 2, SCREEN_HEIGHT // 2 - 45))
    screen.blit(settings_text, (SCREEN_WIDTH // 2 - settings_text.get_width() // 2, SCREEN_HEIGHT // 2 + 25))
    screen.blit(quit_text, (SCREEN_WIDTH // 2 - quit_text.get_width() // 2, SCREEN_HEIGHT // 2 + 95))


def main_menu(screen):
    running = True
    clock = pygame.time.Clock()
    settings_menu = None
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
