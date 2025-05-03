import pygame
import sys
import subprocess

def victory_screen():
    pygame.init()
    width, height = 1440, 900
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Uzvara!")

    # Colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    BUTTON_COLOR = (0, 128, 0)  
    HOVER_COLOR = (0, 200, 0)  # Color for button hover effect

    # Set up fonts
    font = pygame.font.Font("font_assets/medieval_font.ttf", 63)
    small_font = pygame.font.Font("font_assets/medieval_font.ttf", 40)
    
    # Render the victory text
    victory_text = font.render("Tu uzvarēji!", True, BLACK)
    victory_text2 = font.render("Tu izglābi Malburgu!", True, BLACK)

    # Load the background image
    try:
        background_image = pygame.image.load("background_assets/victory.png")  # Replace with your image file name
        background_image = pygame.transform.scale(background_image, (width, height))
    except pygame.error as e:
        print(f"Error loading image: {e}")
        background_image = None  # Set background_image to None if loading fails

    # "Sākt no jauna?" button rectangle
    button_width, button_height = 300, 100
    button_x = width // 2 - button_width // 2 + 400
    button_y = height // 2 - button_height // 2 - 300  # Position the button
    button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Check if the mouse click is within the button area
                if button_rect.collidepoint(event.pos):
                    # Close the victory screen and return to the start screen
                    pygame.quit()
                    subprocess.run(["python3", "start_screen.py"])  # Run the start_screen.py script
                    sys.exit()

        # Clear the screen
        screen.fill(WHITE)

        # Draw the background image
        if background_image:
            screen.blit(background_image, (0, 0))

        # Draw the victory text
        screen.blit(victory_text, (width // 2 - 100 - victory_text.get_width() // 2, height // 3))
        screen.blit(victory_text2, (width // 2 - 100 - victory_text.get_width() // 2, height // 2 - 50))

        # Button hover effect
        mouse_pos = pygame.mouse.get_pos()
        if button_rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, HOVER_COLOR, button_rect)  # Hover color
        else:
            pygame.draw.rect(screen, BUTTON_COLOR, button_rect)  # Default color

        # Render the button text
        back_text = small_font.render("Sākt no jauna?", True, WHITE)
        screen.blit(back_text, (button_x + button_width // 2 - back_text.get_width() // 2,
                                button_y + button_height // 2 - back_text.get_height() // 2))

        # Update the display
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    victory_screen()