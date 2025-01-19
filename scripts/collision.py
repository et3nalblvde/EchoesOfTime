import pygame
class CollisionLevel1:
    def __init__(self):
        self.ladders = [pygame.Rect(514, 1059, 50, 230), pygame.Rect(2423, 431, 50, 200)]
        self.ground_y = 1235
        self.walls = [
            pygame.Rect(600, 1120, 500, 250),  # Пример стены
        ]
        self.platforms = [
            pygame.Rect(591, 1060, 500, 50),
            pygame.Rect(258, 322, 500, 50),
            pygame.Rect(0, 697, 500, 50),
            pygame.Rect(1671, 439, 500, 50),
            pygame.Rect(780, 613, 500, 50),
            pygame.Rect(2180, 732, 500, 50),
            pygame.Rect(1022, 168, 500, 50),
            pygame.Rect(1827, 168, 500, 50),
            # Пример платформы
            pygame.Rect(1315, 934, 500, 50)  # Еще одна платформа
        ]

    def check_wall_collision(self, player):
        for wall in self.walls:
            if player.rect.colliderect(wall):
                player.collision_type = 'wall'  # Устанавливаем тип столкновения как 'wall'

                # Двигается вправо
                if player.velocity_x > 0:
                    if player.rect.right >= wall.left:  # Если игрок в пределах стены
                        player.rect.right = wall.left  # Останавливаем его на границе стены
                        player.velocity_x = 0  # Останавливаем движение по оси X
                        return True  # Возвращаем True, так как была коллизия

                # Двигается влево
                elif player.velocity_x < 0:
                    if player.rect.left <= wall.right:  # Если игрок в пределах стены
                        player.rect.left = wall.right  # Останавливаем его на границе стены
                        player.velocity_x = 0  # Останавливаем движение по оси X
                        return True  # Возвращаем True, так как была коллизия

        return False  # Возвращаем False, если коллизия не была найдена

    def check_ladder_collision(self, player):
        on_ladder = False
        for ladder in self.ladders:
            if ladder.colliderect(player.rect):
                player.collision_type = 'ladder'  # Устанавливаем тип столкновения как 'ladder'
                on_ladder = True
                player.on_ladder = True
                player.rect.bottom = ladder.top
                break  # Если коллизия найдена, больше не проверяем другие лестницы

        if not on_ladder:
            player.on_ladder = False
        return on_ladder

    def check_ground_collision(self, player):
        if player.rect.bottom > self.ground_y:
            player.collision_type = 'ground'  # Устанавливаем тип столкновения как 'ground'
            player.rect.bottom = self.ground_y
            return True
        return False

    def check_platform_collision(self, player):
        for platform in self.platforms:
            if platform.colliderect(player.rect):
                player.collision_type = 'platform'  # Устанавливаем тип столкновения как 'platform'

                # Проверка, что игрок находится над платформой и двигается вниз
                if player.rect.bottom <= platform.top and player.velocity_y >= 0:
                    player.rect.bottom = platform.top  # Останавливаем игрока сверху платформы
                    player.velocity_y = 0  # Останавливаем вертикальное движение (прыжок)

                    # Продолжаем горизонтальное движение по платформе
                    player.rect.x += player.velocity_x  # Двигаем игрока по платформе

                    # Защита от выхода за пределы платформы
                    if player.rect.left < platform.left:
                        player.rect.left = platform.left  # Останавливаем игрока, если он выходит за пределы слева
                    elif player.rect.right > platform.right:
                        player.rect.right = platform.right  # Останавливаем игрока, если он выходит за пределы справа

                # Платформа может принимать игрока только сверху, поэтому исключаем падение через платформу
                elif player.rect.bottom > platform.top and player.velocity_y > 0:
                    # Если игрок идет сверху вниз и попадает на платформу
                    player.rect.bottom = platform.top  # Останавливаем его сверху платформы
                    player.velocity_y = 0  # Останавливаем его вертикальное движение

                    # Горизонтальное движение по платформе
                    player.rect.x += player.velocity_x

                    # Защита от выхода за пределы платформы
                    if player.rect.left < platform.left:
                        player.rect.left = platform.left
                    elif player.rect.right > platform.right:
                        player.rect.right = platform.right

                    return True  # Возвращаем True, если была найдена коллизия с платформой

        return False  # Возвращаем False, если коллизия не была найдена

    def draw_collision_debug(self, screen):
        # Рисуем обводку для лестниц, стен и платформ
        for ladder in self.ladders:
            pygame.draw.rect(screen, (255, 0, 0), ladder, 6)  # Красный для лестницы
        for wall in self.walls:
            pygame.draw.rect(screen, (0, 0, 0), wall, 6)  # Черный для стен
        for platform in self.platforms:
            pygame.draw.rect(screen, (0, 255, 0), platform, 6)  # Зеленый для платформ
