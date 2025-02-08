import pygame

class CollisionLevel1:
    def __init__(self, ):
        # Определение лестниц, стен, платформ и коробок
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
            pygame.Rect(591, 1060, 500, 50),
            pygame.Rect(258, 322, 700, 50),
            pygame.Rect(0, 697, 650, 50),
            pygame.Rect(1671, 439, 750, 50),
            pygame.Rect(780, 613, 800, 50),
            pygame.Rect(2180, 732, 730, 50),
            pygame.Rect(1022, 168, 700, 50),
            pygame.Rect(1827, 168, 730, 50),
            pygame.Rect(1315, 934, 780, 50),
            pygame.Rect(1091, 1145, 90, 90),
            pygame.Rect(1091, 1232, 90, 90),
            pygame.Rect(1177, 1232, 90, 90),
            pygame.Rect(1969, 847, 90, 90),
            pygame.Rect(2128, 1144, 90, 90),
            pygame.Rect(2084, 1227, 90, 90),
            pygame.Rect(2170, 1227, 90, 90),
            pygame.Rect(1620, 1220, 80, 90),
            pygame.Rect(1162, 520, 70, 90),
            pygame.Rect(460, 235, 70, 90),
            pygame.Rect(0, 1319, 2560, 50)
        ]
        self.boxes = [

        ]

    def check_collisions(self, player, objects):
        """
        Общая функция для проверки коллизий.
        :param player: Объект игрока.
        :param objects: Список объектов для проверки коллизий.
        """
        # Применяем перемещение игрока
        player.on_ground = True
        player.x += player.velocity_x
        player.y += player.velocity_y
        player.rect.topleft = (player.x, player.y)

        # Флаги для обработки коллизий
        horizontal_collision = False
        vertical_collision = False

        for obj in objects:
            if player.rect.colliderect(obj):
                # Вычисляем перекрытие по осям X и Y
                overlap_x = min(player.rect.right - obj.left, obj.right - player.rect.left)
                overlap_y = min(player.rect.bottom - obj.top, obj.bottom - player.rect.top)

                # Определяем, какая ось имеет меньшее перекрытие
                if overlap_x < overlap_y:
                    # Горизонтальная коррекция
                    if player.velocity_x > 0:  # Движение вправо
                        player.rect.right = obj.left
                        player.x = player.rect.x
                        player.velocity_x = 0
                        horizontal_collision = True
                    elif player.velocity_x < 0:  # Движение влево
                        player.rect.left = obj.right
                        player.x = player.rect.x
                        player.velocity_x = 0
                        horizontal_collision = True
                else:
                    # Вертикальная коррекция
                    if player.velocity_y > 0:  # Падение на объект
                        player.rect.bottom = obj.top
                        player.y = player.rect.y
                        player.on_ground = True
                        player.velocity_y = 0
                        vertical_collision = True
                        if player.state == "jump":
                            player.change_state("idle")
                    elif player.velocity_y < 0:  # Прыжок вверх
                        player.rect.top = obj.bottom
                        player.y = player.rect.y
                        player.velocity_y = 0
                        vertical_collision = True

        # Если произошла горизонтальная коллизия, но не вертикальная, добавляем эффект скольжения
        if horizontal_collision and not vertical_collision:
            player.velocity_y += player.gravity  # Продолжаем падение вдоль стены

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


import pygame

class CollisionLevel2:
    def __init__(self, ):
        self.ladders = [

        ]
        self.ground_y = 1235
        self.walls = [
            pygame.Rect(0, 0, 2, 1500),
            pygame.Rect(2559, 0, 2, 1500)
        ]
        self.platforms = [
            pygame.Rect(1676, 973, 524, 90),
            pygame.Rect(2300, 973, 524, 90),
            pygame.Rect(1660, 1161, 524, 90),
            pygame.Rect(1121, 959, 524, 90),
            pygame.Rect(407, 957, 524, 90),
            pygame.Rect(2277, 298, 524, 90),
            pygame.Rect(1546, 87, 524, 90),
            pygame.Rect(1010, 316, 524, 90),
            pygame.Rect(434, 439, 504, 90),
            pygame.Rect(0, 157, 484, 90),
            pygame.Rect(0, 1379, 2560, 50)
        ]
        self.boxes = [

        ]

    def check_collisions(self, player, objects):
        """
        Общая функция для проверки коллизий.
        :param player: Объект игрока.
        :param objects: Список объектов для проверки коллизий.
        """
        # Применяем перемещение игрока
        player.on_ground = True
        player.x += player.velocity_x
        player.y += player.velocity_y
        player.rect.topleft = (player.x, player.y)

        # Флаги для обработки коллизий
        horizontal_collision = False
        vertical_collision = False

        for obj in objects:
            if player.rect.colliderect(obj):
                # Вычисляем перекрытие по осям X и Y
                overlap_x = min(player.rect.right - obj.left, obj.right - player.rect.left)
                overlap_y = min(player.rect.bottom - obj.top, obj.bottom - player.rect.top)

                # Определяем, какая ось имеет меньшее перекрытие
                if overlap_x < overlap_y:
                    # Горизонтальная коррекция
                    if player.velocity_x > 0:  # Движение вправо
                        player.rect.right = obj.left
                        player.x = player.rect.x
                        player.velocity_x = 0
                        horizontal_collision = True
                    elif player.velocity_x < 0:  # Движение влево
                        player.rect.left = obj.right
                        player.x = player.rect.x
                        player.velocity_x = 0
                        horizontal_collision = True
                else:
                    # Вертикальная коррекция
                    if player.velocity_y > 0:  # Падение на объект
                        player.rect.bottom = obj.top
                        player.y = player.rect.y
                        player.on_ground = True
                        player.velocity_y = 0
                        vertical_collision = True
                        if player.state == "jump":
                            player.change_state("idle")
                    elif player.velocity_y < 0:  # Прыжок вверх
                        player.rect.top = obj.bottom
                        player.y = player.rect.y
                        player.velocity_y = 0
                        vertical_collision = True

        # Если произошла горизонтальная коллизия, но не вертикальная, добавляем эффект скольжения
        if horizontal_collision and not vertical_collision:
            player.velocity_y += player.gravity  # Продолжаем падение вдоль стены

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