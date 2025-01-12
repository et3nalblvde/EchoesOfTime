import pygame


class Echo:
    """
    Класс Echo представляет одного "двойника" игрока.
    Он содержит траекторию движений и воспроизводит их с задержкой.
    """

    def __init__(self, trail, color=(200, 200, 200), size=40):
        self.trail = trail  # Список позиций, которые должен повторять "эхо"
        self.index = 0  # Текущая позиция в списке
        self.color = color
        self.size = size
        self.rect = pygame.Rect(0, 0, self.size, self.size)

    def update(self):
        """Обновляет положение 'эхо' в соответствии с текущей позицией в траектории."""
        if self.index < len(self.trail):
            self.rect.topleft = self.trail[self.index]
            self.index += 1

    def draw(self, screen):
        """Отрисовывает 'эхо' на экране."""
        pygame.draw.rect(screen, self.color, self.rect)


class EchoManager:
    """
    Класс EchoManager управляет одним "эхо" в игре.
    """

    def __init__(self, delay=60):
        self.echo = None  # Один объект "эхо"
        self.trail = []  # Временное хранилище для записи движений игрока
        self.recording = False  # Флаг записи
        self.delay = delay  # Задержка перед запуском "эхо"

    def record(self, player):
        """
        Начинает или продолжает запись пути игрока.
        :param player: объект pygame.Rect, представляющий игрока
        """
        if not self.recording:
            self.recording = True
            self.trail = []  # Очистка предыдущей записи

        # Добавляем текущую позицию игрока в траекторию
        self.trail.append(player.topleft)

    def stop_recording(self):
        """
        Завершает запись и создает новое "эхо", если траектория не пуста.
        """
        if self.recording:
            self.recording = False
            if len(self.trail) > 0:
                # Если эхо уже существует, заменяем его новым
                self.echo = Echo(self.trail)  # Создаем новое эхо
                self.trail = []  # Очищаем траекторию, так как эхо создано

    def update(self):
        """Обновляет текущее 'эхо'."""
        if self.echo:
            self.echo.update()

    def draw(self, screen):
        """Отрисовывает текущее 'эхо'."""
        if self.echo:
            self.echo.draw(screen)


def main(screen):
    # Переменные игрока
    player_size = 40
    player_color = (255, 200, 0)
    player = pygame.Rect(200, 500, player_size, player_size)
    player_velocity = [0, 0]
    gravity = 0.5
    jump_strength = -12
    speed = 5
    on_ground = False

    # Флаги управления
    keys = {
        "left": False,
        "right": False,
        "jump": False,
        "echo": False,
    }

    # Переключение управления (игрок или эхо)
    control_echo = False  # Изначально управляем игроком

    # Объект EchoManager
    echo_manager = EchoManager()

    running = True
    while running:
        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    keys["left"] = True
                if event.key == pygame.K_RIGHT:
                    keys["right"] = True
                if event.key == pygame.K_SPACE:
                    keys["jump"] = True
                if event.key == pygame.K_e:  # Переключение управления между игроком и эхо
                    if control_echo:
                        control_echo = False  # Управление возвращается игроку
                    else:
                        control_echo = True  # Управление переходит к эхо

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    keys["left"] = False
                if event.key == pygame.K_RIGHT:
                    keys["right"] = False
                if event.key == pygame.K_SPACE:
                    keys["jump"] = False

        # Управление игроком или эхо
        if not control_echo:
            # Управляем игроком
            player_velocity[0] = 0
            if keys["left"]:
                player_velocity[0] = -speed
            if keys["right"]:
                player_velocity[0] = speed
            if keys["jump"] and on_ground:
                player_velocity[1] = jump_strength

            # Обновление позиции игрока
            player_velocity[1] += gravity
            player.x += player_velocity[0]
            player.y += player_velocity[1]

            # Запись движений игрока для эхо
            if keys["echo"]:
                echo_manager.record(player)
            echo_manager.update()

        else:
            # Управляем эхо (по сути, просто следим за его движением)
            echo_manager.update()

        # Проверка на землю
        if player.bottom >= 600:
            player.bottom = 600
            player_velocity[1] = 0
            on_ground = True

        # Отрисовка
        screen.fill((0, 0, 0))  # Очистка экрана
        pygame.draw.rect(screen, player_color, player)  # Отрисовка игрока
        echo_manager.draw(screen)  # Отрисовка эхо

        # Обновление экрана
        pygame.display.flip()
        pygame.time.Clock().tick(60)

    pygame.quit()


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    main(screen)
