import pygame
import os
import time
from game_over import GameOverScreen
from player import Player
from shadow import Shadow
from health import Health
from collision import CollisionLevel1
from pause_menu import PauseMenu
from bat import Bat
from settings import load_sounds
from settings import load_settings

WHITE = (255, 255, 255)
from level_complete import CongratulationsScreen

base_folder = os.path.dirname(os.path.abspath(__file__))
level_1_image_path = os.path.join(base_folder, '..', 'assets', 'sprites', 'maps', 'level_1.png')

level_1_image = pygame.image.load(level_1_image_path)


def scale_background(screen):
    screen_width, screen_height = screen.get_size()
    return pygame.transform.scale(level_1_image, (screen_width, screen_height))


def draw_background(screen):
    scaled_background = scale_background(screen).convert()
    screen.blit(scaled_background, (0, 0))


import json
import os
from lever import Lever


def update_level_status(level, status):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    PROJECT_DIR = os.path.abspath(os.path.join(BASE_DIR, '..'))
    settings_path = os.path.join(PROJECT_DIR, 'save', 'settings.json')

    with open(settings_path, 'r') as file:
        settings = json.load(file)

    settings[level] = status

    with open(settings_path, 'w') as file:
        json.dump(settings, file, indent=4)


def update_level_status(level, status):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    PROJECT_DIR = os.path.abspath(os.path.join(BASE_DIR, '..'))
    settings_path = os.path.join(PROJECT_DIR, 'save', 'settings.json')

    with open(settings_path, 'r') as file:
        settings = json.load(file)

    settings[level] = status

    with open(settings_path, 'w') as file:
        json.dump(settings, file, indent=4)


from Door import Door

import pygame
import time

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


def start_level_1(screen, restart_main_menu, exit_to_main_menu):
    settings = load_settings()
    MUSIC_VOLUME = settings["MUSIC_VOLUME"]
    SFX_VOLUME = settings["SFX_VOLUME"]

    pygame.mixer.music.set_volume(MUSIC_VOLUME)
    player_sounds = load_sounds(SFX_VOLUME)

    player = Player(2023, 63, player_sounds)
    shadow = Shadow(1576, 832)
    health = Health(max_health=3, x=10, y=10, player=player)

    door_x, door_y = 2398, 65
    sprites_path = os.path.join(base_folder, '..', 'assets', 'sprites', 'doors')
    door = Door(door_x, door_y, sprites_path, frame_count=6)

    lever_1_x, lever_1_y = 1576, 892
    lever_2_x, lever_2_y = 2023, 123
    lever_sprites_path = os.path.join(base_folder, '..', 'assets', 'sprites', 'levers')

    lever_1 = Lever(lever_1_x, lever_1_y, lever_sprites_path, frame_count=5)
    lever_2 = Lever(lever_2_x, lever_2_y, lever_sprites_path, frame_count=5)

    all_sprites = pygame.sprite.Group()
    all_sprites.add(door)
    all_sprites.add(player)
    all_sprites.add(shadow)
    all_sprites.add(lever_1)
    all_sprites.add(lever_2)

    bats = pygame.sprite.Group()
    bat = Bat(1830, 103, 2190, 103)
    bats.add(bat)
    all_sprites.add(bat)

    controlling_player = True
    clock = pygame.time.Clock()
    collision = CollisionLevel1()

    running = True
    player_dead = False
    death_animation_playing = False

    pause_menu = PauseMenu(screen)
    is_paused = False
    esc_pressed = False

    complete_level = False

    lever_1_raised = False
    lever_2_raised = False
    lever_activation_time = None
    lever_activation_timeout = 2

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()

        if keys[pygame.K_ESCAPE]:
            if not esc_pressed:
                is_paused = not is_paused
                esc_pressed = True
        else:
            esc_pressed = False

        if is_paused:
            result = pause_menu.handle_events(event)
            pause_menu.draw()

            if result == "quit":
                exit_to_main_menu()

            if result == "continue":
                is_paused = False

            pygame.display.flip()
            continue

        draw_background(screen)

        if keys[pygame.K_e]:
            if controlling_player:
                player.stop()
            else:
                shadow.stop()

            controlling_player = not controlling_player
            pygame.time.wait(200)

        if keys[pygame.K_f]:
            if controlling_player:
                player.attack(bats)

        if keys[pygame.K_t]:
            health.take_damage(health.current_health)
            player.change_state("death")
            death_animation_playing = True
            if not health.is_alive():
                game_over_screen = GameOverScreen(
                    screen,
                    lambda: start_level_1(screen, restart_main_menu, exit_to_main_menu),
                    exit_to_main_menu
                )
                game_over_screen_loop(game_over_screen)
                running = False

        if death_animation_playing:
            if player.is_death_animation_finished():
                player_dead = True
                game_over_screen = GameOverScreen(screen,
                                                  lambda: start_level_1(screen, restart_main_menu, exit_to_main_menu),
                                                  exit_to_main_menu)
                game_over_screen_loop(game_over_screen)
                running = False

        collision.check_ladder_collision(player)
        collision.check_ladder_collision(shadow)
        collision.check_platform_collision(player)
        collision.check_platform_collision(shadow)
        collision.check_wall_collision(player)
        collision.check_wall_collision(shadow)
        collision.check_box_collision(player)
        collision.check_box_collision(shadow)

        if controlling_player:
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                player.move_left()
            elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                player.move_right()
            else:
                player.stop()

            if keys[pygame.K_SPACE]:
                player.jump()
        else:
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                shadow.move_left()
            elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                shadow.move_right()
            else:
                shadow.stop()

            if keys[pygame.K_SPACE]:
                shadow.jump()

            if shadow.on_ladder:
                if keys[pygame.K_UP]:
                    shadow.y -= 10
                    shadow.change_state("idle")
                elif keys[pygame.K_DOWN]:
                    shadow.y += 10
                    shadow.change_state("idle")

        if controlling_player:
            if lever_1.rect.colliderect(player.rect.inflate(30, 30)) and keys[pygame.K_g] and not lever_1_raised:
                lever_1.activate()
                lever_1_raised = True
                print("lever_1_raised =", lever_1_raised)

            if lever_2.rect.colliderect(player.rect.inflate(30, 30)) and keys[pygame.K_g] and not lever_2_raised:
                lever_2.activate()
                lever_2_raised = True
                print("lever_2_raised =", lever_2_raised)
        else:
            if lever_1.rect.colliderect(shadow.rect.inflate(30, 30)) and keys[pygame.K_g] and not lever_1_raised:
                lever_1.activate()
                lever_1_raised = True
                print("lever_1_raised =", lever_1_raised)

            if lever_2.rect.colliderect(shadow.rect.inflate(30, 30)) and keys[pygame.K_g] and not lever_2_raised:
                lever_2.activate()
                lever_2_raised = True
                print("lever_2_raised =", lever_2_raised)

        if lever_1_raised and lever_2_raised:
            if lever_activation_time is None:
                lever_activation_time = time.time()
                print("Both levers raised, starting timer...")

            if time.time() - lever_activation_time < lever_activation_timeout:

                door.open()
                complete_level = True
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
            complete_level = True
            update_level_status("level_1", "complete")
            congratulations_screen = CongratulationsScreen(screen, exit_to_main_menu)
            congratulations_screen.congratulations_screen()
            running = False

        health.draw(screen)

        all_sprites.update(clock.get_time() / 1000)
        all_sprites.draw(screen)
        collision.draw_collision_debug(screen)

        mouse_x, mouse_y = pygame.mouse.get_pos()
        font = pygame.font.Font(None, 36)
        coordinates_text = font.render(f"X: {mouse_x} Y: {mouse_y}", True, WHITE)
        screen.blit(coordinates_text, (10, 10))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
