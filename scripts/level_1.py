import pygame
import os
from game_over import GameOverScreen
from player import Player
from shadow import Shadow
from health import Health
from collision import CollisionLevel1

WHITE = (255, 255, 255)

base_folder = os.path.dirname(os.path.abspath(__file__))
level_1_image_path = os.path.join(base_folder, '..', 'assets', 'sprites', 'maps', 'level_1.png')

level_1_image = pygame.image.load(level_1_image_path)

def scale_background(screen):
    screen_width, screen_height = screen.get_size()
    return pygame.transform.scale(level_1_image, (screen_width, screen_height))

def draw_background(screen):
    scaled_background = scale_background(screen).convert()
    screen.blit(scaled_background, (0, 0))

def start_level_1(screen):
    player = Player(288, 1230)
    shadow = Shadow(100, 1230)
    health = Health(max_health=3, x=10, y=10, player=player)

    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)
    all_sprites.add(shadow)

    controlling_player = True

    clock = pygame.time.Clock()

    collision = CollisionLevel1()

    running = True
    player_dead = False
    death_animation_playing = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()

        if keys[pygame.K_e]:
            if controlling_player:
                player.stop()
            else:
                shadow.stop()

            controlling_player = not controlling_player
            pygame.time.wait(200)

        if keys[pygame.K_f]:
            if controlling_player:
                player.attack()

        if keys[pygame.K_t]:
            health.take_damage(health.current_health)
            player.change_state("death")

        if not health.is_alive() and not player_dead and not death_animation_playing:
            print("Игрок умирает!")
            player.change_state("death")
            death_animation_playing = True
            pygame.time.wait(500)

        if death_animation_playing:
            if player.is_death_animation_finished():
                player_dead = True
                print("Анимация смерти завершена!")
                pygame.time.wait(500)

        if player_dead:
            def restart_game():
                start_level_1(screen)

            def exit_to_main_menu():
                print("Выход в главное меню!")

            game_over_screen = GameOverScreen(screen, restart_game, exit_to_main_menu)
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

        draw_background(screen)

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

def game_over_screen_loop(game_over_screen):
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            game_over_screen.handle_events(event)

        game_over_screen.draw()
        pygame.display.flip()
