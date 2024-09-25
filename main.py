import pygame
import sys
import json
import os
from game import Game
from config import *


default_controls = {
    'left': pygame.K_LEFT,
    'right': pygame.K_RIGHT,
    'up': pygame.K_UP,
    'down': pygame.K_DOWN
}

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Main Menu")

font = pygame.font.Font(None, 74)

button_width = 300
button_height = 50
button_spacing = 20
button_width_for_keybind = 400

# Button positions
continue_button_rect = pygame.Rect((SCREEN_WIDTH // 2 - button_width // 2, SCREEN_HEIGHT // 2 - button_height - button_spacing), (button_width, button_height))
start_button_rect = pygame.Rect((SCREEN_WIDTH // 2 - button_width // 2, SCREEN_HEIGHT // 2), (button_width, button_height))
quit_button_rect = pygame.Rect((SCREEN_WIDTH // 2 - button_width // 2, SCREEN_HEIGHT // 2 + button_height + button_spacing), (button_width, button_height))
left_button_rect = pygame.Rect(400, 100, button_width_for_keybind, button_height)
right_button_rect = pygame.Rect(400, 180, button_width_for_keybind, button_height)
up_button_rect = pygame.Rect(400, 260, button_width_for_keybind, button_height)
down_button_rect = pygame.Rect(400, 340, button_width_for_keybind, button_height)


def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

def draw_button(rect, text):
    pygame.draw.rect(screen, GRAY, rect)
    draw_text(text, font, WHITE, rect.x + 20, rect.y + 5)

#for keybinds
def settings():
    if os.path.isfile('controls.json'):
        with open('controls.json', 'r') as controls_file:
            controls = json.load(controls_file)

    changing_key = None  
    font = pygame.font.Font(None, 36)

    run_settings = True
    while run_settings:
        screen.fill((0, 0, 0))

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run_settings = False  # Return to the game
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Return to game if ESC is pressed
                    run_settings = False
                elif changing_key:
                    # Assign the new key to the selected action
                    controls[changing_key] = event.key
                    changing_key = None
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if left_button_rect.collidepoint(event.pos):
                    changing_key = 'left'
                elif right_button_rect.collidepoint(event.pos):
                    changing_key = 'right'
                elif up_button_rect.collidepoint(event.pos):
                    changing_key = 'up'
                elif down_button_rect.collidepoint(event.pos):
                    changing_key = 'down'

        # Display current key bindings
        draw_text(f"Left: {pygame.key.name(controls['left'])}", font, WHITE, 100, 100)
        draw_text(f"Right: {pygame.key.name(controls['right'])}", font, WHITE, 100, 180)
        draw_text(f"Up: {pygame.key.name(controls['up'])}", font, WHITE, 100, 260)
        draw_text(f"Down: {pygame.key.name(controls['down'])}", font, WHITE, 100, 340)

        draw_button(left_button_rect, "Change Left")
        draw_button(right_button_rect, "Change Right")  
        draw_button(up_button_rect, "Change Up")
        draw_button(down_button_rect, "Change Down")

        pygame.display.update()

    # Save the updated controls
    with open('controls.json', 'w') as controls_file:
        json.dump(controls, controls_file)

def main():
    pygame.mixer.init()
    pygame.mixer.music.load('bg_music.mp3')
    pygame.mixer.music.play(-1)

   
    run = True
    while run:
        screen.fill((0, 0, 0))
        
        search_file_existance = os.path.isfile("character_gold.json") 

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button_rect.collidepoint(event.pos):
                    with open('character_gold.json', "w") as character_gold_file:
                        json.dump(starting_gold, character_gold_file)
                    with open('controls.json', 'w') as controls_file:
                        json.dump(default_controls, controls_file)
                    game = Game()
                    game.run()
                    run = False
                if search_file_existance and continue_button_rect.collidepoint(event.pos):  
                    game = Game()
                    game.run()
                    run = False
                if quit_button_rect.collidepoint(event.pos):
                    run = False

        if search_file_existance: 
            draw_button(screen, continue_button_rect, "Continue", font) 
        draw_button(screen, start_button_rect, "Start", font)
        draw_button(screen, quit_button_rect, "Quit", font)

        pygame.display.update()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()