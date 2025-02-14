import pygame
import os
from PIL import Image
from scripts.settings import load_settings, SettingsMenu
from level_1 import start_level_1
from level_2 import start_level_2
from pause_menu import PauseMenu
import json

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

background_gif_path = os.path.join(ASSETS_DIR, 'sprites', 'background', 'background.gif')
background_image = Image.open(background_gif_path)

background_frames = []
for frame in range(background_image.n_frames):
    background_image.seek(frame)
    frame_data = pygame.image.fromstring(background_image.convert("RGBA").tobytes(), background_image.size, "RGBA")
    background_frames.append(frame_data)

frame_count = len(background_frames)


def update_level_2_status():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    PROJECT_DIR = os.path.abspath(os.path.join(BASE_DIR, '..'))
    settings_path = os.path.join(PROJECT_DIR, 'save', 'settings.json')

    with open(settings_path, 'r') as f:
        settings_data = json.load(f)

    settings_data["Level_2"] = False

    with open(settings_path, 'w') as f:
        json.dump(settings_data, f, indent=4)


def update_button_positions():
    global start_button, settings_button, quit_button, continue_button
    button_width = SCREEN_WIDTH // 3
    button_height = SCREEN_HEIGHT // 10
    center_x = SCREEN_WIDTH // 2
    center_y = SCREEN_HEIGHT // 2
    button_spacing = button_height - 150

    settings = load_settings()

    has_completed_levels = any(
        level in settings and settings[level] == "complete"
        for level in ["level_1", "level_2"]
    )

    if has_completed_levels:
        buttons_count = 4
    else:
        buttons_count = 3

    total_height = buttons_count * button_height + (buttons_count - 1) * button_spacing
    vertical_shift = (SCREEN_HEIGHT - total_height) // 2

    if has_completed_levels:
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
        continue_button = None
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

    if continue_button:
        draw_button(screen, continue_button, "Продолжить игру", is_continue_hovered)

    draw_button(screen, start_button, "Начать игру", is_start_hovered)
    draw_button(screen, settings_button, "Настройки", is_settings_hovered)
    draw_button(screen, quit_button, "Выйти в меню", is_quit_hovered)


def handle_continue_button(event):
    if continue_button and event.type == pygame.MOUSEBUTTONDOWN and continue_button.collidepoint(event.pos):
        saved_state = load_game_state()
        if saved_state:
            level = saved_state["level"]
            player_x = saved_state["player_x"]
            player_y = saved_state["player_y"]
            if level == "level_1":
                start_level_1(screen, restart_main_menu, exit_to_main_menu, player_x, player_y)
            elif level == "level_2":
                start_level_2(screen, restart_main_menu, exit_to_main_menu, player_x, player_y)
        return False
    return True


def handle_start_button(event):
    if event.type == pygame.MOUSEBUTTONDOWN and start_button.collidepoint(event.pos):
        settings = load_settings()
        settings["level_1"] = False

        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        PROJECT_DIR = os.path.abspath(os.path.join(BASE_DIR, '..'))
        settings_path = os.path.join(PROJECT_DIR, 'save', 'settings.json')
        with open(settings_path, 'w') as f:
            json.dump(settings, f, indent=4)

        global continue_button
        continue_button = None

        pygame.mixer.music.fadeout(4000)
        start_level_1(screen, restart_main_menu, exit_to_main_menu)
        return False
    return True


def handle_continue_button(event):
    if continue_button and event.type == pygame.MOUSEBUTTONDOWN and continue_button.collidepoint(event.pos):
        pygame.mixer.music.fadeout(4000)
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


def get_last_completed_level():
    settings = load_settings()
    levels = ["level_1", "level_2"]
    last_completed = None
    for level in levels:
        if level in settings and settings[level] == "complete":
            last_completed = level
    return last_completed


def handle_menu_events(event, settings_menu):
    running = True  # Инициализация переменной running

    if event.type == pygame.QUIT:
        return False, settings_menu

    if settings_menu:
        # Если открыты настройки, блокируем взаимодействие с остальными кнопками
        if not settings_menu.handle_events(event):
            settings_menu = None
            return True, settings_menu
    else:
        if continue_button and event.type == pygame.MOUSEBUTTONDOWN and continue_button.collidepoint(event.pos):
            last_completed_level = get_last_completed_level()
            if last_completed_level == "level_1":
                start_level_2(screen, restart_main_menu, exit_to_main_menu)
            elif last_completed_level == "level_2":
                print("All levels are complete!")
            return False, settings_menu

        running = handle_start_button(event) and running
        running = handle_continue_button(event) and running
        settings_menu, running = handle_settings_button(event, settings_menu)
        running = handle_quit_button(event) and running

    return running, settings_menu


def draw_confirmation_menu(screen):
    # Отрисовка окна подтверждения
    confirmation_text = font.render("Уверены, что хотите начать игру?", True, (255, 255, 255))
    yes_button = pygame.Rect(SCREEN_WIDTH // 3 - SCREEN_WIDTH // 8, SCREEN_HEIGHT // 2, SCREEN_WIDTH // 6,
                             SCREEN_HEIGHT // 10)
    no_button = pygame.Rect(2 * SCREEN_WIDTH // 3 - SCREEN_WIDTH // 8, SCREEN_HEIGHT // 2, SCREEN_WIDTH // 6,
                            SCREEN_HEIGHT // 10)

    pygame.draw.rect(screen, (0, 200, 0), yes_button)
    pygame.draw.rect(screen, (200, 0, 0), no_button)

    yes_text = font.render("Да", True, (0, 0, 0))
    no_text = font.render("Нет", True, (0, 0, 0))

    screen.blit(confirmation_text, (SCREEN_WIDTH // 2 - confirmation_text.get_width() // 2, SCREEN_HEIGHT // 3))
    screen.blit(yes_text,
                (yes_button.centerx - yes_text.get_width() // 2, yes_button.centery - yes_text.get_height() // 2))
    screen.blit(no_text, (no_button.centerx - no_text.get_width() // 2, no_button.centery - no_text.get_height() // 2))

    return yes_button, no_button


def handle_confirmation_events(event, yes_button, no_button):
    if event.type == pygame.MOUSEBUTTONDOWN:
        if yes_button.collidepoint(event.pos):
            return "yes"
        elif no_button.collidepoint(event.pos):
            return "no"
    return None


def main_menu(screen):
    running = True
    clock = pygame.time.Clock()
    settings_menu = None
    current_frame = 0
    frame_delay = 2
    frame_counter = 0
    update_button_positions()

    confirmation_mode = False
    yes_button, no_button = None, None

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if confirmation_mode:
                # Обработка событий окна подтверждения
                result = handle_confirmation_events(event, yes_button, no_button)
                if result == "yes":
                    confirmation_mode = False
                    pygame.mixer.music.fadeout(4000)
                    start_level_1(screen, restart_main_menu, exit_to_main_menu)
                elif result == "no":
                    confirmation_mode = False
            else:
                # Обработка событий главного меню
                running, settings_menu = handle_menu_events(event, settings_menu)
                if not running:
                    break
                if event.type == pygame.MOUSEBUTTONDOWN and start_button.collidepoint(event.pos):
                    confirmation_mode = True
                    yes_button, no_button = draw_confirmation_menu(screen)

        # Отрисовка
        if confirmation_mode:
            screen.fill((0, 0, 0))  # Чёрный фон
            yes_button, no_button = draw_confirmation_menu(screen)
        elif settings_menu:
            settings_menu.draw()
        else:
            if frame_counter >= frame_delay:
                draw_main_menu(screen, current_frame)
                current_frame = (current_frame + 1) % frame_count
                frame_counter = 0
            else:
                frame_counter += 1

        pygame.display.flip()  # Обновление экрана
        clock.tick(FPS)

    pygame.quit()


def restart_main_menu():
    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    main_menu(screen)


def exit_to_main_menu():
    return True
