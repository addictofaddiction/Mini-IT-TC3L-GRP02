import pygame

black = (0,0,0)
white = (255,255,255)

class DialogueBox:
    def __init__(self,game,text,x,y):
        self.game = game
        self.font = pygame.font.Font(None, 36)
        self.box_width = 600
        self.box_height = 100
        self.box_x = x
        self.box_y = y
        self.text = text
        self.active = True
        self.buttons = []
        print(f"DialogueBox created with text:{text}")

    def add_button(self, text, action):
        button_x = self.box_x + (len(self.buttons) * 150) + 50
        button_y = self.box_y - 50
        button = Button(self.game,text,button_x,button_y,action)
        self.buttons.append(button)



    def draw(self, screen):
        # Draw the dialogue box
        print("Drawing DialogueBox")
        pygame.draw.rect(screen, black, (self.box_x, self.box_y, self.box_width, self.box_height))
        pygame.draw.rect(screen, white, (self.box_x, self.box_y, self.box_width, self.box_height), 2)

        # Render the text
        text_surface = self.font.render(self.text, True, white)
        text_rect = text_surface.get_rect(center=(960 // 2, self.box_y + self.box_height // 2))
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

    def draw(self,screen):
        pygame.draw.rect(self.game.screen, white, (self.x, self.y, self.width, self.height))
        text_surface = self.font.render(self.text, True, black)
        text_rect = text_surface.get_rect(center=(self.x + self.width // 2, self.y + self.height // 2))
        screen.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.x <= event.pos[0] <= self.x + self.width and self.y <= event.pos[1] <= self.y + self.height:
                self.action()