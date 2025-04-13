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
    HP = 6  # Player HP if not getting it in data form rn xd (Please import data)
    HP_decrease = False  # To prevent multiple HP decreases
    show_result_delay = 0
    last_click_time = 0 # To prevent rapid clicking
    
    # Colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    BUTTON_COLOR = (0, 128, 0)  
    HOVER_COLOR = (0, 200, 0)
    DISABLED_COLOR = (100, 100, 100)

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
    
    # Fonts
    small_font = pygame.font.Font(None, 50)
    
    # Button
    button_width, button_height = 300, 80
    button_x, button_y = width // 2 - button_width // 2, height - 150
    button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
    
    clock = pygame.time.Clock()
    running = True
    
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
                    button_rect.collidepoint(event.pos)):
                    last_click_time = current_time
                    dice_playing = True
                    dice_visible = False
                    value = random.randint(1, 3)  # 1 = 2DMG, 2 = HEART, 3 = -1Heart, 4 = SHIELD, 5 = Damage, 6 = Miss
                    current_dice_frame = 0
                    dice_frame_counter = 0
                    show_result_delay = 0
                    HP_decrease = False
                    print(HP)

        # Clear screen
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
        
        # Handle dice animation (now using frame delay properly)
        if dice_playing:
            dice_frame_counter += 1
            if dice_frame_counter >= dice_frame_delay:
                dice_frame_counter = 0
                current_dice_frame += 1
                if current_dice_frame >= len(dice_frames):
                    dice_playing = False
                    dice_visible = True
                    if value == 1:
                        show_result_delay = 30  # ~0.5 seconds delay
                    if value == 5:
                        show_result_delay = 30
            
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
            elif value == 5:
                screen.blit(DMG, (width//2 + 180, height//2 + 230))
            elif value == 6:
                screen.blit(MISS, (width//2 + 180, height//2 + 230))
            
            if show_result_delay > 0:
                show_result_delay -= 1
                if show_result_delay == 0:
                    slash_playing = True
                    current_slash_frame = 0
                    slash_frame_counter = 0
            
        
        

        # Handle slash animation (now using frame delay)
        if slash_playing:
            slash_frame_counter += 1
            if slash_frame_counter >= slash_frame_delay:
                slash_frame_counter = 0
                current_slash_frame += 1
                if current_slash_frame >= len(slash_frames):
                    slash_playing = False
            
            # Show current frame
            if current_slash_frame < len(slash_frames):
                frame = pygame.transform.scale(slash_frames[current_slash_frame], (400, 400))
                screen.blit(frame, (width//2 + 200, height//2 - 300))

        # Draw button with proper state
        button_active = not dice_playing and not slash_playing
        button_color = (HOVER_COLOR if button_rect.collidepoint(pygame.mouse.get_pos()) and button_active 
                       else BUTTON_COLOR if button_active 
                       else DISABLED_COLOR)
        
        pygame.draw.rect(screen, button_color, button_rect)
        button_text = small_font.render("Mest kauliņu", True, WHITE)
        screen.blit(button_text, (button_x + button_width//2 - button_text.get_width()//2,
                                button_y + button_height//2 - button_text.get_height()//2))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    battle()