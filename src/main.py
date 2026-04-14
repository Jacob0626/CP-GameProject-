import pygame

# ---------- Game setup ----------
pygame.init()
pygame.display.set_caption("Mini Boss Fight")

victory = False
game_over = False
font = pygame.font.SysFont(None, 60)
small_font = pygame.font.SysFont(None, 35)


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
player_hits = 0

# ----- Boss -----
boss = pygame.Rect((800, 130, 50, 70))
boss_max_hp = 10
boss_hp = 10
boss_bar_bg = pygame.Rect(780, 25, 200, 15)
boss_bullets = []
boss_shoot_cooldown = 0
boss_shoot_delay = 75
boss_speed = 2
boss_direction = 1
boss_left_limit = 765
boss_right_limit = 990

# ---------- Sandwich ----------
sandwich = pygame.Rect((940, 160, 30, 40))
sandwich_collected = False
can_shoot = False
shoot_cooldown = 0
shoot_delay = 30

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

def reset_game():
    global game_over, victory
    global player_x, player_y, player_velocity_y, player, on_ground, facing_right, player_hits
    global sandwich_collected, can_shoot
    global bullets, boss_bullets
    global boss_hp
    global shoot_cooldown, boss_shoot_cooldown
    global boss, boss_direction
    
    game_over = False
    victory = False
    
    player_x = 40
    player_y = 460
    player_velocity_y = 0
    player = pygame.Rect((int(player_x), 460, 50, 50))
    on_ground = True
    facing_right = True
    player_hits = 0
    
    sandwich_collected = False
    can_shoot = False
    
    bullets = []
    boss_bullets = []
    
    boss_hp = boss_max_hp
    
    shoot_cooldown = 0
    boss_shoot_cooldown = 0
    
    boss.x = 800
    boss_direction = 1

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
    if not game_over and not victory:
        boss.x += boss_speed * boss_direction
        if boss.left <= boss_left_limit:
            boss.left = boss_left_limit
            boss_direction = 1
        
        if boss.right >= boss_right_limit:
            boss.right = boss_right_limit
            boss_direction = -1
        
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
        
        for bullet_data in bullets[:]:
            bullet = bullet_data[0]
            if bullet.colliderect(boss):
                boss_hp -= 1
                bullets.remove(bullet_data)
            if boss_hp < 0:
                boss_hp = 0
            if boss_hp == 0:
                victory = True
        
        
        if boss_shoot_cooldown == 0 and not victory:
            if player.centerx < boss.centerx:
                boss_bullet_direction = -1
                boss_bullet = pygame.Rect(boss.left - 10, boss.centery - 5, 10, 10)
            else:
                boss_bullet_direction = 1
                boss_bullet = pygame.Rect(boss.right, boss.centery - 5, 10, 10)
            boss_bullets.append([boss_bullet, boss_bullet_direction])
            boss_shoot_cooldown = boss_shoot_delay
        
        for bullet_data in boss_bullets:
            bullet = bullet_data[0]
            direction = bullet_data[1]
            bullet.x += 6 * direction
        
        for bullet_data in boss_bullets[:]:
            bullet = bullet_data[0]
            if bullet.right <0 or bullet.left > WIDTH:
                boss_bullets.remove(bullet_data)
        
        if boss_shoot_cooldown > 0:
            boss_shoot_cooldown -= 1
        
        for bullet_data in boss_bullets[:]:
            bullet = bullet_data[0]
            if bullet.colliderect(player):
                player_hits += 1
                boss_bullets.remove(bullet_data)
        
        if player_hits >= 3:
            game_over = True
        
        # ---- Keeps player inside screen ----
        if player.left < 0:
            player.left = 0
            player_x = 0
        if player.right > WIDTH:
            player.right = WIDTH
            player_x = player.x 
    
    if (game_over or victory) and key[pygame.K_r]:
        reset_game()
    
    player_lives = 3 - player_hits
    
    # ---- Draw everything ----
    screen.fill((0,0,0))
    #Player 
    pygame.draw.rect(screen, (255, 0, 0), player)
    
    for i in range(player_lives):
        pygame.draw.rect(screen, (255, 0, 0), (20 + i * 35, 20, 25, 25))
    
    #Boss
    pygame.draw.rect(screen, (255, 0, 0), boss)
    
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
    
    #Boss HP bar
    current_bar_width = (boss_hp / boss_max_hp) * boss_bar_bg.width
    boss_bar_current = pygame.Rect(
        boss_bar_bg.x,
        boss_bar_bg.y,
        int(current_bar_width),
        boss_bar_bg.height
    )
    pygame.draw.rect(screen, (80, 80, 80), boss_bar_bg)
    pygame.draw.rect(screen, (255, 0, 0), boss_bar_current)
    
    for bullet_data in boss_bullets:
        bullet = bullet_data[0]
        pygame.draw.rect(screen, (0, 0, 225), bullet)
    
    if game_over:
        game_over_text = font.render("GAME OVER", True, (255, 255, 255))
        screen.blit(game_over_text, (330, 220))
        
        restart_text = small_font.render("Press R to Restart", True, (255, 255, 255))
        screen.blit(restart_text, (355, 320))
    
    if victory:
        victory_text = font.render("YOU WIN!", True,(255, 255, 255))
        screen.blit(victory_text, (360, 220))
        
        restart_text = small_font.render("Press R to Restart", True, (255, 255, 255))
        screen.blit(restart_text, (345, 300))
    
    pygame.display.update() 
    clock.tick(60)
pygame.quit()    