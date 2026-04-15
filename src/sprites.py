import pygame

class Player:
    def __init__(self):
        self.x = 40
        self.y = 460
        self.rect = pygame.Rect(int(self.x), 460, 50, 50)
        self.velocity_y = 0
        self.on_ground = True
        self.facing_right = True
        self.hits = 0
        self.can_shoot = False
    
    def reset(self):
        self.x = 40
        self.y = 460
        self.rect = pygame.Rect(int(self.x), 460, 50, 50)
        self.velocity_y = 0
        self.on_ground = True
        self.facing_right = True
        self.hits = 0
        self.can_shoot = False
    
    def take_hit(self):
        self.hits += 1
    
    def jump(self, jump_strength):
        if self.on_ground:
            self.velocity_y = jump_strength
            self.on_ground = False
    
    def apply_gravity(self, gravity):
        self.velocity_y += gravity
        self.y += self.velocity_y
        self.rect.y = int(self.y)
        self.on_ground = False

class Boss:
    def __init__(self):
        self.rect = pygame.Rect(800, 130, 50, 70)
        self.max_hp = 10
        self.hp = 10
        self.shoot_cooldown = 0
        self.shoot_delay = 75
        self.speed = 2
        self.direction = 1
        self.left_limit = 765
        self.right_limit = 990
    
    def reset(self):
        self.rect.x = 800
        self.rect.y = 130
        self.hp = self.max_hp
        self.shoot_cooldown = 0
        self.direction = 1
    
    def update_movement(self):
        self.rect.x += self.speed * self.direction
        
        if self.rect.left <= self.left_limit:
            self.rect.left = self.left_limit
            self.direction = 1
        
        if self.rect.right >= self.right_limit:
            self.rect.right = self.right_limit
            self.direction = -1
    
    def take_damage(self):
        self.hp -= 1
        if self.hp < 0:
            self.hp = 0