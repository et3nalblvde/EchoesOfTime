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


def update_level_status(level, status):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    PROJECT_DIR = os.path.abspath(os.path.join(BASE_DIR, '..'))
    settings_path  = os.path.join(PROJECT_DIR, 'save', 'settings.json')

    
    with open(settings_path, 'r') as file:
        settings = json.load(file)

    
    settings[level] = status

    
    with open(settings_path, 'w') as file:
        json.dump(settings, file, indent=4)


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


def update_level_status(level, status):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    PROJECT_DIR = os.path.abspath(os.path.join(BASE_DIR, '..'))
    settings_path  = os.path.join(PROJECT_DIR, 'save', 'settings.json')

    
    with open(settings_path, 'r') as file:
        settings = json.load(file)

    
    settings[level] = status

    
    with open(settings_path, 'w') as file:
        json.dump(settings, file, indent=4)


def start_level_1(screen, restart_main_menu, exit_to_main_menu):
    player = Player(288, 1230)
    shadow = Shadow(100, 1230)
    health = Health(max_health=3, x=10, y=10, player=player)

    bat_start_x = 1830
    bat_start_y = 103
    bat_end_x = 2190
    bat_end_y = 103
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)
    all_sprites.add(shadow)

    bats = pygame.sprite.Group()
    bat = Bat(bat_start_x, bat_start_y, bat_end_x, bat_end_y)
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

    
    complete_zone = pygame.Rect(2438, 39, 140, 140)  

    
    lever_1_rect = pygame.Rect(1800, 1000, 50, 100)  
    lever_2_rect = pygame.Rect(2000, 1000, 50, 100)  

    
    lever_1_raised = True
    lever_2_raised = True

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
        collision.check_ground_collision(player)
        collision.check_ground_collision(shadow)
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

        
        if lever_1_rect.collidepoint(player.x, player.y):
            lever_1_raised = True
        if lever_2_rect.collidepoint(player.x, player.y):
            lever_2_raised = True

        
        if lever_1_raised and lever_2_raised and complete_zone.collidepoint(player.x, player.y):
            complete_level = True
            pygame.time.wait(10)  

            
            update_level_status('Level_2', True)

            
            screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            congratulations_screen = CongratulationsScreen(screen,
                                                           lambda: start_level_1(screen, restart_main_menu,
                                                                                 exit_to_main_menu),
                                                           exit_to_main_menu)
            congratulations_screen.congratulations_screen()

        
        pygame.draw.rect(screen, (0, 255, 0), complete_zone, 3)  

        
        pygame.draw.rect(screen, (255, 0, 0), lever_1_rect)  
        pygame.draw.rect(screen, (0, 0, 255), lever_2_rect)  

        health.draw(screen)

        all_sprites.update()
        all_sprites.draw(screen)
        collision.draw_collision_debug(screen)

        mouse_x, mouse_y = pygame.mouse.get_pos()
        font = pygame.font.Font(None, 36)
        coordinates_text = font.render(f"X: {mouse_x} Y: {mouse_y}", True, WHITE)
        screen.blit(coordinates_text, (10, 10))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

