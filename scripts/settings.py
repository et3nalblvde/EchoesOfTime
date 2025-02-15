import pygame
import json
import os
from PIL import Image
import pygame.mixer


pygame.mixer.init()


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.abspath(os.path.join(BASE_DIR, '..'))
ASSETS_DIR = os.path.join(PROJECT_DIR, 'assets')
FONTS_DIR = os.path.join(ASSETS_DIR, 'fonts')
SETTINGS_FILE = os.path.join(PROJECT_DIR, 'save', 'settings.json')
BACKGROUND_GIF_PATH = os.path.join(ASSETS_DIR, 'sprites', 'background', 'background.gif')
MUSIC_FILE = os.path.join(ASSETS_DIR, 'sounds', 'main_theme', 'Resting_Grounds.mp3')


DIFFICULTY_MODIFIERS = {
    "easy": 0.5,   # Легкая сложность: -0.5 сердечка
    "medium": 1.0, # Средняя сложность: -1 сердечко
    "hard": 1.5    # Сложная сложность: -1.5 сердечка
}


def load_sounds(volume):
    sound_folder = os.path.join(BASE_DIR, '..', 'assets', 'sounds', 'effects')
    sounds = {
        "jump": pygame.mixer.Sound(os.path.join(sound_folder, 'jump.mp3')),
        "attack": pygame.mixer.Sound(os.path.join(sound_folder, 'attack.mp3')),
        "walk": pygame.mixer.Sound(os.path.join(sound_folder, 'steps.ogg'))
    }

    for sound in sounds.values():
        sound.set_volume(volume)
    return sounds






background_image = Image.open(BACKGROUND_GIF_PATH)
background_frames = []
for frame in range(background_image.n_frames):
    background_image.seek(frame)
    frame_data = pygame.image.fromstring(background_image.convert("RGBA").tobytes(), background_image.size, "RGBA")
    background_frames.append(frame_data)
frame_count = len(background_frames)

FONT_PATH = os.path.join(FONTS_DIR, 'PressStart2P.ttf')


def load_settings():
    default_settings = {
        "SCREEN_WIDTH": 1024,
        "SCREEN_HEIGHT": 768,
        "FPS": 60,
        "MUSIC_VOLUME": 0.5,
        "SFX_VOLUME": 0.7,
        "ECHO_DELAY": 2,
        "ECHO_OPACITY": 100,
        "FULLSCREEN": False,
        "KEYBINDS": {
            "UP": "w",
            "DOWN": "s",
            "LEFT": "a",
            "RIGHT": "d",
            "JUMP": "space"
        },
        "DIFFICULTY": "medium",
        "RESOLUTION": [1024, 768]
    }

    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r") as file:
            settings = json.load(file)
        for key, value in default_settings.items():
            if key not in settings:
                settings[key] = value
        return settings
    else:
        return default_settings

def save_settings(settings):
    os.makedirs(os.path.dirname(SETTINGS_FILE), exist_ok=True)
    with open(SETTINGS_FILE, "w") as file:
        json.dump(settings, file, indent=4)


settings = load_settings()
SCREEN_WIDTH = settings["SCREEN_WIDTH"]
SCREEN_HEIGHT = settings["SCREEN_HEIGHT"]
FPS = settings["FPS"]
MUSIC_VOLUME = settings["MUSIC_VOLUME"]
SFX_VOLUME = settings["SFX_VOLUME"]
ECHO_DELAY = settings["ECHO_DELAY"]
ECHO_OPACITY = settings["ECHO_OPACITY"]
level_2=settings["Level_2"]


pygame.mixer.music.load(MUSIC_FILE)
pygame.mixer.music.set_volume(MUSIC_VOLUME)
pygame.mixer.music.play(-1)
player_sounds = load_sounds(SFX_VOLUME)

class SettingsMenu:
    def __init__(self, screen, settings):
        self.screen = screen
        self.settings = settings
        self.base_font_size = 18
        self.font = pygame.font.Font(FONT_PATH, self.base_font_size)
        self.back_button_width = 200
        self.back_button_height = 50
        self.slider_width = 200
        self.volume = 0.5
        self.slider_height = 20
        self.options = [
            {"name": "Громкость музыки", "key": "MUSIC_VOLUME", "type": "slider", "range": (0, 1)},
            {"name": "Громкость звуков", "key": "SFX_VOLUME", "type": "slider", "range": (0, 1)},
            {"name": "Сложность", "key": "DIFFICULTY", "type": "select", "options": ["easy", "medium", "hard"]},
        ]

        self.selected_option = None
        self.update_resolution()
        self.is_dragging_slider = False
        self.dragged_slider = None
        self.sound_effects = load_sounds(settings["SFX_VOLUME"])

    def update_resolution(self):
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.screen_width, self.screen_height = self.screen.get_size()
        self.back_button = pygame.Rect(
            self.screen_width * 0.5 - self.back_button_width * 0.5,
            self.screen_height * 0.91 - self.back_button_height + 20,  # Adjusted back button position by 20px
            self.back_button_width, self.back_button_height
        )
        self.slider_x_position = self.screen_width * 0.5 - self.slider_width * 0.5 + 50  # Move sliders to the right
        self.font_size = int(self.base_font_size * (self.screen_width / 1024))
        self.font = pygame.font.Font(FONT_PATH, self.font_size)

    def draw(self):
        frame_skip = 3
        current_frame = (pygame.time.get_ticks() // (100 * frame_skip)) % frame_count
        background_resized = pygame.transform.scale(background_frames[current_frame],
                                                    (self.screen_width, self.screen_height))
        self.screen.blit(background_resized, (0, 0))

        # Заголовок
        title_text = self.font.render("Настройки", True, (255, 255, 255))
        self.screen.blit(title_text, (self.screen_width * 0.5 - title_text.get_width() * 0.5, self.screen_height * 0.1))

        # Отображаем координаты мыши
        mouse_x, mouse_y = pygame.mouse.get_pos()
        mouse_coords_text = self.font.render(f"Мышь: x={mouse_x}, y={mouse_y}", True, (255, 255, 255))
        self.screen.blit(mouse_coords_text, (10, 10))

        # Отрисовка слайдеров
        for i, option in enumerate(self.options):
            color = (255, 255, 0) if self.selected_option == i else (255, 255, 255)
            y_offset = self.screen_height * 0.25 + i * (self.font_size * 2) + 50  # Учитываем смещение

            if option["type"] == "slider":
                slider_value = self.settings[option["key"]]
                value_text = f"{int(slider_value * 100)}%"
                option_text = self.font.render(f"{option['name']}: {value_text}", True, color)
                self.screen.blit(option_text, (self.screen_width * 0.1, y_offset))

                # Отрисовка слайдера
                slider_rect = pygame.Rect(
                    self.slider_x_position + 70,  # Начало слайдера
                    y_offset + 10,  # Смещение вниз
                    self.slider_width,
                    self.slider_height
                )
                pygame.draw.rect(self.screen, (255, 255, 255), slider_rect, 2)  # Рамка слайдера

                # Ползунок слайдера
                handle_x = slider_rect.x + slider_value * self.slider_width - 5
                handle_rect = pygame.Rect(handle_x, slider_rect.y, 10, self.slider_height)
                pygame.draw.rect(self.screen, (255, 255, 0), handle_rect)

            elif option["type"] == "select":
                option_text = self.font.render(f"{option['name']}: {self.settings[option['key']]}", True, color)
                self.screen.blit(option_text, (self.screen_width * 0.1, y_offset))

        # Кнопка "Назад"
        pygame.draw.rect(self.screen, (255, 255, 255), self.back_button, 2)
        back_text = self.font.render("Назад", True, (255, 255, 255))
        self.screen.blit(back_text, (
            self.screen_width * 0.5 - back_text.get_width() * 0.5,
            self.screen_height * 0.85 + 60
        ))

    def handle_events(self, event):
        if not pygame.display.get_active():
            return True  # Игнорируем все события, если окно не активно

        mouse_x, mouse_y = pygame.mouse.get_pos()

        if event.type == pygame.MOUSEBUTTONDOWN:
            # Проверяем кнопку "Назад"
            if self.back_button.collidepoint(mouse_x, mouse_y):
                self.save_settings()
                return False  # Выход из меню настроек

            # Обрабатываем клики по слайдерам
            for i, option in enumerate(self.options):
                y_offset = self.screen_height * 0.25 + i * (self.font_size * 2) + 50  # Учитываем смещение
                if option["type"] == "slider":
                    slider_rect = pygame.Rect(
                        self.slider_x_position + 70,  # Начало слайдера
                        y_offset + 10,  # Смещение вниз
                        self.slider_width,
                        self.slider_height
                    )
                    if slider_rect.collidepoint(mouse_x, mouse_y):
                        self.is_dragging_slider = True
                        self.dragged_slider = i  # Запоминаем, какой слайдер тянем
                        self.adjust_slider(option, mouse_x)  # Немедленно обновляем значение
                        break
                elif option["type"] == "select":
                    text_rect = pygame.Rect(
                        self.screen_width * 0.1,
                        y_offset,
                        400,
                        self.font_size
                    )
                    if text_rect.collidepoint(mouse_x, mouse_y):
                        self.adjust_select(option)
                        break

        elif event.type == pygame.MOUSEBUTTONUP:
            # Прекращаем перетаскивание слайдера
            self.is_dragging_slider = False
            self.dragged_slider = None

        elif event.type == pygame.MOUSEMOTION:
            # Если слайдер тянется, обновляем его значение
            if self.is_dragging_slider and self.dragged_slider is not None:
                option = self.options[self.dragged_slider]
                self.adjust_slider(option, mouse_x)

        return True

    def adjust_slider(self, option, mouse_x):
        if self.is_dragging_slider:
            # Учитываем смещение слайдера (70 пикселей вправо)
            slider_start_x = self.slider_x_position + 70
            # Вычисляем новое значение слайдера относительно его реального начала
            relative_x = mouse_x - slider_start_x
            new_value = max(0, min(1, relative_x / self.slider_width))

            # Обновляем значение в настройках
            self.settings[option["key"]] = new_value

            # Применяем изменения в игре
            if option["key"] == "MUSIC_VOLUME":
                pygame.mixer.music.set_volume(new_value)
            elif option["key"] == "SFX_VOLUME":
                for sound_name, sound in self.sound_effects.items():
                    sound.set_volume(new_value)
                if hasattr(self, "player"):
                    self.player.update_sfx_volume(new_value)

            # Сохраняем настройки
            self.save_settings()

    def adjust_select(self, option):
        current_value = self.settings[option["key"]]
        options = option["options"]
        new_value = options[(options.index(current_value) + 1) % len(options)]
        self.settings[option["key"]] = new_value

        if option["key"] == "RESOLUTION":
            width, height = map(int, new_value.split("x"))
            self.screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
            self.settings["SCREEN_WIDTH"] = width
            self.settings["SCREEN_HEIGHT"] = height
            self.update_resolution()

        if option["key"] == "DIFFICULTY":
            self.settings["DIFFICULTY"] = new_value

        self.save_settings()

    def save_settings(self):
        with open(SETTINGS_FILE, "w") as file:
            json.dump(self.settings, file, indent=4)


