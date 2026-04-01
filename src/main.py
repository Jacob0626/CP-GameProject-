import pygame

pygame.init()
pygame.display.set_caption("Mini Boss Fight")

width = 1000
height = 600
screen = pygame.display.set_mode((width, height))

gravity = 0.03
jump_strength = -3.0
player_speed = 0.5
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

#solid platforms
platform3 = pygame.Rect((345, 300, 295, 15))

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
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
    
    
    if player.left < 0:
        player.left = 0
        player_x = 0
    if player.right > width:
        player.right = width
        player_x = player.x 
    
    screen.fill((0,0,0))
    pygame.draw.rect(screen, (255, 0, 0), player)
    pygame.draw.rect(screen, (0, 180, 0), grass)
    pygame.draw.rect(screen, (139, 69, 19), soil)
    pygame.draw.rect(screen, (255, 255, 255), platform1)
    pygame.draw.rect(screen, (255, 255, 255), platform2)
    pygame.draw.rect(screen, (255, 140, 0), platform3)
    
    
    pygame.display.update() 
pygame.quit()