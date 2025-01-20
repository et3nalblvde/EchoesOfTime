import pygame
import sys

class GameOverScreen:
    def __init__(self, screen, restart_game, exit_to_main_menu):
        self.screen = screen
        self.restart_game = restart_game
        self.exit_to_main_menu = exit_to_main_menu

        self.screen_width, self.screen_height = screen.get_size()
        self.font = pygame.font.Font(None, 74)
        self.small_font = pygame.font.Font(None, 36)
        self.text_color = (255, 255, 255)
        self.overlay_color = (0, 0, 0, 180)

        self.setup_buttons()

    def setup_buttons(self):
        self.restart_button = pygame.Rect(self.screen_width // 3, self.screen_height // 2, self.screen_width // 3, 50)
        self.exit_button = pygame.Rect(self.screen_width // 3, self.screen_height // 2 + 70, self.screen_width // 3, 50)

    def draw(self):
        overlay = pygame.Surface((self.screen_width, self.screen_height))
        self.screen.blit(overlay, (0, 0))

        text = self.font.render("Вы погибли", True, self.text_color)
        text_rect = text.get_rect(center=(self.screen_width // 2, self.screen_height // 4))
        self.screen.blit(text, text_rect)

        pygame.draw.rect(self.screen, (255, 0, 0), self.restart_button)
        pygame.draw.rect(self.screen, (255, 0, 0), self.exit_button)

        restart_text = self.small_font.render("Начать заново", True, (255, 255, 255))
        exit_text = self.small_font.render("В главное меню", True, (255, 255, 255))

        restart_text_rect = restart_text.get_rect(center=self.restart_button.center)
        exit_text_rect = exit_text.get_rect(center=self.exit_button.center)

        self.screen.blit(restart_text, restart_text_rect)
        self.screen.blit(exit_text, exit_text_rect)

    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.restart_button.collidepoint(event.pos):
                self.restart_game()
            elif self.exit_button.collidepoint(event.pos):
                self.exit_to_main_menu()
