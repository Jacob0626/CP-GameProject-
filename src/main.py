import pygame


pygame.init()
width = 1000
height = 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Mini Boss Fight")

player_velocity_y = 0
gravity = 0.4
jump_strength = -11
ground_y = 460

player = pygame.Rect((200, 460, 50, 50))
grass = pygame.Rect((0, 510, 1000, 20))
soil = pygame.Rect((0, 530, 1000, 80))

run = True
while run:
    screen.fill((0,0,0))
    
    pygame.draw.rect(screen, (255, 0, 0), player)
    pygame.draw.rect(screen, (0, 180, 0), grass)
    pygame.draw.rect(screen, (139, 69, 19), soil)
    
    key = pygame.key.get_pressed()
    if key[pygame.K_a] == True:
        player.move_ip(-1,0) 
    elif pygame.key.get_pressed():
        if key[pygame.K_d] == True:
            player.move_ip(1,0) 
    
    if key[pygame.K_SPACE] and player.y == ground_y:
        player_velocity_y = jump_strength
    
    player_velocity_y += gravity
    player.y += int(player_velocity_y)
    
    if player.y > ground_y:
        player.y = ground_y
        player_velocity_y = 0
    
    if player.left < 0:
        player.left = 0
    if player.right > width:
        player.right = width
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    pygame.display.update() 
pygame.quit()