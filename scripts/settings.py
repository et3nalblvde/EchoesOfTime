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
        self.selected_option = None
        self.update_resolution()
        self.keybindings_menu = None
        self.options = [
            {"name": "Громкость музыки", "key": "MUSIC_VOLUME", "type": "slider", "range": (0, 1)},
            {"name": "Громкость звуков", "key": "SFX_VOLUME", "type": "slider", "range": (0, 1)},
            {"name": "Управление", "key": "KEYBINDS", "type": "menu"},
            {"name": "Сложность", "key": "DIFFICULTY", "type": "select", "options": ["easy", "medium", "hard"]},
            {"name": "Разрешение", "key": "RESOLUTION", "type": "select",
             "options": ["1024x768", "1280x720", "1366x768", "1600x900", "1920x1080", "2560x1440"]},
        ]
        self.selected_option = None
        self.update_resolution()

    def update_resolution(self):
        self.screen_width = self.settings["SCREEN_WIDTH"]
        self.screen_height = self.settings["SCREEN_HEIGHT"]
        self.back_button = pygame.Rect(
            self.screen_width * 0.5 - self.back_button_width * 0.5,
            self.screen_height - self.back_button_height - 20,
            self.back_button_width, self.back_button_height
        )
        self.slider_x_position = self.screen_width * 0.5 - self.slider_width * 0.5
        self.font_size = int(self.base_font_size * (self.screen_width / 1024))
        self.font = pygame.font.Font(None, self.font_size)

    def draw(self):
        self.screen.fill((30, 30, 30))
        title_text = self.font.render("Настройки", True, (255, 255, 255))
        self.screen.blit(title_text, (self.screen_width * 0.5 - title_text.get_width() * 0.5, self.screen_height * 0.1))

        for i, option in enumerate(self.options):
            color = (255, 255, 0) if self.selected_option == i else (255, 255, 255)
            y_offset = self.screen_height * 0.2 + i * (self.font_size * 1.5) - 30
            if option["type"] == "slider":
                slider_value = self.settings[option["key"]]
                value_text = f"{int(slider_value * 100)}%"
                option_text = self.font.render(f"{option['name']}: {value_text}", True, color)
                self.screen.blit(option_text, (self.screen_width * 0.1, y_offset))
                pygame.draw.rect(self.screen, (255, 255, 255),
                                 (self.slider_x_position, y_offset + self.font_size, self.slider_width, self.slider_height))
                pygame.draw.rect(self.screen, (255, 255, 0),
                                 (self.slider_x_position + slider_value * self.slider_width - 5,
                                  y_offset + self.font_size, 10, self.slider_height))

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
        if self.keybindings_menu:
            result = self.keybindings_menu.handle_events(event)
            if result == "back":
                self.keybindings_menu = None  # Возвращаемся в главное меню
            elif result == "waiting_for_input":
                return "waiting_for_input"
            return result

        if event.type == pygame.MOUSEMOTION:
            mouse_x, mouse_y = event.pos
            self.selected_option = None
            for i, option in enumerate(self.options):
                y_offset = self.screen_height * 0.2 + i * (self.font_size * 1.5) - 30
                if option["type"] == "menu" and option["key"] == "KEYBINDS":
                    text_rect = pygame.Rect(self.screen_width * 0.1, y_offset, 400, self.font_size)
                    if text_rect.collidepoint(mouse_x, mouse_y):
                        self.selected_option = i  # Выделяем кнопку "Управление"
                        break

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            if self.back_button.collidepoint(event.pos):
                self.save_settings()
                return False

            if self.selected_option is not None:
                option = self.options[self.selected_option]
                if option["type"] == "menu" and option["key"] == "KEYBINDS":
                    self.keybindings_menu = KeyBindingsMenu(self.screen, self.settings)
                    return "keybindings"  # Переход в меню управления клавишами

        return True

    def save_settings(self):
        with open(SETTINGS_FILE, "w") as file:
            json.dump(self.settings, file, indent=4)


class KeyBindingsMenu:
    def __init__(self, screen, settings):
        self.screen = screen
        self.settings = settings
        self.font_size = 40
        self.font = pygame.font.Font(None, self.font_size)
        self.back_button_width = 200
        self.back_button_height = 50
        self.keybinding_width = 400
        self.keybinding_height = 50
        self.selected_key = None

        self.back_button = pygame.Rect(
            self.screen.get_width() * 0.5 - self.back_button_width * 0.5,
            self.screen.get_height() - self.back_button_height - 20,
            self.back_button_width, self.back_button_height
        )

        self.keybinding_buttons = self.create_keybinding_buttons()

    def create_keybinding_buttons(self):
        keybinding_buttons = []
        keybinds = self.settings.get("KEYBINDS", {})
        y_offset = self.screen.get_height() * 0.2

        for action, key in keybinds.items():
            keybinding_buttons.append({
                "action": action,
                "key": key,
                "rect": pygame.Rect(self.screen.get_width() * 0.5 - self.keybinding_width * 0.5, y_offset,
                                    self.keybinding_width, self.keybinding_height)
            })
            y_offset += self.keybinding_height + 10

        return keybinding_buttons

    def draw(self):
        self.screen.fill((30, 30, 30))

        title_text = self.font.render("Управление", True, (255, 255, 255))
        self.screen.blit(title_text,
                         (self.screen.get_width() * 0.5 - title_text.get_width() * 0.5, self.screen.get_height() * 0.1))

        for button in self.keybinding_buttons:
            action_text = self.font.render(f"{button['action']}: {button['key']}", True, (255, 255, 255))
            self.screen.blit(action_text, (button['rect'].x + 10, button['rect'].y + 10))
            pygame.draw.rect(self.screen, (255, 255, 255), button['rect'], 2)

        pygame.draw.rect(self.screen, (255, 255, 255), self.back_button)
        back_text = self.font.render("Назад", True, (0, 0, 0))
        self.screen.blit(back_text,
                         (self.screen.get_width() * 0.5 - back_text.get_width() * 0.5, self.screen.get_height() * 0.9))

    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            if self.back_button.collidepoint(event.pos):
                return "back"  # Возвращаемся обратно в меню настроек

            # Обработка изменения клавиши
            if self.selected_key is not None:
                key_action = self.keybinding_buttons[self.selected_key]["action"]
                self.change_keybinding(key_action)

        if event.type == pygame.MOUSEMOTION:
            mouse_x, mouse_y = event.pos
            self.selected_key = None
            for i, button in enumerate(self.keybinding_buttons):
                if button['rect'].collidepoint(mouse_x, mouse_y):
                    self.selected_key = i
                    break

        return True

    def change_keybinding(self, action):
        new_key = self.get_new_key_for_action(action)
        if new_key:
            self.settings["KEYBINDS"][action] = new_key
            self.keybinding_buttons = self.create_keybinding_buttons()

    def get_new_key_for_action(self, action):
        input_active = True
        new_key = None

        prompt_text = self.font.render(f"Нажмите новую клавишу для {action}", True, (255, 255, 255))
        self.screen.blit(prompt_text, (
        self.screen.get_width() * 0.5 - prompt_text.get_width() * 0.5, self.screen.get_height() * 0.5))

        pygame.display.flip()

        while input_active:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    new_key = pygame.key.name(event.key)
                    input_active = False
                    break
                if event.type == pygame.QUIT:
                    pygame.quit()

        return new_key
