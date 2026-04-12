import pygame

# ---------- Game setup ----------
pygame.init()
pygame.display.set_caption("Mini Boss Fight")

WIDTH = 1000
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# ---------- Player movement / physics ----------
gravity = 0.6 
jump_strength = -14
player_speed = 5
ground_y = 460

# ---------- Player ----------
player_x = 40
player = pygame.Rect((int(player_x), 460, 50, 50))
player_y = 460
player_velocity_y = 0 
on_ground = True

# ---------- Ground ---------
grass = pygame.Rect((0, 510, 1000, 20))
soil = pygame.Rect((0, 530, 1000, 80))

#---------- Platforms ----------
# one way platforms 
platform1 = pygame.Rect((100, 420, 130, 10))
platform2 = pygame.Rect((770, 420, 130, 10))    #Player can land on top, but can pass through form below
platform5 = pygame.Rect((510, 100, 130, 10))
one_way_platforms = [platform1, platform2, platform5]

#solid platforms
platform3 = pygame.Rect((345, 300, 295, 15))
platform4 = pygame.Rect((90, 160, 130, 15))     #Player collides from all sides
platform6 = pygame.Rect((765, 200, 235, 15))
solid_platforms = [platform3, platform4, platform6]

#---------- Main game loop ----------
run = True
while run:
    #---- Quit event ----
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    previous_player = player.copy()    # Save previous player position for solid platform collision checks 
    
    # ---- Keyboard input ----
    key = pygame.key.get_pressed()
    
    if key[pygame.K_a]:
        player_x -= player_speed
    if key[pygame.K_d]:
        player_x += player_speed 
    
    player.x = int(player_x)
    
    # ---- Jump ----
    if key[pygame.K_SPACE] and on_ground:
        player_velocity_y = jump_strength
        on_ground = False
    
    # ---- Gravity ----
    player_velocity_y += gravity
    player_y += player_velocity_y 
    player.y = int(player_y)
    
    on_ground = False     # Assume player is in air until floor/platform collision proves otherwise
    
    # ---- Ground collision ----
    if player.y >= ground_y:
        player.y = ground_y
        player_y = ground_y 
        player_velocity_y = 0
        on_ground = True
    
    # ---- One way platform collision ----
    if player_velocity_y > 0:
        for platform in one_way_platforms:
            if player.colliderect(platform):
                player.bottom = platform.top
                player_y = player.y
                player_velocity_y = 0
                on_ground = True 
    
    # ---- Solid platform collision ----
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
    
    
    # ---- Keeps player inside screen ----
    if player.left < 0:
        player.left = 0
        player_x = 0
    if player.right > WIDTH:
        player.right = WIDTH
        player_x = player.x 
    
    # ---- Draw everything ----
    screen.fill((0,0,0))
    #Player 
    pygame.draw.rect(screen, (255, 0, 0), player)
    
    #Ground
    pygame.draw.rect(screen, (0, 180, 0), grass)
    pygame.draw.rect(screen, (139, 69, 19), soil)
    
    # Platforms 
    pygame.draw.rect(screen, (255, 255, 255), platform1)
    pygame.draw.rect(screen, (255, 255, 255), platform2)
    pygame.draw.rect(screen, (255, 140, 0), platform3)
    pygame.draw.rect(screen, (255, 140, 0), platform4)
    pygame.draw.rect(screen, (255, 255, 255), platform5) 
    pygame.draw.rect(screen, (255, 140, 0), platform6)
    
    pygame.display.update() 
    clock.tick(60)
pygame.quit()