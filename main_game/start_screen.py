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
    small_font = pygame.font.Font("font_assets/medieval_font.ttf", 40)
    
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

    #  "Victory" button rectangle
    victory_button_width, victory_button_height = 200, 100
    victory_button_x = width // 1.1 - victory_button_width // 2
    victory_button_y = height // 8 - victory_button_height // 2 + 50  # Move down to make space for the first button
    victory_button_rect = pygame.Rect(victory_button_x, victory_button_y, victory_button_width, victory_button_height)

    #  "End" button rectangle
    end_button_width, end_button_height = 500, 100
    end_button_x = width // 1 - end_button_width // 2 - 280
    end_button_y = height // 8 - end_button_height // 2 + 160  # Move down to make space for the first button
    end_button_rect = pygame.Rect(end_button_x, end_button_y, end_button_width, end_button_height)

    #  "Defeat" button rectangle
    defeat_button_width, defeat_button_height = 230, 100
    defeat_button_x = width // 1 - defeat_button_width // 2 - 145
    defeat_button_y = height // 8 - defeat_button_height // 2 + 270  # Move down to make space for the first button
    defeat_button_rect = pygame.Rect(defeat_button_x, defeat_button_y, defeat_button_width, defeat_button_height)

     #  "Rules" button rectangle
    rules_button_width, rules_button_height = 230, 100
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
                # Check if the mouse click is within the "Victory Screen" button area
                elif victory_button_rect.collidepoint(event.pos):
                    pygame.quit()
                    subprocess.run(["python", "victory.py"])  # Run the victory.py script
                    sys.exit()

                elif end_button_rect.collidepoint(event.pos):
                    pygame.quit()
                    subprocess.run(["python", "game_end_final.py"]) # run the end game scene that appears after a boss has defeated the player
                    sys.exit()

                elif defeat_button_rect.collidepoint(event.pos):
                    pygame.quit()
                    subprocess.run(["python", "defeat.py"]) # run the defeat game scene that appears after the player's hearts have run out
                    sys.exit()

                elif rules_button_rect.collidepoint(event.pos):
                    pygame.quit()
                    subprocess.run(["python", "tutorial.py"]) # run the tutorial game scene
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
        start_text = small_font.render("Sākt", True, WHITE)
        screen.blit(start_text, (start_button_x + start_button_width // 2 - start_text.get_width() // 2,
                                 start_button_y + start_button_height // 2 - start_text.get_height() // 2))
        # Render the "End" button text
        end_text = small_font.render("Spēles Bossa Zaudējums", True, WHITE)
        screen.blit(end_text, (end_button_x + end_button_width // 2 - end_text.get_width() // 2,
                                 end_button_y + end_button_height // 2 - end_text.get_height() // 2))
        # Render the "Defeat" button text
        defeat_text = small_font.render("Zaudējums", True, WHITE)
        screen.blit(end_text, (defeat_button_x + defeat_button_width // 2 - defeat_text.get_width() // 2,
                                 defeat_button_y + defeat_button_height // 2 - defeat_text.get_height() // 2))

        # Button hover effect for "Victory Screen" button
        if victory_button_rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, GENERAL_HOVER_COLOR, victory_button_rect)  # Hover color
        else:
            pygame.draw.rect(screen, GENERAL_BUTTON_COLOR, victory_button_rect)  # Default color

        # Button hover effect for "End" button
        if end_button_rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, GENERAL_HOVER_COLOR, end_button_rect)  # Hover color
        else:
            pygame.draw.rect(screen, GENERAL_BUTTON_COLOR, end_button_rect)  # Default color

        # Button hover effect for "Defeat" button
        if defeat_button_rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, GENERAL_HOVER_COLOR, defeat_button_rect)  # Hover color
        else:
            pygame.draw.rect(screen, GENERAL_BUTTON_COLOR, defeat_button_rect)  # Default color

         # Button hover effect for "Rules" button
        if rules_button_rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, GENERAL_HOVER_COLOR, rules_button_rect)  # Hover color
        else:
            pygame.draw.rect(screen, GENERAL_BUTTON_COLOR, rules_button_rect)  # Default color


        # Render the "Victory Screen" button text
        victory_text = small_font.render("Victory", True, WHITE)
        screen.blit(victory_text, (victory_button_x + victory_button_width // 2 - victory_text.get_width() // 2,
                                   victory_button_y + victory_button_height // 2 - victory_text.get_height() // 2))
        
        # Render the "End" button text
        end_text = small_font.render("Spēles Bossa Zaudējums", True, WHITE)
        screen.blit(end_text, (end_button_x + end_button_width // 2 - end_text.get_width() // 2,
                                   end_button_y + end_button_height // 2 - end_text.get_height() // 2))
        
        # Render the "Defeat" button text
        end_text = small_font.render("Zaudējums", True, WHITE)
        screen.blit(end_text, (defeat_button_x + defeat_button_width // 2 - defeat_text.get_width() // 2,
                                   defeat_button_y + defeat_button_height // 2 - defeat_text.get_height() // 2))
        
         # Render the "Rules" button text
        rules_text = small_font.render("Noteikumi", True, WHITE)
        screen.blit(rules_text, (rules_button_x + rules_button_width // 2 - rules_text.get_width() // 2,
                                   rules_button_y + rules_button_height // 2 - rules_text.get_height() // 2))

        # Update the display
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    start_screen()