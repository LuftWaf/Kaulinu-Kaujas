import pygame
import sys
import random
from PIL import Image, ImageSequence
import subprocess
import time 

def fade_to_black(screen, width, height, duration=3000):
    """Fade the screen to black."""
    fade_surface = pygame.Surface((width, height))
    fade_surface.fill((0, 0, 0))  # Black color
    fade_surface.set_alpha(0)  # Start fully transparent

    for alpha in range(0, 256):  # Gradually increase alpha from 0 to 255
        fade_surface.set_alpha(alpha)
        screen.blit(fade_surface, (0, 0))  # Draw the fade surface
        pygame.display.flip()  # Update the display
        pygame.time.delay(duration // 255)  # Control the fade speed


def load_gif_frames(gif_path):
    # Load all frames from a GIF file using Pillow
    frames = []
    with Image.open(gif_path) as img:
        for frame in ImageSequence.Iterator(img):
            frame = frame.convert("RGBA")
            frame_data = frame.tobytes()
            size = frame.size
            pygame_frame = pygame.image.fromstring(frame_data, size, "RGBA")
            frames.append(pygame_frame)
    return frames

def battle():
    pygame.init()
    width, height = 1440, 900
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Cīņa")
    
    # Game state
    value = 0
    dice_visible = True
    HP = 6  # Player HP
    enemy_HP = 6  # Enemy HP
    HP_decrease = False  # To prevent multiple HP decreases
    show_result_delay = 0
    last_click_time = 0 # To prevent rapid clicking
    roll_count = 0  # Track number of player rolls
    enemy_attack_delay = 0  # Delay before enemy attacks
    pending_enemy_damage = 0  # Damage to apply after slash animation
    
    # Colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    BUTTON_COLOR = (0, 128, 0)  
    HOVER_COLOR = (0, 200, 0)
    DISABLED_COLOR = (100, 100, 100)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)

    # Load all assets first
    try:
        # Background
        background = pygame.image.load("fight_scene/fight_scene_full.png").convert()
        background = pygame.transform.scale(background, (width, height))

        # Background2
        background2 = pygame.image.load("fight_scene/fight_scene_5.png").convert()
        background2 = pygame.transform.scale(background2, (width, height))

        background3 = pygame.image.load("fight_scene/fight_scene_4.png").convert()
        background3 = pygame.transform.scale(background3, (width, height))

        background4 = pygame.image.load("fight_scene/fight_scene_3.png").convert()
        background4 = pygame.transform.scale(background4, (width, height))

        background5 = pygame.image.load("fight_scene/fight_scene_2.png").convert()
        background5 = pygame.transform.scale(background5, (width, height))

        background6 = pygame.image.load("fight_scene/fight_scene_1.png").convert()
        background6 = pygame.transform.scale(background6, (width, height))

        background7 = pygame.image.load("fight_scene/fight_scene_0.png").convert()
        background7 = pygame.transform.scale(background7, (width, height))

        # Dice results
        DMG2 = pygame.image.load("dice_end_assets/2damage_end.png").convert_alpha()
        DMG2 = pygame.transform.scale(DMG2, (265, 265))
        HEART = pygame.image.load("dice_end_assets/plusheart_end.png").convert_alpha()
        HEART = pygame.transform.scale(HEART, (265, 265))
        minus_heart = pygame.image.load("dice_end_assets/minusheart_end.png").convert_alpha()
        minus_heart = pygame.transform.scale(minus_heart, (265, 265))
        SHIELD = pygame.image.load("dice_end_assets/shield_end.png").convert_alpha()
        SHIELD = pygame.transform.scale(SHIELD, (265, 265))
        DMG = pygame.image.load("dice_end_assets/damage_end.png").convert_alpha()
        DMG = pygame.transform.scale(DMG, (265, 265))
        MISS = pygame.image.load("dice_end_assets/miss_end.png").convert_alpha()
        MISS = pygame.transform.scale(MISS, (265, 265))
        
        # Animations
        dice_frames = load_gif_frames("gif_assets/dice.gif")
        slash_frames = load_gif_frames("gif_assets/slash.gif")
        enemy_attack_frames = load_gif_frames("gif_assets/inverted_slash.gif")
        
        # Enemies
        enemy = pygame.image.load("enemy_assets/worm.png")
        enemy = pygame.transform.scale(enemy, (400, 550))
      
        # screen.blit(enemy, (width // 2 - enemy.get_width() // 2, height // 2 - 200)) KO SIS KODS SEIT DARA

    except Exception as e:
        print(f"Error loading assets: {e}")
        pygame.quit()
        sys.exit()
    

    # Animation control
    dice_playing = False
    current_dice_frame = 0
    dice_frame_counter = 0
    dice_frame_delay = 5  # Higher = slower animation
    
    slash_playing = False
    current_slash_frame = 0
    slash_frame_counter = 0
    slash_frame_delay = 3  # Now actually used
    
    enemy_attacking = False
    current_enemy_attack_frame = 0
    enemy_attack_frame_counter = 0
    enemy_attack_frame_delay = 3
    
    # Fonts
    small_font = pygame.font.Font(None, 50)
    
    # Button
    button_width, button_height = 300, 80
    button_x, button_y = width // 2 - button_width // 2, height - 150
    button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
    
    clock = pygame.time.Clock()
    running = True
    shield_active = False
    
    while running:
        current_time = pygame.time.get_ticks()
        
       
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Prevent rapid clicking (300ms cooldown) and check animations
                if (current_time - last_click_time > 1200 and 
                    not dice_playing and 
                    not slash_playing and 
                    not enemy_attacking and
                    button_rect.collidepoint(event.pos)):
                    last_click_time = current_time
                    dice_playing = True
                    dice_visible = False
                    value = random.randint(1, 6)  # 1 = 2DMG, 2 = HEART, 3 = -1Heart, 4 = SHIELD, 5 = Damage, 6 = Miss
                    current_dice_frame = 0
                    dice_frame_counter = 0
                    show_result_delay = 0
                    HP_decrease = False
                    roll_count += 1
                    print(f"Player HP: {HP}, Enemy HP: {enemy_HP}")

        # Clear screen and add new background
        screen.fill(BLACK)
        if HP == 6:
            screen.blit(background, (0, 0))
        if HP < 6:
            if HP == 5:
                screen.blit(background2, (0, 0))
            if HP == 4:
                screen.blit(background3, (0, 0))
            if HP == 3:
                screen.blit(background4, (0, 0))
            if HP == 2:
                screen.blit(background5, (0, 0))
            if HP == 1:
                screen.blit(background6, (0, 0))
            if HP == 0:
                screen.blit(background7, (0, 0))
                if (current_time - last_click_time > 1200 and 
                    not dice_playing and 
                    not slash_playing):
                        fade_to_black(screen, width, height)
                        pygame.quit()
                        subprocess.run(["python", "defeat.py"])
                        sys.exit()

        if enemy:
            screen.blit(enemy, (width // 2 + 410 - enemy.get_width() // 2, height // 2 - 400))
        
        # Handle dice animation
        if dice_playing:
            dice_frame_counter += 1
            if dice_frame_counter >= dice_frame_delay:
                dice_frame_counter = 0
                current_dice_frame += 1
                if current_dice_frame >= len(dice_frames):
                    dice_playing = False
                    dice_visible = True
                    if value == 1:
                        show_result_delay = 40  # ~0.5 seconds delay
                        pending_enemy_damage = 2  # 2 damage to enemy (applied after slash)
                    if value == 5:
                        show_result_delay = 40
                        pending_enemy_damage = 1  # 1 damage to enemy (applied after slash)
            
            # Show current frame
            frame = pygame.transform.scale(dice_frames[current_dice_frame % len(dice_frames)], (200, 200))
            screen.blit(frame, (width//2 + 180, height//2 + 230))

        # Show static dice result
        if dice_visible and not dice_playing:
            if value == 1:
                screen.blit(DMG2, (width//2 + 180, height//2 + 230))
            elif value == 2:
                screen.blit(HEART, (width//2 + 180, height//2 + 230))
                if not HP_decrease and not HP > 5:
                    HP += 1
                    HP_decrease = True
            elif value == 3:
                screen.blit(minus_heart, (width//2 + 180, height//2 + 230))
                if not HP_decrease:
                    HP -= 1
                    HP_decrease = True
            elif value == 4:
                screen.blit(SHIELD, (width//2 + 180, height//2 + 230))
                if not shield_active:
                    shield_active = True
            elif value == 5:
                screen.blit(DMG, (width//2 + 180, height//2 + 230))
            elif value == 6:
                screen.blit(MISS, (width//2 + 180, height//2 + 230))
            elif value == 0:
                screen.blit(SHIELD, (width//2 + 180, height//2 + 230))
            
            if show_result_delay > 0:
                show_result_delay -= 1
                if show_result_delay == 0 and (value == 1 or value == 5):
                    slash_playing = True
                    current_slash_frame = 0
                    slash_frame_counter = 0
            
            # Check if enemy should attack (after every 2 rolls)
            if roll_count % 2 == 0 and roll_count > 0 and not enemy_attacking and not slash_playing:
                if enemy_attack_delay <= 0:
                    enemy_attack_delay = 60  # ~1 second delay before enemy attacks
                else:
                    enemy_attack_delay -= 1
                    if enemy_attack_delay == 0:
                        enemy_attacking = True 
                        current_enemy_attack_frame = 0
                        enemy_attack_frame_counter = 0
                        # Enemy will deal damage after attack animation
                        pending_enemy_damage = -1  # Negative for player damage
                        roll_count = 0  # Reset roll count after attack
                        if shield_active == True:
                            pending_enemy_damage = 0
                            shield_active = False
                            if value == 4:
                                value = 0
        
        # Handle slash animation (player attacking enemy)
        if slash_playing:
            slash_frame_counter += 1
            if slash_frame_counter >= slash_frame_delay:
                slash_frame_counter = 0
                current_slash_frame += 1
                if current_slash_frame >= len(slash_frames):
                    slash_playing = False
                    # Apply damage to enemy after animation completes
                    if pending_enemy_damage > 0:
                        enemy_HP -= pending_enemy_damage
                        pending_enemy_damage = 0
                        print(f"Enemy took {pending_enemy_damage} damage! Enemy HP: {enemy_HP}")
            
            # Show current frame
            if current_slash_frame < len(slash_frames):
                frame = pygame.transform.scale(slash_frames[current_slash_frame], (400, 400))
                screen.blit(frame, (width//2 + 200, height//2 - 450))

        # Handle enemy attack animation
        if enemy_attacking:
            enemy_attack_frame_counter += 1
            if enemy_attack_frame_counter >= enemy_attack_frame_delay:
                enemy_attack_frame_counter = 0
                current_enemy_attack_frame += 1
                if current_enemy_attack_frame >= len(enemy_attack_frames):
                    enemy_attacking = False
                    # Apply damage to player after animation completes
                    if pending_enemy_damage < 0:
                        HP += pending_enemy_damage  # pending_enemy_damage is negative
                        pending_enemy_damage = 0
                        print(f"Player took {-pending_enemy_damage} damage! Player HP: {HP}")
            
            # Show current frame
            if current_enemy_attack_frame < len(enemy_attack_frames):
                frame = pygame.transform.scale(enemy_attack_frames[current_enemy_attack_frame], (400, 400))
                screen.blit(frame, (width//2 - 650, height//2 - 230))  # Show on left side for enemy attack

        # Draw button with proper state
        button_active = not dice_playing and not slash_playing and not enemy_attacking
        button_color = (HOVER_COLOR if button_rect.collidepoint(pygame.mouse.get_pos()) and button_active 
                       else BUTTON_COLOR if button_active 
                       else DISABLED_COLOR)
        
        pygame.draw.rect(screen, button_color, button_rect)
        button_text = small_font.render("Mest kauliņu", True, WHITE)
        screen.blit(button_text, (button_x + button_width//2 - button_text.get_width()//2,
                                button_y + button_height//2 - button_text.get_height()//2))
        
        # Draw the enemy
        
        
        # Draw enemy health bar
        enemy_health_width = 200
        enemy_health_height = 20
        enemy_health_x = width // 2  - enemy_health_width // 2  + 400
        enemy_health_y = height // 2 - 420
        
        # Background of health bar (empty part)
        pygame.draw.rect(screen, RED, (enemy_health_x, enemy_health_y, enemy_health_width, enemy_health_height))
        # Current health
        current_enemy_health_width = max(0, (enemy_health_width * enemy_HP) // 6)
        pygame.draw.rect(screen, GREEN, (enemy_health_x, enemy_health_y, current_enemy_health_width, enemy_health_height))
        
        # Check if enemy is defeated
        if enemy_HP <= 0:
            fade_to_black(screen, width, height)
            pygame.quit()
            subprocess.run(["python", "main.py"])  
            sys.exit()
        
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    battle()
