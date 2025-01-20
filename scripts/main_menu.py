import pygame
import sys
import os
from PIL import Image
from scripts.settings import load_settings, SettingsMenu
from level_1 import start_level_1

pygame.init()
settings = load_settings()
SCREEN_WIDTH = settings["SCREEN_WIDTH"]
SCREEN_HEIGHT = settings["SCREEN_HEIGHT"]
FPS = settings["FPS"]
MUSIC_VOLUME = settings["MUSIC_VOLUME"]
pygame.mixer.music.set_volume(MUSIC_VOLUME)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.join(BASE_DIR, '..')
ASSETS_DIR = os.path.join(PROJECT_DIR, 'assets')
FONTS_DIR = os.path.join(ASSETS_DIR, 'fonts')
FONT_PATH = os.path.join(FONTS_DIR, 'PressStart2P.ttf')

base_font_size = 25
font = pygame.font.Font(FONT_PATH, base_font_size)

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
SCREEN_WIDTH, SCREEN_HEIGHT = screen.get_size()

background_gif_path = os.path.join(ASSETS_DIR, 'sprites','background', 'background.gif')
background_image = Image.open(background_gif_path)

background_frames = []
for frame in range(background_image.n_frames):
    background_image.seek(frame)
    frame_data = pygame.image.fromstring(background_image.convert("RGBA").tobytes(), background_image.size, "RGBA")
    background_frames.append(frame_data)

frame_count = len(background_frames)

def update_button_positions():
    global start_button, settings_button, quit_button, continue_button
    button_width = SCREEN_WIDTH // 3
    button_height = SCREEN_HEIGHT // 10

    center_x = SCREEN_WIDTH // 2
    center_y = SCREEN_HEIGHT // 2

    # Уменьшаем расстояние между кнопками
    button_spacing = button_height -150  # Уменьшено расстояние между кнопками

    # Определяем, сколько кнопок будет отображаться
    if settings.get("Level_2", False):  # Если "Продолжить игру" True
        buttons_count = 4  # 4 кнопки, включая "Продолжить игру"
    else:
        buttons_count = 3  # 3 кнопки, без "Продолжить игру"

    # Местоположение кнопок по вертикали
    total_height = buttons_count * button_height + (buttons_count - 1) * button_spacing
    vertical_shift = (SCREEN_HEIGHT - total_height) // 2  # Сдвиг для центрирования кнопок

    # Перемещаем кнопку "Продолжить игру" на первую позицию, если она должна быть
    if settings.get("Level_2", False):
        continue_button = pygame.Rect(
            center_x - button_width // 2,
            vertical_shift,
            button_width, button_height
        )
        start_button = pygame.Rect(
            center_x - button_width // 2,
            vertical_shift + button_height + button_spacing,
            button_width, button_height
        )
        settings_button = pygame.Rect(
            center_x - button_width // 2,
            vertical_shift + 2 * (button_height + button_spacing),
            button_width, button_height
        )
        quit_button = pygame.Rect(
            center_x - button_width // 2,
            vertical_shift + 3 * (button_height + button_spacing),
            button_width, button_height
        )
    else:
        continue_button = None  # Если не True, скрываем кнопку
        start_button = pygame.Rect(
            center_x - button_width // 2,
            vertical_shift,
            button_width, button_height
        )
        settings_button = pygame.Rect(
            center_x - button_width // 2,
            vertical_shift + button_height + button_spacing,
            button_width, button_height
        )
        quit_button = pygame.Rect(
            center_x - button_width // 2,
            vertical_shift + 2 * (button_height + button_spacing),
            button_width, button_height
        )







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

def draw_button(surface, button, text, is_hovered):
    pygame.draw.rect(surface, (255, 255, 0), button, 3)
    text_surface = font.render(text, True, (255, 255, 255))
    surface.blit(text_surface, (
        button.centerx - text_surface.get_width() // 2,
        button.centery - text_surface.get_height() // 2
    ))

def draw_main_menu(screen, current_frame):
    background_resized = pygame.transform.scale(background_frames[current_frame], (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(background_resized, (0, 0))

    mouse_x, mouse_y = pygame.mouse.get_pos()

    is_start_hovered = start_button.collidepoint(mouse_x, mouse_y)
    is_settings_hovered = settings_button.collidepoint(mouse_x, mouse_y)
    is_quit_hovered = quit_button.collidepoint(mouse_x, mouse_y)
    is_continue_hovered = continue_button.collidepoint(mouse_x, mouse_y) if continue_button else False

    draw_button(screen, start_button, "Начать игру", is_start_hovered)
    draw_button(screen, settings_button, "Настройки", is_settings_hovered)
    draw_button(screen, quit_button, "Выйти в меню", is_quit_hovered)

    if continue_button:
        draw_button(screen, continue_button, "Продолжить игру", is_continue_hovered)

def handle_start_button(event):
    if event.type == pygame.MOUSEBUTTONDOWN and start_button.collidepoint(event.pos):
        pygame.mixer.music.fadeout(4000)
        start_level_1(screen)
        return False
    return True

def handle_continue_button(event):
    if continue_button and event.type == pygame.MOUSEBUTTONDOWN and continue_button.collidepoint(event.pos):
        # В будущем, когда добавите 2-й уровень, здесь будет вызов функции для начала 2-го уровня
        pygame.mixer.music.fadeout(4000)
        # start_level_2(screen)  # Вызывать второй уровень, когда он будет готов
        return False
    return True


def handle_settings_button(event, settings_menu):
    if event.type == pygame.MOUSEBUTTONDOWN and settings_button.collidepoint(event.pos):
        settings_menu = SettingsMenu(screen, settings)
        return settings_menu, True
    return settings_menu, True

def handle_quit_button(event):
    if event.type == pygame.MOUSEBUTTONDOWN and quit_button.collidepoint(event.pos):
        return False
    return True

def handle_menu_events(event, settings_menu):
    if event.type == pygame.QUIT:
        return False, settings_menu

    if settings_menu:
        if not settings_menu.handle_events(event):
            settings_menu = None
        return True, settings_menu

    running = True
    running = handle_start_button(event) and running
    running = handle_continue_button(event) and running  # Обработка кнопки продолжить
    settings_menu, running = handle_settings_button(event, settings_menu)
    running = handle_quit_button(event) and running

    return running, settings_menu

def main_menu(screen):
    running = True
    clock = pygame.time.Clock()
    settings_menu = None
    current_frame = 0
    frame_delay = 2
    frame_counter = 0

    update_button_positions()

    while running:
        for event in pygame.event.get():
            running, settings_menu = handle_menu_events(event, settings_menu)
            if not running:
                break  

        if settings_menu:
            settings_menu.draw()
        else:
            if frame_counter >= frame_delay:
                draw_main_menu(screen, current_frame)
                current_frame = (current_frame + 1) % frame_count
                frame_counter = 0
            else:
                frame_counter += 1

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()  
