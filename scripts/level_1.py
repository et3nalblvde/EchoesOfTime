import pygame
from game_over import GameOverScreen
from player import Player
from shadow import Shadow
from health import Health

WHITE = (255, 255, 255)
DARK_GREEN = (34, 139, 34)
BROWN = (139, 69, 19)
GREY = (169, 169, 169)
BLACK = (0, 0, 0)

column_image = pygame.Surface((50, 200))
column_image.fill(GREY)
moss_image = pygame.Surface((50, 50))
moss_image.fill(DARK_GREEN)
vine_image = pygame.Surface((30, 200))
vine_image.fill(BROWN)

def draw_background(screen):
    screen.fill(WHITE)

    for i in range(0, screen.get_width(), 100):
        screen.blit(column_image, (i, screen.get_height() - 200))

    for i in range(0, screen.get_width(), 150):
        screen.blit(moss_image, (i, screen.get_height() - 220))

    for i in range(0, screen.get_width(), 150):
        screen.blit(vine_image, (i, screen.get_height() - 200))

    pygame.draw.rect(screen, (255, 255, 200), pygame.Rect(100, 50, 200, 100), 2)

def start_level_1(screen):
    player = Player(100, 400)
    shadow = Shadow(100, 400)

    
    health = Health(max_health=3, x=10, y=10, player=player)

    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)
    all_sprites.add(shadow)

    controlling_player = True

    clock = pygame.time.Clock()

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

        if keys[pygame.K_e]:  
            health.take_damage(0.5)  

        
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

        draw_background(screen)

        
        health.draw(screen)

        all_sprites.update()

        all_sprites.draw(screen)

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
