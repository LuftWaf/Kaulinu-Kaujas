import pygame
import sys
import subprocess

def defeat():
    pygame.init()
    width, height = 1440, 900
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Zaudēji 1 Dzīvību!")

    # Colors
    WHITE = (255, 255, 255)
    BUTTON_COLOR = (0, 128, 0)  
    HOVER_COLOR = (0, 200, 0)  # Color for button hover effect

    # Set up fonts
    font = pygame.font.Font(None, 65)
    small_font = pygame.font.Font(None, 50)
    
    # Render the victory text
    end_text = font.render("Gandrīz nomiri, bet paveicās, šoreiz tikai zaudē 1 dzīvību!", True, WHITE)

    # Load the background image
    try:
        background_image = pygame.image.load("picture_assets/brokenheart.png")
        background_image = pygame.transform.scale(background_image, (width, height))
    except pygame.error as e:
        print(f"Error loading image: {e}")
        background_image = None  # Set background_image to None if loading fails

    # "Turpināt spēlēt" button rectangle
    button_width, button_height = 500, 100
    button_x = width // 2 - button_width // 2 + 300
    button_y = height // 2 - button_height // 2 + 300  # Position the button
    button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Check if the mouse click is within the button area
                if button_rect.collidepoint(event.pos):
                    # Close the end screen and return to the start screen
                    pygame.quit()
                    subprocess.run(["python", "main.py"])  # Go back to the main game
                    sys.exit()

        # Clear the screen
        screen.fill(WHITE)

        # Draw the background image
        if background_image:
            screen.blit(background_image, (0, 0))

        # Draw the end text
        screen.blit(end_text, (width // 2 + 35 - end_text.get_width() // 2, height // 2 - 100))


        # Button hover effect
        mouse_pos = pygame.mouse.get_pos()
        if button_rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, HOVER_COLOR, button_rect)  # Hover color
        else:
            pygame.draw.rect(screen, BUTTON_COLOR, button_rect)  # Default color

        # Render the button text
        back_text = small_font.render("Turpini spēlēt..", True, WHITE)
        screen.blit(back_text, (button_x + button_width // 2 - back_text.get_width() // 2,
                                button_y + button_height // 2 - back_text.get_height() // 2))

        # Update the display
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    defeat()