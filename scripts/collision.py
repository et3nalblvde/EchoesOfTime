import pygame

class CollisionLevel1:
    def __init__(self):
        # Пример с несколькими лестницами
        self.ladders = [pygame.Rect(514, 1059, 50, 230), pygame.Rect(2423, 431, 50, 200)]
        self.ground_y = 1235
        # Добавляем стены как глухие барьеры
        self.walls = [
            pygame.Rect(685, 1060, 150, 250),  # Пример стены
            pygame.Rect(2000, 900, 50, 300)  # Еще одна стена
        ]
        # Платформы
        self.platforms = [
            pygame.Rect(500, 1100, 150, 20),  # Пример платформы
            pygame.Rect(1800, 1150, 200, 20)  # Еще одна платформа
        ]

    def check_ladder_collision(self, player):
        on_ladder = False

        for ladder in self.ladders:
            # Проверка коллизии для игрока
            if ladder.colliderect(player.rect):
                on_ladder = True
                player.on_ladder = True
                player.rect.bottom = ladder.top  # Установить игрока на верх лестницы

                # Если у игрока есть тень, обработать коллизию и для неё
                if hasattr(player, 'shadow') and ladder.colliderect(player.shadow.rect):
                    player.shadow.on_ladder = True
                    player.shadow.rect.bottom = ladder.top  # Установить тень на верх лестницы
                    player.shadow.velocity_y = 0  # Остановить гравитацию для тени
                else:
                    if hasattr(player, 'shadow'):
                        player.shadow.on_ladder = False
                        player.shadow.velocity_y = player.shadow.gravity  # Восстановить гравитацию для тени
                break  # Если коллизия найдена, больше не проверяем другие лестницы

        if not on_ladder:
            player.on_ladder = False
            if hasattr(player, 'shadow'):
                player.shadow.on_ladder = False
                player.shadow.velocity_y = player.shadow.gravity  # Применение гравитации для тени, если она не на лестнице

        return on_ladder

    def check_ground_collision(self, player):
        if player.rect.bottom > self.ground_y:
            player.rect.bottom = self.ground_y
            return True
        return False

    def check_wall_collision(self, player):
        for wall in self.walls:
            if wall.colliderect(player.rect):
                # Горизонтальная коллизия
                if player.rect.centerx < wall.centerx:
                    player.rect.right = wall.left  # Останавливаем движение вправо
                    player.velocity_x = 0
                else:
                    player.rect.left = wall.right  # Останавливаем движение влево
                    player.velocity_x = 0

                # Вертикальная коллизия (верх/низ)
                if player.rect.bottom > wall.top and player.rect.top < wall.bottom:
                    # Если игрок столкнулся с верхней частью стены, останавливаем его движение вниз
                    if player.rect.centery < wall.centery:
                        player.rect.bottom = wall.top  # Останавливаем движение вниз
                        player.velocity_y = 0  # Останавливаем падение
                    # Если игрок столкнулся с нижней частью стены, останавливаем его движение вверх
                    else:
                        player.rect.top = wall.bottom  # Останавливаем движение вверх
                        player.velocity_y = 0  # Останавливаем подъем

                # Остановка тени (если она есть)
                if hasattr(player, 'shadow'):
                    player.shadow.velocity_x = 0  # Останавливаем тень по горизонтали
                    player.shadow.velocity_y = 0  # Останавливаем тень по вертикали

                return True
        return False

    def check_platform_collision(self, player):
        for platform in self.platforms:
            if platform.colliderect(player.rect):
                if player.rect.bottom <= platform.top and player.velocity_y >= 0:
                    player.rect.bottom = platform.top  # Останавливаем движение вниз
                    player.velocity_y = 0  # Останавливаем падение
                    if hasattr(player, 'shadow'):
                        player.shadow.velocity_y = 0  # Останавливаем падение тени
                # Проверка, если игрок стоит на платформе сверху (если падал сверху)
                elif player.rect.top >= platform.bottom and player.velocity_y <= 0:
                    player.rect.top = platform.bottom  # Останавливаем движение вверх
                    player.velocity_y = 0  # Останавливаем подъем
                # Горизонтальные коллизии, если игрок упал на платформу с боков
                elif player.rect.left < platform.right and player.rect.right > platform.left:
                    if player.velocity_x > 0:  # Двигается вправо
                        player.rect.right = platform.left  # Останавливаем движение вправо
                    elif player.velocity_x < 0:  # Двигается влево
                        player.rect.left = platform.right  # Останавливаем движение влево
                return True
        return False

    def draw_collision_debug(self, screen):
        # Рисуем обводку для лестниц, стен и платформ
        for ladder in self.ladders:
            pygame.draw.rect(screen, (255, 0, 0), ladder, 6)  # Красный для лестницы
        for wall in self.walls:
            pygame.draw.rect(screen, (0, 0, 0), wall, 6)  # Черный для стен
        for platform in self.platforms:
            pygame.draw.rect(screen, (0, 255, 0), platform, 6)  # Зеленый для платформ
