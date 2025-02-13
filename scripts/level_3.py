import pygame
import os
from game_over import GameOverScreen
from player import Player
from health import Health
from collision import CollisionLevel3
from pause_menu import PauseMenu
from bat import Bat
from settings import load_sounds, load_settings
from shadow import Shadow

WHITE = (255, 255, 255)

settings = load_settings()
MUSIC_VOLUME = settings["MUSIC_VOLUME"]
SFX_VOLUME = settings["SFX_VOLUME"]

pygame.mixer.music.set_volume(MUSIC_VOLUME)

base_folder = os.path.dirname(os.path.abspath(__file__))
level_2_image_path = os.path.join(base_folder, '..', 'assets', 'sprites', 'maps', 'level_3.png')
level_2_image = pygame.image.load(level_2_image_path)


def scale_background(screen):
    screen_width, screen_height = screen.get_size()
    return pygame.transform.scale(level_2_image, (screen_width, screen_height))


def draw_background(screen):
    scaled_background = scale_background(screen).convert()
    screen.blit(scaled_background, (0, 0))


def start_level_3(screen, restart_main_menu, exit_to_main_menu):
    player_sounds = load_sounds(SFX_VOLUME)
    player = Player(128, 1302, player_sounds, 3)
    shadow = Shadow(1576, 832, 3)
    health = Health(max_health=3, x=10, y=10, player=player)
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)
    all_sprites.add(shadow)
    bats = pygame.sprite.Group()


    bat1 = Bat(1553, 26, 2015, 26)
    bat2 = Bat(439, 889, 1172, 885)
    bats.add(bat1, bat2)
    all_sprites.add(bat1, bat2)

    collision = CollisionLevel3()

    clock = pygame.time.Clock()
    running = True
    is_paused = False
    control_shadow = False

    pause_menu = PauseMenu(screen)

    while running:
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

        all_sprites.update(clock.get_time() / 1000)
        all_sprites.draw(screen)

        health.draw(screen)

        mouse_x, mouse_y = pygame.mouse.get_pos()
        font = pygame.font.Font(None, 36)
        coordinates_text = font.render(f"X: {mouse_x} Y: {mouse_y}", True, WHITE)
        screen.blit(coordinates_text, (10, 10))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
