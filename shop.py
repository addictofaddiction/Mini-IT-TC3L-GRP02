import pygame
import sys
import json
import os

pygame.init()

# Create game main menu window
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)  # Make the window resizable
pygame.display.set_caption("Shop")

WHITE = (255, 255, 255)
GRAY = (100, 100, 100)
YELLOW = (255, 255, 0)

font = pygame.font.Font(None, 50)
gold_font = pygame.font.Font(None, 40)

button_width = 140
button_height = 50
image_size = (100, 100)

# Button positions
purchase1_rect = pygame.Rect((100, 500), (button_width, button_height))
purchase2_rect = pygame.Rect((250, 500), (button_width, button_height))
purchase3_rect = pygame.Rect((400, 500), (button_width, button_height))

# Image positions
image1_rect = pygame.Rect(purchase1_rect.x + (button_width - image_size[0]) // 2, purchase1_rect.y - image_size[1] - 10, *image_size)
image2_rect = pygame.Rect(purchase2_rect.x + (button_width - image_size[0]) // 2, purchase2_rect.y - image_size[1] - 10, *image_size)
image3_rect = pygame.Rect(purchase3_rect.x + (button_width - image_size[0]) // 2, purchase3_rect.y - image_size[1] - 10, *image_size)

# Load images using relative paths
item1_image = pygame.image.load(os.path.join('image', 'item01.png')).convert_alpha()
item2_image = pygame.image.load(os.path.join('image', 'item02.png')).convert_alpha()
item3_image = pygame.image.load(os.path.join('image', 'item03.png')).convert_alpha()

# Scale images to fit the defined size
item1_image = pygame.transform.scale(item1_image, image_size)
item2_image = pygame.transform.scale(item2_image, image_size)
item3_image = pygame.transform.scale(item3_image, image_size)

# Load background image
background_image = pygame.image.load(os.path.join('image', 'shop.png')).convert_alpha()

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

def draw_button(rect, text):
    pygame.draw.rect(screen, GRAY, rect)
    draw_text(text, font, WHITE, rect.x + 20, rect.y + 5)

def load_gold():
    if os.path.exists("character_gold.json"):
        with open("character_gold.json", "r") as current_gold_file:
            data = json.load(current_gold_file)
            return data.get("character_gold", 0)
    return 0

def save_gold(gold):
    with open("character_gold.json", "w") as file:
        json.dump({"character_gold": gold}, file)

def load_character_stats():
    if os.path.exists("character_stats.json"):
        with open("character_stats.json", "r") as stats_file:
            return json.load(stats_file)
    else:
        return {
            "base_damage": 10,
            "max_hp": 30,
            "current_hp": 30,
            "potion_effectiveness": 1.0,
            "potions": 3
        }

def save_character_stats(stats):
    with open("character_stats.json", "w") as stats_file:
        json.dump(stats, stats_file)

def run_shop(character):
    # Load character's current gold from the file or use initial value
    character.gold = load_gold()
    current_gold = character.gold
    character_stats = load_character_stats()
    shop_page = True
    
    while shop_page:
        # Get current screen size
        SCREEN_WIDTH, SCREEN_HEIGHT = screen.get_size()

        # Scale the background image to fit the current window size
        scaled_background = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        screen.blit(scaled_background, (0, 0))  # Display the scaled background

        # Display current gold
        gold_text = f"Gold: {current_gold}"
        draw_text(gold_text, gold_font, YELLOW, 10, 10)

        # Draw images above buttons
        screen.blit(item1_image, image1_rect.topleft)
        screen.blit(item2_image, image2_rect.topleft)
        screen.blit(item3_image, image3_rect.topleft)

        # Draw buttons
        draw_button(purchase1_rect, "100$")
        draw_button(purchase2_rect, "200$")
        draw_button(purchase3_rect, "300$")

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                shop_page = False
                return None
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    shop_page = False
                    return current_gold

            # Purchasing
            if event.type == pygame.MOUSEBUTTONDOWN:
                if purchase1_rect.collidepoint(event.pos) and current_gold >= 100:
                    current_gold -= 100
                    character_stats["base_damage"] += 10  # Increase base damage
                elif purchase2_rect.collidepoint(event.pos) and current_gold >= 200:
                    current_gold -= 200
                    character_stats["max_hp"] += 20  # Increase max health
                    character_stats["current_hp"] += 20  # Heal the player with the increased health
                elif purchase3_rect.collidepoint(event.pos) and current_gold >= 300:
                    current_gold -= 300
                    character_stats["potion_effectiveness"] *= 1.3  # Increase potion effectiveness by 30%
                    character_stats["potions"] += 1  # Increase potion count

                # Save the updated gold and character stats after every purchase
                save_gold(current_gold)
                save_character_stats(character_stats)

        pygame.display.update()

    character.gold = current_gold
    save_gold(character.gold)
    save_character_stats(character_stats)
    return current_gold
