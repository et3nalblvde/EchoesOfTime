import pygame
from scripts.settings import load_settings
from main_menu import main_menu
from settings import *

settings = load_settings()
pygame.init()
SCREEN_WIDTH = settings["SCREEN_WIDTH"]
SCREEN_HEIGHT = settings["SCREEN_HEIGHT"]
FPS = settings["FPS"]
BACKGROUND_COLOR = settings["BACKGROUND_COLOR"]
MUSIC_VOLUME = settings["MUSIC_VOLUME"]
SFX_VOLUME = settings["SFX_VOLUME"]
pygame.mixer.music.set_volume(MUSIC_VOLUME)
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("Echoes Of time")


def main():
    main_menu(screen)



if __name__ == "__main__":
    main()
