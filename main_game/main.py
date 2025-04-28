import pygame
import sys
import os
import subprocess
import json


def battle_phase(ball_number):
    """
    Placeholder for the battle phase
    """
    print(f"Entering battle phase for ball {ball_number}")
    fight_scenes = {
        1: "battle_assets/battle1.py",
        2: "battle_assets/battle2.py",
        3: "battle_assets/battle3.py",
        4: "battle_assets/battle4.py",
    }
    fight_scene = fight_scenes.get(ball_number, None)
    if fight_scene:
        pygame.quit()
        subprocess.run(["python", fight_scene])  # Run the specific battle scene
        sys.exit()
    else:
        print(f"No fight scene defined for ball {ball_number}")
        return False



def create_dimmed_image(image, alpha=128):
    dimmed_image = image.copy()
    dimmed_image.fill((0, 0, 0, alpha), special_flags=pygame.BLEND_RGBA_MULT)
    return dimmed_image

def main_game():
    pygame.init()
    width, height = 1440, 900
    os.environ['SDL_VIDEO_WINDOW_POS'] = '1' # center the window
    pygame.display.set_caption("Kauliņu Kaujas")

    screen = pygame.display.set_mode((width, height))
    # background image
    background = pygame.image.load("background_assets/map_background.png")
    background = pygame.transform.scale(background, (width, height))

    # ball images
    ball_image = pygame.image.load("picture_assets/ball.png")
    ball_image = pygame.transform.scale(ball_image, (60, 60))

    dimmed_ball_image = create_dimmed_image(ball_image, alpha=128)

    # Define positions
    balls = [
        {"pos": (50, 630), "completed": True, "clickable": False},  # Starting ball
        {"pos": (100, 474), "completed": False, "clickable": True},  # First pathway ball (b1)
        {"pos": (150, 320), "completed": False, "clickable": False}, # b2
        {"pos": (270, 230), "completed": False, "clickable": False}, # b3 (boss battle)
        {"pos": (375, 333), "completed": False, "clickable": False}, # b4
        {"pos": (485, 470), "completed": False, "clickable": False}, # b5
        {"pos": (642, 553), "completed": False, "clickable": False}, # b6 (boss battle)
        {"pos": (942, 520), "completed": False, "clickable": False}, # b7
        {"pos": (1103, 557), "completed": False, "clickable": False}, # b8
        {"pos": (1265, 355), "completed": False, "clickable": False}, # b9 (final boss)
    ]

    boss_ball = [
        {"pos": (1265, 355), "completed": False, "clickable": False}, # b9 (final boss)
    ]

    with open('player_data.json', 'r') as json_file:
             player_data = json.load(json_file)
             print(player_data)
    
    if player_data["completed_stages"] == 1:
        balls[1]["completed"] = True
        balls[1]["clickable"] = False

        balls[2]["clickable"] = True

    if player_data["completed_stages"] == 2:
        balls[1]["completed"] = True
        balls[1]["clickable"] = False

        balls[2]["completed"] = True
        balls[2]["clickable"] = False

        balls[3]["clickable"] = True

    if player_data["completed_stages"] == 3:
        balls[1]["completed"] = True
        balls[1]["clickable"] = False

        balls[2]["completed"] = True
        balls[2]["clickable"] = False

        balls[3]["completed"] = True
        balls[3]["clickable"] = False

        balls[4]["clickable"] = True

    if player_data["completed_stages"] == 4:
        balls[1]["completed"] = True
        balls[1]["clickable"] = False

        balls[2]["completed"] = True
        balls[2]["clickable"] = False

        balls[3]["completed"] = True
        balls[3]["clickable"] = False

        balls[4]["completed"] = True
        balls[4]["clickable"] = False

        balls[5]["clickable"] = True

    if player_data["completed_stages"] == 5:
        balls[1]["completed"] = True
        balls[1]["clickable"] = False

        balls[2]["completed"] = True
        balls[2]["clickable"] = False

        balls[3]["completed"] = True
        balls[3]["clickable"] = False

        balls[4]["completed"] = True
        balls[4]["clickable"] = False

        balls[5]["completed"] = True
        balls[5]["clickable"] = False

        balls[6]["clickable"] = True

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i, ball in enumerate(balls):
                    # Use different sizes for boss balls
                    ball_size = (53, 53) 
                    ball_rect = pygame.Rect(ball["pos"], ball_size)
                    
                    if ball_rect.collidepoint(event.pos) and ball["clickable"]:
                        if battle_phase(i):  # Simulate a successful battle
                            ball["completed"] = True
                            # Unlock the next balls in the pathway
                            if i < len(balls) - 1:  # If not the last ball
                                balls[i+1]["clickable"] = True  # Unlock the next ball


        # background
        screen.blit(background, (0, 0))

        # Draw balls
        for ball in balls:
            if ball["clickable"] or ball["completed"]:
                # normal ball for clickable or completed balls
                screen.blit(ball_image, ball["pos"])
            else:
                # dimmed ball for non-clickable and incomplete balls
                screen.blit(dimmed_ball_image, ball["pos"])


        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main_game()
