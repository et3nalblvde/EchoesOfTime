import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.join(BASE_DIR, '..')
ASSETS_DIR = os.path.join(PROJECT_DIR, 'assets')
FONTS_DIR = os.path.join(ASSETS_DIR, 'fonts')
SETTINGS_FILE = os.path.join(PROJECT_DIR, 'save', 'settings.json')


def load_settings():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r") as file:
            settings = json.load(file)
            return settings
    else:
        return {
            "SCREEN_WIDTH": 1024,
            "SCREEN_HEIGHT": 768,
            "FPS": 60,
            "BACKGROUND_COLOR": [0, 0, 0],
            "MUSIC_VOLUME": 0.5,
            "SFX_VOLUME": 0.7,
            "ECHO_DELAY": 2,
            "ECHO_OPACITY": 100
        }


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
import pygame


class SettingsMenu:
    def __init__(self, screen, settings):
        self.screen = screen
        self.settings = settings
        self.font = pygame.font.Font(None, 50)
        self.back_button = pygame.Rect(self.settings["SCREEN_WIDTH"] // 2 - 100,
                                       self.settings["SCREEN_HEIGHT"] // 2 + 50, 200, 50)

    def draw(self):
        self.screen.fill((0, 0, 0))
        pygame.draw.rect(self.screen, (255, 255, 255), self.back_button)
        back_text = self.font.render("Назад", True, (0, 0, 0))
        self.screen.blit(back_text, (
            self.settings["SCREEN_WIDTH"] // 2 - back_text.get_width() // 2, self.settings["SCREEN_HEIGHT"] // 2 + 55))

    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.back_button.collidepoint(event.pos):
                return False
        return True
