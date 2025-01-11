import pygame


class UI:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont("Arial", 24)
        self.score = 0
        self.game_over_text = None
        self.game_over_rect = None

    def update(self):
        pass

    def draw(self):
        score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))
        if self.game_over_text:
            self.screen.blit(self.game_over_text, self.game_over_rect)

    def set_game_over(self):
        self.game_over_text = self.font.render("Game Over", True, (255, 0, 0))
        self.game_over_rect = self.game_over_text.get_rect(
            center=(self.screen.get_width() // 2, self.screen.get_height() // 2))

    def increase_score(self, points):
        self.score += points
