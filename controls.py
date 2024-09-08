import pygame
import json
import os
import sys

font = pygame.font.Font(None, 74)
WHITE = (255, 255, 255)
GRAY = (100, 100, 100)
button_width = 300
button_height = 50
button_spacing = 20
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

def draw_button(rect, text):
    pygame.draw.rect(screen, GRAY, rect)
    draw_text(text, font, WHITE, rect.x + 20, rect.y + 5)

def settings():
    # Define the controls settings and a way to modify them
    controls = {
        'left': pygame.K_LEFT,
        'right': pygame.K_RIGHT,
        'up': pygame.K_UP,
        'down': pygame.K_DOWN
    }

    # Load existing controls from file if available
    if os.path.isfile('controls.json'):
        with open('controls.json', 'r') as controls_file:
            controls = json.load(controls_file)

    changing_key = None  # Track which key is being changed
    font = pygame.font.Font(None, 36)

    run_settings = True
    while run_settings:
        screen.fill((0, 0, 0))

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run_settings = False
            elif event.type == pygame.KEYDOWN and changing_key:
                # Assign the new key to the selected action
                controls[changing_key] = event.key
                changing_key = None
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Check if any control key button is clicked to change
                if left_button_rect.collidepoint(event.pos):
                    changing_key = 'left'
                elif right_button_rect.collidepoint(event.pos):
                    changing_key = 'right'
                elif up_button_rect.collidepoint(event.pos):
                    changing_key = 'up'
                elif down_button_rect.collidepoint(event.pos):
                    changing_key = 'down'

        # Draw the current controls and buttons
        draw_text(f"Left: {pygame.key.name(controls['left'])}", font, WHITE, 100, 100)
        draw_text(f"Right: {pygame.key.name(controls['right'])}", font, WHITE, 100, 150)
        draw_text(f"Up: {pygame.key.name(controls['up'])}", font, WHITE, 100, 200)
        draw_text(f"Down: {pygame.key.name(controls['down'])}", font, WHITE, 100, 250)

        draw_button(left_button_rect, "Change Left")
        draw_button(right_button_rect, "Change Right")  
        draw_button(up_button_rect, "Change Up")
        draw_button(down_button_rect, "Change Down")

        pygame.display.update()

    # Save the updated controls to a file
    with open('controls.json', 'w') as controls_file:
        json.dump(controls, controls_file)



    # Exit settings
    pygame.quit()
    sys.exit()

left_button_rect = pygame.Rect(400, 100, button_width, button_height)
right_button_rect = pygame.Rect(400, 150, button_width, button_height)
up_button_rect = pygame.Rect(400, 200, button_width, button_height)
down_button_rect = pygame.Rect(400, 250, button_width, button_height)