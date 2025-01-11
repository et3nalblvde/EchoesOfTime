import json
import os
import pygame
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.abspath(os.path.join(BASE_DIR, '..'))
ASSETS_DIR = os.path.join(PROJECT_DIR, 'assets')
FONTS_DIR = os.path.join(ASSETS_DIR, 'fonts')
SETTINGS_FILE = os.path.join(PROJECT_DIR, 'save', 'settings.json')
print(SETTINGS_FILE,FONTS_DIR,ASSETS_DIR,PROJECT_DIR,BASE_DIR)

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
BACKGROUND_COLOR = tuple(settings["BACKGROUND_COLOR"])
MUSIC_VOLUME = settings["MUSIC_VOLUME"]
SFX_VOLUME = settings["SFX_VOLUME"]
ECHO_DELAY = settings["ECHO_DELAY"]
ECHO_OPACITY = settings["ECHO_OPACITY"]



class SettingsMenu:
    def __init__(self, screen, settings):
        self.screen = screen
        self.settings = settings
        self.base_font_size = 40
        self.font = pygame.font.Font(None, self.base_font_size)
        self.back_button_width = 200
        self.back_button_height = 50
        self.slider_width = 200
        self.slider_height = 20
        self.options = [
            {"name": "Громкость музыки", "key": "MUSIC_VOLUME", "type": "slider", "range": (0, 1)},
            {"name": "Громкость звуков", "key": "SFX_VOLUME", "type": "slider", "range": (0, 1)},
            {"name": "Управление", "key": "KEYBINDS", "type": "menu"},
            {"name": "Сложность", "key": "DIFFICULTY", "type": "select", "options": ["easy", "medium", "hard"]},
            {"name": "Разрешение", "key": "RESOLUTION", "type": "select",
             "options": ["1024x768", "1280x720", "1366x768", "1600x900", "1920x1080", "2560x1440"]}
        ]

        self.selected_option = 0
        self.change_key = False
        self.current_key_action = None

        self.update_resolution()

    def update_resolution(self):
        self.screen_width = self.settings["SCREEN_WIDTH"]
        self.screen_height = self.settings["SCREEN_HEIGHT"]

        # Пересчитываем размеры и позицию элементов относительно разрешения экрана
        self.back_button = pygame.Rect(self.screen_width * 0.5 - self.back_button_width * 0.5,
                                       self.screen_height - self.back_button_height - 20,
                                       self.back_button_width, self.back_button_height)

        self.slider_x_position = self.screen_width * 0.5 - self.slider_width * 0.5

        self.font_size = int(self.base_font_size * (self.screen_width / 1024))  # Пропорциональный размер шрифта
        self.font = pygame.font.Font(None, self.font_size)

    def draw(self):
        self.screen.fill((30, 30, 30))
        title_text = self.font.render("Настройки", True, (255, 255, 255))
        self.screen.blit(title_text, (self.screen_width * 0.5 - title_text.get_width() * 0.5, self.screen_height * 0.1))

        for i, option in enumerate(self.options):
            color = (255, 255, 0) if i == self.selected_option else (255, 255, 255)
            y_offset = self.screen_height * 0.2 + i * (self.font_size * 1.5)
            if option["type"] == "slider":
                slider_value = self.settings[option["key"]]
                value_text = f"{int(slider_value * 100)}%"
                option_text = self.font.render(f"{option['name']}: {value_text}", True, color)
                self.screen.blit(option_text, (self.screen_width * 0.1, y_offset))
                pygame.draw.rect(self.screen, (255, 255, 255), (self.slider_x_position, y_offset, self.slider_width, self.slider_height))
                pygame.draw.rect(self.screen, (255, 255, 0),
                                 (self.slider_x_position + slider_value * self.slider_width, y_offset, 10, self.slider_height))

            elif option["type"] == "menu":
                option_text = self.font.render(f"{option['name']}", True, color)
                self.screen.blit(option_text, (self.screen_width * 0.1, y_offset))

            elif option["type"] == "select":
                option_text = self.font.render(f"{option['name']}: {self.settings[option['key']]}", True, color)
                self.screen.blit(option_text, (self.screen_width * 0.1, y_offset))

        pygame.draw.rect(self.screen, (255, 255, 255), self.back_button)
        back_text = self.font.render("Назад", True, (0, 0, 0))
        self.screen.blit(back_text, (
            self.screen_width * 0.5 - back_text.get_width() * 0.5, self.screen_height * 0.9))

    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.back_button.collidepoint(event.pos):
                self.save_settings()
                return False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_option = (self.selected_option - 1) % len(self.options)
            elif event.key == pygame.K_DOWN:
                self.selected_option = (self.selected_option + 1) % len(self.options)
            elif event.key == pygame.K_LEFT:
                self.adjust_setting(-1)
            elif event.key == pygame.K_RIGHT:
                self.adjust_setting(1)

        return True

    def adjust_setting(self, direction):
        option = self.options[self.selected_option]
        if option["type"] == "slider":
            min_val, max_val = option["range"]
            step = 0.1 if option["key"] in ["MUSIC_VOLUME", "SFX_VOLUME"] else 1
            new_value = self.settings[option["key"]] + direction * step
            self.settings[option["key"]] = max(min(new_value, max_val), min_val)
        elif option["type"] == "select":
            current_value = self.settings[option["key"]]
            options = option["options"]

            new_value = options[(options.index(current_value) + direction) % len(options)]
            self.settings[option["key"]] = new_value

            if option["key"] == "RESOLUTION":
                width, height = map(int, new_value.split("x"))
                self.screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
                self.settings["SCREEN_WIDTH"] = width
                self.settings["SCREEN_HEIGHT"] = height
                self.update_resolution()  # Обновляем разрешение и элементы

                self.save_settings()

        return True

    def save_settings(self):
        os.makedirs(os.path.dirname(SETTINGS_FILE), exist_ok=True)
        with open(SETTINGS_FILE, "w") as f:
            json.dump(self.settings, f, indent=4)




class KeyBindingsMenu:
    def __init__(self, screen, settings, close_callback):
        self.screen = screen
        self.settings = settings
        self.font = pygame.font.Font(None, 40)
        self.back_button = pygame.Rect(self.settings["SCREEN_WIDTH"] // 2 - 100,
                                       self.settings["SCREEN_HEIGHT"] - 100, 200, 50)
        self.current_key_action = None
        self.close_callback = close_callback

    def draw(self):
        self.screen.fill((30, 30, 30))
        title_text = self.font.render("Управление", True, (255, 255, 255))
        self.screen.blit(title_text, (self.settings["SCREEN_WIDTH"] // 2 - title_text.get_width() // 2, 50))

        keybinds = self.settings["KEYBINDS"]
        y_offset = 150
        for action, key in keybinds.items():
            option_text = self.font.render(f"{action}: {key}", True, (255, 255, 255))
            self.screen.blit(option_text, (100, y_offset))
            y_offset += 50

        pygame.draw.rect(self.screen, (255, 255, 255), self.back_button)
        back_text = self.font.render("Назад", True, (0, 0, 0))
        self.screen.blit(back_text, (
            self.settings["SCREEN_WIDTH"] // 2 - back_text.get_width() // 2, self.settings["SCREEN_HEIGHT"] - 90))

    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.back_button.collidepoint(event.pos):
                self.close_callback()

        if event.type == pygame.KEYDOWN:
            if event.key != pygame.K_ESCAPE:
                self.settings["KEYBINDS"][self.current_key_action] = pygame.key.name(event.key)
            self.current_key_action = None

        return True





def set_resolution(resolution):
    if resolution == "1024x768":
        self.settings["SCREEN_WIDTH"] = 1024
        self.settings["SCREEN_HEIGHT"] = 768
    elif resolution == "1280x720":
        self.settings["SCREEN_WIDTH"] = 1280
        self.settings["SCREEN_HEIGHT"] = 720
    elif resolution == "1920x1080":
        self.settings["SCREEN_WIDTH"] = 1920
        self.settings["SCREEN_HEIGHT"] = 1080


