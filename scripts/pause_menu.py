import pygame
import os
  


pygame.init()
pygame.font.init()  


WHITE = (255, 255, 255)
BUTTON_COLOR = (100, 100, 255)  
HOVER_COLOR = (150, 150, 255)


BASE_FOLDER = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_FOLDER, '..', 'assets')  


class PauseMenu:
    def __init__(self, screen):
        self.screen = screen
        font_path = os.path.join(BASE_FOLDER, '..', 'fonts', 'PressStart2P.ttf')  
        self.font = pygame.font.Font(font_path, 30)  
        self.buttons = []
        self.create_buttons()

        
        self.background_gif_path = os.path.join(ASSETS_DIR, 'sprites', 'background', 'background.gif')
        self.frames = self.load_gif_frames(self.background_gif_path)
        self.current_frame = 0
        self.frame_delay = 100

    def create_buttons(self):
        
        button_width, button_height = 200, 50
        screen_width, screen_height = self.screen.get_size()

        
        continue_button = pygame.Rect(screen_width // 2 - button_width // 2, screen_height // 2 - 50, button_width,
                                      button_height)
        quit_button = pygame.Rect(screen_width // 2 - button_width // 2, screen_height // 2 + 50, button_width,
                                  button_height)
        self.buttons = [(continue_button, "Продолжить"), (quit_button, "Выйти")]

    def load_gif_frames(self, gif_path):
        
        try:
            gif = pygame.image.load(gif_path)
            frames = []
            width, height = gif.get_width(), gif.get_height()
            num_frames = gif.get_width() // width
            for i in range(num_frames):
                frame = gif.subsurface(i * width, 0, width, height)
                frames.append(frame)
            return frames
        except pygame.error:
            print(f"Не удалось загрузить GIF: {gif_path}")
            return []

    def draw(self):
        
        self.screen.blit(pygame.transform.scale(self.frames[self.current_frame], self.screen.get_size()), (0, 0))

        
        self.current_frame += 1
        if self.current_frame >= len(self.frames):
            self.current_frame = 0
        pygame.time.wait(self.frame_delay)  

        
        for button, text in self.buttons:
            text_surface = self.font.render(text, True, WHITE)
            self.screen.blit(text_surface, (button.x + (button.width - text_surface.get_width()) // 2,
                                            button.y + (button.height - text_surface.get_height()) // 2))
        pygame.display.flip()

    def handle_events(self, event):
        from main_menu import main_menu
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                pos = pygame.mouse.get_pos()
                for button, text in self.buttons:
                    if button.collidepoint(pos):
                        if text == "Продолжить":
                            return "continue"
                        elif text == "Выйти":
                            global show_confirmation_menu
                            show_confirmation_menu = False  # Сбрасываем флаг окна подтверждения
                            main_menu(self.screen)
                            return "quit"
        return None
