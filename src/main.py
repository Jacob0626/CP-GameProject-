import pygame
from sprites import Player, Boss

# ---------- Game setup ----------
pygame.init()
pygame.display.set_caption("Mini Boss Fight")

WIDTH = 1000
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

font = pygame.font.SysFont(None, 60)
small_font = pygame.font.SysFont(None, 35)

# ---------- Constants ----------
gravity = 0.6 
jump_strength = -14
player_speed = 5
ground_y = 460

shoot_delay = 30

# ---------- Game State ---------- 
victory = False
game_over = False

# ---------- Player ----------
player = Player()

# ---------- Boss ----------
boss = Boss()
boss_bar_bg = pygame.Rect(780, 25, 200, 15)
boss_bullets = []

# ---------- Sandwich ----------
sandwich = pygame.Rect((940, 160, 30, 40))
sandwich_collected = False

# ---------- Bullets ----------
bullets = []
shoot_cooldown = 0

# ---------- Ground ----------
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


# ---------- Functions ----------
def reset_game():
    global game_over, victory
    global sandwich_collected
    global bullets, boss_bullets
    global shoot_cooldown
    
    game_over = False
    victory = False
    
    player.reset()
    boss.reset()
    
    sandwich_collected = False
    
    bullets = []
    boss_bullets = []
    
    shoot_cooldown = 0


def handle_player_input(key):
    global shoot_cooldown, bullets
    
    if key[pygame.K_a]:
        player.x -= player_speed
        player.facing_right = False
    if key[pygame.K_d]:
        player.x += player_speed 
        player.facing_right = True
    
    if key[pygame.K_j] and player.can_shoot and shoot_cooldown == 0:
        if player.facing_right:
            bullet = pygame.Rect(player.rect.right, player.rect.centery - 5, 10, 10)
            bullets.append([bullet, 1])
        else:
            bullet = pygame.Rect(player.rect.left - 10, player.rect.centery -5, 10, 10)
            bullets.append([bullet, -1])
        
        shoot_cooldown = shoot_delay
    
    if key[pygame.K_SPACE] and player.on_ground:
            player.velocity_y = jump_strength
            player.on_ground = False



def apply_gravity():
    player.velocity_y += gravity
    player.y += player.velocity_y
    player.rect.y = int(player.y)
    
    player.on_ground = False



def handle_ground_collision():
    if player.rect.y >= ground_y:
        player.rect.y = ground_y
        player.y = ground_y 
        player.velocity_y = 0
        player.on_ground = True



def handle_one_way_collisions():
    if player.velocity_y > 0:
        for platform in one_way_platforms:
            if player.rect.colliderect(platform):
                player.rect.bottom = platform.top
                player.y = player.rect.y
                player.velocity_y = 0
                player.on_ground = True 



def handle_solid_collisions(previous_player):
    for platform in solid_platforms:
        if player.rect.colliderect(platform):
            if previous_player.bottom <= platform.top and player.velocity_y > 0:
                player.rect.bottom = platform.top 
                player.y = player.rect.y
                player.velocity_y = 0 
                player.on_ground = True
            elif previous_player.top >= platform.bottom and player.velocity_y < 0:
                player.rect.top = platform.bottom
                player.y = player.rect.y
                player.velocity_y = 0
            elif previous_player.right <= platform.left:
                player.rect.right = platform.left
                player.x = player.rect.x
            elif previous_player.left >= platform.right:
                player.rect.left = platform.right
                player.x = player.rect.x 



def handle_sandwich_pickup():
    if not sandwich_collected and player.rect.colliderect(sandwich):
        player.can_shoot = True
        return True
    return sandwich_collected



def keep_player_inside_screen():
    if player.rect.left < 0:
        player.rect.left = 0
        player.x = 0
    if player.rect.right > WIDTH:
        player.rect.right = WIDTH
        player.x = player.rect.x

def update_player_bullets():
    global shoot_cooldown, victory, bullets
    
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
        if bullet.colliderect(boss.rect):
            boss.take_damage()
            bullets.remove(bullet_data)
        
        if boss.hp == 0:
            victory = True



def update_boss_bullets():
    global game_over, boss_bullets
    
    if boss.shoot_cooldown == 0 and not victory:
        if player.rect.centerx < boss.rect.centerx:
            boss_bullet_direction = -1
            boss_bullet = pygame.Rect(boss.rect.left - 10, boss.rect.centery - 5, 10, 10)
        else:
            boss_bullet_direction = 1
            boss_bullet = pygame.Rect(boss.rect.right, boss.centery - 5, 10, 10)
    
        boss_bullets.append([boss_bullet, boss_bullet_direction])
        boss.shoot_cooldown = boss.shoot_delay
    
    for bullet_data in boss_bullets:
        bullet = bullet_data[0]
        direction = bullet_data[1]
        bullet.x += 6 * direction
    
    for bullet_data in boss_bullets[:]:
        bullet = bullet_data[0]
        if bullet.right <0 or bullet.left > WIDTH:
            boss_bullets.remove(bullet_data)
    
    if boss.shoot_cooldown > 0:
        boss.shoot_cooldown -= 1
    
    for bullet_data in boss_bullets[:]:
        bullet = bullet_data[0]
        if bullet.colliderect(player.rect):
            player.hits += 1
            boss_bullets.remove(bullet_data)
    
    if player.hits >= 3:
        game_over = True


def draw_game():
    screen.fill((0, 0, 0))
    
    #Player
    pygame.draw.rect(screen, (255, 0, 0), player.rect)
    
    #player lives 
    player_lives = 3 - player.hits
    for i in range(player_lives):
        pygame.draw.rect(screen, (255, 0, 0), (20 + i * 35, 20, 25, 25))
    
    #Boss
    pygame.draw.rect(screen, (255, 0, 0), boss.rect)
    
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
        
    #Player bullets
    for bullet_data in bullets:
        bullet = bullet_data[0]
        pygame.draw.rect(screen, (255, 255, 0), bullet)
    
    #Boss HP bar
    current_bar_width = (boss.hp / boss.max_hp) * boss_bar_bg.width
    boss_bar_current = pygame.Rect(
        boss_bar_bg.x,
        boss_bar_bg.y,
        int(current_bar_width),
        boss_bar_bg.height
    )
    pygame.draw.rect(screen, (80, 80, 80), boss_bar_bg)
    pygame.draw.rect(screen, (255, 0, 0), boss_bar_current)
    
    #Boss bullets
    for bullet_data in boss_bullets:
        bullet = bullet_data[0]
        pygame.draw.rect(screen, (0, 0, 225), bullet)
    
    #Game over text
    if game_over:
        game_over_text = font.render("GAME OVER", True, (255, 255, 255))
        screen.blit(game_over_text, (330, 220))
        
        restart_text = small_font.render("Press R to Restart", True, (255, 255, 255))
        screen.blit(restart_text, (355, 320))
    
    #Victory text
    if victory:
        victory_text = font.render("YOU WIN!", True,(255, 255, 255))
        screen.blit(victory_text, (360, 220))
        
        restart_text = small_font.render("Press R to Restart", True, (255, 255, 255))
        screen.blit(restart_text, (345, 300))


#---------- Main game loop ----------
run = True
while run:
    # Quit event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    previous_player = player.rect.copy()    # Save previous player position for solid platform collision checks 
    key = pygame.key.get_pressed()
    
    if not game_over and not victory:
        boss.update_movement()
        
        handle_player_input(key)
        
        player.rect.x = int(player.x)
        
        apply_gravity()
        handle_ground_collision()
        handle_one_way_collisions()
        handle_solid_collisions(previous_player)
        
        sandwich_collected = handle_sandwich_pickup()
        
        update_player_bullets()
        update_boss_bullets()
        
        keep_player_inside_screen()
    
    if (game_over or victory) and key[pygame.K_r]:
        reset_game()
    
    draw_game()
    pygame.display.update() 
    clock.tick(60)

pygame.quit()    