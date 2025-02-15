import pygame
import os
from game_over import GameOverScreen
from player import Player
from health import Health
from collision import CollisionLevel3
from pause_menu import PauseMenu
from bat import Bat
from Door import Door
from lever import Lever  # Импортируем Lever
from settings import load_sounds, load_settings
from shadow import Shadow
import time
from trap import NeedleTrap
import json
from endscene import CreditsScreen
WHITE = (255, 255, 255)

settings = load_settings()
MUSIC_VOLUME = settings["MUSIC_VOLUME"]
SFX_VOLUME = settings["SFX_VOLUME"]

pygame.mixer.music.set_volume(MUSIC_VOLUME)

base_folder = os.path.dirname(os.path.abspath(__file__))
level_2_image_path = os.path.join(base_folder, '..', 'assets', 'sprites', 'maps', 'level_3.png')
level_2_image = pygame.image.load(level_2_image_path)

def game_over_screen_loop(game_over_screen):
    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            result = game_over_screen.handle_events(event)
            if result == "quit":
                running = False
        game_over_screen.draw()
        pygame.display.flip()
        clock.tick(60)


def scale_background(screen):
    screen_width, screen_height = screen.get_size()
    return pygame.transform.scale(level_2_image, (screen_width, screen_height))


def draw_background(screen):
    scaled_background = scale_background(screen).convert()
    screen.blit(scaled_background, (0, 0))


def update_level_status(level, status):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    PROJECT_DIR = os.path.abspath(os.path.join(BASE_DIR, '..'))
    settings_path = os.path.join(PROJECT_DIR, 'save', 'settings.json')


def start_level_3(screen, restart_main_menu, exit_to_main_menu):
    pygame.mixer.music.set_volume(MUSIC_VOLUME)
    player_sounds = load_sounds(SFX_VOLUME)
    difficulty = settings.get("DIFFICULTY", "medium")
    player = Player(128, 1302, player_sounds, 3, difficulty)
    shadow = Shadow(1576, 832, 3)
    health = Health(max_health=3, x=10, y=10, player=player)
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)
    all_sprites.add(shadow)
    bats = pygame.sprite.Group()

    running = True
    player_dead = False
    death_animation_playing = False

    needle1 = NeedleTrap(567, 990, 64, 64)
    needle2 = NeedleTrap(2036, 690, 64, 64)
    all_sprites.add(needle1, needle2)


    bat1 = Bat(1919, 1077, 2200, 1077)
    bat2 = Bat(2216, 240, 2508, 240)
    bat3 = Bat(1324, 1288, 1703, 1288)
    bat4 = Bat(226, 237, 586, 237)
    bats.add(bat1, bat2,bat3,bat4)
    all_sprites.add(bat1, bat2,bat3,bat4)

    collision = CollisionLevel3()

    clock = pygame.time.Clock()
    running = True
    is_paused = False
    control_shadow = False

    pause_menu = PauseMenu(screen)

    # Создаем двери и рычаги
    door_x, door_y = 1806, 1065
    sprites_path = os.path.join(base_folder, '..', 'assets', 'sprites', 'doors')
    door = Door(door_x, door_y, sprites_path, frame_count=6)
    all_sprites.add(door)

    lever_1_x, lever_1_y = 2043, 1139
    lever_2_x, lever_2_y = 2449, 1320
    lever_3_x, lever_3_y = 2336, 280
    lever_sprites_path = os.path.join(base_folder, '..', 'assets', 'sprites', 'levers')

    lever_1 = Lever(lever_1_x, lever_1_y, lever_sprites_path, frame_count=5)
    lever_2 = Lever(lever_2_x, lever_2_y, lever_sprites_path, frame_count=5)
    lever_3 = Lever(lever_3_x, lever_3_y, lever_sprites_path, frame_count=5)
    all_sprites.add(lever_1)
    all_sprites.add(lever_2)
    all_sprites.add(lever_3)

    lever_1_raised = False
    lever_2_raised = False
    lever_3_raised = False
    lever_activation_time = None
    lever_activation_timeout = 2
    complete_level = False

    while running:
        dt = clock.get_time() / 1000
        current_time = pygame.time.get_ticks()

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

        if death_animation_playing:
            if player.is_death_animation_finished():
                player_dead = True
                time.sleep(1)
                game_over_screen = GameOverScreen(screen,
                                                  lambda: start_level_3(screen, restart_main_menu, exit_to_main_menu),
                                                  exit_to_main_menu)
                game_over_screen_loop(game_over_screen)
                running = False

        death_animation_finished = False

        if not health.is_alive() or death_animation_finished:
            if not player_dead:
                time.sleep(1)
                game_over_screen = GameOverScreen(
                    screen,
                    lambda: start_level_3(screen, restart_main_menu, exit_to_main_menu),
                    exit_to_main_menu
                )
                game_over_screen_loop(game_over_screen)
                player_dead = True
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

        all_sprites.update(clock.get_time() / 1000)
        all_sprites.draw(screen)

        health.draw(screen)

        mouse_x, mouse_y = pygame.mouse.get_pos()
        font = pygame.font.Font(None, 36)
        coordinates_text = font.render(f"X: {mouse_x} Y: {mouse_y}", True, WHITE)
        screen.blit(coordinates_text, (10, 10))

        # Логика активации рычагов
        if not control_shadow:
            if lever_1.rect.colliderect(player.rect.inflate(30, 30)) and keys[pygame.K_g] and not lever_1_raised:
                lever_1.activate()
                lever_1_raised = True
                print("lever_1_raised =", lever_1_raised)

            if lever_2.rect.colliderect(player.rect.inflate(30, 30)) and keys[pygame.K_g] and not lever_2_raised:
                lever_2.activate()
                lever_2_raised = True
                print("lever_2_raised =", lever_2_raised)

            if lever_3.rect.colliderect(player.rect.inflate(30, 30)) and keys[pygame.K_g] and not lever_3_raised:
                lever_3.activate()
                lever_3_raised = True
                print("lever_3_raised =", lever_3_raised)
        else:
            if lever_1.rect.colliderect(shadow.rect.inflate(30, 30)) and keys[pygame.K_g] and not lever_1_raised:
                lever_1.activate()
                lever_1_raised = True
                print("lever_1_raised =", lever_1_raised)

            if lever_2.rect.colliderect(shadow.rect.inflate(30, 30)) and keys[pygame.K_g] and not lever_2_raised:
                lever_2.activate()
                lever_2_raised = True
                print("lever_2_raised =", lever_2_raised)

            if lever_3.rect.colliderect(shadow.rect.inflate(30, 30)) and keys[pygame.K_g] and not lever_3_raised:
                lever_3.activate()
                lever_3_raised = True
                print("lever_3_raised =", lever_3_raised)

        if lever_1_raised and lever_2_raised and lever_3_raised:
            if lever_activation_time is None:
                lever_activation_time = time.time()
                print("All levers raised, starting timer...")

            if time.time() - lever_activation_time < lever_activation_timeout:
                door.open()
                complete_level = True
            else:
                lever_1_raised = False
                lever_2_raised = False
                lever_3_raised = False
                lever_activation_time = None
                print("Timeout reached, resetting levers...")
                print("lever_1_raised =", lever_1_raised)
                print("lever_2_raised =", lever_2_raised)
                print("lever_3_raised =", lever_3_raised)

                lever_1.deactivate()
                lever_2.deactivate()
                lever_3.deactivate()

                lever_1.current_frame = 0
                lever_1.image = lever_1.frames[lever_1.current_frame]
                lever_2.current_frame = 0
                lever_2.image = lever_2.frames[lever_2.current_frame]
                lever_3.current_frame = 0
                lever_3.image = lever_3.frames[lever_3.current_frame]
                door.close()

        if door.is_open and door.rect.colliderect(player.rect):
            complete_level = True
            update_level_status("level_3", "complete")
            all_sprites.empty()
            collision.platforms.clear()
            collision.walls.clear()
            credits_screen = CreditsScreen(screen)
            credits_screen.run()
            running = False

        if needle1.rect.colliderect(player.rect):
            player.take_damage(1)




        for bat in bats:
            bat.attack(player)


        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
