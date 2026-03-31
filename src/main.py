import pygame


pygame.init()
width = 1000
height = 600
screen = pygame.display.set_mode((width, height))

player = pygame.Rect((200, 350, 50, 50))


run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
pygame.quit()