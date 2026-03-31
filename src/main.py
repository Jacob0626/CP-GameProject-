import pygame


pygame.init()
width = 1000
height = 600
screen = pygame.display.set_mode((width, height))

player = pygame.Rect((200, 350, 50, 50))
ground = pygame.Rect((0,550, 1000, 50))

run = True
while run:
    screen.fill((0,0,0))
    
    pygame.draw.rect(screen, (255, 0, 0), player)
    pygame.draw.rect(screen, (6528, 0, 0), ground)
    key = pygame.key.get_pressed()
    if key[pygame.K_a] == True:
        player.move_ip(-1,0) 
    elif pygame.key.get_pressed():
        if key[pygame.K_d] == True:
            player.move_ip(1,0) 
    
    if player.left < 0:
        player.left = 0
    if player.right > width:
        player.right = width
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    pygame.display.update() 
pygame.quit()