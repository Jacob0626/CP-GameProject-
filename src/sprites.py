import pygame

class Player:
    def __init__(self):
        self.x = 40
        self.y = 460
        self.rect = pygame.Rect(int(self.x), 450, 50, 50)
        self.velocity_y = 0
        self.on_ground = True
        self.facing_right = True
        self.hits = 0
        self.can_shoot = False
    
    def reset(self):
        self.x = 40
        self.y = 460
        self.rect = pygame.Rect(int(self.x), 450, 50, 50)
        self.velocity_y = 0
        self.on_ground = True
        self.facing_right = True
        self.hits = 0
        self.can_shoot = False


class Boss:
    def __init__(self):
        self.rect = pygame.Rect(800, 130, 50, 70)
        self.max_hp = 10
        