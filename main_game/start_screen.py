import pygame
import sys
import main
import subprocess

def start_screen():
    pygame.init()
    width, height = 1440, 900
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Kauliņu Kaujas")


    # Colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    BUTTON_COLOR = (0, 128, 0)  
    HOVER_COLOR = (0, 200, 0)  # Color for button hover effect
    GENERAL_BUTTON_COLOR = (128, 0, 128)  # Color for all the buttons
    GENERAL_HOVER_COLOR = (200, 0, 200)  # Hover color for all the buttons

    # Set up fonts
    font = pygame.font.Font("font_assets/medieval_font.ttf", 74)
    small_font = pygame.font.Font("font_assets/medieval_font.ttf", 38)
    
    # Render the title text
    title_text = font.render("Kauliņu Kaujas", True, BLACK)

    # Load and scale the image
    try:
        img = pygame.image.load("picture_assets/screen_cube.png")
    except pygame.error as e:
        print(f"Error loading image: {e}")
        img = None  # Set img to None if loading fails

    # "Sākt" button rectangle
    start_button_width, start_button_height = 200, 100
    start_button_x = width // 2 - start_button_width // 2
    start_button_y = height // 2 - start_button_height // 2 - 280  # Move up to make space for the second button
    start_button_rect = pygame.Rect(start_button_x, start_button_y, start_button_width, start_button_height)

    #  "Sākt jaunu spēli" button rectangle
    rules_button_width, rules_button_height = 280, 100
    rules_button_x = width // 2 - rules_button_width // 2
    rules_button_y = height // 2 - rules_button_height // 2 - 150  # Move down to make space for the first button
    rules_button_rect = pygame.Rect(rules_button_x, rules_button_y, rules_button_width, rules_button_height)

   
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Check if the mouse click is within the "Sākt" button area
                if start_button_rect.collidepoint(event.pos):
                    main.main_game()  # Call the main game function
                    running = False  # Close the start screen

                elif rules_button_rect.collidepoint(event.pos):
                    # Reset player data
                    pygame.quit()
                    subprocess.run(["python3", "tutorial.py"]) # run the tutorial game scene
                    sys.exit()

        # Clear the screen
        screen.fill(WHITE)

        # Draw the title text
        screen.blit(title_text, (width // 2 - title_text.get_width() // 2, height // 7 - 120))

        # Draw the image (if loaded successfully)
        if img:
            screen.blit(img, (width // 2 - img.get_width() // 2, height // 2 - 50))

        # Button hover effect for "Sākt" button
        mouse_pos = pygame.mouse.get_pos()
        if start_button_rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, HOVER_COLOR, start_button_rect)  # Hover color
        else:
            pygame.draw.rect(screen, BUTTON_COLOR, start_button_rect)  # Default color

        # Render the "Sākt" button text
        start_text = small_font.render("Turpināt", True, WHITE)
        screen.blit(start_text, (start_button_x + start_button_width // 2 - start_text.get_width() // 2,
                                 start_button_y + start_button_height // 2 - start_text.get_height() // 2))


        # Button hover effect for "Sākt jaunu spēli" button
        if rules_button_rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, GENERAL_HOVER_COLOR, rules_button_rect)  # Hover color
        else:
            pygame.draw.rect(screen, GENERAL_BUTTON_COLOR, rules_button_rect)  # Default color

        
         # Render the "Sākt jaunu spēli" button text
        rules_text = small_font.render("Sākt jaunu spēli", True, WHITE)
        screen.blit(rules_text, (rules_button_x + rules_button_width // 2 - rules_text.get_width() // 2,
                                   rules_button_y + rules_button_height // 2 - rules_text.get_height() // 2))

        # Update the display
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    start_screen()
