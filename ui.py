import pygame
import json
import os
import config

def draw_text(screen, text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

def draw_button(screen, rect, text):
    pygame.draw.rect(screen, config.GRAY, rect)
    draw_text(screen, text, pygame.font.Font(None, 74), config.WHITE, rect.x + 20, rect.y + 5)

def settings():
    if os.path.isfile('controls.json'):
        with open('controls.json', 'r') as controls_file:
            controls = json.load(controls_file)

    changing_key = None  
    font = pygame.font.Font(None, 36)

    run_settings = True
    while run_settings:
        config.screen.fill((0, 0, 0))

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
                if config.left_button_rect.collidepoint(event.pos):
                    changing_key = 'left'
                elif config.right_button_rect.collidepoint(event.pos):
                    changing_key = 'right'
                elif config.up_button_rect.collidepoint(event.pos):
                    changing_key = 'up'
                elif config.down_button_rect.collidepoint(event.pos):
                    changing_key = 'down'

        # Display current key bindings
        draw_text(config.screen, f"Left: {pygame.key.name(controls['left'])}", font, config.WHITE, 100, 100)
        draw_text(config.screen, f"Right: {pygame.key.name(controls['right'])}", font, config.WHITE, 100, 180)
        draw_text(config.screen, f"Up: {pygame.key.name(controls['up'])}", font, config.WHITE, 100, 260)
        draw_text(config.screen, f"Down: {pygame.key.name(controls['down'])}", font, config.WHITE, 100, 340)

        draw_button(config.screen, config.left_button_rect, "Change Left")
        draw_button(config.screen, config.right_button_rect, "Change Right")  
        draw_button(config.screen, config.up_button_rect, "Change Up")
        draw_button(config.screen, config.down_button_rect, "Change Down")

        pygame.display.update()

    # Save the updated controls
    with open('controls.json', 'w') as controls_file:
        json.dump(controls, controls_file)

class DialogueBox:
    def __init__(self, game, text, x, y):
        print(f"DialogueBox created with text:{text},x:{x},y:{y}")
        self.game = game
        self.font = pygame.font.Font(None, 36)
        self.box_width = 600
        self.box_height = 100
        self.box_x = x
        self.box_y = y
        self.text = text
        self.active = True
        self.buttons = []
        
    def add_button(self, text, action):
        button_x = self.box_x + (len(self.buttons) * 150) + 50
        button_y = self.box_y + self.box_height + 10
        button = Button(self.game, text, button_x, button_y, action)
        self.buttons.append(button)
        print(f"Added button: {text}")

    def draw(self, screen):
        # Draw the dialogue box
        print("Drawing DialogueBox")
        pygame.draw.rect(screen, config.black, (self.box_x, self.box_y, self.box_width, self.box_height))
        pygame.draw.rect(screen, config.white, (self.box_x, self.box_y, self.box_width, self.box_height), 2)

        # Render the text
        text_surface = self.font.render(self.text, True, config.white)
        text_rect = text_surface.get_rect(center=(self.box_x + self.box_width // 2, self.box_y + self.box_height // 2))
        screen.blit(text_surface, text_rect)

        for button in self.buttons:
            button.draw(screen)

    def handle_event(self, event):
        for button in self.buttons:
            button.handle_event(event)

class Button:
    def __init__(self, game, text, x, y, action):
        self.game = game
        self.text = text
        self.x = x
        self.y = y
        self.width = 140
        self.height = 40
        self.action = action
        self.font = pygame.font.Font(None, 32)

    def draw(self, screen):
        pygame.draw.rect(self.game.screen, config.white, (self.x, self.y, self.width, self.height))
        text_surface = self.font.render(self.text, True, config.black)
        text_rect = text_surface.get_rect(center=(self.x + self.width // 2, self.y + self.height // 2))
        screen.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.x <= event.pos[0] <= self.x + self.width and self.y <= event.pos[1] <= self.y + self.height:
                self.action()