import pygame
import sys
import os
from game import Game
from ui import draw_button, draw_text, settings
from config import *
import json

pygame.mixer.init()
pygame.mixer.music.load('audio/bg_music.mp3')
pygame.mixer.music.play(-1)

default_controls = {
    'left': pygame.K_LEFT,
    'right': pygame.K_RIGHT,
    'up': pygame.K_UP,
    'down': pygame.K_DOWN
}

# Default starting stats
default_stats = {
    "base_damage": 10,
    "max_hp": 30,
    "current_hp": 30,
    "potion_effectiveness": 1.0,
    "potions": 3
}

pygame.init()

# Create game main menu window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Main Menu")

font = pygame.font.Font(None, 74)

# Button positions
continue_button_rect = pygame.Rect((SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2, SCREEN_HEIGHT // 2 - BUTTON_HEIGHT - BUTTON_SPACING), (BUTTON_WIDTH, BUTTON_HEIGHT))
start_button_rect = pygame.Rect((SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2, SCREEN_HEIGHT // 2), (BUTTON_WIDTH, BUTTON_HEIGHT))
quit_button_rect = pygame.Rect((SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2, SCREEN_HEIGHT // 2 + BUTTON_HEIGHT + BUTTON_SPACING), (BUTTON_WIDTH, BUTTON_HEIGHT))

def reset_stats():
    # Reset the stats and save them to the character_stats.json file
    with open('character_stats.json', 'w') as stats_file:
        json.dump(default_stats, stats_file)

    # Reset the gold and save it to the character_gold.json file
    with open('character_gold.json', "w") as character_gold_file:
        json.dump({"character_gold": 300}, character_gold_file)  # Starting gold of 300

def start_game():
    g = Game()
    g.new()
    while g.running:
        g.main()

# Main menu loop
run = True
while run:
    screen.fill((0, 0, 0))
    search_file_existance = os.path.isfile("character_gold.json")

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if start_button_rect.collidepoint(event.pos):
                # Reset stats before starting a new game
                reset_stats()
                # Save default controls
                with open('controls.json', 'w') as controls_file:
                    json.dump(default_controls, controls_file)
                
                start_game()
                run = False
            if search_file_existance and continue_button_rect.collidepoint(event.pos):
                start_game()
                run = False
            if quit_button_rect.collidepoint(event.pos):
                run = False
    # Draw buttons
    if search_file_existance: 
        draw_button(screen, continue_button_rect, "Continue") 
    draw_button(screen, start_button_rect, "Start")
    draw_button(screen, quit_button_rect, "Quit")

    pygame.display.update()

pygame.quit()
sys.exit()
