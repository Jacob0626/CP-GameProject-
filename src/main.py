import pygame

pygame.init()
pygame.display.set_caption("Mini Boss Fight")

WIDTH = 1000
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))

gravity = 0.03
jump_strength = -3.3
player_speed = 0.6
ground_y = 460

player_x = 40
player = pygame.Rect((int(player_x), 460, 50, 50))
player_y = 460
player_velocity_y = 0 
on_ground = True


grass = pygame.Rect((0, 510, 1000, 20))
soil = pygame.Rect((0, 530, 1000, 80))

# one way platforms
platform1 = pygame.Rect((100, 420, 130, 10))
platform2 = pygame.Rect((770, 420, 130, 10))
platform5 = pygame.Rect((510, 100, 130, 10))

#solid platforms
platform3 = pygame.Rect((345, 300, 295, 15))
platform4 = pygame.Rect((90, 160, 130, 15))
platform6 = pygame.Rect((765, 200, 235, 15))


run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    previous_player = player.copy()
    
    key = pygame.key.get_pressed()
    
    if key[pygame.K_a]:
        player_x -= player_speed
    if key[pygame.K_d]:
        player_x += player_speed 
    
    player.x = int(player_x)
    
    if key[pygame.K_SPACE] and on_ground:
        player_velocity_y = jump_strength
        on_ground = False
    
    player_velocity_y += gravity
    player_y += player_velocity_y 
    player.y = int(player_y)
    
    on_ground = False
    
    if player.y >= ground_y:
        player.y = ground_y
        player_y = ground_y 
        player_velocity_y = 0
        on_ground = True
    
    
    if player_velocity_y > 0:
        if player.colliderect(platform1):
            player.bottom = platform1.top
            player_y = player.y
            player_velocity_y = 0
            on_ground = True 
    
    if player_velocity_y > 0:
        if player.colliderect(platform2):
            player.bottom = platform2.top
            player_y = player.y
            player_velocity_y = 0
            on_ground = True 
    
    if player_velocity_y > 0:
        if player.colliderect(platform5):
            player.bottom = platform5.top
            player_y = player.y
            player_velocity_y = 0
            on_ground = True 
    
    if player.colliderect(platform3):
        if previous_player.bottom <= platform3.top and player_velocity_y > 0:
            player.bottom = platform3.top 
            player_y = player.y
            player_velocity_y = 0 
            on_ground = True
        elif previous_player.top >= platform3.bottom and player_velocity_y < 0:
            player.top = platform3.bottom
            player_y = player.y
            player_velocity_y = 0
        elif previous_player.right <= platform3.left:
            player.right = platform3.left
            player_x = player.x
        elif previous_player.left >= platform3.right:
            player.left = platform3.right
            player_x = player.x 
    
    if player.colliderect(platform4):
        if previous_player.bottom <= platform4.top and player_velocity_y > 0:
            player.bottom = platform4.top 
            player_y = player.y
            player_velocity_y = 0 
            on_ground = True
        elif previous_player.top >= platform4.bottom and player_velocity_y < 0:
            player.top = platform4.bottom
            player_y = player.y
            player_velocity_y = 0
        elif previous_player.right <= platform4.left:
            player.right = platform4.left
            player_x = player.x
        elif previous_player.left >= platform4.right:
            player.left = platform4.right
            player_x = player.x
    
    if player.colliderect(platform6):
        if previous_player.bottom <= platform6.top and player_velocity_y > 0:
            player.bottom = platform6.top 
            player_y = player.y
            player_velocity_y = 0 
            on_ground = True
        elif previous_player.top >= platform6.bottom and player_velocity_y < 0:
            player.top = platform6.bottom
            player_y = player.y
            player_velocity_y = 0
        elif previous_player.right <= platform6.left:
            player.right = platform6.left
            player_x = player.x
        elif previous_player.left >= platform6.right:
            player.left = platform6.right
            player_x = player.x
    
    
    
    if player.left < 0:
        player.left = 0
        player_x = 0
    if player.right > WIDTH:
        player.right = WIDTH
        player_x = player.x 
    
    screen.fill((0,0,0))
    pygame.draw.rect(screen, (255, 0, 0), player)
    pygame.draw.rect(screen, (0, 180, 0), grass)
    pygame.draw.rect(screen, (139, 69, 19), soil)
    pygame.draw.rect(screen, (255, 255, 255), platform1)
    pygame.draw.rect(screen, (255, 255, 255), platform2)
    pygame.draw.rect(screen, (255, 140, 0), platform3)
    pygame.draw.rect(screen, (255, 140, 0), platform4)
    pygame.draw.rect(screen, (255, 255, 255), platform5) 
    pygame.draw.rect(screen, (255, 140, 0), platform6)
    
    pygame.display.update() 
pygame.quit()