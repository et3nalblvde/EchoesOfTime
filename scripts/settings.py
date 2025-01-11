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
        self.font = pygame.font.Font(None, 40)
        self.back_button = pygame.Rect(self.settings["SCREEN_WIDTH"] // 2 - 100,
                                       self.settings["SCREEN_HEIGHT"] - 100, 200, 50)
        self.slider_x_position = 500
        self.options = [
            {"name": "Громкость музыки", "key": "MUSIC_VOLUME", "type": "slider", "range": (0, 1)},
            {"name": "Громкость звуков", "key": "SFX_VOLUME", "type": "slider", "range": (0, 1)},
            {"name": "Управление", "key": "KEYBINDS", "type": "menu"},
            {"name": "Сложность", "key": "DIFFICULTY", "type": "select", "options": ["easy", "medium", "hard"]},
            {"name": "Разрешение", "key": "RESOLUTION", "type": "select",
             "options": ["1024x768", "1280x720", "1366x768", "1600x900", "1920x1080", "2560x1440", "3840x2160"]}
        ]

        self.selected_option = 0
        self.change_key = False
        self.current_key_action = None
        self.keybinding_window_open = False
        self.mouse_held = False


    def draw(self):
        self.screen.fill((30, 30, 30))
        title_text = self.font.render("Настройки", True, (255, 255, 255))
        self.screen.blit(title_text, (self.settings["SCREEN_WIDTH"] // 2 - title_text.get_width() // 2, 50))

        for i, option in enumerate(self.options):
            color = (255, 255, 0) if i == self.selected_option else (255, 255, 255)
            if option["type"] == "slider":
                slider_value = self.settings[option["key"]]
                value_text = f"{int(slider_value * 100)}%"
                option_text = self.font.render(f"{option['name']}: {value_text}", True, color)
                self.screen.blit(option_text, (100, 150 + i * 50))
                pygame.draw.rect(self.screen, (255, 255, 255), (self.slider_x_position, 150 + i * 50, 200, 20))
                pygame.draw.rect(self.screen, (255, 255, 0),
                                 (self.slider_x_position + slider_value * 200, 150 + i * 50, 10, 20))

            elif option["type"] == "menu":
                option_text = self.font.render(f"{option['name']}", True, color)
                self.screen.blit(option_text, (100, 150 + i * 50))

            elif option["type"] == "select":
                option_text = self.font.render(f"{option['name']}: {self.settings[option['key']]}", True, color)
                self.screen.blit(option_text, (100, 150 + i * 50))

        pygame.draw.rect(self.screen, (255, 255, 255), self.back_button)
        back_text = self.font.render("Назад", True, (0, 0, 0))
        self.screen.blit(back_text, (
            self.settings["SCREEN_WIDTH"] // 2 - back_text.get_width() // 2, self.settings["SCREEN_HEIGHT"] - 90))

    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.back_button.collidepoint(event.pos):
                self.save_settings()
                return False

            for i, option in enumerate(self.options):
                if option["type"] == "slider":
                    slider_rect = pygame.Rect(self.slider_x_position, 150 + i * 50, 200, 20)
                    if slider_rect.collidepoint(event.pos):
                        self.adjust_setting_with_mouse(i, event.pos)
                        self.mouse_held = True

                elif option["type"] == "menu" and self.selected_option == i:
                    self.open_keybindings_callback()

                elif option["type"] == "select" and self.selected_option == i:
                    self.adjust_setting(1)

                elif option["type"] == "select" and option["key"] == "RESOLUTION":
                    select_rect = pygame.Rect(100, 150 + i * 50, 400, 50)
                    if select_rect.collidepoint(event.pos):
                        self.adjust_setting(1)

        if event.type == pygame.MOUSEMOTION and self.mouse_held:
            for i, option in enumerate(self.options):
                if option["type"] == "slider":
                    slider_rect = pygame.Rect(self.slider_x_position, 150 + i * 50, 200, 20)
                    if slider_rect.collidepoint(event.pos):
                        self.adjust_setting_with_mouse(i, event.pos)

        if event.type == pygame.MOUSEBUTTONUP:
            self.mouse_held = False

        if event.type == pygame.KEYDOWN:
            if self.change_key:
                if event.key != pygame.K_ESCAPE:
                    self.settings["KEYBINDS"][self.current_key_action] = pygame.key.name(event.key)
                self.change_key = False
                self.current_key_action = None
            elif event.key == pygame.K_UP:
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

            if option["key"] == "RESOLUTION" and isinstance(current_value, list):
                current_value = f"{current_value[0]}x{current_value[1]}"
                self.settings[option["key"]] = current_value

            if current_value not in options:
                self.settings[option["key"]] = options[0]
                current_value = options[0]

            new_value = options[(options.index(current_value) + direction) % len(options)]
            self.settings[option["key"]] = new_value

            if option["key"] == "RESOLUTION":
                resolution = new_value.split("x")
                self.screen = pygame.display.set_mode((int(resolution[0]), int(resolution[1])), pygame.RESIZABLE)

    def adjust_setting_with_mouse(self, option_index, mouse_pos):
        option = self.options[option_index]
        min_val, max_val = option["range"]
        slider_rect = pygame.Rect(self.slider_x_position, 150 + option_index * 50, 200, 20)
        if slider_rect.collidepoint(mouse_pos):
            mouse_x = mouse_pos[0] - slider_rect.left
            slider_value = max(0, min(1, mouse_x / 200))
            self.settings[option["key"]] = slider_value

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


