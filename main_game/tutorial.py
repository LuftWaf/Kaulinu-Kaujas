import pygame
import sys
import subprocess
import textwrap

def render_wrapped_text(surface, text, font, color, x, y, max_width, line_spacing=5):
    wrapped_lines = textwrap.wrap(text, width=50)  # Adjust width as needed
    for i, line in enumerate(wrapped_lines):
        rendered_line = font.render(line, True, color)
        surface.blit(rendered_line, (x, y + i * (font.get_height() + line_spacing)))

def victory_screen():
    pygame.init()
    width, height = 1440, 900
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Spēles Pamācība")

    # Colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    BUTTON_COLOR = (0, 128, 0)  
    HOVER_COLOR = (0, 200, 0)  # Color for button hover effect
    GREEN = (49, 141, 53)

    # Set up fonts
    font = pygame.font.Font("font_assets/medieval_font.ttf", 69)
    rules_small_font = pygame.font.Font("font_assets/medieval_font.ttf", 22)
    button_font = pygame.font.Font("font_assets/medieval_font.ttf", 50)
    motivation_font = pygame.font.Font("font_assets/medieval_font.ttf", 28)

     # Load the background image
    try:
        background_image = pygame.image.load("background_assets/tutorial.png")  # Replace with your image file name
        background_image = pygame.transform.scale(background_image, (width, height))
    except pygame.error as e:
        print(f"Error loading image: {e}")
        background_image = None  # Set background_image to None if loading fails
    
    # render the text
    rules_text = "Spēles noteikumi."
    rules_text2 = (
    "1. Spēlētājs sāk uz starta laukuma, uzspiežot uz nākamo bumbu, "
    "spēlētājs nonāk cīņas fāzē."
)
    rules_text3 = (
    "2. Kad spēlētājs nonāk cīņas fāzē, var mest kauliņu, kuru uzmetot "
    "var veikt vienu no darbībām."
)
    rules_text4 = (
    "3. Ir iespēja uzbrukt pretiniekam 1 reizi, 2 reizes, iegūt sirsniņu, "
    "zaudēt sirsniņu, iegūt vairogu, kas aizsargā no jebkura pretinieka uzbrukuma, "
    "un arī spēlētājs var izdarīt neko."
)
    rules_text5 = ( "4. Tad kad spēlētājs ir veiksmīgi uzvarējis cīņu, nonāk atpakaļ kartē un var sākt nākamo līmeni."
)
    rules_text6 = ( "5. Kad visi līmeņi ir izieti uz kartes, spēlētājs nonāk "
    "nākmajā līmeni, bet kartē ir arī bosa līmeņi kuri būs grūtāki."
)
    rules_text7 = ("6. Spēlētājs spēli uzvar, ja visus līmeņus ir izgājis, gan pirmo, gan otro karti un izveicis pēdējo bosu. "
)
    rules_text8 = ( "7. Spēlētājs spēli zaudē, ja zaudē cīņā visas esošāš sirsniņas,līdz ar  to zaudē vienu sirsniņu, kas ir redzama uz kartes. Zaudējot visas sirsniņas, spēle ir jāsāk no jauna."
)
    rules_text9 = ( "Lai tev veicas izglābt Mālburgu! Tikai tev ir iespēja to izdarīt!")

    


    # "Atpakaļ" button rectangle
    back_button_width, back_button_height = 300, 70
    back_button_x = width // 2 - back_button_width // 2 + 220
    back_button_y = height // 2 - back_button_height // 2 + 400  # Position the button
    back_button_rect = pygame.Rect(back_button_x, back_button_y, back_button_width, back_button_height)

    # "Sākt spēli" button rectangle
    start_button_width, start_button_height = 300, 70
    start_button_x = width // 2 - start_button_width // 2 + 530
    start_button_y = height // 2 - start_button_height // 2 + 400  # Position the button
    start_button_rect = pygame.Rect(start_button_x, start_button_y, start_button_width, start_button_height)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Check if the mouse click is within the button area
                if back_button_rect.collidepoint(event.pos):
                    # Close the rules screen and return to the start screen
                    pygame.quit()
                    subprocess.run(["python", "start_screen.py"])  # Run the start_screen.py script
                    sys.exit()
                if start_button_rect.collidepoint(event.pos):
                    # close the rules screen and go straight into the game screen
                    pygame.quit()
                    subprocess.run(["python", "main.py"])

        

        # Clear the screen
        screen.fill(BLACK)

        # Draw the background image
        if background_image:
            screen.blit(background_image, (0, 0))

        # Rendering wrapped text
        render_wrapped_text(screen, rules_text, font, WHITE, width // 2 - 200, height // 2 - 400, max_width=700)
        render_wrapped_text(screen, rules_text2, rules_small_font, WHITE, width // 2 - 480, height // 2 - 300, max_width=700)
        render_wrapped_text(screen, rules_text3, rules_small_font, WHITE, width // 2 - 480, height // 2 - 220, max_width=700)
        render_wrapped_text(screen, rules_text4, rules_small_font, WHITE, width // 2 - 480, height // 2 - 115, max_width=700)
        render_wrapped_text(screen, rules_text5, rules_small_font, WHITE, width // 2 - 480, height // 2 + 50, max_width=700)
        render_wrapped_text(screen, rules_text6, rules_small_font, WHITE, width // 2 - 480, height // 2 + 125, max_width=700)
        render_wrapped_text(screen, rules_text7, rules_small_font, WHITE, width // 2 - 480, height // 2 + 235, max_width=700)
        render_wrapped_text(screen, rules_text8, rules_small_font, WHITE, width // 2 + 43, height // 2 - 295, max_width=700)
        render_wrapped_text(screen, rules_text9, motivation_font, GREEN, width // 2 - 10 , height // 2 + 260, max_width=700)

        # Button hover effect
        mouse_pos = pygame.mouse.get_pos()
        if back_button_rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, HOVER_COLOR, back_button_rect)  # Hover color
        else:
            pygame.draw.rect(screen, BUTTON_COLOR, back_button_rect)  # Default color
        mouse_pos = pygame.mouse.get_pos()

        if start_button_rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, HOVER_COLOR, start_button_rect)  # Hover color
        else:
            pygame.draw.rect(screen, BUTTON_COLOR, start_button_rect)  # Default color

        # Render the button text
        back_text = button_font.render("Atpakaļ", True, WHITE)
        screen.blit(back_text, (back_button_x + back_button_width // 2 - back_text.get_width() // 2,
                                back_button_y + back_button_height // 2 - back_text.get_height() // 2))
        
        start_text = button_font.render("Sākt spēli", True, WHITE)
        screen.blit(start_text, (start_button_x + start_button_width // 2 - start_text.get_width() // 2,
                                start_button_y + start_button_height // 2 - start_text.get_height() // 2))

        # Update the display
        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    victory_screen()