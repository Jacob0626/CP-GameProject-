import pygame


pygame.init()
width = 1000
height = 600
screen = pygame.display.set_mode((width, height))

player = pygame.Rect((200, 350, 50, 50))


run = True
while run:
    
    pygame.draw.rect(screen, (255, 0, 0), player)
    
    key = pygame.key.get_pressed()
    if key[pygame.K_a] == True:
        player.move_ip(-1,0) 
    elif pygame.key.get_pressed():
        if key[pygame.K_d] == True:
            player.move_ip(1,0) 
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    pygame.display.update() 
pygame.quit()