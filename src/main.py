import pygame
from sprites import Player, Boss

# ---------- Game setup ----------
pygame.init()
pygame.display.set_caption("Mini Boss Fight")

WIDTH = 1000
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

font = pygame.font.SysFont("timesnewroman", 60)
small_font = pygame.font.SysFont("timesnewroman", 35)
boss_font = pygame.font.SysFont("timesnewroman", 20)

player_image = pygame.image.load("src/assets/Player.png").convert_alpha()
player_image = pygame.transform.scale(player_image, (50, 50))

boss_image = pygame.image.load("src/assets/Boss.png").convert_alpha()
boss_image = pygame.transform.scale(boss_image, (50, 70))

sandwich_image = pygame.image.load("src/assets/Sandwich.png").convert_alpha()
sandwich_image = pygame.transform.scale(sandwich_image, (30, 40))

platform_oneway_image = pygame.image.load("src/assets/oneway_platform.png").convert_alpha()
platform_solid_image = pygame.image.load("src/assets/solid_platform.png").convert_alpha()

background_image = pygame.image.load("src/assets/background.png").convert()
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

heart_image = pygame.image.load("src/assets/heart.png").convert_alpha()
heart_image = pygame.transform.scale(heart_image, (25, 25))

# ---------- Constants ----------
gravity = 0.6 
jump_strength = -14
player_speed = 5
ground_y = 460

shoot_delay = 30

# ---------- Game State ---------- 
victory = False
game_over = False
game_started = False
play_button = pygame.Rect(380, 300, 240, 70)

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
platform1 = pygame.Rect((100, 420, 130, 15))
platform2 = pygame.Rect((770, 420, 130, 15))    #Player can land on top, but can pass through form below
platform5 = pygame.Rect((510, 100, 130, 15))
one_way_platforms = [platform1, platform2, platform5]

#solid platforms
platform3 = pygame.Rect((345, 300, 295, 25))
platform4 = pygame.Rect((90, 160, 130, 25))     #Player collides from all sides
platform6 = pygame.Rect((765, 200, 235, 25))
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
    
    if key[pygame.K_SPACE]:
        player.jump(jump_strength)


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
    global sandwich_collected
    
    if not sandwich_collected and player.rect.colliderect(sandwich):
        sandwich_collected = True
        player.can_shoot = True



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
        if bullet.right < 0 or bullet.left > WIDTH:        # If the bullet goes out of the window,it is removed from the list
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
            boss_bullet = pygame.Rect(boss.rect.right, boss.rect.centery - 5, 10, 10)
    
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
            player.take_hit()
            boss_bullets.remove(bullet_data)
    
    if player.hits >= 3:
        game_over = True

def draw_outlined_text(surface, text, font, text_color, outline_color, x, y):
    base_text = font.render(text, True, text_color)
    outline_text = font.render(text, True, outline_color)

    surface.blit(outline_text, (x - 2, y))
    surface.blit(outline_text, (x + 2, y))
    surface.blit(outline_text, (x, y - 2))
    surface.blit(outline_text, (x, y + 2))

    surface.blit(base_text, (x, y))

def draw_start_menu():
    screen.blit(background_image, (0, 0))
    
    draw_outlined_text(screen, "MINI BOSS FIGHT", font, (255, 255, 255), (0, 0, 0), 245, 150)
    
    pygame.draw.rect(screen, (50, 50, 50), play_button)
    pygame.draw.rect(screen, (255, 255, 255), play_button, 3)
    
    play_text = small_font.render("PLAY", True, (255, 255, 255))
    play_text_rect = play_text.get_rect(center=play_button.center)
    screen.blit(play_text, play_text_rect)

def draw_game():
    screen.fill((0, 0, 0))
    screen.blit(background_image, (0, 0))
    
    
    #Player
    screen.blit(player_image, player.rect)
    
    #player lives 
    player_lives = 3 - player.hits
    for i in range(player_lives):
        screen.blit(heart_image, (20 + i * 35, 20))
    
    #Boss
    screen.blit(boss_image, boss.rect)    
    #Ground
    pygame.draw.rect(screen, (20, 120, 20), grass)
    pygame.draw.rect(screen, (90, 55, 20), soil)
    
    #One way platforms  
    for platform in one_way_platforms:
        visual_height = platform.height + 15
        scaled_oneway = pygame.transform.scale(platform_oneway_image, (platform.width, platform.height))
        screen.blit(scaled_oneway, (platform.x, platform.y -8))
    
    #solid platforms
    for platform in solid_platforms:
        visual_width = platform.width + 20
        visual_height = platform.height + 17
        scaled_solid = pygame.transform.scale(platform_solid_image, (platform.width, platform.height))
        screen.blit(scaled_solid, (platform.x -10, platform.y -8))
    
    #Sandwich
    if not sandwich_collected:
        screen.blit(sandwich_image, sandwich)
    
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
    pygame.draw.rect(screen, (255, 255, 255), boss_bar_bg, 2)
    boss_label = boss_font.render("BOSS HP", True, (255, 255, 255))
    screen.blit(boss_label, (boss_bar_bg.x, boss_bar_bg.y - 22))
    
    #Boss bullets
    for bullet_data in boss_bullets:
        bullet = bullet_data[0]
        pygame.draw.rect(screen, (0, 0, 225), bullet)
    
    #Game over text
    if game_over:
        draw_outlined_text(screen, "GAME OVER", font, (255, 255, 255), (0, 0, 0), 330, 220)
        draw_outlined_text(screen, "Press R to Restart", small_font, (255, 255, 255), (0, 0, 0), 375, 320)
    
    #Victory text
    if victory:
        draw_outlined_text(screen, "YOU WIN!", font, (255, 255, 255), (0, 0, 0), 360, 220)
        draw_outlined_text(screen, "Press R to Restart", small_font, (255, 255, 255), (0, 0, 0), 370, 300)


#---------- Main game loop ----------
run = True
while run:
    # Quit event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        
        if event.type == pygame.MOUSEBUTTONDOWN and not game_started:
            if play_button.collidepoint(event.pos):
                game_started = True
    
    previous_player = player.rect.copy()    # Save previous player position for solid platform collision checks 
    key = pygame.key.get_pressed()
    
    if game_started and not game_over and not victory:
        boss.update_movement()
        
        handle_player_input(key)
        
        player.rect.x = int(player.x)
        
        player.apply_gravity(gravity)
        handle_ground_collision()
        handle_one_way_collisions()
        handle_solid_collisions(previous_player)
        
        handle_sandwich_pickup()
        
        update_player_bullets()
        update_boss_bullets()
        
        keep_player_inside_screen()
    
    if (game_over or victory) and key[pygame.K_r]:
        reset_game()
    
    if not game_started:
        draw_start_menu()
    else:
        draw_game()
    
    pygame.display.update() 
    clock.tick(60)

pygame.quit()    