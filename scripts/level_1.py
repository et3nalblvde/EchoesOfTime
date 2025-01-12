import pygame
import sys
from scripts.echo import EchoManager

pygame.init()

# Инициализация игры
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60
BACKGROUND_COLOR = (50, 50, 80)  # Темный фон для атмосферы

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Эхо — Первый уровень")
clock = pygame.time.Clock()

# Игровые объекты
player_size = 40
player_color = (255, 200, 0)
button_color = (100, 200, 100)
door_color = (150, 50, 50)
wall_color = (100, 100, 100)
platform_color = (150, 150, 150)

# Переменные для игрока
player = pygame.Rect(200, SCREEN_HEIGHT - 100, player_size, player_size)
player_velocity = [0, 0]
gravity = 0.5
jump_strength = -12
speed = 5
on_ground = False

# Кнопка, дверь, платформа и стены
button = pygame.Rect(400, SCREEN_HEIGHT - 70, 50, 20)
door = pygame.Rect(1000, SCREEN_HEIGHT - 200, 100, 200)
platform = pygame.Rect(600, SCREEN_HEIGHT - 300, 200, 20)

# Стены
left_wall = pygame.Rect(0, 0, 50, SCREEN_HEIGHT)
right_wall = pygame.Rect(SCREEN_WIDTH - 50, 0, 50, SCREEN_HEIGHT)

# Модели эха
echo_manager = EchoManager()

# Обработка событий игрока
keys = {
    "left": False,
    "right": False,
    "jump": False,
    "echo": False,
}

# Флаги
control_echo = False  # Флаг, кто управляет, изначально игрок
is_echo_recording = False  # Флаг для записи эхо

# Функции для отрисовки
def draw_level():
    screen.fill(BACKGROUND_COLOR)

    # Отрисовка стен
    pygame.draw.rect(screen, wall_color, left_wall)
    pygame.draw.rect(screen, wall_color, right_wall)

    # Отрисовка кнопки
    pygame.draw.rect(screen, button_color, button)

    # Отрисовка двери
    if not door_open:
        pygame.draw.rect(screen, door_color, door)

    # Отрисовка платформы
    pygame.draw.rect(screen, platform_color, platform)

    # Отрисовка игрока
    pygame.draw.rect(screen, player_color, player)

    # Отрисовка "Эхо"
    echo_manager.draw(screen)


def handle_collisions():
    global on_ground, door_open

    # Гравитация и платформа
    on_ground = False
    if player.colliderect(platform) and player_velocity[1] > 0:
        player.bottom = platform.top
        player_velocity[1] = 0
        on_ground = True

    # Пол
    if player.bottom >= SCREEN_HEIGHT:
        player.bottom = SCREEN_HEIGHT
        player_velocity[1] = 0
        on_ground = True

    # Кнопка
    if player.colliderect(button):
        door_open = True

    # Стены
    if player.colliderect(left_wall) or player.colliderect(right_wall):
        if player_velocity[0] < 0:  # Столкновение с левой стеной
            player.left = left_wall.right
        if player_velocity[0] > 0:  # Столкновение с правой стеной
            player.right = right_wall.left


def handle_input():
    global control_echo

    if control_echo and echo_manager.echo:  # Проверка, что эхо существует
        # Управление эхо (оно повторяет движения игрока)
        if keys["left"]:
            echo_manager.echo.rect.x -= speed
        if keys["right"]:
            echo_manager.echo.rect.x += speed
        if keys["jump"] and on_ground:
            echo_manager.echo.rect.y += jump_strength
    else:
        # Управление игроком
        player_velocity[0] = 0
        if keys["left"]:
            player_velocity[0] = -speed
        if keys["right"]:
            player_velocity[0] = speed
        if keys["jump"] and on_ground:
            player_velocity[1] = jump_strength


def main(screen):
    global keys, door_open  # Объявляем переменную door_open глобальной, если она должна быть доступна в других функциях
    global control_echo, is_echo_recording  # Объявляем переменные глобальными

    # Инициализация переменной door_open
    door_open = False  # Устанавливаем начальное значение как False

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
                if event.key == pygame.K_e:  # Клавиша для переключения между игроком и эхо
                    control_echo = not control_echo  # Переключаем управление

                    if control_echo:  # Если переключили на эхо, начинаем запись
                        if not is_echo_recording:
                            echo_manager.record(player)  # Начать запись
                            is_echo_recording = True
                    else:  # Если возвращаемся к игроку, останавливаем запись
                        if is_echo_recording:
                            echo_manager.stop_recording()  # Завершаем запись
                            is_echo_recording = False

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    keys["left"] = False
                if event.key == pygame.K_RIGHT:
                    keys["right"] = False
                if event.key == pygame.K_SPACE:
                    keys["jump"] = False

        # Управление игроком или эхо
        handle_input()

        # Обновление позиции игрока
        player_velocity[1] += gravity
        if not control_echo:
            player.x += player_velocity[0]
            player.y += player_velocity[1]

        # Обновление "Эхо"
        echo_manager.update()

        # Проверка коллизий
        handle_collisions()

        # Открытие двери
        if door_open:
            door_color = (100, 200, 100)

        # Отрисовка уровня
        draw_level()

        # Обновление экрана
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main(screen)
