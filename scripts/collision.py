import pygame

class CollisionLevel1:
    def __init__(self):
        self.ladders = [pygame.Rect(514, 1059, 50, 230), pygame.Rect(2423, 431, 50, 200)]
        self.ground_y = 1235
        self.walls = [
            pygame.Rect(600, 1120, 500, 250),  
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
            pygame.Rect(1315, 934, 500, 50)  
        ]
        
        self.boxes = [
            pygame.Rect(1091, 1145, 90, 90),
            pygame.Rect(1091, 1232, 90, 90),
            pygame.Rect(1177, 1232, 90, 90),
            
            pygame.Rect(1500, 900, 50, 50),   
        ]
        self.box_collision_debugged = False  

    def check_wall_collision(self, player):
        for wall in self.walls:
            if player.rect.colliderect(wall):
                player.collision_type = 'wall'  

                
                if player.velocity_x > 0:
                    if player.rect.right >= wall.left:  
                        player.rect.right = wall.left  
                        player.velocity_x = 0  
                        return True  

                
                elif player.velocity_x < 0:
                    if player.rect.left <= wall.right:  
                        player.rect.left = wall.right  
                        player.velocity_x = 0  
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
                player.collision_type = 'platform'  

                
                if player.rect.bottom <= platform.top and player.velocity_y >= 0:
                    player.rect.bottom = platform.top  
                    player.velocity_y = 0  

                    
                    player.rect.x += player.velocity_x  

                    
                    if player.rect.left < platform.left:
                        player.rect.left = platform.left  
                    elif player.rect.right > platform.right:
                        player.rect.right = platform.right  

                
                elif player.rect.bottom > platform.top and player.velocity_y > 0:
                    
                    player.rect.bottom = platform.top  
                    player.velocity_y = 0  

                    
                    player.rect.x += player.velocity_x

                    
                    if player.rect.left < platform.left:
                        player.rect.left = platform.left
                    elif player.rect.right > platform.right:
                        player.rect.right = platform.right

                    return True  

        return False  

    def check_box_collision(self, player):
        for box in self.boxes:
            if player.rect.colliderect(box):
                player.collision_type = 'box'  

                
                if player.velocity_y > 0:
                    if player.rect.bottom <= box.top:  
                        player.rect.bottom = box.top  
                        player.rect.x += player.velocity_x  
                        return True  

                
                elif player.velocity_y < 0:
                    if player.rect.top >= box.bottom:  
                        player.rect.top = box.bottom  
                        player.velocity_y = 0  
                        return True  

                
                if player.velocity_x > 0:  
                    if player.rect.right >= box.left:  
                        player.rect.right = box.left  
                        
                        return True  

                elif player.velocity_x < 0:  
                    if player.rect.left <= box.right:  
                        player.rect.left = box.right  
                        
                        return True  

        return False  

    def draw_collision_debug(self, screen):
        
        for ladder in self.ladders:
            pygame.draw.rect(screen, (255, 0, 0), ladder, 6)  
        for wall in self.walls:
            pygame.draw.rect(screen, (0, 0, 0), wall, 6)  
        for platform in self.platforms:
            pygame.draw.rect(screen, (0, 255, 0), platform, 6)  
        for box in self.boxes:
            pygame.draw.rect(screen, (0, 0, 255), box, 6)  
