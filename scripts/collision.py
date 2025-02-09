import pygame

class CollisionLevel1:
    def __init__(self, ):
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

    import math

    def check_collisions(self, player, objects):

        player.on_ground = True
        new_x = player.x + player.velocity_x
        new_y = player.y + player.velocity_y

        temp_rect = player.rect.copy()
        temp_rect.topleft = (new_x, new_y)

        horizontal_collision = False
        vertical_collision = False

        for obj in objects:
            if temp_rect.colliderect(obj):
                player_center = (temp_rect.centerx, temp_rect.centery)
                obj_center = (obj.centerx, obj.centery)

                dx = player_center[0] - obj_center[0]
                dy = player_center[1] - obj_center[1]

                overlap_x = (temp_rect.width / 2) + (obj.width / 2) - abs(dx)
                overlap_y = (temp_rect.height / 2) + (obj.height / 2) - abs(dy)

                if overlap_x > 0 and overlap_y > 0:
                    if overlap_x < overlap_y:
                        if dx > 0:
                            player.x += overlap_x
                        else:
                            player.x -= overlap_x
                        player.velocity_x = 0
                        horizontal_collision = True
                    else:
                        if dy > 0:
                            player.y += overlap_y
                            player.velocity_y = 0
                            player.on_ground = True
                            if player.state == "jump":
                                player.change_state("idle")
                        else:
                            player.y -= overlap_y
                            player.velocity_y = 0
                        vertical_collision = True

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

        for ladder in self.ladders:
            pygame.draw.rect(screen, (255, 0, 0), ladder, 6)
        for wall in self.walls:
            pygame.draw.rect(screen, (0, 0, 0), wall, 6)
        for platform in self.platforms:
            pygame.draw.rect(screen, (0, 255, 0), platform, 6)
        for box in self.boxes:
            pygame.draw.rect(screen, (0, 0, 255), box, 6)


import pygame

class CollisionLevel2:
    def __init__(self, ):
        self.ladders = [
            pygame.Rect(2202, 306, 50, 340),
            pygame.Rect(500, 157, 50, 270),
            pygame.Rect(1170, 1281, 90, 90),
            pygame.Rect(345, 960, 60, 340),
            pygame.Rect(2190,1166 ,50, 90)


        ]
        self.walls = [
            pygame.Rect(0, 0, 2, 1500),
            pygame.Rect(2559, 0, 2, 1500)
        ]
        self.platforms = [
            pygame.Rect(1767, 688, 524, 90),
            pygame.Rect(2300, 973, 524, 90),
            pygame.Rect(1660, 1161, 524, 90),
            pygame.Rect(407, 957, 1254, 90),
            pygame.Rect(2277, 298, 524, 90),
            pygame.Rect(1546, 87, 524, 90),
            pygame.Rect(1010, 316, 524, 90),
            pygame.Rect(434, 439, 504, 90),
            pygame.Rect(0, 157, 484, 90),
            pygame.Rect(0, 1365, 2560, 50)
        ]
        self.boxes = [
            pygame.Rect(904, 1280, 90, 90),
            pygame.Rect(1138, 1192, 90, 90),
            pygame.Rect(1091, 1280, 90, 90),
            pygame.Rect(1170, 1281, 90, 90),
            pygame.Rect(1391, 1327, 125, 90),
            pygame.Rect(1410, 1242, 90, 90),
            pygame.Rect(2016, 1077, 90, 90),
            pygame.Rect(1270, 873, 90, 90),
            pygame.Rect(1900, 604, 90, 90),
            pygame.Rect(1234, 230, 90, 90),
            pygame.Rect(710, 358, 90, 90),

        ]

    def check_collisions(self, player, objects):

        player.on_ground = True
        new_x = player.x + player.velocity_x
        new_y = player.y + player.velocity_y

        temp_rect = player.rect.copy()
        temp_rect.topleft = (new_x, new_y)

        horizontal_collision = False
        vertical_collision = False

        for obj in objects:
            if temp_rect.colliderect(obj):
                player_center = (temp_rect.centerx, temp_rect.centery)
                obj_center = (obj.centerx, obj.centery)

                dx = player_center[0] - obj_center[0]
                dy = player_center[1] - obj_center[1]

                overlap_x = (temp_rect.width / 2) + (obj.width / 2) - abs(dx)
                overlap_y = (temp_rect.height / 2) + (obj.height / 2) - abs(dy)

                if overlap_x > 0 and overlap_y > 0:
                    if overlap_x < overlap_y:
                        if dx > 0:
                            player.x += overlap_x
                        else:
                            player.x -= overlap_x
                        player.velocity_x = 0
                        horizontal_collision = True
                    else:
                        if dy > 0:
                            player.y += overlap_y
                            player.velocity_y = 0
                            player.on_ground = True
                            if player.state == "jump":
                                player.change_state("idle")
                        else:
                            player.y -= overlap_y
                            player.velocity_y = 0
                        vertical_collision = True

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
        for ladder in self.ladders:
            pygame.draw.rect(screen, (255, 0, 0), ladder, 6)
        for wall in self.walls:
            pygame.draw.rect(screen, (0, 0, 0), wall, 6)
        for platform in self.platforms:
            pygame.draw.rect(screen, (0, 255, 0), platform, 6)
        for box in self.boxes:
            pygame.draw.rect(screen, (0, 0, 255), box, 6)