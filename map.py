import pygame
import sys
import json
import os

starting_gold = {
    "character_gold": 300  
}

pygame.init()

# Create game main menu window
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Main Menu")

WHITE = (255, 255, 255)
GRAY = (100, 100, 100)

font = pygame.font.Font(None, 74)

button_width = 300
button_height = 50
button_spacing = 20

player_layer = 3
block_layer = 2
ground_layer = 1
red = (255, 0, 0)
black = (0, 0, 0)
green = (0, 255, 0)
tilesize = 32
tilemap = [
    'llllllllllllllllllllllllllllll',
    'bbbb.....................bbbbb',
    'bbbbN....................bbbbb',
    'bbbbb....................bbbbb',
    'B..........................lll',
    '.B.........................lll',
    'B............C.............lll',
    '.B.........................lBl',
    'B............................l',
    '.B.........nlll.............Bl',
    'B..........llll..............l',
    '.B.........llll.............Bl',
    'B..........llll..............l',
    '.B..........................Bl',
    'B............................l',
    '.B..........................ll',
    'B........................bbbbb',
    '.B........................bbbb',
    'B.........................bbbb',
    '.B...................bbbbbbbbb',
    
]

FPS = 30

# Button positions
continue_button_rect = pygame.Rect((SCREEN_WIDTH // 2 - button_width // 2, SCREEN_HEIGHT // 2 - button_height - button_spacing), (button_width, button_height))
start_button_rect = pygame.Rect((SCREEN_WIDTH // 2 - button_width // 2, SCREEN_HEIGHT // 2), (button_width, button_height))
quit_button_rect = pygame.Rect((SCREEN_WIDTH // 2 - button_width // 2, SCREEN_HEIGHT // 2 + button_height + button_spacing), (button_width, button_height))

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

def draw_button(rect, text):
    pygame.draw.rect(screen, GRAY, rect)
    draw_text(text, font, WHITE, rect.x + 20, rect.y + 5)

class Spritesheet:
    def __init__(self, file):
        self.sheet = pygame.image.load(file).convert()

    def get_sprite(self, x, y, width, height):
        sprite = pygame.Surface([width, height])
        sprite.blit(self.sheet, (0, 0), (x, y, width, height))
        sprite.set_colorkey(black)
        return sprite

class Character(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = player_layer
        self.groups = self.game.sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * tilesize
        self.y = y * tilesize
        self.width = tilesize
        self.height = tilesize
        self.x_change = 0
        self.y_change = 0

        self.facing = 'down'
        self.animation_loop = 1

        self.image = self.game.character_spritesheet.get_sprite(55, 2, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        self.movement()
        self.animate()
        self.rect.x += self.x_change
        self.rect.y += self.y_change
        self.x_change = 0
        self.y_change = 0

    def movement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            for sprite in self.game.sprites:
                sprite.rect.x += 5
            self.x_change -= 5
            self.facing = 'left'
        if keys[pygame.K_RIGHT]:
            for sprite in self.game.sprites:
                sprite.rect.x -= 5
            self.x_change += 5
            self.facing = 'right'
        if keys[pygame.K_UP]:
            for sprite in self.game.sprites:
                sprite.rect.y  += 5
            self.y_change -= 5
            self.facing = 'up'
        if keys[pygame.K_DOWN]:
            for sprite in self.game.sprites:
                sprite.rect.y -= 5
            self.y_change += 5
            self.facing = 'down'

    def collide(self, direction):
        if direction == "x":
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.x_change > 0:
                    self.rect.x = hits[0].rect.left - self.rect.width
                if self.x_change < 0:
                    self.rect.x = hits[0].rect.right

        if direction == "y":
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.y_change > 0:
                    self.rect.y = hits[0].rect.top - self.rect.height
                if self.y_change < 0:
                    self.rect.y = hits[0].rect.bottom

    def animate(self):
        down_animations = [self.game.character_spritesheet.get_sprite(55, 2, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(5, 2, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(105, 2, self.width, self.height)]
        
        up_animations = [self.game.character_spritesheet.get_sprite(55, 146, self.width, self.height),
                         self.game.character_spritesheet.get_sprite(5, 146, self.width, self.height),
                         self.game.character_spritesheet.get_sprite(105, 146, self.width, self.height)]

        left_animations = [self.game.character_spritesheet.get_sprite(55, 50, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(5, 50, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(105, 50, self.width, self.height)]
        
        right_animations = [self.game.character_spritesheet.get_sprite(55, 98, self.width, self.height),
                            self.game.character_spritesheet.get_sprite(5, 98, self.width, self.height),
                            self.game.character_spritesheet.get_sprite(105, 98, self.width, self.height)]

        if self.facing == "down":
            if self.y_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(55, 2, self.width, self.height)
            else:
                self.image = down_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1

        if self.facing == "up":
            if self.y_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(55, 146, self.width, self.height)
            else:
                self.image = up_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1

        if self.facing == "left":
            if self.x_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(55, 50, self.width, self.height)
            else:
                self.image = left_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1

        if self.facing == "right":
            if self.x_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(55, 98, self.width, self.height)
            else:
                self.image = right_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1

class NPC(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = player_layer
        self.groups = self.game.sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x * tilesize
        self.y = y * tilesize
        self.width = tilesize
        self.height = tilesize

        self.image = self.game.npc_spritesheet.get_sprite(3, 2, self.width, self.height)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Block4(pygame.sprite.Sprite):  # Renamed to avoid conflict
    def __init__(self, game, x, y):
        self.game = game
        self._layer = block_layer
        self.groups = self.game.sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x * tilesize
        self.y = y * tilesize
        self.width = tilesize
        self.height = tilesize

        self.image = self.game.terrain_spritesheet.get_sprite(960, 448, self.width, self.height)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Game:
    def __init__(self):
        self.sprites = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.character_spritesheet = Spritesheet('character.png')
        self.npc_spritesheet = Spritesheet('npc.png')
        self.terrain_spritesheet = Spritesheet('terrain.png')
        self.player = Character(self, 1, 2)
        self.npc = NPC(self, 10, 5)
        self.block = Block4(self, 10, 6)

        self.tilemap = tilemap

    def create_tilemap(self):
        for i, row in enumerate(self.tilemap):
            for j, column in enumerate(row):
                if column == "B":
                    Block4(self, j, i)
                if column == "C":
                    Character(self, j, i)
                if column == "N":
                    NPC(self, j, i)

    def save_new_game(self):
        with open("savegame.json", "w") as save_file:
            json.dump({"character_gold": starting_gold}, save_file)

    def load_game(self):
        with open("savegame.json", "r") as save_file:
            save_data = json.load(save_file)
            return save_data

def main_menu():
    run = True
    while run:
        screen.fill(WHITE)

        draw_button(continue_button_rect, "Continue")
        draw_button(start_button_rect, "Start New Game")
        draw_button(quit_button_rect, "Quit")

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if continue_button_rect.collidepoint(event.pos):
                    print("Continue button clicked")
                if start_button_rect.collidepoint(event.pos):
                    print("Start New Game button clicked")
                    Game().save_new_game()  # Save new game state
                if quit_button_rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

main_menu()
