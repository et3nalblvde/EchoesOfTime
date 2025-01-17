import pygame
import os
import re

# Инициализация Pygame
pygame.init()

# Параметры окна
window_width = 800
window_height = 600
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('Эхо Анимация')

# Путь к папке со спрайтами
sprite_folder = r'C:\Users\aroki\PycharmProjects\EchoesOfTime\assets\sprites\shadows'


# Функция для извлечения числовой части из имени файла
def extract_number(filename):
    match = re.search(r'(\d+)', filename)  # Ищем числа в имени файла
    return int(match.group(1)) if match else -1  # Возвращаем число или -1, если чисел нет


# Функция для создания эффекта тени
def create_echo(sprite, shadow_intensity=100):
    # Создаём поверхностный объект с тем же размером
    shadow = pygame.Surface(sprite.get_size(), pygame.SRCALPHA)

    # Закрашиваем тень в полупрозрачный серый
    shadow.fill((0, 0, 0, shadow_intensity))  # Чёрный цвет с прозрачностью

    # Накладываем тень на оригинальный спрайт
    shadow.blit(sprite, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

    return shadow


# Загружаем файлы для различных анимаций
animations = {
    "idle": sorted(
        [f for f in os.listdir(os.path.join(sprite_folder, "idle")) if f.endswith(('.png', '.jpg', '.jpeg'))],
        key=extract_number),
    "run": sorted([f for f in os.listdir(os.path.join(sprite_folder, "run")) if f.endswith(('.png', '.jpg', '.jpeg'))],
                  key=extract_number),
    "jump": sorted(
        [f for f in os.listdir(os.path.join(sprite_folder, "jump")) if f.endswith(('.png', '.jpg', '.jpeg'))],
        key=extract_number),
    "fall": sorted(
        [f for f in os.listdir(os.path.join(sprite_folder, "fall")) if f.endswith(('.png', '.jpg', '.jpeg'))],
        key=extract_number),
    "death": sorted(
        [f for f in os.listdir(os.path.join(sprite_folder, "death")) if f.endswith(('.png', '.jpg', '.jpeg'))],
        key=extract_number)
}

# Создаем список анимаций и анимаций с эхо
animation_frames = {}
animation_echo_frames = {}

# Загружаем изображения из отсортированных файлов и создаём тени для них
for anim in animations:
    animation_frames[anim] = [pygame.image.load(os.path.join(sprite_folder, anim, file)) for file in animations[anim]]
    animation_echo_frames[anim] = [create_echo(frame) for frame in animation_frames[anim]]

# Параметры анимации
frame_rate = 10  # Частота кадров
clock = pygame.time.Clock()

# Начальное состояние
current_state = "idle"
current_frame = 0

# Основной цикл игры
running = True
while running:
    window.fill((255, 255, 255))  # Заполняем фон белым цветом

    # Обрабатываем события
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            # Меняем анимацию в зависимости от нажатой клавиши
            if event.key == pygame.K_SPACE:  # Прыжок
                current_state = "jump"
                current_frame = 0  # Сброс кадра
            elif event.key == pygame.K_DOWN:  # Падение
                if animation_frames["fall"]:  # Проверяем, что анимация падения существует
                    current_state = "fall"
                    current_frame = 0  # Сброс кадра
            elif event.key == pygame.K_UP:  # Смерть
                if animation_frames["death"]:  # Проверяем, что анимация смерти существует
                    current_state = "death"
                    current_frame = 0  # Сброс кадра
            elif event.key == pygame.K_RIGHT:  # Бег
                current_state = "run"
                current_frame = 0  # Сброс кадра
            elif event.key == pygame.K_LEFT:  # Стояние
                current_state = "idle"
                current_frame = 0  # Сброс кадра

    # Проверяем, что у нас есть кадры для текущего состояния
    if animation_frames.get(current_state):
        # Отображаем текущий спрайт
        window.blit(animation_frames[current_state][current_frame], (
        window_width // 2 - animation_frames[current_state][current_frame].get_width() // 2,
        window_height // 2 - animation_frames[current_state][current_frame].get_height() // 2))

        # Отображаем "эхо"
        window.blit(animation_echo_frames[current_state][current_frame], (
        window_width // 2 - animation_echo_frames[current_state][current_frame].get_width() // 2 + 10,
        window_height // 2 - animation_echo_frames[current_state][
            current_frame].get_height() // 2 + 10))  # Легкий сдвиг тени

        # Переход к следующему кадру для текущей анимации
        current_frame = (current_frame + 1) % len(animation_frames[current_state])

    # Обновляем экран
    pygame.display.update()

    # Устанавливаем частоту кадров
    clock.tick(frame_rate)

# Закрытие Pygame
pygame.quit()
