import pygame
import os


class CreditsScreen:
    def __init__(self, screen):
        self.screen = screen
        font_path = os.path.join(os.path.dirname(__file__), "..", "fonts", "PressStart2P.ttf")
        if not os.path.exists(font_path):
            raise FileNotFoundError(f"Шрифт {font_path} не найден. Убедитесь, что файл существует.")
        self.font = pygame.font.Font(font_path, 36)

        self.text_color = (255, 255, 255)
        self.background_color = (0, 0, 0)
        self.credits_text = [
            "Благодарим вас за участие в нашем проекте!",
            "",
            "Мы вложили в него душу и страсть, ",
            "",
            "и надеемся",
            "",
            "что он подарил вам незабываемые эмоции.",
            "",
            "Команда разработчиков:",
            "",
            "Николай \"Revolvotron\" Бонадренко",
            "",
            "Создание механик и настройка игрового процесса",
            "",
            "Григорий \"et3nalblvde\" Матыскин",
            "",
            "Программирование и оптимизация кода",
            "",
            "Всеволод \"Thisskrembl\" Пьянов",
            "",
            "Дизайн уровней и художественное оформление",
            "",
            "Наш проект на GitHub:",
            "",
            "https://github.com/et3nalblvde/EchoesOfTime",
            "",
            "Если у вас есть идеи, пожелания или отзывы,",
            "",
            "будем рады услышать вас:",
            "",
            "",
            "anemokapibara@yandex.ru",
            "",
            "Каждое ваше мнение для нас бесценно.",
            "",
            "До новых встреч в мире будущих приключений!",
            "",
            "Помните:",
            "",
            "Мир игры существует",
            "",
            "",
            "",
            "Пока вы в него верите..."
        ]

        self.scroll_speed = 1
        self.y_offset = screen.get_height()

    def draw(self):
        self.screen.fill(self.background_color)
        y_offset = self.y_offset
        for line in self.credits_text:
            text_surface = self.font.render(line, True, self.text_color)
            text_rect = text_surface.get_rect(center=(self.screen.get_width() // 2, y_offset))
            self.screen.blit(text_surface, text_rect)
            y_offset += 40

        pygame.display.flip()

    def run(self):
        clock = pygame.time.Clock()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        return

            self.draw()
            self.y_offset -= self.scroll_speed

            if self.y_offset < -len(self.credits_text) * 40:
                running = False

            clock.tick(60)
