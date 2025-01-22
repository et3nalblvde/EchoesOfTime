import pygame
import os
from PIL import Image
import time


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.join(BASE_DIR, '..')
ASSETS_DIR = os.path.join(PROJECT_DIR, 'assets')
FONTS_DIR = os.path.join(ASSETS_DIR, 'fonts')
FONT_PATH = os.path.join(FONTS_DIR, 'PressStart2P.ttf')

class GameOverScreen:
    def __init__(self, screen, restart_game, exit_to_main_menu):
        self.screen = screen
        self.restart_game = restart_game
        self.exit_to_main_menu = exit_to_main_menu

        self.screen_width, self.screen_height = screen.get_size()

        
        self.font = pygame.font.Font(FONT_PATH, 74)
        self.small_font = pygame.font.Font(FONT_PATH, 36)
        self.text_color = (255, 255, 255)

        self.overlay_color = (0, 0, 0, 180)

        
        self.background_gif_path = os.path.join(ASSETS_DIR, 'sprites', 'background', 'background.gif')  
        self.background_image = Image.open(self.background_gif_path)
        self.background_frames = []
        for frame in range(self.background_image.n_frames):
            self.background_image.seek(frame)
            frame_data = pygame.image.fromstring(self.background_image.convert("RGBA").tobytes(), self.background_image.size, "RGBA")
            self.background_frames.append(frame_data)

        self.frame_count = len(self.background_frames)
        self.last_frame_time = time.time()  
        self.frame_delay = 0.2  
        self.frame_counter = 0

        self.setup_buttons()

    def setup_buttons(self):
        self.restart_button = pygame.Rect(self.screen_width // 3, self.screen_height // 2, self.screen_width // 3, 50)
        self.exit_button = pygame.Rect(self.screen_width // 3, self.screen_height // 2 + 70, self.screen_width // 3, 50)

    def draw(self):
        
        current_time = time.time()
        if current_time - self.last_frame_time >= self.frame_delay:
            self.frame_counter = (self.frame_counter + 1) % self.frame_count  
            self.last_frame_time = current_time  

        
        current_frame = self.frame_counter
        background_resized = pygame.transform.scale(self.background_frames[current_frame], (self.screen_width, self.screen_height))
        self.screen.blit(background_resized, (0, 0))

        
        text = self.font.render("Вы погибли", True, self.text_color)
        text_rect = text.get_rect(center=(self.screen_width // 2, self.screen_height // 4))
        self.screen.blit(text, text_rect)

        
        pygame.draw.rect(self.screen, (255, 0, 0), self.restart_button, 2)  
        pygame.draw.rect(self.screen, (255, 0, 0), self.exit_button, 2)  

        restart_text = self.small_font.render("Начать заново", True, self.text_color)
        exit_text = self.small_font.render("В главное меню", True, self.text_color)

        restart_text_rect = restart_text.get_rect(center=self.restart_button.center)
        exit_text_rect = exit_text.get_rect(center=self.exit_button.center)

        self.screen.blit(restart_text, restart_text_rect)
        self.screen.blit(exit_text, exit_text_rect)

    def handle_events(self, event):
        from main_menu import main_menu
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.restart_button.collidepoint(event.pos):
                self.restart_game()
            elif self.exit_button.collidepoint(event.pos):
                main_menu(self.screen)