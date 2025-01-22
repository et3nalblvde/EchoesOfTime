import pygame

class CollisionLevel1:
    def __init__(self):
        self.ladders = [pygame.Rect(514, 1059, 50, 230), pygame.Rect(2423, 431, 50, 250),pygame.Rect(961, 323, 50, 25)]
        self.ground_y = 1235
        self.walls = [pygame.Rect(591, 1080, 500, 50),
            pygame.Rect(258, 342, 700, 50),
            pygame.Rect(0, 717, 650, 50),
            pygame.Rect(1671, 459, 750, 50),
            pygame.Rect(780, 633, 800, 50),
            pygame.Rect(2180, 752, 700, 50),
            pygame.Rect(1022, 180, 700, 50),
            pygame.Rect(1827, 188, 700, 50),
            pygame.Rect(1315, 950, 750, 50),
            pygame.Rect(0, 0, 2, 1500),
            pygame.Rect(2559 , 0, 2, 1500)

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
            pygame.Rect(1315, 934, 780, 50)
        ]

        self.boxes = [
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
        ]
        self.box_collision_debugged = False

    def check_wall_collision(self, player):
        for wall in self.walls:
            if player.rect.colliderect(wall):
                player.collision_type = 'wall'
                if player.velocity_x > 0:
                    if player.rect.right >= wall.left:
                        player.rect.right = wall.left
                        player.velocity_y = -10
                        return True


                if player.velocity_y > 0:
                    if player.rect.right >= wall.left:
                        player.rect.right = wall.left
                        player.velocity_x = 0
                        player.velocity_y = 7
                        return True


                elif player.velocity_y < 0:
                    if player.rect.left <= wall.right:
                        player.rect.left = wall.right
                        player.velocity_x = 0
                        player.velocity_y = 7
                        return True

        return False

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

    def check_ground_collision(self, player):
        if player.rect.bottom > self.ground_y:
            player.collision_type = 'ground'
            player.rect.bottom = self.ground_y
            return True
        return False

    def check_platform_collision(self, player):
        for platform in self.platforms:
            if platform.colliderect(player.rect):
                player.on_ground = True
                player.collision_type = 'platform'
                if player.velocity_y > 0:
                    player.rect.bottom = platform.top
                    player.velocity_y = -1.5
                    player.on_ground = True
                    return True
        return False

    def check_box_collision(self, player):
        for box in self.boxes:
            if player.rect.colliderect(box):
                player.collision_type = 'box'
                if player.velocity_y >= 0:
                    player.rect.bottom = box.top
                    player.velocity_y = -1.5
                    player.velocity_x = 0
                    player.on_ground = True
                    return True
        return False


    def draw_collision_debug(self, screen):
        pass