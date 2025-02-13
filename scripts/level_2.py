import pygame
import os
from game_over import GameOverScreen
from player import Player
from health import Health
from collision import CollisionLevel2
from pause_menu import PauseMenu
from bat import Bat
from settings import load_sounds, load_settings
from shadow import Shadow
from trap import NeedleTrap, SpittingHead  # Импортируем SpittingHead
from Door import Door  # Импортируем Door
from lever import Lever  # Импортируем Lever
import time
WHITE = (255, 255, 255)
from level_3 import start_level_3
settings = load_settings()
MUSIC_VOLUME = settings["MUSIC_VOLUME"]
SFX_VOLUME = settings["SFX_VOLUME"]

pygame.mixer.music.set_volume(MUSIC_VOLUME)

base_folder = os.path.dirname(os.path.abspath(__file__))
level_2_image_path = os.path.join(base_folder, '..', 'assets', 'sprites', 'maps', 'level_2.png')
level_2_image = pygame.image.load(level_2_image_path)


def scale_background(screen):
    screen_width, screen_height = screen.get_size()
    return pygame.transform.scale(level_2_image, (screen_width, screen_height))


def draw_background(screen):
    scaled_background = scale_background(screen).convert()
    screen.blit(scaled_background, (0, 0))


def start_level_2(screen, exit_to_main_menu, restart_main_menu):


    from level_complete import CongratulationsScreen
    player_sounds = load_sounds(SFX_VOLUME)
    player = Player(2314, 192, player_sounds, 2)
    shadow = Shadow(1576, 832, 2)
    health = Health(max_health=3, x=10, y=10, player=player)
    all_sprites = pygame.sprite.Group()
    spitting_heads = pygame.sprite.Group()  # Новая группа для SpittingHead
    all_sprites.add(player)
    all_sprites.add(shadow)

    # Создаем экземпляры NeedleTrap и SpittingHead
    needle1 = NeedleTrap(724, 906, 64, 64)
    needle2 = NeedleTrap(747, 747, 64, 64)
    spitting_head1 = SpittingHead(2516, 904, 64, 64)  # Позиция SpittingHead на уровне
    spitting_head2 = SpittingHead(2552, 907, 64, 64)  # Позиция SpittingHead на уровне

    # Добавляем их в группу спрайтов
    all_sprites.add(needle1, needle2)
    spitting_heads.add(spitting_head1, spitting_head2)  # Добавляем в новую группу

    # Анимация двери и система рычагов
    door_x, door_y = 2398, 65
    sprites_path = os.path.join(base_folder, '..', 'assets', 'sprites', 'doors')
    door = Door(door_x, door_y, sprites_path, frame_count=6)
    lever_1_x, lever_1_y = 1576, 892
    lever_2_x, lever_2_y = 2023, 123
    lever_sprites_path = os.path.join(base_folder, '..', 'assets', 'sprites', 'levers')
    lever_1 = Lever(lever_1_x, lever_1_y, lever_sprites_path, frame_count=5)
    lever_2 = Lever(lever_2_x, lever_2_y, lever_sprites_path, frame_count=5)
    all_sprites.add(door)
    all_sprites.add(lever_1)
    all_sprites.add(lever_2)

    bats = pygame.sprite.Group()
    bat1 = Bat(1553, 26, 2015, 26)
    bat2 = Bat(439, 889, 1172, 885)
    bats.add(bat1, bat2)
    all_sprites.add(bat1, bat2)

    collision = CollisionLevel2()

    clock = pygame.time.Clock()
    running = True
    is_paused = False
    control_shadow = False
    lever_1_raised = False
    lever_2_raised = False
    lever_activation_time = None
    lever_activation_timeout = 2

    pause_menu = PauseMenu(screen)

    while running:
        dt = clock.get_time() / 1000  # delta time
        current_time = pygame.time.get_ticks()  # Текущее время

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    is_paused = not is_paused
                    pause_menu.draw()
                elif event.key == pygame.K_e:
                    control_shadow = not control_shadow

            if is_paused:
                result = pause_menu.handle_events(event)
                if result == "quit":
                    exit_to_main_menu()
                if result == "continue":
                    is_paused = False
                continue

        if is_paused:
            continue

        draw_background(screen)
        keys = pygame.key.get_pressed()
        controlled_character = shadow if control_shadow else player

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            controlled_character.move_left()
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            controlled_character.move_right()
        else:
            controlled_character.stop()
        if keys[pygame.K_SPACE]:
            controlled_character.jump()
        if keys[pygame.K_f] and not control_shadow:
            player.attack(bats)

        if not health.is_alive():
            game_over_screen = GameOverScreen(
                screen,
                lambda: start_level_2(screen, restart_main_menu, exit_to_main_menu),
                exit_to_main_menu
            )
            game_over_screen_loop(game_over_screen)
            running = False

        collision.check_ladder_collision(player)
        collision.check_platform_collision(player)
        collision.check_wall_collision(player)
        collision.check_box_collision(player)
        collision.check_ladder_collision(shadow)
        collision.check_platform_collision(shadow)
        collision.check_wall_collision(shadow)
        collision.check_box_collision(shadow)
        collision.draw_collision_debug(screen)

        # Обновление анимации иголок
        needle1.update(dt)
        needle2.update(dt)
        all_sprites.update(dt)
        all_sprites.draw(screen)

        # Обновление и рисование SpittingHead отдельно
        spitting_heads.update(dt, current_time)
        spitting_heads.draw(screen)

        for spitting_head in spitting_heads:
            spitting_head.draw_fireballs(screen)

        # Система рычагов и анимация двери
        if control_shadow:
            if lever_1.rect.colliderect(shadow.rect.inflate(30, 30)) and keys[pygame.K_g] and not lever_1_raised:
                lever_1.activate()
                lever_1_raised = True
                print("lever_1_raised =", lever_1_raised)

            if lever_2.rect.colliderect(shadow.rect.inflate(30, 30)) and keys[pygame.K_g] and not lever_2_raised:
                lever_2.activate()
                lever_2_raised = True
                print("lever_2_raised =", lever_2_raised)
        else:
            if lever_1.rect.colliderect(player.rect.inflate(30, 30)) and keys[pygame.K_g] and not lever_1_raised:
                lever_1.activate()
                lever_1_raised = True
                print("lever_1_raised =", lever_1_raised)

            if lever_2.rect.colliderect(player.rect.inflate(30, 30)) and keys[pygame.K_g] and not lever_2_raised:
                lever_2.activate()
                lever_2_raised = True
                print("lever_2_raised =", lever_2_raised)

        if lever_1_raised and lever_2_raised:
            if lever_activation_time is None:
                lever_activation_time = time.time()
                print("Both levers raised, starting timer...")

            if time.time() - lever_activation_time < lever_activation_timeout:
                door.open()
            else:
                lever_1_raised = False
                lever_2_raised = False
                lever_activation_time = None
                print("Timeout reached, resetting levers...")
                print("lever_1_raised =", lever_1_raised)
                print("lever_2_raised =", lever_2_raised)

                lever_1.deactivate()
                lever_2.deactivate()

                lever_1.current_frame = 0
                lever_1.image = lever_1.frames[lever_1.current_frame]
                lever_2.current_frame = 0
                lever_2.image = lever_2.frames[lever_2.current_frame]
                door.close()

        if door.is_open and door.rect.colliderect(player.rect):
            congratulations_screen = CongratulationsScreen(screen, exit_to_main_menu)
            congratulations_screen.congratulations_screen()
            running = False

        health.draw(screen)

        mouse_x, mouse_y = pygame.mouse.get_pos()
        font = pygame.font.Font(None, 36)
        coordinates_text = font.render(f"X: {mouse_x} Y: {mouse_y}", True, WHITE)
        screen.blit(coordinates_text, (10, 10))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
