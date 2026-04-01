import pygame

pygame.init()
pygame.display.set_caption("Mini Boss Fight")

width = 1000
height = 600
screen = pygame.display.set_mode((width, height))

gravity = 0.35
jump_strength = -8.5
player_speed = 3
ground_y = 460

player = pygame.Rect((200, 460, 50, 50))
player_y = 460
player_velocity_y = 0 
on_ground = True

grass = pygame.Rect((0, 510, 1000, 20))
soil = pygame.Rect((0, 530, 1000, 80))

run = True
while run:
    screen.fill((0,0,0))
    
    key = pygame.key.get_pressed()
    
    if key[pygame.K_a]:
        player.x -= player_speed
    if key[pygame.K_d]:
        player.x += player_speed
    
    
    if key[pygame.K_SPACE] and on_ground:
        player_velocity_y = jump_strength
        on_ground = False
    
    player_velocity_y += gravity
    player_y += player_velocity_y 
    player.y += int(player_y)
    
    if player.y > ground_y:
        player.y = ground_y
        player_y = ground_y 
        player_velocity_y = 0
        on_ground = True
    
    if player.left < 0:
        player.left = 0
    if player.right > width:
        player.right = width
    
    
    pygame.draw.rect(screen, (255, 0, 0), player)
    pygame.draw.rect(screen, (0, 180, 0), grass)
    pygame.draw.rect(screen, (139, 69, 19), soil)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    pygame.display.update() 
pygame.quit()