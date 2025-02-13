import pygame
import os
from PIL import Image
from scripts.settings import load_settings
from level_2 import start_level_2
from level_3 import start_level_3
pygame.init()

class CongratulationsScreen:
    def __init__(self, screen, exit_to_main_menu):
        
        self.settings = load_settings()
        self.SCREEN_WIDTH = self.settings["SCREEN_WIDTH"]
        self.SCREEN_HEIGHT = self.settings["SCREEN_HEIGHT"]
        self.FPS = self.settings["FPS"]
        self.exit_to_main_menu = exit_to_main_menu  
        
        self.BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        self.PROJECT_DIR = os.path.join(self.BASE_DIR, '..')
        self.ASSETS_DIR = os.path.join(self.PROJECT_DIR, 'assets')
        self.FONTS_DIR = os.path.join(self.ASSETS_DIR, 'fonts')
        self.FONT_PATH = os.path.join(self.FONTS_DIR, 'PressStart2P.ttf')

        
        self.base_font_size = 30
        self.font = pygame.font.Font(self.FONT_PATH, self.base_font_size)

        
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.SCREEN_WIDTH, self.SCREEN_HEIGHT = self.screen.get_size()  
        pygame.display.set_caption("Поздравление")

        
        background_gif_path = os.path.join(self.ASSETS_DIR, 'sprites', 'background', 'background.gif')
        self.background_image = Image.open(background_gif_path)

        
        self.background_frames = []
        for frame in range(self.background_image.n_frames):
            self.background_image.seek(frame)
            frame_data = pygame.image.frombuffer(self.background_image.convert("RGBA").tobytes(), self.background_image.size, "RGBA")
            self.background_frames.append(frame_data)
        self.frame_count = len(self.background_frames)

        
        self.running = True
        self.next_level_button = None
        self.main_menu_button = None
        self.update_button_positions()

    def draw_button(self, surface, button, text, is_hovered):
        
        color = (255, 255, 0) if is_hovered else (255, 255, 255)
        pygame.draw.rect(surface, color, button, 3)
        text_surface = self.font.render(text, True, color)
        surface.blit(text_surface, (
            button.centerx - text_surface.get_width() // 2,
            button.centery - text_surface.get_height() // 2
        ))

    def draw_congratulations(self, screen, current_frame):
        
        frame_width, frame_height = self.background_frames[current_frame].get_size()

        
        background_resized = pygame.transform.scale(self.background_frames[current_frame],
                                                    (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        screen.blit(background_resized, (0, 0))

        
        text_surface = self.font.render("Поздравляем!", True, (255, 255, 255))
        screen.blit(text_surface, (
            self.SCREEN_WIDTH // 2 - text_surface.get_width() // 2,
            self.SCREEN_HEIGHT // 4
        ))

    def update_button_positions(self):
        
        button_width = self.SCREEN_WIDTH // 3
        button_height = self.SCREEN_HEIGHT // 10

        center_x = self.SCREEN_WIDTH // 2
        center_y = self.SCREEN_HEIGHT // 2
        button_spacing = button_height // 2

        
        self.next_level_button = pygame.Rect(
            center_x - button_width // 2,
            center_y - button_height - button_spacing,
            button_width, button_height
        )
        self.main_menu_button = pygame.Rect(
            center_x - button_width // 2,
            center_y + button_spacing,
            button_width, button_height
        )

    def handle_events(self, event):
        from main_menu import main_menu
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.next_level_button.collidepoint(event.pos):
                print("Next level button clicked")
                return "next_level"
            elif self.main_menu_button.collidepoint(event.pos):
                print("Main menu button clicked")
                return "main_menu"
        return None

    def congratulations_screen(self):
        clock = pygame.time.Clock()
        current_frame = 0
        frame_delay = 2
        frame_counter = 0

        while self.running:
            for event in pygame.event.get():
                action = self.handle_events(event)
                if action == "next_level":
                    print("Starting level 2...")
                    pygame.init()
                    self.running = False
                    start_level_2(self.screen, self.exit_to_main_menu, self.exit_to_main_menu)
                elif action == "main_menu":
                    print("Returning to main menu...")
                    self.running = False
                    self.exit_to_main_menu()


            if frame_counter >= frame_delay:
                current_frame = (current_frame + 1) % self.frame_count
                frame_counter = 0
            else:
                frame_counter += 1

            self.draw_congratulations(self.screen, current_frame)
            mouse_x, mouse_y = pygame.mouse.get_pos()
            is_next_hovered = self.next_level_button.collidepoint(mouse_x, mouse_y)
            is_main_menu_hovered = self.main_menu_button.collidepoint(mouse_x, mouse_y)
            self.draw_button(self.screen, self.next_level_button, "Следующий уровень", is_next_hovered)
            self.draw_button(self.screen, self.main_menu_button, "Главное меню", is_main_menu_hovered)

            pygame.display.flip()
            clock.tick(self.FPS)
