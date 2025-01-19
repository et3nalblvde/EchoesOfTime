import pygame
import os
import re


from collision import CollisionLevel1  


base_folder = os.path.dirname(os.path.abspath(__file__))
sprite_folder = os.path.join(base_folder, '..', 'assets', 'sprites')

def load_animations(folder, animation_names, scale_factor=2):
    animations = {}
    for anim in animation_names:
        anim_folder = os.path.join(folder, anim)
        files = sorted([f for f in os.listdir(anim_folder) if f.endswith(('.png', '.jpg', '.jpeg'))],
                       key=lambda f: int(re.search(r'(\d+)', f).group(1) if re.search(r'(\d+)', f) else -1))
        animations[anim] = []
        for file in files:
            image = pygame.image.load(os.path.join(anim_folder, file))
            scaled_image = pygame.transform.scale(image, (
                image.get_width() * scale_factor, image.get_height() * scale_factor))
            animations[anim].append(scaled_image)
    return animations


animation_names = ["idle", "run", "jump", "fall", "death", "attack"]
player_animations = load_animations(sprite_folder, animation_names)

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        
        self.x = x
        self.y = y
        self.state = "idle"
        self.animations = player_animations
        self.frame_index = 0
        self.image = self.animations[self.state][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)
        self.on_platform = False
        self.scale_factor = 2
        self.velocity_x = 0
        self.velocity_y = 0
        self.speed = 5
        self.gravity = 0.5
        self.jump_strength = -16
        self.on_ground = False
        self.on_ladder = False
        self.animation_counter = 0
        self.facing_left = False
        self.health = 3
        self.last_direction = None
        self.last_jump_time = 0
        self.jump_delay = 500
        self.collision_type = 'none'
        
        self.boxes = [pygame.Rect(1000, 1000, 100, 50), pygame.Rect(1500, 950, 100, 50)]  
        self.animation_delays = {
            "idle": 200,
            "run": 4,
            "jump": 10,
            "fall": 10,
            "death": 10,
            "attack": 10
        }

        
        self.collision = CollisionLevel1()

    def update(self):
        if self.health <= 0:
            self.change_state("death")
            self.frame_index = len(self.animations["death"]) - 1
            self.image = self.animations["death"][self.frame_index]
            self.rect = self.image.get_rect()
            self.rect.topleft = (self.x, self.y)
        else:
            self.animation_counter += 1
            if self.animation_counter >= self.animation_delays[self.state]:
                self.frame_index = (self.frame_index + 1) % len(self.animations[self.state])
                self.image = self.animations[self.state][self.frame_index]

                self.image = pygame.transform.scale(self.image, (
                    self.image.get_width() * self.scale_factor, self.image.get_height() * self.scale_factor))

                if self.facing_left:
                    self.image = pygame.transform.flip(self.image, True, False)

                self.rect = self.image.get_rect()
                self.rect.topleft = (self.x, self.y)

                self.animation_counter = 0

            if self.on_ladder:
                self.velocity_y = 0

                keys = pygame.key.get_pressed()
                if keys[pygame.K_UP]:
                    self.y -= 10
                    self.change_state("idle")
                elif keys[pygame.K_DOWN]:
                    self.y += 10
                    self.change_state("idle")
            else:
                if not self.on_platform:
                    self.velocity_y += self.gravity

                self.y += self.velocity_y

            self.on_platform = self.collision.check_platform_collision(self)

            
            self.on_boxes = self.check_box_collision()  

            if self.on_boxes:
                
                self.x += self.velocity_x

            self.handle_collisions()

            if self.y >= 1228:
                self.y = 1228
                self.velocity_y = 0
                self.on_ground = True
            else:
                self.on_ground = False

            self.x += self.velocity_x
            self.rect.topleft = (self.x, self.y)

    def handle_collisions(self):
        if not self.collision.check_wall_collision(self):
            self.x += self.velocity_x
        else:
            if self.collision_type == 'wall':
                if self.velocity_x > 0:
                    if self.rect.right + 5 >= self.collision.walls[0].left:
                        self.rect.right = self.collision.walls[0].left - 5
                        self.velocity_x = 0
                    else:
                        self.x += self.velocity_x
                elif self.velocity_x < 0:
                    if self.rect.left - 5 <= self.collision.walls[0].right:
                        self.rect.left = self.collision.walls[0].right + 5
                        self.velocity_x = 0
                    else:
                        self.x += self.velocity_x
            if abs(self.velocity_x) > 0:
                if self.rect.colliderect(self.collision.walls[0]):
                    if self.velocity_x > 0:
                        while self.rect.colliderect(self.collision.walls[0]):
                            self.rect.x -= 1000
                        self.velocity_x = 0
                    elif self.velocity_x < 0:
                        while self.rect.colliderect(self.collision.walls[0]):
                            self.rect.x += 1
                        self.velocity_x = 0

        self.velocity_x = 0

    def check_box_collision(self):
        for box in self.boxes:
            if self.rect.colliderect(box):
                self.rect.y = box.top - self.rect.height  
                self.velocity_y = 0  
                return True
        return False

    def take_damage(self, amount):
        self.health -= amount
        if self.health < 0:
            self.health = 0

    def change_state(self, new_state):
        if new_state == "death" or (new_state != "idle" and new_state in self.animations and new_state != self.state):
            self.state = new_state
            self.frame_index = 0
            self.image = self.animations[self.state][self.frame_index]

            self.image = pygame.transform.scale(self.image, (
                self.image.get_width() * self.scale_factor, self.image.get_height() * self.scale_factor))

            if self.facing_left:
                self.image = pygame.transform.flip(self.image, True, False)

            self.rect = self.image.get_rect()
            self.rect.topleft = (self.x, self.y)

    def move_left(self):
        self.velocity_x = -self.speed
        self.change_state("run")
        self.facing_left = True

    def move_right(self):
        self.velocity_x = self.speed
        self.change_state("run")
        self.facing_left = False

    def jump(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_jump_time >= self.jump_delay and (
                self.on_ground or self.on_platform or self.on_ladder):
            self.velocity_y = self.jump_strength
            self.change_state("jump")
            self.last_jump_time = current_time

    def stop(self):
        self.velocity_x = 0
        if self.on_ground and not self.on_ladder:
            self.change_state("idle")

    def attack(self):
        self.change_state("attack")

    def is_death_animation_finished(self):
        if self.state == "death" and self.frame_index == len(self.animations["death"]) - 1:
            return True
        return False

    def climb_ladder(self):
        self.on_ladder = True
        self.change_state("idle")
        self.velocity_y = 0
