import pygame

from scripts.collision import CollisionLevel1


class CollisionLevel2:
    def __init__(self):
        self.platforms.clear()
        self.walls.clear()
        self.ladders.clear()
        self.boxes.clear()

        self.ladders = [
            pygame.Rect(514, 1059, 50, 230),
            pygame.Rect(2423, 431, 50, 250),
            pygame.Rect(961, 323, 50, 25)
        ]
        self.ground_y = 1235
        self.walls = [
            pygame.Rect(0, 0, 2, 1500),
            pygame.Rect(2559, 0, 2, 1500)
        ]
        self.platforms = [
            pygame.Rect(0, 155, 484, 85),
            pygame.Rect(460, 235, 70, 90),
            pygame.Rect(460, 235, 70, 90),
            pygame.Rect(0, 1372, 2560, 50)
        ]
        self.boxes = [

        ]

    def check_collisions(self, player, objects):
        # Сохраняем текущую позицию игрока
        original_x, original_y = player.x, player.y

        # Обновляем позицию игрока
        player.on_ground = True
        player.x += player.velocity_x
        player.y += player.velocity_y
        player.rect.topleft = (player.x, player.y)

        for obj in objects:
            if player.rect.colliderect(obj):
                # Вычисляем перекрытие по осям X и Y
                overlap_x = min(player.rect.right - obj.left, obj.right - player.rect.left)
                overlap_y = min(player.rect.bottom - obj.top, obj.bottom - player.rect.top)

                if overlap_x < overlap_y:
                    # Горизонтальная коррекция
                    if player.velocity_x > 0:  # Движение вправо
                        player.rect.right = obj.left
                    elif player.velocity_x < 0:  # Движение влево
                        player.rect.left = obj.right
                    player.x = player.rect.x
                    player.velocity_x = 0
                else:
                    # Вертикальная коррекция
                    if player.velocity_y > 0:  # Падение на объект
                        player.rect.bottom = obj.top
                        player.on_ground = True
                        if player.state == "jump":
                            player.change_state("idle")
                    elif player.velocity_y < 0:  # Прыжок вверх
                        player.rect.top = obj.bottom
                    player.y = player.rect.y
                    player.velocity_y = 0

        # Обновляем прямоугольник коллизии после всех изменений
        player.rect.topleft = (player.x, player.y)

    def check_wall_collision(self, player):
        self.check_collisions(player, self.walls)

    def check_ladder_collision(self, player):
        on_ladder = False
        for ladder in self.ladders:
            if ladder.colliderect(player.rect):
                player.collision_type = 'ladder'
                on_ladder = True
                player.on_ladder = True
                player.rect.bottom = ladder.top
                break
        if not on_ladder:
            player.on_ladder = False
        return on_ladder

    def check_platform_collision(self, player):
        self.check_collisions(player, self.platforms)

    def check_box_collision(self, player):
        self.check_collisions(player, self.boxes)

    def draw_collision_debug(self, screen):
        # Отрисовка отладочных прямоугольников
        for ladder in self.ladders:
            pygame.draw.rect(screen, (255, 0, 0), ladder, 6)  # Красный цвет для лестниц
        for wall in self.walls:
            pygame.draw.rect(screen, (0, 0, 0), wall, 6)  # Черный цвет для стен
        for platform in self.platforms:
            pygame.draw.rect(screen, (0, 255, 0), platform, 6)  # Зеленый цвет для платформ
        for box in self.boxes:
            pygame.draw.rect(screen, (0, 0, 255), box, 6)  # Синий цвет для коробок
