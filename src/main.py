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
facing_right = True

# ---------- Sandwich ----------
sandwich = pygame.Rect((765, 160, 30, 40))
sandwich_collected = False
can_shoot = False
shoot_cooldown = 0
shoot_delay = 20

bullets = []

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
        facing_right = False
    if key[pygame.K_d]:
        player_x += player_speed 
    facing_right = True
    
    if key[pygame.K_j] and can_shoot and shoot_cooldown == 0:
        if facing_right:
            bullet = pygame.Rect(player.right, player.centery - 5, 10, 10)
            bullets.append([bullet, 1])
        else:
            bullet = pygame.Rect(player.left - 10, player.centery -5, 10, 10)
            bullets.append([bullet, -1])
        
        shoot_cooldown = shoot_delay
    
    player.x = int(player_x)
    
    #Jump
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
    for platform in solid_platforms:
        if player.colliderect(platform):
            if previous_player.bottom <= platform.top and player_velocity_y > 0:
                player.bottom = platform.top 
                player_y = player.y
                player_velocity_y = 0 
                on_ground = True
            elif previous_player.top >= platform.bottom and player_velocity_y < 0:
                player.top = platform.bottom
                player_y = player.y
                player_velocity_y = 0
            elif previous_player.right <= platform.left:
                player.right = platform.left
                player_x = player.x
            elif previous_player.left >= platform.right:
                player.left = platform.right
                player_x = player.x 
    
    
    if not sandwich_collected and player.colliderect(sandwich):
        sandwich_collected = True
        can_shoot = True
    
    for bullet_data in bullets:
        bullet = bullet_data[0]
        direction = bullet_data[1]
        bullet.x += 8 * direction
    
    for bullet_data in bullets[:]:
        bullet = bullet_data[0]
        if bullet.right < 0 or bullet.left > WIDTH:        # If the bullet goes out the window, it's remove from list
            bullets.remove(bullet_data)
    
    if shoot_cooldown > 0:
        shoot_cooldown -= 1
    
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
    
    #One way platforms  
    for platform in one_way_platforms:
        pygame.draw.rect(screen, (255, 255, 255),platform)
    
    #solid platforms
    for platform in solid_platforms:
        pygame.draw.rect(screen, (255, 140, 0), platform)
    
    #Sandwich
    if not sandwich_collected:
        pygame.draw.rect(screen,(0, 255, 255), sandwich)
    
    #Bullet
    for bullet_data in bullets:
        bullet = bullet_data[0]
        pygame.draw.rect(screen, (255, 255, 0), bullet)
    
    pygame.display.update() 
    clock.tick(60)
pygame.quit()